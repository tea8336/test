$(
    addToDo(), storageModify()
)

function addToDo() {
    $('input[name="add"]').on('click', function() {
        let todo = $('#newItem').val();
        let important = $('input[type="radio"]:checked').val();
        addItem(todo, status = 'todo', important);
        initToDo();
    })
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
    if (todo_list != null && todo_list.length) {
        let todo_1 = todo_list.filter(x => x.important == 1);
        let todo_2 = todo_list.filter(x => x.important == 2);
        let todo_3 = todo_list.filter(x => x.important == 3);
        let todo_4 = todo_list.filter(x => x.important == 4);
        inserTodo(todo_1, box_type='td-1');
        inserTodo(todo_2, box_type='td-2');
        inserTodo(todo_3, box_type='td-3');
        inserTodo(todo_4, box_type='td-4');
        updateDoneList();
    }
}

function getTodoList() {
    return JSON.parse(localStorage.getItem('ywbToDo'));
}

function inserTodo(todos, box_type) {
    if (!todos.length) {
        return;
    }
    let class_id = box_type.split('-')[1];
    clearToDo(class_id);
    let n = 1;
    for (let todo of todos) {
        $('#' + box_type).append('<li id=' + box_type + '-' + n + '><input type="checkbox" onclick="checkItem(this);" name="item" id=' + todo.id + '>' + todo.text +'</li>');
        $('#' + box_type + '-' + n).attr('name', 'toDoList' + class_id);
        updateDoneStyle(todo, $('#' + box_type + '-' + n));
        n += 1;
    }
}

function clearToDo(class_id) {
    let item_id = 'toDoList' + class_id;
    let list = $('li[name="'+ item_id + '"]');
    list.each(function(){
        let item = $(this);
        item.remove();
    })
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
    console.log(li);
    if (todo.status == 'done'){
        li.css("text-decoration", "line-through");
        li.find('input[name="item"]').prop("checked", true);
    }else{
        li.css("text-decoration", "none");
        li.find('input[name="item"]').prop("checked", false);
    }
}

function updateDoneList() {
    let box = $('#memoDone-list');
    box.html('');
    let done_list = getTodoList().filter(x => x.status == 'done');
    let n = 1;
    for (let todo of done_list) {
        box.append('<li id=li' + n + '></li>');
        $('#li' + n).html(todo.text);
        n += 1;
    }
}

function storageModify() {
    $('input[name="clear"]').on('click', function() {
        var storage=window.localStorage;
        console.log(storage);
        storage.removeItem('ywbToDo');
        location.reload(true);
    })
}

initToDo();
