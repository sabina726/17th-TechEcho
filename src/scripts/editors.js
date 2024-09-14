import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';



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
		return document.getElementById('editor_worker').value;
	}
};

monaco.editor.create(document.getElementById('editor'), {
	value: ['function x() {', '\tconsole.log("Hello world!");', '}'].join('\n'),
	language: 'html'
});

