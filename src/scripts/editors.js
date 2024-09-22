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

const editor = monaco.editor.create(document.getElementById('editor'), {
	value: getDefaultSnippets("javascript"),
	language: "javascript",
	theme: "vs-light",
	fontSize: 12
});

const ydoc = new Y.Doc();
const editorId = document.getElementById("editor-id").value;
const provider = new WebsocketProvider('/ws/editor/collab/',`${editorId}/`, ydoc);
const awareness = provider.awareness
const yText = ydoc.getText();
new MonacoBinding(yText, editor.getModel(), new Set([editor]), awareness);

function debounce(func, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}

const debouncedSetCursorAwareness = debounce((position) => {
  awareness.setLocalStateField('cursor', { position });
}, 200);

editor.onDidChangeCursorSelection(_ => {
	const position = editor.getPosition();
	debouncedSetCursorAwareness(position);
})

const languageSelect = document.getElementById('language-select');
let currentLanguage = awareness.getLocalState()?.selectedLanguage || 'javascript';
monaco.editor.setModelLanguage(editor.getModel(), currentLanguage);
languageSelect.value = currentLanguage;

const debouncedSelectChange = debounce((selectedLanguage) => {
	awareness.setLocalStateField('language', { selectedLanguage });
}, 200);


languageSelect.addEventListener('change', (e) => {
	const selectedLanguage = e.target.value;
	monaco.editor.setModelLanguage(editor.getModel(), selectedLanguage);
	editor.setValue(getDefaultSnippets(languageSelect.value));
	debouncedSelectChange(selectedLanguage);
});

const remoteCursors = editor.createDecorationsCollection([]);
let count = 0;
awareness.on('change', _ => {
	awareness.getStates().forEach((state, clientId) => {
		if (clientId !== awareness.clientID) {
			const cursor = state.cursor;
			if (cursor) {
				const decorations = [];
				const { position } = cursor;

				decorations.push({
					range: new monaco.Range(position.lineNumber, position.column, position.lineNumber, position.column),
					options: {
						className: 'remote-cursor',
						stickiness: monaco.editor.TrackedRangeStickiness.NeverGrowsWhenTypingAtEdges
					}
				});

				remoteCursors.set(decorations);
			}
			const languageState = state.language;
			if (languageState) {
				const { selectedLanguage } = languageState;
				monaco.editor.setModelLanguage(editor.getModel(), selectedLanguage);
				languageSelect.value = selectedLanguage;
			}
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
	const code = editor.getValue().trim();
	if (code === "") {
		document.getElementById("result").innerText = "請先輸入程式代碼";
	} else {
		const params = {
			code: code,
			language: languageSelect.value
		}
		resultWebSocket.send(JSON.stringify(params));
		document.getElementById("result").innerText = "執行程式中......";
	}
})

resultWebSocket.onmessage = event => {
	const show = document.getElementById("result")
	show.innerText = JSON.parse(event.data);
};




