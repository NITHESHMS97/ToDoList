from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"


@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        print(f"{title} {description}")
        todo = Todo(title=title,description=description)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    #print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    print(type(allTodo))
    return 'show'

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.description = description
        print(f"{title} {description}")
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    updateTodo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html',updateTodo=updateTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    RemoveTodo = Todo.query.filter_by(sno = sno).first()
    print(RemoveTodo)
    db.session.delete(RemoveTodo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)