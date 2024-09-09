import "./fontawesome";
import "./components"
import "htmx.org";
import Alpine from 'alpinejs';
import Swal from "sweetalert2";

const container = document.getElementById('container');

        const codes = [
            {
                element: document.getElementById('code1'),
                xSpeed: 3,
                ySpeed: 3,
                xPos: Math.random() * (container.clientWidth - 50),
                yPos: Math.random() * (container.clientHeight - 50),
                isBlurred: true
            },
            {
                element: document.getElementById('code2'),
                xSpeed: 2,
                ySpeed: 2,
                xPos: Math.random() * (container.clientWidth - 50),
                yPos: Math.random() * (container.clientHeight - 50),
                isBlurred: true
            }
        ];

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

window.Swal = Swal;
Alpine.start();