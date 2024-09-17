import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
import Cookies from 'js-cookie';
import getDefaultSnippets from '../constants/editorDefaultSnippets';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { MonacoBinding } from 'y-monaco';

self.MonacoEnvironment = {
	getWorkerUrl: function (_, label) {
		if (label === 'typescript' || label === 'javascript') {
			return document.getElementById('typescript').value;
		}
		return document.getElementById('editor-worker').value;
	}
};

const ydoc = new Y.Doc();
const provider = new WebsocketProvider('ws://localhost:8000/ws/editor/','test/', ydoc);

// const provider = new WebsocketProvider('ws://localhost:8000/ws/editor/{{ room_name }}/', ydoc);

let language = 'javascript';
const editor = monaco.editor.create(document.getElementById('editor'), {
	value: getDefaultSnippets(language),
	language: language,
	theme: 'vs-light',
	fontSize: 12
});

const monacoBinding = new MonacoBinding(ydoc.getText('monaco'), editor.getModel(), new Set([editor]));


const languageSelect = document.getElementById('language-select');
languageSelect.value = language;
languageSelect.addEventListener('change', (event) => {
	language = event.target.value;
	editor.setValue(getDefaultSnippets(language))
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

