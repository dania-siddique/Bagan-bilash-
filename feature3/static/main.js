function addMessage(text, className, sender, time) {
    const box = document.getElementById("chat-box") || document.getElementById("admin-chat-box");
    const msg = document.createElement("div");
    msg.className = `p-3 rounded-lg shadow ${className} bg-white`;
    msg.innerHTML = `<strong>${sender}</strong>: ${text} <br><span class="text-xs text-gray-500">${new Date(time).toLocaleTimeString()}</span>`;
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

const userId = `user_${Math.random().toString(36).substr(2, 8)}`;
const userSocket = new WebSocket(`ws://${window.location.host}/ws/user/${userId}`);

userSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "admin_reply") {
        addMessage(data.text, 'bg-green-100', 'Admin', data.time);
    }
};

if (window.location.pathname === '/admin') {
    const adminSocket = new WebSocket(`ws://${window.location.host}/ws/admin`);
    adminSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "user_message") {
            addMessage(data.text, 'bg-blue-100', data.sender, data.time);
            document.getElementById('current-user').value = data.sender;
        }
    };
}

document.getElementById("chat-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const input = document.getElementById("message-input");
    const message = input.value.trim();
    if (message) {
        userSocket.send(message);
        addMessage(message, 'bg-gray-100', 'You', new Date().toISOString());
        input.value = "";
    }
});

window.sendAdminMessage = async () => {
    const msg = document.getElementById('admin-message').value.trim();
    const userId = document.getElementById('current-user').value;
    if (msg && userId) {
        await fetch(`/admin/reply?sender_id=${userId}&content=${encodeURIComponent(msg)}`, {
            method: 'POST'
        });
        addMessage(msg, 'bg-gray-200', 'You', new Date().toISOString());
        document.getElementById('admin-message').value = '';
    }
};
