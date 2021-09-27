from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Todo
from . import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return render_template('index.html')

    todos = (
        Todo.query.filter_by(owner_id=current_user.id)
        .order_by(Todo.date_added.desc())
        .all()
    )

    if request.method == 'POST':
        if 'is_done' in request.form:
            todo = Todo.query.get_or_404(request.form.get('is_done'))
            todo.is_done = not todo.is_done
            db.session.commit()
            return redirect(url_for('main.home'))
        elif 'todo' in request.form:
            todo_text = request.form.get('todo')

            if todo_text.strip() and not todo_text.isspace():
                new_todo = Todo(text=todo_text, owner_id=current_user.id)
                db.session.add(new_todo)
                db.session.commit()
                return redirect(url_for('main.home'))
            else:
                flash('Todo text cannot be empty.', 'info')
                return redirect(request.path)
        else:
            return redirect(url_for('main.home'))
    return render_template('index.html', todo_list=todos)


@main.route('/edit/<int:pk>', methods=['GET', 'POST'])
@login_required
def edit_todo(pk):
    todo = Todo.query.get_or_404(pk)

    if request.method == 'POST':
        todo_text = request.form.get('todo')

        if todo_text.strip() and not todo_text.isspace():
            todo.text = todo_text
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('Todo text cannot be empty.', 'info')
            return redirect(request.path)
    return render_template('index.html', todo=todo)


@main.route('/delete/<int:pk>', methods=['POST'])
@login_required
def delete_todo(pk):
    todo = Todo.query.get_or_404(pk)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.home'))
