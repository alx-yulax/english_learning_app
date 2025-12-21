//const tg = window.Telegram.WebApp;
//tg.ready();
//
//async function apiMe() {
//    const response = await fetch("/api/me", {
//        headers: {
//            "X-Telegram-Init-Data": tg.initData
//        }
//    });
//
//    const data = await response.json();
//    console.log(data);
//}
//
//apiMe();


const tg = window.Telegram.WebApp;
tg.ready();

async function loadRepetitions() {
    const response = await fetch("/api/repetitions", {
        headers: {
            "X-Telegram-Init-Data": tg.initData
        }
    });

    const data = await response.json();
    console.log("REPETITIONS:", data);
}

loadRepetitions();
