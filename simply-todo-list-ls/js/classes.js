class LS {
  constructor(listName) {
    this.listName = listName;
  }

  loadList() {
    // Load list from LS or create empty
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
    localStorage.setItem(this.listName, JSON.stringify(list));
  }

  updateIds(list) {
    // Start with 0
    list.forEach((item, index) => {
      item.id = index;
    })
  }

  addItem(text) {
    const todoList = this.loadList();
    let newItem = { id: 0, text: text, isDone: false };
    todoList.unshift(newItem);
    this.updateIds(todoList);
    this.saveList(todoList);
    return newItem;
  }

  deleteItem(itemId) {
    const todoList = this.loadList();

    todoList.forEach((item, i) => {
      if (i == itemId) {
        todoList.splice(i, 1);
        this.updateIds(todoList);
        this.saveList(todoList);
        return; // breaks
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
        this.updateIds(todoList);
        this.saveList(todoList);
        return;
      }
    });
  }

  editItem(itemId, newText) {
    const todoList = this.loadList();

    todoList.forEach((item, i) => {
      if (i == itemId) {
        item.text = newText;
        // Don't update ids
        this.saveList(todoList);
        return;
      }
    });
  }

  saveSort(positions) {
    const todoList = this.loadList();

    todoList.sort((a, b) => {
      // Sort list item ids based on positions array
      return positions.indexOf(a.id) - positions.indexOf(b.id);
    });
    todoList.forEach((item, i) => {
      item.id = i;
    });
    this.saveList(todoList);
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
        <li class="item" id="${item.id}" draggable="true">
          <form class="check">
            <div class="checkbox-wrap">
              <input type="checkbox" class="main-checkbox" ${checked}>
              <label></label>
            </div>
          </form>
          <p class="${isDoneClasses}">${item.text}</p>
          <div class="manage">
            <button class="link-btn text-muted edit" title="Edit">
              <span><i class="fas fa-pencil-alt"></i></span>
            </button>
            <button class="link-btn text-muted copy" onclick="copyToClipboard(this)" title="Copy text">
              <span><i class="far fa-copy"></i></span>
            </button>
            <button class="link-btn text-muted delete" title="Delete">
              <span><i class="far fa-times-circle"></i></span>
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
    handleSorting();
  }

  addElem(text, parent) {
    // Create li with styles and inner text
    this.ls.addItem(text);
    this.displayList(parent);
  }

  toggleCheck(item) {
    this.ls.toggleDone(item.id);
    this.displayList(item.parentElement);
  }

  updateElem(item, newText) {
    this.ls.editItem(item.id, newText)
    this.displayList(item.parentElement);
  }

  deleteElem(itemToRemove) {
    // Remove elem from the DOM and LS
    this.ls.deleteItem(itemToRemove.id);
    let parent = itemToRemove.parentElement;
    itemToRemove.remove();
    this.displayList(parent);
  }

  saveSort(positions, parent) {
    this.ls.saveSort(positions);
    this.displayList(parent);
  }
}
