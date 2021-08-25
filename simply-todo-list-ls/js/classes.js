class LS {
  constructor(listName) {
    this.listName = listName;
  }

  loadList() {
    // Load list from LS or create empty (getItem)
    let todoList;
    const loadedList = localStorage.getItem(this.listName);
    if (loadedList === null) {
      todoList = [];
    } else {
      todoList = JSON.parse(loadedList);
    }
    return todoList;
  }

  saveList(list) {
    // Update ids and save list to LS
    list.forEach((item, index) => {
      item.id = index;
    })
    localStorage.setItem(this.listName, JSON.stringify(list));
  }

  addItem(text) {
    const todoList = this.loadList();
    let newItem = { id: 0, text: text, isDone: false };
    todoList.unshift(newItem);
    this.saveList(todoList);
    return newItem;
  }

  deleteItem(itemId) {
    const todoList = this.loadList();

    todoList.forEach((item, i) => {
      if (i == itemId) {
        todoList.splice(i, 1);
        this.saveList(todoList);
        this.loadList();
        return false;
      }
    });
  }

  toggleDone(itemId) {
    const todoList = this.loadList();

    todoList.forEach((item, i) => {
      if (i == itemId) {
        item.isDone = !item.isDone;
        let popped = todoList.splice(i, 1)[0];

        if (item.isDone) {
          // Move item under undone elements
          let newIdx = todoList.filter(x => x.isDone === false).length;
          todoList.splice(newIdx, 0, popped);
        } else {
          todoList.unshift(popped);
        }
        this.saveList(todoList);
        return false; // break
      }
    });
  }

  editItem(itemId) {
    // To-do
  }
}


class UI {
  constructor(ls) {
    this.ls = ls;
  }

  formatElem(item) {
    let isDoneClasses = '';
    let checked = '';
    if (item.isDone) isDoneClasses = 'done text-muted';
    if (item.isDone) checked = "checked";

    const newElem = `
        <li class="item" id="${item.id}">
          <form id="check">
            <div class="checkbox-wrap">
              <input type="checkbox" class="main-checkbox" ${checked}>
              <label></label>
            </div>
          </form>
          <p class="${isDoneClasses}">${item.text}</p>
          <div class="manage">
            <button class="link-btn text-muted edit" title="Edit">
              <small><i class="fas fa-pencil-alt"></i></small>
            </button>
            <button class="link-btn text-muted copy" onclick="copyToClipboard(this)" title="Copy text">
              <small><i class="far fa-copy"></i></small>
            </button>
            <button class="link-btn text-muted delete" title="Delete">
              <small><i class="far fa-times-circle"></i></small>
            </button>
          </div>     
        </li>`;
    return newElem;
  }

  displayList(parent) {
    let todoList = this.ls.loadList();
    let output = '';
    todoList.forEach((item) => {
      output += this.formatElem(item);
    });
    parent.innerHTML = output;
  }

  addElem(text, parent) {
    // Create li with styles and inner text
    let newItem = this.ls.addItem(text);
    let newElem = this.formatElem(newItem);
    parent.innerHTML = newElem + parent.innerHTML;
  }

  toggleCheck(item) {
    this.ls.toggleDone(item.id);
    this.displayList(item.parentElement);
  }

  updateElem(item) {
    // To-do
  }

  deleteElem(itemToRemove) {
    // Remove elem from DOM and from LS
    this.ls.deleteItem(itemToRemove.id);
    let parent = itemToRemove.parentElement;
    itemToRemove.remove();
    this.displayList(parent);
  }
}