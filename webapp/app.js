const tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
}

const result = document.getElementById("result");
const pingButton = document.getElementById("ping-btn");

pingButton.addEventListener("click", async () => {
  result.textContent = "Загрузка...";
  try {
    const response = await fetch("/api/ping");
    const payload = await response.json();
    result.textContent = JSON.stringify(payload, null, 2);
  } catch (error) {
    result.textContent = `Ошибка: ${error}`;
  }
});
