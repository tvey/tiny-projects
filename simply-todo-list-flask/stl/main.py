from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'blah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stl.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id}>'


@app.route('/', methods=['GET', 'POST'])
def home():
    todos = Todo.query.all()
    print(todos)

    if request.method == 'POST':
        todo_text = request.form.get('todo')
        print(todo_text)

        if todo_text.strip() and not todo_text.isspace():
            new_todo = Todo(text=todo_text)
            print('new todo', new_todo)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    return render_template('index.html', todo_list=todos)



@app.route('/edit/<int:pk>', methods=['GET', 'POST'])
def edit_todo(pk):
    todo = Todo.query.get_or_404(pk)

    if request.method == 'POST':
        todo.text = request.form.get('todo')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', todo=todo)



@app.route('/delete/<int:pk>', methods=['POST'])
def delete_todo(pk):
    todo = Todo.query.get_or_404(pk)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
