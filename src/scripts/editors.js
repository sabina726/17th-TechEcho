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

let language = 'javascript';
const editor = monaco.editor.create(document.getElementById('editor'), {
	value: '',
	language: language,
	theme: 'vs-light',
	fontSize: 12
});

const ydoc = new Y.Doc();
const editorId = document.getElementById("editor-id").value;
const URL = `/ws/editor/${editorId}/`;
const provider = new WebsocketProvider('/ws/editor/',`${editorId}/`, ydoc);
const yText = ydoc.getText();
new MonacoBinding(yText, editor.getModel(), new Set([editor]), provider.awareness);

// const socket = new WebSocket('/ws/editor/')


// const socket = new WebSocket(wsUrl);

// socket.onmessage = function(event) {
// const data = JSON.parse(event.data);

// // If the message is a code result, display it
// if (data.type === 'code_result') {
// 	displayResult(data.result);
// }
// };

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

