 const API_URL = 'http://localhost:5001/messages'; // 端口改成你 Flask 的端口

async function submitMessage() {
  const username = document.getElementById('usernameInput').value.trim();
  const message = document.getElementById('messageInput').value.trim();

  if (username === '' || message === '') return; // 防止空输入

  await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, message })
  });

  document.getElementById('messageInput').value = '';
  loadMessages(); // 提交后刷新留言列表
}

async function loadMessages() {
  const res = await fetch('http://localhost:5001/messages');
  const messages = await res.json();

  const list = document.getElementById('messageList');
  list.innerHTML = ''; // 清空旧内容

  messages.forEach(msg => {
    const li = document.createElement('li');
    li.innerText = `${msg.username}：${msg.content}`;
    list.appendChild(li);
  });
}

// 页面加载时自动获取留言
window.onload = loadMessages;
