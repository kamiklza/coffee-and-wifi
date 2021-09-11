from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)



coffee_quality = ["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"]
wifi_quality = ["💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
power_supply = ["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]



class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location', validators=[DataRequired()])
    opening_time = StringField('Opening Time e.g 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g 6PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[(1, coffee_quality[0]), (2, coffee_quality[1]), ("test", coffee_quality[2]), (4, coffee_quality[3]), (5, coffee_quality[4])])
    wifi_signal = StringField('Wifi Signal', validators=[DataRequired()])
    power_socket = StringField('Power Socket Available', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit() and request.method == "POST":
        with open('cafe-data.csv', 'a') as csv_file:
            csv_file.write(f"\n{form.cafe.data},{form.location.data}.{form.opening_time.data},{form.closing_time.data},"
                           f"{form.coffee_rating.data},{form.wifi_signal.data},{form.power_socket.data}")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='',  encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
