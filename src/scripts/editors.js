import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
import Cookies from 'js-cookie'

let language = 'javascript';

self.MonacoEnvironment = {
	getWorkerUrl: function (_, label) {
		if (label === 'css' || label === 'scss' || label === 'less') {
			return document.getElementById('css').value;
		}
		if (label === 'html' || label === 'handlebars' || label === 'razor') {
			return document.getElementById('html').value;
		}
		if (label === 'typescript' || label === 'javascript') {
			return document.getElementById('typescript').value;
		}
		return document.getElementById('editor-worker').value;
	}
};

const editor = monaco.editor.create(document.getElementById('editor'), {
	value: "console.log('Hello World')",
	language: language,
	theme: 'vs-light',
	fontSize: 12
});

const languageSelect = document.getElementById('language-select');
languageSelect.value = language;
console.log(language)
languageSelect.addEventListener('change', (event) => {
	language = event.target.value;
	monaco.editor.setModelLanguage(editor.getModel(), language);
});

const themeSelect = document.getElementById('theme-select');
themeSelect.addEventListener('change', (event) => {
	const theme = event.target.value;
	monaco.editor.setTheme(theme);
});

const fontSizeSelect = document.getElementById('font-size-select');
fontSizeSelect.addEventListener('change', (event) => {
    const fontSize = parseInt(event.target.value, 10);
    editor.updateOptions({ fontSize: fontSize });
});


const evalBtn = document.getElementById('eval');
evalBtn.addEventListener('click', async () => {
	const params = new URLSearchParams();
	params.append('code', editor.getValue());
	params.append('language', language);
	try {
		const response = await fetch(document.getElementById('eval-url').value, {
			method: 'POST',
			headers: {
				'X-CSRFToken': Cookies.get('csrftoken'),
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: params.toString(),
		})

		const data = await response.json();

		alert(data.result)

	} catch (error) {
		alert('An error occurred during the request.');
	}
})

