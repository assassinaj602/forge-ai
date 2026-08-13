import { setToken, apiRequest, renderApp } from "../app.js";

export function renderAuthView() {
  setTimeout(() => {
    const authForm = document.getElementById("auth-form");
    if (authForm) {
      authForm.onsubmit = async (e) => {
        e.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const isRegister = e.submitter.dataset.action === "register";

        try {
          if (isRegister) {
            await apiRequest("/auth/register", "POST", { email, password });
          }
          
          const formData = new URLSearchParams();
          formData.append("username", email);
          formData.append("password", password);

          const res = await fetch("http://localhost:8000/api/v1/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
          });

          if (!res.ok) throw new Error("Authentication failed");
          const data = await res.json();
          setToken(data.access_token);
          renderApp();
        } catch (err) {
          alert(err.message);
        }
      };
    }
  }, 0);

  return `
    <div class="auth-wrapper card">
      <h2 style="margin-bottom: 1.5rem; color: var(--primary);">ForgeAI Workspace</h2>
      <form id="auth-form">
        <input type="email" id="email" class="input-field" placeholder="Email Address" required />
        <input type="password" id="password" class="input-field" placeholder="Password (min 8 chars)" required minlength="8" />
        <div style="display: flex; gap: 1rem;">
          <button type="submit" data-action="login" class="btn" style="flex: 1;">Login</button>
          <button type="submit" data-action="register" class="btn" style="flex: 1; background: var(--bg-dark); border: 1px solid var(--border-card);">Register</button>
        </div>
      </form>
    </div>
  `;
}
