// ForgeAI Frontend State & Router Engine

const API_BASE = "http://localhost:8000/api/v1";

export const state = {
  token: localStorage.getItem("forgeai_token") || null,
  user: null,
  activeRoute: "dashboard",
  metrics: null,
  conversations: [],
  activeConversation: null,
  knowledgeCollections: [],
  agents: [],
  evalSuites: []
};

export async function apiRequest(endpoint, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) {
    headers["Authorization"] = `Bearer ${state.token}`;
  }

  const options = { method, headers };
  if (body && !(body instanceof FormData)) {
    options.body = JSON.stringify(body);
  } else if (body instanceof FormData) {
    delete headers["Content-Type"];
    options.body = body;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  if (response.status === 401) {
    state.token = null;
    localStorage.removeItem("forgeai_token");
    renderApp();
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "API Request Failed");
  }

  if (response.status === 204) return null;
  return await response.json();
}

export function setToken(token) {
  state.token = token;
  localStorage.setItem("forgeai_token", token);
}

export function logout() {
  state.token = null;
  state.user = null;
  localStorage.removeItem("forgeai_token");
  renderApp();
}

export function navigateTo(route) {
  state.activeRoute = route;
  renderApp();
}

import { renderAuthView } from "./views/auth.js";
import { renderDashboardView } from "./views/dashboardView.js";
import { renderChatView } from "./views/chatView.js";
import { renderKnowledgeView } from "./views/knowledgeView.js";
import { renderAgentsView } from "./views/agentsView.js";
import { renderEvalObsView } from "./views/evalObsView.js";

export function renderApp() {
  const container = document.getElementById("app");
  if (!state.token) {
    container.innerHTML = renderAuthView();
    return;
  }

  let mainViewHtml = renderDashboardView();
  if (state.activeRoute === "chat") mainViewHtml = renderChatView();
  else if (state.activeRoute === "knowledge") mainViewHtml = renderKnowledgeView();
  else if (state.activeRoute === "agents") mainViewHtml = renderAgentsView();
  else if (state.activeRoute === "evaluations" || state.activeRoute === "observability") mainViewHtml = renderEvalObsView();

  container.innerHTML = `
    <div class="app-container">
      <aside class="sidebar">
        <div class="brand">
          <div class="brand-icon">F</div>
          <span>ForgeAI</span>
        </div>
        <nav class="nav-menu">
          <div class="nav-item ${state.activeRoute === 'dashboard' ? 'active' : ''}" onclick="window.navigateTo('dashboard')">Dashboard</div>
          <div class="nav-item ${state.activeRoute === 'chat' ? 'active' : ''}" onclick="window.navigateTo('chat')">AI Chat</div>
          <div class="nav-item ${state.activeRoute === 'knowledge' ? 'active' : ''}" onclick="window.navigateTo('knowledge')">Knowledge RAG</div>
          <div class="nav-item ${state.activeRoute === 'agents' ? 'active' : ''}" onclick="window.navigateTo('agents')">AI Agents</div>
          <div class="nav-item ${state.activeRoute === 'evaluations' ? 'active' : ''}" onclick="window.navigateTo('evaluations')">Evaluations</div>
          <div class="nav-item ${state.activeRoute === 'observability' ? 'active' : ''}" onclick="window.navigateTo('observability')">Observability</div>
        </nav>
        <div class="user-profile">
          <span>User Account</span>
          <button class="btn" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;" onclick="window.logout()">Logout</button>
        </div>
      </aside>
      <main class="main-content" id="main-view">
        ${mainViewHtml}
      </main>
    </div>
  `;
}

window.navigateTo = navigateTo;
window.logout = logout;

// Initial App Boot
document.addEventListener("DOMContentLoaded", () => {
  renderApp();
});
