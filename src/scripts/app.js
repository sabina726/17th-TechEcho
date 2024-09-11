import "./components"
import "htmx.org";


const container = document.getElementById('container');
const codes = [];

for (let i = 1; i <= 3; i++) {
    const fontSize = Math.random() * (60 - 40) + 20;
    const element = document.getElementById(`code${i}`);

    element.style.fontSize = `${fontSize}px`;
    codes.push({
        element: document.getElementById(`code${i}`),
        xSpeed: (i % 2 === 0) ? 2 : 3,
        ySpeed: (i % 2 === 0) ? 2 : 3,
        xPos: Math.random() * (container.clientWidth - 50),
        yPos: Math.random() * (container.clientHeight - 50),
        isBlurred: true
    });
}

function randomColor() {
    return `hsl(${Math.random() * 360}, 100%, 50%)`;
}

function toggleBlur(code) {
    code.element.style.filter = code.isBlurred ? 'blur(0px)' : 'blur(5px)';
    code.isBlurred = !code.isBlurred;
}

function moveCodes() {
    codes.forEach(code => {
        const codeWidth = code.element.offsetWidth;
        const codeHeight = code.element.offsetHeight;

        code.xPos += code.xSpeed;
        code.yPos += code.ySpeed;

        if (code.xPos + codeWidth >= container.clientWidth || code.xPos <= 0) {
            code.xSpeed *= -1;
            code.element.style.color = randomColor();
            toggleBlur(code);
        }

        if (code.yPos + codeHeight >= container.clientHeight || code.yPos <= 0) {
            code.ySpeed *= -1;
            code.element.style.color = randomColor();
            toggleBlur(code);
        }

        code.element.style.transform = `translate(${code.xPos}px, ${code.yPos}px)`;
    });

    requestAnimationFrame(moveCodes);
}

moveCodes();

