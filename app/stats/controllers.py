import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import os




###############################################################################
#                       yearAnaDF(df,anaPar)
# This function takes the dictionary of DF and returns two new DFs that have
# columns as years and rows as months. The first DF is for income and the
# second DF is for expenses. Belwo is the output DF Structure
#     | Year 1 | Year 2 | Year 3
# M 1 | Total  |  Total | Total
# M 2 | Total  |  Total | Total
# M 3 | Total  |  Total | Total
###############################################################################
def yearAnaDF(df,years):
    inDF = df[df['Credit']!=0]
    exDF = df[df['Debit']!=0]
    monInTotal = {}
    monExTotal = {}

    for y in years:
        monInTotal[y]=(inDF[inDF['Year']==y].groupby('Month').sum()['Credit'])
        monInTotal[y].index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug',
                                'Sep','Oct','Nov','Dec']
        monExTotal[y]=(exDF[exDF['Year']==y].groupby('Month').sum()['Debit'])
        monExTotal[y].index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug',
                                'Sep','Oct','Nov','Dec']

    monInDF = pd.DataFrame(monInTotal)
    monExDF = pd.DataFrame(monExTotal)

    return monInDF, monExDF




###############################################################################
#                       monAnaDF(df,anaPar)
# This function takes the df and returns 2 Panda Series for Total Monthly
# Income and Total monthly expenses. anaPar is the analysis Parameter
# (Category or Account)
###############################################################################
def monAnaDF(df,anaPar,month,year):
    inDF = df[df['Credit']!=0]
    exDF = df[df['Debit']!=0]
    monExp= exDF[(exDF['Month']==month) & (exDF['Year']==year)
                    ].groupby(anaPar).sum()['Debit']
    monIn= inDF[(inDF['Month']==month) & (inDF['Year']==year)
                    ].groupby(anaPar).sum()['Credit']
    saving = (monIn.sum())-(monExp.sum())
    return monExp, monIn, saving




###############################################################################
#                       graphPlot(s1,s2,name)
# This function takes the series 1 and Series 2 and the file name and then saves
# a plot of these series in a path to view later in the web page
#
###############################################################################
def graphPlot(s1,s2,name):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    sns.set(font_scale=7)
    fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(70,49))
    ax[0].set(xlabel='Amount (OMR)', ylabel='Category', title="Expenses")
    sns_plot = sns.barplot(x=s1.values,y=s1.index,ax=ax[0])
    ax[1].set(xlabel='Amount (OMR)', ylabel='Category', title="Income")
    sns_plot = sns.barplot(x=s2.values,y=s2.index,ax=ax[1])
    fig.tight_layout()
    sns_plot.figure.savefig(f"{base_dir}/static/images/{name}",
                            transparent=True)
