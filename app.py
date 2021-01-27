from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # refrencing this file

# index route when we go to the main URL


# here is the path for our database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  #intialise a data base

class Todo(db.Model): # create a model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):   # return task and id of the task created
        return '<Task %r>' % self.id


# function for that route
# url string for the website , this will accept two things and send data to our database

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # the input of the task content in the index page
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #newest to older
        return render_template('index.html', tasks=tasks) #pass this to our template


@app.route('/delete/<int:id>')
def delete(id): #function 
    task_to_delete = Todo.query.get_or_404(id) #variable to get the id

    try:
        db.session.delete(task_to_delete) 
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content'] #update logic the current content is getiing updated 

        try:
            db.session.commit() 
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__": #if error thatyll pop error on the screen   
    app.run(debug=True)