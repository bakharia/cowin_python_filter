from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, InputRequired

class InputForm(FlaskForm):
    mobile = IntegerField('Mobile Number', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), validators.Required("Please enter your age.")])
    pincode = IntegerField('Pincode', validators = [DataRequired(), validators.Required("Please enter your pincode.")])
    type = SelectField(default = 'none', choices=[('all', 'All'),('paid','Paid'),('free','Free'),('none', '--SELECT FEE TYPE--')])
    start_date = DateField('Start Date', validators=[DataRequired()], format = '%d/%m/%Y', description = 'Time that the event will occur')
    availability = SelectField(default = 'none', choices=[('all', 'All'),('stock','In Stock'),('none', '--SELECT AVAILABILITY--')])
    submit = SubmitField('Submit')