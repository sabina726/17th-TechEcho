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
const provider = new WebsocketProvider('/ws/editor/',`${editorId}/`, ydoc);
const awareness = provider.awareness
const yText = ydoc.getText();
new MonacoBinding(yText, editor.getModel(), new Set([editor]), awareness);

const userId = document.getElementById("user-id").value;
function changeLanguage(newLanguage) {
	monaco.editor.setModelLanguage(editor.getModel(), newLanguage);
	awareness.setLocalStateField('language', { language: newLanguage, sender: userId});
}

languageSelect.addEventListener('change', _ => {
	console.log("change: ", languageSelect.value)
	changeLanguage(languageSelect.value);
	editor.setValue(getDefaultSnippets(languageSelect.value));
});

awareness.on('change', _ => {
	const states = awareness.getStates();
	states.forEach(ele => {
		if (ele.language && ele.language.language !== languageSelect.value) {
			languageSelect.value = ele.language.language;
			console.log("awareness: ", languageSelect.value);
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


const evalBtn = document.getElementById('eval');
evalBtn.addEventListener('click', async () => {
	const params = new URLSearchParams();
	params.append('code', editor.getValue());
	params.append('language', languageSelect.value);
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
		const show = document.getElementById("result")
		show.innerHTML = data.result;
	} catch (error) {
		alert('An error occurred during the request.');
	}
})

// const socket = new WebSocket('/ws/editor/')


// const socket = new WebSocket(wsUrl);

// socket.onmessage = function(event) {
// const data = JSON.parse(event.data);

// // If the message is a code result, display it
// if (data.type === 'code_result') {
// 	displayResult(data.result);
// }
// };
