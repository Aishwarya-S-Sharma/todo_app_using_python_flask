from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)  # Updated to use utcnow

    def __repr__(self) :
        return '<Task %r>'%self.id

with app.app_context():
        db.create_all()

@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
             return 'There was an issue adding your task'

    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Failed to delete your tasks'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)  # Retrieve the task to update

    if request.method == 'POST':
        task_to_update.content = request.form['content']  # Update the task content
        try:
            db.session.commit()  # Commit the changes
            return redirect('/')  # Redirect after updating
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task_to_update)  # Render update form
if __name__=="__main__":
    app.run(debug=True)