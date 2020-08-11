from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Databse Configuration And Location
db = SQLAlchemy(app) # Initialize Database


# Database Structure
class Todo(db.Model):
    # Database Columns
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__():
        return '<Task %s>' % self.id


@app.route("/", methods= ['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_name = request.form['task']
        task_content = request.form['content']

        new_task = Todo(task=task_name, content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Sorry, There was an issue creating your Task."

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)