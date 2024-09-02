from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# Configure SQLAlchemy with SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    priority = db.Column(db.Integer)

    def __repr__(self):
        return f'<Todo {self.task}>'

# Create tables when the application starts
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.priority.desc(), Todo.due_date).all()
    return render_template("index.html", todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    due_date = request.form.get('due_date')
    priority = int(request.form.get('priority'))
    
    if task:
        due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
        new_todo = Todo(task=task, due_date=due_date, priority=priority)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':
        todo.task = request.form.get('task')
        todo.due_date = request.form.get('due_date')
        todo.priority = int(request.form.get('priority'))
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo)

@app.route('/done/<int:todo_id>')
def mark_done(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.done = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)