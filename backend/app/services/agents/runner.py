from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models_agent import Agent, AgentExecution
from app.services.tools.registry import global_tool_registry
from app.services.llm.factory import get_llm_provider
from app.services.llm.base import LLMMessage

class AgentRunner:
    """
    Autonomous ReAct (Reasoning & Acting) Agent Runner.
    Performs multi-step task execution: Understand Task -> Plan -> Tool Selection -> Observation -> Reflection -> Final Output.
    Enforces strict max_iterations loop safeguards.
    """
    @staticmethod
    async def run(
        agent: Agent,
        task: str,
        execution: AgentExecution,
        db: AsyncSession
    ) -> AgentExecution:
        llm_provider = get_llm_provider(agent.provider)
        
        # Resolve enabled tools for agent
        available_tools = global_tool_registry.get_openai_tools_schema()
        if agent.tools:
            available_tools = [
                t for t in available_tools 
                if t.get("function", {}).get("name") in agent.tools
            ]

        steps_trace = []
        iteration = 0
        final_answer = None
        current_observation = None

        while iteration < agent.max_iterations:
            iteration += 1
            
            # Construct multi-step reasoning context prompt
            history_prompt = f"System Goal: {agent.system_instructions}\nTask: {task}\n"
            if steps_trace:
                history_prompt += "\nPrevious Reason & Tool Traces:\n"
                for step in steps_trace:
                    history_prompt += f"Step {step['step']}: Thought: {step['thought']}"
                    if step.get('action'):
                        history_prompt += f" | Action: {step['action']} | Input: {step['action_input']} | Result: {step['observation']}\n"

            messages = [LLMMessage(role="user", content=history_prompt)]
            
            # 1. Reason / Plan / Select Tool Step
            response = await llm_provider.generate(
                messages=messages,
                system_prompt=agent.system_instructions,
                model=agent.model,
                tools=available_tools
            )

            # Check if model called a tool
            if response.tool_calls:
                tool_call = response.tool_calls[0]
                tool_name = tool_call["name"]
                tool_args = tool_call["arguments"]

                if tool_name == "document_search":
                    tool_args["user_id"] = agent.user_id

                # 2. Execute Tool & Observe Result
                obs = await global_tool_registry.execute_tool(tool_name, tool_args)
                
                step_record = {
                    "step": iteration,
                    "thought": f"Iteration {iteration}: Decide to execute tool {tool_name}.",
                    "action": tool_name,
                    "action_input": tool_args,
                    "observation": obs
                }
                steps_trace.append(step_record)
            else:
                # 3. Model produced final response
                final_answer = response.content
                step_record = {
                    "step": iteration,
                    "thought": f"Iteration {iteration}: Task objective completed.",
                    "action": None,
                    "action_input": None,
                    "observation": "Final Answer Produced."
                }
                steps_trace.append(step_record)
                break

        # Safeguard iteration limit check
        if not final_answer:
            if iteration >= agent.max_iterations:
                execution.status = "max_iterations_reached"
                final_answer = f"Agent reached safeguard max iteration limit ({agent.max_iterations}) before producing final answer."
            else:
                execution.status = "completed"
        else:
            execution.status = "completed"

        execution.final_answer = final_answer
        execution.iteration_count = iteration
        execution.steps_log = steps_trace
        execution.completed_at = datetime.utcnow()

        await db.commit()
        await db.refresh(execution)
        return execution
