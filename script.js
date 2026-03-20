// To-Do List Application with Local Storage

// Function to add a new to-do item
def addTodo() {
    const todoInput = document.getElementById('todo-input');
    const todoValue = todoInput.value;
    if (todoValue) {
        const todoList = getTodos();
        todoList.push(todoValue);
        saveTodos(todoList);
        todoInput.value = '';
        renderTodos();
    }
}

// Function to get to-do items from local storage
function getTodos() {
    return JSON.parse(localStorage.getItem('todos')) || [];
}

// Function to save to-do items to local storage
function saveTodos(todos) {
    localStorage.setItem('todos', JSON.stringify(todos));
}

// Function to render to-do items on the page
function renderTodos() {
    const todos = getTodos();
    const todoListElement = document.getElementById('todo-list');
    todoListElement.innerHTML = '';
    todos.forEach((todo, index) => {
        const todoItem = document.createElement('li');
        todoItem.textContent = todo;
        todoListElement.appendChild(todoItem);
    });
}

// Initial rendering of to-dos
renderTodos();

// Event listener for the add button
const addButton = document.getElementById('add-button');
addButton.addEventListener('click', addTodo);