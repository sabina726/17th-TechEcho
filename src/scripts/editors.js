import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
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

const languageSelect = document.getElementById('language-select');
languageSelect.value = "javascript";
const editor = monaco.editor.create(document.getElementById('editor'), {
	value: '',
	language: languageSelect.value,
	theme: 'vs-light',
	fontSize: 12
});

const ydoc = new Y.Doc();
const editorId = document.getElementById("editor-id").value;
const provider = new WebsocketProvider('/ws/editor/collab/',`${editorId}/`, ydoc);
const awareness = provider.awareness
const yText = ydoc.getText();
new MonacoBinding(yText, editor.getModel(), new Set([editor]), awareness);

function changeLanguage(newLanguage) {
	monaco.editor.setModelLanguage(editor.getModel(), newLanguage);
	awareness.setLocalStateField('language', { language: newLanguage});
}

languageSelect.addEventListener('change', _ => {
	changeLanguage(languageSelect.value);
	editor.setValue(getDefaultSnippets(languageSelect.value));
});

awareness.on('change', _ => {
	const states = awareness.getStates();
	states.forEach(ele => {
		if (ele.language && ele.language.language !== languageSelect.value) {
			languageSelect.value = ele.language.language;
			monaco.editor.setModelLanguage(editor.getModel(), languageSelect.value);
		}
	})
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


const resultWebSocket = new WebSocket(`/ws/editor/result/${editorId}/`)
const evalBtn = document.getElementById('eval');
evalBtn.addEventListener('click', () => {
	document.getElementById("result").innerText = "執行程式中......"
	const params = {
		code: editor.getValue(),
		language: languageSelect.value
	}
	resultWebSocket.send(JSON.stringify(params));
})

resultWebSocket.onmessage = event => {
	const show = document.getElementById("result")
	show.innerText = JSON.parse(event.data);
};




