import { apiRequest } from "../app.js";

export function renderChatView() {
  setTimeout(() => {
    const sendBtn = document.getElementById("send-chat-btn");
    const chatInput = document.getElementById("chat-input");
    const chatHistory = document.getElementById("chat-history");

    if (sendBtn && chatInput) {
      sendBtn.onclick = async () => {
        const msg = chatInput.value.trim();
        if (!msg) return;

        chatHistory.innerHTML += `
          <div style="margin-bottom: 1rem; text-align: right;">
            <div style="display: inline-block; padding: 0.75rem 1rem; background: var(--primary); border-radius: 12px; color: white;">
              ${msg}
            </div>
          </div>
        `;
        chatInput.value = "";

        const assistantMsgDiv = document.createElement("div");
        assistantMsgDiv.style.marginBottom = "1rem";
        assistantMsgDiv.innerHTML = `
          <div style="display: inline-block; padding: 0.75rem 1rem; background: rgba(30, 41, 59, 0.9); border: 1px solid var(--border-card); border-radius: 12px; color: white;">
            <span class="assistant-content">Thinking...</span>
          </div>
        `;
        chatHistory.appendChild(assistantMsgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
          const res = await apiRequest("/chat/completions", "POST", {
            message: msg,
            provider: "mock",
            model: "mock-v1"
          });
          assistantMsgDiv.querySelector(".assistant-content").innerText = res.message.content;
        } catch (err) {
          assistantMsgDiv.querySelector(".assistant-content").innerText = "Error: " + err.message;
        }
      };
    }
  }, 0);

  return `
    <div style="display: flex; flex-direction: column; height: calc(100vh - 4rem);">
      <h1 style="margin-bottom: 1rem;">AI Chat Studio</h1>
      <div class="card" id="chat-history" style="flex: 1; overflow-y: auto; margin-bottom: 1rem;">
        <div style="margin-bottom: 1rem;">
          <div style="display: inline-block; padding: 0.75rem 1rem; background: rgba(30, 41, 59, 0.9); border: 1px solid var(--border-card); border-radius: 12px; color: white;">
            Hello! I am ForgeAI Assistant. How can I help you engineering AI systems today?
          </div>
        </div>
      </div>
      <div style="display: flex; gap: 0.75rem; align-items: center;">
        <input type="file" id="chat-image-input" accept="image/*" style="display: none;" />
        <button class="btn" style="background: var(--bg-dark); border: 1px solid var(--border-card);" onclick="document.getElementById('chat-image-input').click()">📷 Image</button>
        <input type="text" id="chat-input" class="input-field" placeholder="Ask ForgeAI assistant or attach image..." style="margin-bottom: 0;" />
        <button id="send-chat-btn" class="btn">Send</button>
      </div>
    </div>
  `;
}
