function injectScript(file, node) {
    var e = document.getElementsByTagName(node)[0];
    var script = document.createElement('script');
    script.setAttribute('type', 'text/javascript');
	script.setAttribute('src', file);
	e.insertBefore(script, e.childNodes[0]);
	e.appendChild(script);
}

injectScript(chrome.extension.getURL('window_reader.js'), 'html');
