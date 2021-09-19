function moveCursorToEnd(el) {
  if (typeof el.selectionStart == "number") {
    el.selectionStart = el.selectionEnd = el.value.length;
  } else if (typeof el.createTextRange != "undefined") {
    el.focus();
    let range = el.createTextRange();
    range.collapse(false);
    range.select();
  }
}

function copyToClipboard(elem) {
  let textElem = elem.parentElement.previousElementSibling;
  let range = document.createRange();
  range.selectNode(textElem);
  window.getSelection().removeAllRanges(); 
  window.getSelection().addRange(range); 
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
}
