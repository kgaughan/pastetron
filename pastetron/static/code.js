function selectText(id) {
	var elem = document.getElementById(id);
	var range = document.createRange();
	range.selectNode(elem);
	window.getSelection().addRange(range);
}
