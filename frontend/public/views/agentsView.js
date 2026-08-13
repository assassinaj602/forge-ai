export function renderAgentsView() {
  return `
    <div>
      <h1 style="margin-bottom: 1.5rem;">Autonomous Agents Studio</h1>
      <div class="card" style="margin-bottom: 2rem;">
        <h3 style="margin-bottom: 1rem;">Configure New ReAct Agent</h3>
        <input type="text" class="input-field" placeholder="Agent Name e.g. Research Analyst" />
        <textarea class="input-field" placeholder="System Instructions" style="height: 100px;"></textarea>
        <button class="btn">Create Agent</button>
      </div>
    </div>
  `;
}
