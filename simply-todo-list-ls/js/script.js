const ls = new LS('todo_list');
const ui = new UI(ls);

const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('new-todo');
const todoUl = document.getElementById('todo-list');

document.addEventListener('DOMContentLoaded', () => {
  ui.displayList(todoUl);
});

todoForm.addEventListener('submit', (e) => {
  let text = todoInput.value;
  if (text.trim()) {
    ui.addElem(text, todoUl);
    todoInput.value = '';
  }
  e.preventDefault();
});

todoUl.addEventListener('click', (e) => {
  handleIsDone(e);
  // handleEdit(e);
  handleDelete(e);
});

function handleIsDone(e) {
  let checkbox = e.target.previousElementSibling;
  if (checkbox && checkbox.classList.contains('main-checkbox')) {
    let item = checkbox;
    item = findItem(item);
    ui.toggleCheck(item);
  }
}

function handleEdit(e) {
  if (e.target.parentElement.parentElement.classList.contains('edit')) {
    let itemToUpdate = e.target.parentElement;
    itemToUpdate = findItem(itemToUpdate);
    ui.updateElem(itemToUpdate);
  }
}

function handleDelete(e) {
  if (e.target.parentElement.parentElement.classList.contains('delete')) {
    let itemToRemove = e.target.parentElement;
    itemToRemove = findItem(itemToRemove);
    ui.deleteElem(itemToRemove);
  }
}

function findItem(elem) {
  while (!elem.classList.contains('item')) {
    elem = elem.parentElement;
  }
  return elem;
}

// Utilities

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