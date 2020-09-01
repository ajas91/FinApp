from flask_wtf import FlaskForm
from wtforms import *
import app.gv as gv
import operator
from wtforms.validators import ValidationError, InputRequired, Email



# This form is used in Upload statement page to give the user a choice to select
# which bank statement they are uploading.
class StatementForm(FlaskForm):
    bank = SelectField('Bank', choices=[('nbo','NBO Account'),
                                        ('muscat','Bank Muscat Account'),
                                        ('mct_crdt','Bank Muscat Credit Card')])

    accounts = gv.accountList
    accounts = SelectField('Accounts', choices= accounts)



class CategoriesList(FlaskForm):
    incomeCat = gv.incomeCatList
    expenseCat = gv.expenseCatList
    incomeCat.sort(key = operator.itemgetter(1))
    expenseCat.sort(key = operator.itemgetter(1))
    in_category = SelectField('Category', choices= incomeCat, default=0)
    ex_category = SelectField('Category', choices= expenseCat, default=0)



class StatementInput(CategoriesList):
    months = [(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'Jun'),
              (7,'Jul'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec')]
    months = []
    yearsList = [] # a list of all years in the the db duplicated
    years=[('','')] # list of years not duplicated
    save = SubmitField('Save')
    # month = SelectField('Month')
    year = SelectField('Year',choices = years)





class tranInput(StatementInput):
    description = TextField('Description', validators=[InputRequired()])
    debit = FloatField('Debit', default=0.0)
    credit = FloatField('Credit', default=0.0)
    date = DateField('Date', format='%m/%d/%Y', validators=[InputRequired()])
