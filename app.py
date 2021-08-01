from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///widgets.db'
db = SQLAlchemy(app)


class Widgets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    num_parts = db.Column(db.Integer, nullable=False)
    row_location = db.Column(db.String(20), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.name}: {self.id}"
# end Widgets model


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        widget_content = request.form.get('widget')
        pieces_value = request.form.get('parts')
        row_loc = request.form.get("row_location")
        new_widget = Widgets(name=widget_content, num_parts=pieces_value,
                             row_location=row_loc)

        try:
            db.session.add(new_widget)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue adding the new widget!!'
    else:
        widgets = Widgets.query.order_by(Widgets.created_date).all()
        return render_template('index.html', widgets=widgets)


@app.route('/add')
def insert_new_record():
    return render_template('insert_record.html')


@app.route('/delete/<int:id>')
def delete_widget(id):
    widget_to_delete = Widgets.query.get_or_404(id)
    try:
        db.session.delete(widget_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return "There was issue deleting the widget"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_widget(id):
    widget_to_update = Widgets.query.get_or_404(id)
    if request.method == 'POST':
        widget_to_update.name = request.form.get('widget')
        widget_to_update.num_parts = request.form.get('parts')
        widget_to_update.row_location = request.form.get('row_location')

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return "Issue updating the widget"

    else:
        return render_template('update.html', widget=widget_to_update)


if __name__ == '__main__':
    app.run()
