from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_wtf.csrf import CSRFProtect
from service import check_data,check_vaccine
from input_form import InputForm

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    DEBUG = True
))
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


@app.route("/", methods=["GET", "POST"])
def index():
    form = InputForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('index.jinja2', form = form)
        else:
             return render_template('data.jinja2', form = form)
    elif request.method == 'GET':
        return render_template('index.jinja2', form = form)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     mobile = InputForm()

#     if request.method == 'POST':
#         print(requests.post("https://cdn-api.co-vin.in/api/v2/auth/generateOTP", data = {'mobile': 9113598549}))
#         return render_template('index.jinja2', mobile = mobile)
#     return render_template('authentication.jinja2', mobile = mobile)

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == 'POST':
        
        flag, state, district = check_data(request.form['age'],request.form['pincode'])
        print(request.form['pincode'], request.form['age'],request.form['start_date'], request.form['type'], request.form['availability'])

        if flag == True and int(request.form['age']) >= 18:
        
            data = check_vaccine(request.form['pincode'], request.form['age'],request.form['start_date'], request.form['type'], request.form['availability'])
            if not data.empty:
                return render_template("data.jinja2",template="data-template", data = data, state = state, district = district)
            else:
                return render_template("index.jinja2", form = InputForm())
        
        else:
            flash("Bad Data")
            return render_template("index.jinja2", form = InputForm())

    return render_template("data.jinja2")

if __name__ == "__main__":
    app.run(debug = True)