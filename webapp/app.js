const tg = window.Telegram?.WebApp;
if (tg) tg.ready();

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

const textEl = document.getElementById("text");
const pdfBtn = document.getElementById("pdf-btn");

pdfBtn.addEventListener("click", async () => {
  const text = textEl.value || "";
  result.textContent = "Открываю ссылку на PDF...";

  // Важно: делаем нормальный HTTPS URL (не blob)
  const urlPath = `/api/render?text=${encodeURIComponent(text)}`;
  const fullUrl = `${window.location.origin}${urlPath}`;

  try {
    // В Telegram WebApp лучше открывать так
    if (tg && tg.openLink) {
      tg.openLink(fullUrl);
    } else {
      // В обычном браузере
      window.open(fullUrl, "_blank");
    }
    result.textContent = "Готово ✅ Если не началась загрузка — проверь всплывающие окна/загрузки.";
  } catch (e) {
    result.textContent = `Ошибка: ${e}`;
  }
});
