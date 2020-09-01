from flask import (Blueprint, render_template, session, redirect,
                    url_for, request,flash)
from passlib.hash import pbkdf2_sha256
import os
from .forms import StatementForm, StatementInput, tranInput
from .models import trans
from app import db
from flask_login import (current_user, login_required)
from app.profile.controllers import encrypt
from .controllers import allowed_file, read_statement,addSel2DF,convertDF2DB
from datetime import datetime



# Blueprint Configuration
trans_bp = Blueprint('trans_bp',__name__,
                    template_folder='templates',
                    static_folder='static'
                    )
dir = os.path.dirname(__file__)





###############################################################################
#                           UPLOAD STATEMENT PAGE
# This page allows the user to upload his statements.
# None logged in users cannot view this page
###############################################################################
@trans_bp.route("/up_statement", methods=["GET","POST"])
@login_required
def up_statement():
    session['upload']=dir+'/upload'
    form = StatementForm()

    if request.method == 'POST':
        file = request.files['file']
        fileName = str(current_user.id)+file.filename
        if allowed_file(file.filename):
            session['file'] = os.path.join(session['upload'],
                              fileName) #save the file path
            file.save(session['file']) #save the file in the directory
            session['selected_bank']=form.bank.data
            session['selected_account_id']=int(form.accounts.data)
            session['selected_account']=dict(form.accounts.choices).get(
                                                    int(form.accounts.data))
            return redirect(url_for('trans_bp.confirm_statement'))
        else:
            flash("File Extension not allowed!")
    return render_template("up_statement.html", form=form)





###############################################################################
#                   STATEMENT COMPLETION & CONFIRMATION PAGE
# This page appears after the user uploads the bank statement and allows them to
# choose the account and the category
###############################################################################
@trans_bp.route("/up_statement/confirm_statement", methods=["GET","POST"])
@login_required
def confirm_statement():

    forms = []
    #convert the uploaded statement into dataframe
    df = read_statement(session['file'],session['selected_bank'])
    #read the account selected when uploading the statement
    df['Account'] = session['selected_account']
    #create the account and category choosing buttons
    for i in range(len(df)):
        forms.append(StatementInput(prefix = str(i)))
    #check if the user clicked on Save, then add the selection to the DF,
    #add the DF to DB
    if forms[0].save.data:
        new_df = addSel2DF(forms,df)
        new_df['user_id']= current_user.id
        new_df['Account']= session['selected_account_id']
        print(f"#############{new_df['date']}")
        new_df['date']=new_df['date'].apply(lambda x: datetime.strptime(x,
                                            '%Y/%m/%d').date())
        convertDF2DB(new_df)
        # remove the uploaded excel file
        os.remove(session['file'])

        return redirect(url_for('profile_bp.welcome'))

    return render_template("confirm_statement.html",
                            df = df,
                            forms = forms, leng=len(df))




###############################################################################
#                           ADD TRANSACTIONS PAGE
# This page presents the transactions of the user
#
###############################################################################
@trans_bp.route("/addtrans", methods=["GET","POST"])
@login_required
def addTrans():
    form = tranInput()
    accForm = StatementForm()
    PASS = os.getenv('PASS')
    if request.method == 'POST':
        date = datetime.strptime(request.form.get("date"),'%Y-%m-%d').date()
        print(f"###########################{date}")
        description = form.description.data
        selectValue = int(request.form.get('SelectCat'))
        if (selectValue == 1):
            category = int(form.in_category.data)
        elif (selectValue == 2):
            category = int(form.ex_category.data)
        account = int(accForm.accounts.data)
        credit = form.credit.data
        debit = form.debit.data
        tran = trans(user = current_user,
                    date = date,
                    description = encrypt(PASS,description),
                    debit = encrypt(PASS,str(debit)),
                    credit = encrypt(PASS,str(credit)),
                    category_id = category,
                    account_id = account)
        db.session.add(tran)
        db.session.commit()
        return redirect(url_for('profile_bp.welcome'))

    return render_template("addtrans.html", form = form, accForm = accForm)
