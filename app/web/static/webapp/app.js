const tg = window.Telegram.WebApp;
tg.ready();

const statusEl = document.getElementById("status");
const wordsEl = document.getElementById("words");

/**
 * Авторизация WebApp
 */
async function auth() {
    const response = await fetch("/webapp/auth", {
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
        throw new Error(data.error || "Auth failed");
    }

    return data.user;
}

/**
 * Загрузка слов
 */
async function loadWords() {
    const response = await fetch("/webapp/words", {
        headers: {
            "X-Telegram-InitData": tg.initData
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Failed to load words");
    }

    return data;
}

/**
 * Инициализация
 */
async function init() {
    try {
        const user = await auth();
        statusEl.innerText = `Hello, ${user.first_name}`;

        const words = await loadWords();

        wordsEl.innerHTML = "";

        for (const w of words) {
            const li = document.createElement("li");
            li.innerText = `${w.english} → ${w.translation}`;
            wordsEl.appendChild(li);
        }

        if (words.length === 0) {
            wordsEl.innerHTML = "<li>No words yet</li>";
        }

    } catch (err) {
        console.error(err);
        statusEl.innerText = "Error: " + err.message;
    }
}

init();
