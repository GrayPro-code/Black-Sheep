

document.addEventListener("DOMContentLoaded", () => {
    const title = document.getElementById("explode-title");
    const text = title.innerText;
    title.innerHTML = "";

    // Разбиваем на буквы
    text.split("").forEach(char => {
        const span = document.createElement("span");
        span.innerText = char;
        title.appendChild(span);
    });

    const letters = title.querySelectorAll("span");

    title.addEventListener("mouseenter", () => {
        letters.forEach(letter => {
            const x = (Math.random() - 0.5) * 200; // разлет по X
            const y = (Math.random() - 0.5) * 200; // разлет по Y
            const rotate = (Math.random() - 0.5) * 180;

            letter.style.transform = `translate(${x}px, ${y}px) rotate(${rotate}deg)`;
            letter.style.opacity = 0.3;
        });
    });

    title.addEventListener("mouseleave", () => {
        letters.forEach(letter => {
            letter.style.transform = `translate(0, 0) rotate(0deg)`;
            letter.style.opacity = 1;
        });
    });
});
