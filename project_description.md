# MASTER BUILD PROMPT — ForgeAI: Production AI Workspace

You are a senior AI Engineer, backend engineer, frontend engineer, DevOps engineer, and software architect.

Your task is to build a production-grade AI Engineering portfolio project called:

# ForgeAI — Production AI Workspace

This is NOT a simple ChatGPT clone.

The goal is to create a complete AI Engineering platform demonstrating real-world skills including:

* LLM API integration
* Prompt engineering
* Structured outputs
* Schema validation
* FastAPI
* REST APIs
* Authentication
* Conversation memory
* File processing
* RAG
* Embeddings
* Vector databases
* Retrieval
* Tool calling
* AI agents
* MCP
* Multimodal AI
* AI evaluation
* Automated testing
* Observability
* Streaming
* Caching
* Cost tracking
* Security
* Docker
* Production deployment

The application should be architected so that features can be added incrementally without rewriting the entire system.

---

# 1. PRODUCT VISION

ForgeAI is a personal AI workspace.

Users can create AI conversations, upload knowledge sources, create AI assistants, connect tools, run agents, and evaluate the quality and cost of their AI interactions.

The platform should feel like a serious developer/AI product rather than a student demo.

The UI should be modern, clean, responsive, and professional.

Do NOT copy ChatGPT's UI exactly.

Use an original dashboard-oriented design.

---

# 2. CORE USER EXPERIENCE

The application should contain:

## Authentication

Users should be able to:

* Register
* Login
* Logout
* View profile
* Manage their sessions

All user-specific data must be isolated.

Never expose another user's conversations, files, documents, API usage, or agent configurations.

---

# 3. MAIN DASHBOARD

After login, users should see a dashboard containing:

* Total conversations
* Documents uploaded
* AI requests
* Tokens consumed
* Estimated AI cost
* Average response latency
* Active AI assistants
* Recent conversations
* Recent activity

Create a clean sidebar navigation.

Suggested navigation:

Dashboard
Chat
Knowledge
Agents
Tools
Evaluations
Observability
Settings

---

# 4. AI CHAT SYSTEM

Build a real AI chat backend.

Requirements:

* User sends message
* Backend receives request
* Backend constructs model request
* LLM generates response
* Response is streamed to frontend
* Conversation is persisted
* Messages are associated with the authenticated user

Support:

* System prompts
* User messages
* Assistant messages
* Conversation titles
* Conversation history
* New conversation
* Delete conversation
* Rename conversation

Do not hard-code one model provider into the architecture.

Create an abstraction layer so different providers/models can be added later.

For example:

LLMProvider
├── OpenAIProvider
├── GeminiProvider
└── OtherProvider

The application should not directly depend on provider-specific code throughout the entire codebase.

---

# 5. STRUCTURED OUTPUTS

Implement structured AI responses using schemas.

For example:

User asks:

"Analyze this job description."

The model should be capable of returning structured information such as:

{
"role": "...",
"required_skills": [],
"preferred_skills": [],
"experience_level": "...",
"technologies": [],
"summary": "..."
}

Validate model output before returning it to the user.

Invalid model responses should be handled gracefully.

---

# 6. FILE UPLOAD SYSTEM

Users should be able to upload documents.

Initially support:

* PDF
* TXT
* Markdown
* DOCX if practical

For every uploaded document:

1. Validate file type
2. Validate file size
3. Store metadata
4. Extract text
5. Clean text
6. Split text into chunks
7. Generate embeddings
8. Store embeddings
9. Associate document with user

Display processing status:

Uploading
Processing
Embedding
Ready
Failed

The user should be able to see their uploaded documents.

---

# 7. RAG KNOWLEDGE SYSTEM

Create a Knowledge section.

Users can create knowledge collections.

Example:

"Machine Learning Notes"

Inside a collection:

* Multiple documents
* Document metadata
* Embeddings
* Chunks

When a user asks a question, the system should be capable of:

User Question
↓
Query Embedding
↓
Vector Search
↓
Relevant Chunks
↓
Context Construction
↓
LLM
↓
Answer

The AI should cite the retrieved sources.

Example:

"According to your uploaded lecture notes..."

Then display:

Sources

* lecture_05.pdf — page 12
* lecture_07.pdf — page 4

Do not allow the model to pretend it retrieved information that it did not retrieve.

---

# 8. VECTOR DATABASE

Use a vector database appropriate for a production portfolio project.

Keep the vector database behind an abstraction.

Do not spread vector-database-specific code throughout the application.

Create a repository/service layer.

The architecture should make it possible to replace the vector database later.

---

# 9. CONVERSATION MEMORY

Implement memory.

The system should support:

### Short-term memory

Recent conversation messages.

### Long-term/user memory

Important user information that the application explicitly chooses to remember.

Do NOT blindly store every message as permanent memory.

Create a controlled memory system.

Allow users to:

* View memories
* Delete memories
* Disable memory

---

# 10. TOOL CALLING

Implement a tool framework.

The LLM should be able to decide when a tool is necessary.

Example tools:

* Calculator
* Current date/time
* Web search abstraction
* Document search
* Weather abstraction
* Code execution sandbox if safely implemented

Architecture:

LLM
↓
Tool decision
↓
Tool registry
↓
Selected tool
↓
Tool result
↓
LLM
↓
Final response

Tools should be registered dynamically.

Do not hard-code tool logic into the chat endpoint.

---

# 11. AI AGENTS

Create an Agents section.

Users should be able to create/configure AI agents.

Agent configuration should include:

* Name
* Description
* System instructions
* Model
* Available tools
* Knowledge sources
* Maximum iterations
* Temperature where supported

An agent should be able to:

1. Understand task
2. Plan
3. Select tools
4. Execute tools
5. Observe results
6. Continue reasoning
7. Produce final response

Implement safeguards against infinite loops.

Every agent execution should have a maximum iteration limit.

---

# 12. MCP SUPPORT

Add Model Context Protocol support as an advanced feature.

Design ForgeAI so external MCP servers/tools can be connected.

Users should eventually be able to configure:

* MCP server
* Available tools
* Authentication/configuration where required
* Enable/disable tools

The architecture must keep MCP integration isolated from the rest of the application.

---

# 13. MULTIMODAL AI

Add multimodal capabilities.

Depending on model/provider capabilities, support:

* Image understanding
* Image/document analysis
* Vision questions

Example:

User uploads an image of a diagram.

User asks:

"Explain this architecture."

The application sends the image and prompt to a vision-capable model.

Display the response inside the conversation.

---

# 14. AI EVALUATION SYSTEM

This is VERY important.

Do not make ForgeAI only an AI application.

Make it capable of evaluating AI applications.

Create an Evaluation section.

Users should be able to create test cases such as:

Input:
"What is the capital of France?"

Expected:
"Paris"

Then execute the test against a selected model/agent.

Track:

* Pass/fail
* Response
* Expected response
* Latency
* Token usage
* Cost
* Evaluation score

Add multiple evaluation strategies where practical.

For example:

* Exact match
* Contains
* Semantic similarity
* LLM-as-judge

This feature should demonstrate that you understand that production AI systems need evaluation rather than blindly trusting model output.

---

# 15. OBSERVABILITY

Create an Observability dashboard.

Track every AI request.

Metrics should include:

* Request ID
* User
* Model
* Provider
* Input tokens
* Output tokens
* Total tokens
* Latency
* Estimated cost
* Success/failure
* Error
* Tool calls
* Retrieved documents
* Agent iterations

Create visualizations for:

* Requests over time
* Token consumption
* Cost over time
* Average latency
* Error rate
* Model usage

Allow developers to inspect individual traces.

---

# 16. PROMPT MANAGEMENT

Create a prompt management system.

Users should be able to save prompts.

A prompt should contain:

* Name
* Description
* Template
* Variables
* Version
* Created date
* Updated date

Example:

Resume Analyzer

Variables:

{{resume}}
{{job_description}}

Allow prompt versions.

Example:

v1
v2
v3

This demonstrates prompt engineering as an actual engineering discipline rather than just writing random prompts.

---

# 17. SECURITY

Treat security as a first-class requirement.

Implement:

* Password hashing
* JWT/session authentication
* Authorization
* Input validation
* File validation
* File size limits
* Rate limiting where practical
* Environment variables for secrets
* No API keys in frontend code
* User-level data isolation
* Safe error messages
* Protection against prompt injection in RAG/tool workflows where practical

Never expose:

API keys
database credentials
secret tokens
internal configuration

to the frontend.

---

# 18. COST MANAGEMENT

Every AI request should attempt to calculate estimated cost.

Track:

Input tokens
Output tokens
Total tokens
Model
Provider
Estimated price

Dashboard should show:

Today's cost
This week's cost
This month's cost

Allow administrators/users to set configurable usage limits.

---

# 19. CACHING

Implement caching where appropriate.

Potential candidates:

* Repeated embeddings
* Repeated retrieval
* Repeated deterministic requests

Do NOT add caching just for the sake of saying "Redis."

Explain why each cached operation is safe.

---

# 20. STREAMING

AI responses should stream to the frontend.

The user should see:

Generating...

then tokens appearing progressively.

Handle:

* Connection interruption
* Timeout
* Cancellation
* Partial responses
* Backend errors

---

# 21. ERROR HANDLING

The application must never simply crash and display a Python traceback to the user.

Implement structured errors.

Example:

{
"error": {
"code": "MODEL_TIMEOUT",
"message": "The AI provider did not respond in time.",
"request_id": "..."
}
}

Log detailed technical information internally.

Show safe messages to users.

---

# 22. BACKEND ARCHITECTURE

Use Python.

Use FastAPI.

Organize the backend cleanly.

Suggested structure:

backend/
app/
main.py

```
    api/
        routes/

    core/
        config.py
        security.py
        logging.py

    models/

    schemas/

    services/
        llm/
        rag/
        embeddings/
        agents/
        tools/
        memory/
        evaluation/
        observability/

    repositories/

    middleware/

    utils/

tests/
```

Keep business logic out of route handlers.

Routes should primarily handle:

request
→ validation
→ service call
→ response

---

# 23. DATABASE

Use a relational database for application data.

Store things such as:

Users
Conversations
Messages
Documents
Knowledge collections
Agents
Tools
Prompts
Evaluations
AI requests
Usage records

Use migrations.

Do not manually modify production database schemas.

---

# 24. FRONTEND

Create a professional frontend.

Use a modern web framework.

The UI should include:

Dashboard
Chat interface
Knowledge manager
Agent builder
Tool manager
Evaluation dashboard
Observability dashboard
Prompt manager
Settings

Important:

Do not make the UI visually overloaded.

Use:

* Cards
* Tables
* Charts
* Tabs
* Side navigation
* Status indicators
* Loading states
* Empty states
* Error states

Responsive design is required.

---

# 25. CHAT UI

The chat interface should support:

* Markdown
* Code blocks
* Copy code
* Streaming
* Source citations
* Tool execution indicators
* File attachments
* Regenerate response
* Stop generation
* Conversation history

When RAG is used, visually distinguish cited sources.

When tools are used, show:

"Using Calculator..."

"Searching Knowledge Base..."

"Calling Tool..."

This makes the AI system behavior understandable.

---

# 26. DEVELOPER EXPERIENCE

Create:

README.md

The README must explain:

1. What ForgeAI is
2. Why it exists
3. Architecture
4. Tech stack
5. Installation
6. Environment variables
7. Running locally
8. Database setup
9. Running tests
10. Docker setup
11. Deployment
12. API documentation
13. Screenshots
14. Example workflows
15. Architecture diagram
16. Future roadmap

---

# 27. API DOCUMENTATION

FastAPI's automatic documentation should be available.

Clearly organize endpoints.

Examples:

/auth/*
/chat/*
/conversations/*
/documents/*
/knowledge/*
/agents/*
/tools/*
/evaluations/*
/observability/*
/prompts/*

Use request/response schemas.

---

# 28. TESTING

Write tests.

At minimum:

* Authentication tests
* API tests
* RAG retrieval tests
* Tool tests
* Agent tests
* Validation tests
* Evaluation tests

Include mocked LLM calls where appropriate.

Do not make the entire test suite dependent on paid API calls.

---

# 29. DOCKER

Create Docker configuration.

The project should eventually be runnable with something conceptually similar to:

docker compose up

Services may include:

Frontend
Backend
Database
Vector database
Cache

Only include services that are actually necessary.

---

# 30. CI/CD

Create a GitHub Actions workflow.

On pull request/push:

1. Install dependencies
2. Run formatting/linting
3. Run tests
4. Build application

The CI pipeline should fail if tests fail.

---

# 31. ARCHITECTURE DOCUMENTATION

Create:

docs/architecture.md

Explain:

Frontend
↓
API
↓
Application Services
↓
LLM / RAG / Agent / Tool Layer
↓
Database / Vector Store / Cache
↓
External AI Providers

Include an architecture diagram.

Also document:

* Request lifecycle
* RAG lifecycle
* Agent lifecycle
* Tool-calling lifecycle
* Evaluation lifecycle

---

# 32. DEVELOPMENT STRATEGY

IMPORTANT:

Do NOT attempt to implement the entire system at once.

Build vertically in milestones.

## Milestone 1

Environment + project skeleton

## Milestone 2

Authentication

## Milestone 3

Basic LLM chat

## Milestone 4

Streaming + conversation persistence

## Milestone 5

File uploads

## Milestone 6

RAG

## Milestone 7

Tool calling

## Milestone 8

Agents

## Milestone 9

MCP

## Milestone 10

Multimodal AI

## Milestone 11

Evaluation

## Milestone 12

Observability

## Milestone 13

Security + cost + caching

## Milestone 14

Docker + CI/CD

## Milestone 15

Production polish

---

# 33. IMPORTANT CODING RULES

Before writing code:

1. Inspect the existing repository.
2. Understand the current architecture.
3. Create/update an implementation plan.
4. Explain the intended change.
5. Implement one milestone at a time.
6. Run tests after changes.
7. Fix errors before moving forward.
8. Do not rewrite working components unnecessarily.
9. Keep commits logically separated.
10. Do not introduce dependencies without justification.

Do NOT create fake functionality.

If a feature cannot actually work because an API/service is unavailable, clearly mark it as incomplete rather than creating a fake demo.

---

# 34. AI ENGINEERING QUALITY BAR

The goal is NOT:

"Make something that looks impressive."

The goal is:

"Build something that demonstrates that the developer understands how production AI systems are engineered."

Therefore prioritize:

Architecture
Reliability
Evaluation
Observability
Security
Testing
Cost
Maintainability
Scalability

over visual gimmicks.

---

# 35. PORTFOLIO QUALITY

The finished project should be impressive enough to demonstrate:

"I can build and operate AI systems."

It should NOT communicate:

"I copied a tutorial for a chatbot."

The GitHub repository should look like a serious open-source project.

Include:

* Clean README
* Architecture diagram
* Screenshots
* Demo video placeholder
* Documentation
* Tests
* CI
* Docker
* Issues
* Roadmap
* Contributing guide
* License

---

# 36. DO NOT HIDE COMPLEXITY

When implementing important AI components, document why they exist.

For example:

Why chunk documents?

Why overlap chunks?

Why embeddings?

Why vector search?

Why reranking?

Why tool calling?

Why agent iteration limits?

Why evaluation?

Why tracing?

Why caching?

Why structured outputs?

These decisions should be documented in the repository.

---

# 37. FINAL SUCCESS CRITERIA

The project is considered complete only when a new developer can:

1. Clone the repository.
2. Configure environment variables.
3. Start the application.
4. Register an account.
5. Chat with an LLM.
6. Upload a PDF.
7. Ask questions about the PDF.
8. See retrieved sources.
9. Create an AI agent.
10. Give the agent tools.
11. Execute an agent task.
12. Inspect its execution.
13. Run an evaluation.
14. Inspect latency/token/cost information.
15. Run automated tests.
16. Run the application with Docker.

---

# 38. YOUR FIRST TASK

DO NOT build the entire application immediately.

First:

1. Inspect the repository.
2. Determine whether this is an existing project or empty repository.
3. Propose the complete architecture.
4. Propose the technology stack.
5. Propose the database schema.
6. Propose the folder structure.
7. Propose Milestone 1.
8. Identify potential technical risks.
9. Identify which components should be abstracted.
10. Wait for confirmation before implementing major architecture.

When implementing future milestones, always preserve backward compatibility with previously completed functionality.

The end goal is a polished, production-oriented AI Engineering portfolio project.

Build ForgeAI like an engineer would build a real product.
