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
const pdfLink = document.getElementById("pdf-link");

pdfBtn.addEventListener("click", async () => {
  result.textContent = "Генерирую PDF...";
  pdfLink.style.display = "none";

  try {
    const resp = await fetch("/api/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: textEl.value || "" }),
    });

    if (!resp.ok) {
      const t = await resp.text();
      throw new Error(t || `HTTP ${resp.status}`);
    }

    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);

    pdfLink.href = url;
    pdfLink.style.display = "inline-block";
    pdfLink.textContent = "Скачать PDF ✅";

    result.textContent = "Готово. Нажми «Скачать PDF»";
  } catch (e) {
    result.textContent = `Ошибка: ${e}`;
  }
});
