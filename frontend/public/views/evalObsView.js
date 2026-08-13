export function renderEvalObsView() {
  return `
    <div>
      <h1 style="margin-bottom: 1.5rem;">Evaluations & Observability Dashboard</h1>
      <div class="grid-metrics">
        <div class="card">
          <div class="metric-title">Latency (Avg)</div>
          <div class="metric-value">120 ms</div>
        </div>
        <div class="card">
          <div class="metric-title">Pass Rate Score</div>
          <div class="metric-value" style="color: var(--success);">100%</div>
        </div>
      </div>
    </div>
  `;
}
