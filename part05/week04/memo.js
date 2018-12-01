function addToDo() {
    let todo = document.getElementById('newItem').value;
    let important = document.querySelector('input[type="radio"]:checked').value;
    addItem(todo, status = 'todo', important);
    initToDo();
}

function addItem(memo, status = 'todo', important = 1) {
    let todo_list = [];
    let old_list = localStorage.getItem('ywbToDo');
    if (old_list) {
        todo_list = JSON.parse(old_list);
    }
    let todo = {}
    todo.id = 1;
    if (old_list) {
        todo.id += parseInt(todo_list[todo_list.length - 1].id);
    }
    todo.text = memo;
    todo.status = status;
    todo.important = important;
    todo_list.push(todo);
    localStorage.setItem('ywbToDo', JSON.stringify(todo_list))
}

function initToDo() {
    let todo_list = getTodoList();
    if (todo_list.length) {
        let todo_1 = todo_list.filter(x => x.important == 1);
        let todo_2 = todo_list.filter(x => x.important == 2);
        let todo_3 = todo_list.filter(x => x.important == 3);
        let todo_4 = todo_list.filter(x => x.important == 4);
        inserTodo(todo_1);
        inserTodo(todo_2, box_type='td-2');
        inserTodo(todo_3, box_type='td-3');
        inserTodo(todo_4, box_type='td-4');
    }
    updateDoneList();
}

function getTodoList() {
    return JSON.parse(localStorage.getItem('ywbToDo'));
}

function inserTodo(todos, box_type='td-1') {
    if (!todos.length) {
        return;
    }
    let class_id = box_type.split('-')[1];
    clearToDo(class_id);
    let box = document.getElementById(box_type);
    for (let todo of todos) {
        let li = document.createElement('li');
        li.className='toDoList' + class_id;
        li.innerHTML = ' <input type="checkbox" onclick="checkItem(this);" name="item" id=' + todo.id + '>' + todo.text;
        box.appendChild(li);
        updateDoneStyle(todo, li);
    }
}

function clearToDo(class_id) {
    let item_id = 'toDoList' + class_id;
    let list = document.getElementsByClassName(item_id);
    if(list.length){
        for(let i=list.length; i>0; i--){
            list[i-1].remove();
        }
    }
}

function checkItem(item) {
    let li = item.parentElement;
    if (item.checked) {
        li.style.textDecoration = 'line-through';
        changeStatus(item.id, 'done');
    }else{
        changeStatus(item.id, 'todo');
        li.style.textDecoration = '';
    }
    updateDoneList();
}

function changeStatus(id, status){
    let todo_list = getTodoList();
    for (let todo of todo_list){
        if(todo.id == id){
            todo.status = status;
        }
    }
    localStorage.setItem('ywbToDo', JSON.stringify(todo_list));
}

function updateDoneStyle(todo, li) {
    if (todo.status == 'done'){
        li.style.textDecoration = 'line-through';
        li.firstElementChild.checked = true;
    }else{
        li.style.textDecoration = '';
        li.firstElementChild.checked = false;
    }
}

function updateDoneList() {
    let box = document.getElementById('memoDone-list');
    box.innerHTML = '';
    let done_list = getTodoList().filter(x => x.status == 'done');

    for (let todo of done_list) {
        let li = document.createElement('li');
        li.innerHTML = todo.text;
        box.appendChild(li);
    }
}

function storageModify() {
    var storage=window.localStorage;
    console.log(storage);
    storage.removeItem('ywbToDo');
    storage.removeItem('de8ugtodo');
    location.reload(true);
}

initToDo();
