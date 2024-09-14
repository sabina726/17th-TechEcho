import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
import Cookies from 'js-cookie'

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
	value: "",
	language: 'javascript',
	theme: 'vs-light',
	fontSize: 12
});

// Handle language selection
const languageSelect = document.getElementById('language-select');
languageSelect.addEventListener('change', (event) => {
	const language = event.target.value;
	monaco.editor.setModelLanguage(editor.getModel(), language);
});

// Handle theme selection
const themeSelect = document.getElementById('theme-select');
themeSelect.addEventListener('change', (event) => {
	const theme = event.target.value;
	monaco.editor.setTheme(theme);
});

// Handle font size selection
const fontSizeSelect = document.getElementById('font-size-select');
fontSizeSelect.addEventListener('change', (event) => {
    const fontSize = parseInt(event.target.value, 10);
    editor.updateOptions({ fontSize: fontSize });
});


const evalBtn = document.getElementById('eval');
evalBtn.addEventListener('click', async () => {
	// Get the value from the editor
	const text = editor.getValue();

	// Prepare the data to send as URL-encoded form data
	const params = new URLSearchParams();
	params.append('text', text);
	console.log(params)

	try {
		// Send the POST request using fetch with the CSRF token
		const response = await fetch(document.getElementById('eval-url').value, {
			method: 'POST',
			headers: {
				'X-CSRFToken': Cookies.get('csrftoken'),
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: params.toString(),
		})

		// const data = await response.json();

		// if (data.status === 'fail') {
		// 	if (data.result === '') {
		// 		alert('Invalid code.');
		// 	} else {
		// 		alert('An error occurred.');
		// 	}
		// } else if (data.status === 'success') {
		// 	alert(data.result);
		// }
	} catch (error) {
		alert('An error occurred during the request.');
	}
})

