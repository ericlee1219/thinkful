
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf
import math

get_ipython().magic('matplotlib inline')


# In[2]:

df = pd.read_csv("https://raw.githubusercontent.com/Thinkful-Ed/curric-data-001-data-sets/master/loans/loansData.csv")


# In[3]:

df.head()


# In[12]:

cleanIntRate = df["Interest.Rate"].map(lambda x: float(x.rstrip('%')))
cleanDebtToInc = df['Debt.To.Income.Ratio'].map(lambda x: float(x.rstrip('%')))
cleanLoanLength = df['Loan.Length'].map(lambda x: float(x.rstrip(' months')))
cleanFICORange = df['FICO.Range'].map(lambda x: x.split('-'))
cleanFICORange = cleanFICORange.map(lambda x: [int(n) for n in x])


# In[14]:

lowerFICO = [item[0] for item in cleanFICORange]


# In[15]:

upperFICO = [item[1] for item in cleanFICORange]


# In[39]:

df['Interest_Rate'] = cleanIntRate
df['Debt_To_Inc_Ratio'] = cleanDebtToInc
df['Loan_Length'] = cleanLoanLength
df['LowerFICO'] = lowerFICO
df['UpperFICO'] = upperFICO
df['Monthly_Income'] = df['Monthly.Income']
df['Home_Ownership'] = df['Home.Ownership']


# In[21]:

df.head()


# Use income (annual_inc) to model interest rates (int_rate).
# Add home ownership (home_ownership) to the model.
# Does that affect the significance of the coefficients in the original model?
# Try to add the interaction of home ownership and incomes as a term. How does this impact the new model?

# In[40]:

est = smf.ols(formula = 'Interest_Rate ~ Monthly_Income + Home_Ownership', data=df).fit()
est.summary()


# In[32]:

df['Home.Ownership'].unique()


# In[38]:

est = smf.ols(formula = "Interest_Rate ~ Monthly_Income + ", data = df).fit()
est.summary()


# In[ ]:



