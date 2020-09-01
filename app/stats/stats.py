from flask import Blueprint, render_template, session, redirect, url_for, request
import os
from app.trans.forms import StatementInput
from app import db
import app.gv as gv
from .controllers import yearAnaDF, monAnaDF, graphPlot
from flask_login import (current_user, login_required)
import pandas as pd
import json



# Blueprint Configuration
stats_bp = Blueprint('stats_bp',__name__,
                    template_folder='templates',
                    static_folder='static'
                    )




###############################################################################
#                           TRANSACTIONS PAGE
# This page presents the transactions of the user
#
###############################################################################
@stats_bp.route("/transactions")
@login_required
def transactions():
    df = gv.df
    df['Debit'] = round(df['Debit'],3)
    df['Credit'] = round(df['Credit'],3)
    return render_template("transactions.html", df=df, leng=len(df))




###############################################################################
#                              STATISTICS PAGE
# This page displays the statistics of user's spending
# None logged in users cannot view this page
###############################################################################
@stats_bp.route("/statistics", methods=["GET","POST"])
@login_required
def statistics():
    # check that years gets updated in the form before loding the page
    # StatementInput.yearsList=[]
    while StatementInput.yearsList != gv.yearsList:
        StatementInput.yearsList = gv.yearsList
        for y in StatementInput.yearsList:
            StatementInput.years.append((y,y))

    form = StatementInput()
    df = gv.df
    monthDic = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
                'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    if request.method == 'POST':
        option = request.form["top_options"]
        if (option == "Category" or option == "Account"):
            year = int(form.year.data)
            month = monthDic[request.form.get('month')]
            monExp, monIn, saving = monAnaDF(df,option,month,year)
            graphPlot(monExp,monIn,f"{current_user.id}output")
        elif (option == "Year Average"):
            monInDF, monExpDF = yearAnaDF(df,gv.yearsList)
            monIn = round(monInDF.mean(axis=1),3)
            monExp = round(monExpDF.mean(axis=1),3)
            saving = (monIn.sum())-(monExp.sum())
            graphPlot(monExp,monIn,f"{current_user.id}output")
        else:
            option = ""
            monExp, monIn = pd.DataFrame(),pd.DataFrame()
            saving = 0

    else:
        option = ""
        monExp, monIn = pd.DataFrame(),pd.DataFrame()
        saving = 0
    return render_template("statistics.html", form = form,
                                    option=option,
                                    monExp=round(monExp,3), exLen = len(monExp),
                                    monIn=round(monIn,3), inLen = len(monIn),
                                    saving=round(saving,3),
                                    monDic = json.dumps(gv.monDic),
                                    name=f"{current_user.id}output")
