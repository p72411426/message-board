const API_URL = 'https://message-board-5jhw.onrender.com/messages';

async function submitMessage() {
  const username = document.getElementById('usernameInput').value.trim();
  const message = document.getElementById('messageInput').value.trim();

  if (username === '' || message === '') return;

  await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, message })
  });

  document.getElementById('messageInput').value = '';
  loadMessages();
}

async function loadMessages() {
  const res = await fetch(API_URL);
  const messages = await res.json();

  const list = document.getElementById('messageList');
  list.innerHTML = '';

  messages.forEach(msg => {
    const li = document.createElement('li');
    li.innerText = `${msg.username}：${msg.content}`;
    list.appendChild(li);
  });
}

window.onload = loadMessages;
