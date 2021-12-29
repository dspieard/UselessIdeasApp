import re
from flask import Flask, render_template, url_for, request, redirect
from flask.json.tag import TaggedJSONSerializer
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Ideas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __rep__(self):
        return '<Idea %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        idea_content = request.form["content"]
        new_idea = Ideas(content=idea_content)

        try:
            db.session.add(new_idea)
            db.session.commit()
            return redirect('/')
        except:
            return "Diz No Work"

    else:
        ideas = Ideas.query.order_by(Ideas.date_created).all()
        return render_template("index.html", ideas=ideas )

@app.route('/delete/<int:id>')
def delete(id):
    idea_to_delete = Ideas.query.get_or_404(id)

    try:
        db.session.delete(idea_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Diz No Work"

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    idea = Ideas.query.get_or_404(id)

    if request.method == 'POST':
        idea.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Diz No Work"

    else:
        return render_template('update.html', idea = idea)

@app.route('/complete/<int:id>', methods=['GET','POST'])
def complete(id):
    idea = Ideas.query.get_or_404(id)

    idea.completed = 0 if idea.completed == 1 else 1

    try:
        db.session.commit()
        return redirect('/')
    except:
        return "Diz No Work"


    return render_template('/', idea = idea)


if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')
