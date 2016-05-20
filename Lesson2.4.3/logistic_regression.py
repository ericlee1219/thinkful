
# coding: utf-8

# In[100]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import collections
import scipy.stats as stats
import math
get_ipython().magic('matplotlib inline')


# In[44]:

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')
loansData.head()


# Clean Interest Rate column by removing "%" and converting to float

# In[45]:

cleanInterestRate = loansData['Interest.Rate'].map(lambda x: float(x.rstrip('%'))/100)
loansData['Interest.Rate'] = cleanInterestRate


# Clean Loan Length column by removing " month" and converting to integer

# In[46]:

cleanLoanLength = loansData['Loan.Length'].map(lambda x: int(x.rstrip(" months")))
loansData['Loan.Length'] = cleanLoanLength


# Convert FICO-Range to Series of Lists

# In[47]:

cleanFICORange = loansData['FICO.Range'].map(lambda x: x.split("-"))
type(cleanFICORange.head().values[0][0])


# Convert strings to integers using list comprehension

# In[48]:

cleanFICORange = cleanFICORange.map(lambda x:[int(n) for n in x])
type(cleanFICORange.head().values[0][0])


# Add Lower, Upper and Avg FICO score to DF

# In[49]:

LowerFICORange = [item[0] for item in cleanFICORange]
UpperFICORange = [item[1] for item in cleanFICORange]
loansData['LowerFICO'] = LowerFICORange
loansData['UpperFICO'] = UpperFICORange
loansData['FICO.Avg'] = loansData[['LowerFICO','UpperFICO']].mean(axis=1)
loansData.head()


# Added new column to data frame (binary) of 0 or 1 depending on if loan is > 12%.  Used querying function in pandas

# In[129]:

loansData['IR_TF'] = 0
loansData['IR_TF'][loansData['Interest.Rate']<0.12] = 1
loansData['IR_TF'][loansData['Interest.Rate']>=0.12] = 0
loansData.head()


# In[130]:

loansData['Intercept'] = 1.0


# In[131]:

loansData['LowerFICO'].astype(float)


# Make list of independent variables that we want to test

# In[132]:

ind_vars = ["Amount.Requested", 'LowerFICO','Intercept']


# Initialize Logistic Regression

# In[133]:

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])
result = logit.fit()
coeff = result.params
result.summary()


# Write a function that determines probability of getting a loan interest rate less than 12%

# In[134]:

print(coeff)


# In[137]:

def logistic_function(FICOScore, LoanAmount):
    return (1/(1 + math.exp((-0.000174)*(LoanAmount) + 0.087423*(FICOScore) - 60.125045)))


# In[140]:

logistic_function(720, 10000)


# In[ ]:



