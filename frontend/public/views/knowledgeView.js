import { apiRequest } from "../app.js";

export function renderKnowledgeView() {
  return `
    <div>
      <h1 style="margin-bottom: 1.5rem;">Knowledge Workspace & RAG Engine</h1>
      <div class="card" style="margin-bottom: 2rem;">
        <h3 style="margin-bottom: 1rem;">Create Knowledge Collection</h3>
        <input type="text" class="input-field" placeholder="Collection Name e.g. Machine Learning Notes" />
        <button class="btn">Create Collection</button>
      </div>
      <div class="card">
        <h3>Uploaded Knowledge Documents</h3>
        <p style="color: var(--text-muted); margin-top: 0.5rem;">No documents uploaded yet. Select a collection to upload PDF/TXT files.</p>
      </div>
    </div>
  `;
}
