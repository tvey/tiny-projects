function moveCursorToEnd(el) {
  if (typeof el.selectionStart == 'number') {
    el.selectionStart = el.selectionEnd = el.value.length;
  } else if (typeof el.createTextRange != 'undefined') {
    el.focus();
    let range = el.createTextRange();
    range.collapse(false);
    range.select();
  }
}

function copyToClipboard(elem) {
  let textElem = elem.parentElement.previousElementSibling;
  navigator.clipboard.writeText(textElem.textContent);
  showNotification('Copied!');
}

function showNotification(message) {
  const n = document.createElement('div');
  n.classList.add('notification');
  n.innerText = message;
  document.getElementById('notify').appendChild(n);
  setTimeout(() => {
    n.remove();
  }, 2000);
}
