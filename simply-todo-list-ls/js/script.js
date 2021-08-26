const ls = new LS('todo_list');
const ui = new UI(ls);

const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('new-todo');
const todoUl = document.getElementById('todo-list');
const submitBtn = document.querySelector('#todo-form button[type="submit"]')

document.addEventListener('DOMContentLoaded', () => {
  ui.displayList(todoUl);
});

todoForm.addEventListener('submit', (e) => {
  let text = todoInput.value;
  if (text.trim()) {
    if (todoForm.classList.contains('editing')) {
      todoForm.classList.remove('editing');
      submitBtn.classList.remove('btn-accent');
      submitBtn.innerText = '+';
      todoInput.style.borderColor = '#3aa128';
      let idHolder = document.querySelector('#todo-form input[type="hidden"]');
      let itemId = idHolder.value;
      idHolder.remove();
      let item = document.getElementById(`${itemId}`);
      ui.updateElem(item, text);
    } else {
      ui.addElem(text, todoUl);
    }
    todoInput.value = '';
  }
  e.preventDefault();
});

todoUl.addEventListener('click', (e) => {
  handleIsDone(e);
  handleEdit(e);
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
    let itemText = itemToUpdate.querySelector('p').innerHTML;
    let todoInput = todoForm.children[0];
    todoForm.classList.add('editing');
    submitBtn.classList.add('btn-accent');
    todoInput.style.borderColor = '#fcca03';
    submitBtn.innerHTML = '<i class="fas fa-check"></i>';
    todoInput.value = itemText;
    todoInput.focus();

    let idHolder = document.querySelector('#todo-form input[type="hidden"]');
    if (idHolder) idHolder.remove();
    idHolder = document.createElement('input');
    idHolder.type = 'hidden';
    idHolder.value = itemToUpdate.id;
    todoForm.appendChild(idHolder);
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
  // Not for mobile
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