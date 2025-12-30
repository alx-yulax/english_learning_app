const tg = window.Telegram.WebApp;
tg.ready();

const statusEl = document.getElementById("status");

async function auth() {
    if (!tg.initData) {
        statusEl.innerText = "Auth error: initData is empty";
        return;
    }

    try {
        const response = await fetch("/api/webapp/auth", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                initData: tg.initData
            })
        });

        const data = await response.json();

        if (!response.ok) {
            statusEl.innerText = "Auth error: " + (data.error || "unknown");
            return;
        }

        statusEl.innerText = "Hello, " + data.user.first_name;
    } catch (e) {
        console.error(e);
        statusEl.innerText = "Network error";
    }
}

auth();
