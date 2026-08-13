export function renderDashboardView() {
  return `
    <div>
      <h1 style="margin-bottom: 1.5rem;">Dashboard Overview</h1>
      <div class="grid-metrics">
        <div class="card">
          <div class="metric-title">Active Conversations</div>
          <div class="metric-value" id="m-conversations">12</div>
        </div>
        <div class="card">
          <div class="metric-title">Uploaded Documents</div>
          <div class="metric-value" id="m-documents">5</div>
        </div>
        <div class="card">
          <div class="metric-title">Total Tokens Consumed</div>
          <div class="metric-value" id="m-tokens">45,210</div>
        </div>
        <div class="card">
          <div class="metric-title">Estimated Cost</div>
          <div class="metric-value" id="m-cost" style="color: var(--success);">$0.0904</div>
        </div>
      </div>

      <div class="card" style="margin-top: 2rem;">
        <h3 style="margin-bottom: 1rem;">Recent AI Engineering Activity</h3>
        <p style="color: var(--text-muted);">Platform connected to FastAPI async engine, PostgreSQL database, and Qdrant/Memory Vector Store.</p>
      </div>
    </div>
  `;
}
