const tg = window.Telegram.WebApp;
tg.ready();

async function auth() {
    const response = await fetch("/webapp/auth", {
        method: "POST",
        headers: {
            "X-Telegram-InitData": tg.initData,
        },
    });

    const data = await response.json();

    const statusEl = document.getElementById("status");
    if (response.ok) {
        statusEl.innerText = `Hello, ${data.user.first_name}`;
    } else {
        statusEl.innerText = `Auth error: ${data.error}`;
    }
}

auth();
