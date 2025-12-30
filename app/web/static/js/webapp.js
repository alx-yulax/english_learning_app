const tg = window.Telegram.WebApp;
tg.ready();

const initData = tg.initData;

async function loadWords() {
    try {
        const response = await fetch("/webapp/words", {
            headers: {
                "X-Telegram-InitData": initData
            }
        });

        const data = await response.json();

        if (!response.ok) {
            document.getElementById("status").innerText =
                "Error: " + (data.error || "Unknown error");
            return;
        }

        console.log("WORDS:", data);

        document.getElementById("status").innerText =
            "Words loaded: " + data.length;

    } catch (err) {
        console.error(err);
        document.getElementById("status").innerText =
            "Network error";
    }
}

loadWords();
