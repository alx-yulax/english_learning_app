const tg = window.Telegram.WebApp;
tg.ready();

console.log("INIT DATA:", tg.initData);

fetch("/webapp/words", {
    headers: {
        "X-Telegram-InitData": tg.initData
    }
})
.then(res => {
    console.log("STATUS:", res.status);
    return res.text();   // ⚠️ ВАЖНО: не json()
})
.then(text => {
    console.log("RAW RESPONSE:", text);
})
.catch(err => console.error("FETCH ERROR:", err));
