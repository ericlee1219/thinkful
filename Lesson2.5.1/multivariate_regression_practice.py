
# coding: utf-8

# In[11]:

import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import collections
import statsmodels.api as sm
import statsmodels.formula.api as smf
get_ipython().magic(u'matplotlib inline')


# In[2]:

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')
loansData.head()
loansData = loansData.dropna()
loansData['Interest.Rate'][0:5]


# In[3]:

cleanInterestRate = loansData['Interest.Rate'].map(lambda x: float(x.rstrip('%')))
cleanInterestRate.head()


# In[4]:

loansData['Loan.Length'][0:5]


# In[5]:

cleanLoanLength = loansData['Loan.Length'].map(lambda x: float(x.rstrip(" months")))
cleanFICORange = loansData['FICO.Range'].map(lambda x: x.split("-"))
cleanDebtToIncome = loansData['Debt.To.Income.Ratio'].map(lambda x: float(x.rstrip('%')))
cleanFICORange = cleanFICORange.map(lambda x: [int(n) for n in x])
loansData['FICO.Range'] = cleanFICORange
loansData.head()
cleanEmploymentLength = loansData['Employment.Length'].map(lambda x: x.rstrip(" years"))
cleanEmploymentLength = cleanEmploymentLength.map(lambda x: x.rstrip("+"))
cleanEmploymentLength[cleanEmploymentLength == '< 1'] = 1
cleanEmploymentLength[cleanEmploymentLength == 'n/'] = 0
cleanEmploymentLength = cleanEmploymentLength.map(lambda x: int(x))
loansData['Employment.Length'] = cleanEmploymentLength
loansData['Interest.Rate'] = cleanInterestRate
loansData['Loan.Length'] = cleanLoanLength
loansData['Debt.To.Income.Ratio'] = cleanDebtToIncome
loansData.head()


# In[41]:

loansData['IR_TF'] = 0
loansData['IR_TF'][loansData['Interest.Rate'] < 12] = 0
loansData['IR_TF'][loansData['Interest.Rate'] >= 12] = 1
loansData.head()


# In[6]:

cleanFICORangeAverages = [np.mean(item) for item in cleanFICORange]
cleanFICORangeAverages
cleanFICORange2 = [item[0] for item in cleanFICORange]
loansData['FICO.Range'] = cleanFICORange2
plt.figure()
p = loansData['FICO.Range'].hist()
plt.show()


# In[13]:

loansData['Interest_Rate'] = loansData['Interest.Rate']
loansData['Amount_Requested'] = loansData['Amount.Requested']
loansData['FICO_Range'] = loansData['FICO.Range']


# In[7]:

a = pd.scatter_matrix(loansData, alpha = 0.05, figsize = (10,10))
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Range']


# In[8]:

# MODEL #1 With Loan Amount / FICO Score and Interest Rate
y = np.array(intrate).transpose()
x1 = np.array(loanamt).transpose()
x2 = np.array(fico).transpose()


# In[33]:

loansData.shape


# In[45]:

est = smf.ols(formula='Interest_Rate ~ Amount_Requested + IR_TF', data=loansData).fit()
est.summary()

est2 = smf.ols(formula='Interest_Rate ~ Amount_Requested * IR_TF', data=loansData).fit()
est2.summary()

est3 = smf.ols(formula='Interest_Rate ~ Amount_Requested', data=loansData).fit()
est3.summary()


# In[47]:

plt.scatter(loansData.Amount_Requested, loansData.Interest_Rate, alpha=0.3)
Amount_Requested_linspace = np.linspace(loansData.Amount_Requested.min(), loansData.Amount_Requested.max(), 2498)
Amount_Requested_linspace
plt.plot(Amount_Requested_linspace, est3.predict(Amount_Requested_linspace), 'r')
plt.xlabel('Amount_Requested')
plt.ylabel('Interest_Rate')


# In[9]:

x_1 = np.column_stack([x1,x2])
X1 = sm.add_constant(x_1)
model1 = sm.OLS(y,X1)
f1 = model1.fit()
f1.summary()


# In[ ]:




# In[ ]:



