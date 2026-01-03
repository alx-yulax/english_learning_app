const tg = window.Telegram.WebApp;
tg.ready();

const initData = tg.initData;

async function auth() {
    const response = await fetch("/webapp/auth", {
        method: "POST",
        headers: {
            "X-Telegram-InitData": window.Telegram.WebApp.initData
        }
    });

    const data = await response.json();

    if (response.ok) {
        document.getElementById("status").innerText =
            "Hello, " + data.user.first_name;
    } else {
        document.getElementById("status").innerText =
            "Auth error: " + data.error;
    }
}

auth();
