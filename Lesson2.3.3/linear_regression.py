
# coding: utf-8

# In[116]:

import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import collections
import statsmodels.api as sm
get_ipython().magic('matplotlib inline')


# In[2]:

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')
loansData.head()


# In[163]:

loansData = loansData.dropna()


# In[3]:

loansData['Interest.Rate'][0:5]


# In[54]:

cleanInterestRate = loansData['Interest.Rate'].map(lambda x: float(x.rstrip('%')))
cleanInterestRate.head()


# In[6]:

loansData['Loan.Length'][0:5]


# In[7]:

cleanLoanLength = loansData['Loan.Length'].map(lambda x: float(x.rstrip(" months")))


# In[14]:

cleanFICORange = loansData['FICO.Range'].map(lambda x: x.split("-"))


# In[59]:

cleanDebtToIncome = loansData['Debt.To.Income.Ratio'].map(lambda x: float(x.rstrip('%')))


# In[22]:

cleanFICORange = cleanFICORange.map(lambda x: [int(n) for n in x])


# In[23]:

loansData['FICO.Range'] = cleanFICORange


# In[24]:

loansData.head()


# In[41]:

cleanEmploymentLength = loansData['Employment.Length'].map(lambda x: x.rstrip(" years"))


# In[42]:

cleanEmploymentLength = cleanEmploymentLength.map(lambda x: x.rstrip("+"))


# In[48]:

cleanEmploymentLength[cleanEmploymentLength == '< 1'] = 1
cleanEmploymentLength[cleanEmploymentLength == 'n/'] = 0


# In[49]:

cleanEmploymentLength = cleanEmploymentLength.map(lambda x: int(x))


# In[60]:

loansData['Employment.Length'] = cleanEmploymentLength
loansData['Interest.Rate'] = cleanInterestRate
loansData['Loan.Length'] = cleanLoanLength
loansData['Debt.To.Income.Ratio'] = cleanDebtToIncome


# In[117]:

loansData.head()


# In[128]:

cleanFICORangeAverages = [np.mean(item) for item in cleanFICORange]
cleanFICORangeAverages


# In[113]:

cleanFICORange2 = [item[0] for item in cleanFICORange]
loansData['FICO.Range'] = cleanFICORange2


# In[115]:

plt.figure()
p = loansData['FICO.Range'].hist()
plt.show()


# In[142]:

a = pd.scatter_matrix(loansData, alpha = 0.05, figsize = (10,10))


# In[177]:

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Range']


# MODEL #1 With Loan Amount / FICO Score and Interest Rate

# In[178]:

y = np.array(intrate).transpose()
x1 = np.array(loanamt).transpose()
x2 = np.array(fico).transpose()


# In[170]:

x_1 = np.column_stack([x1,x2])
X1 = sm.add_constant(x_1)
model1 = sm.OLS(y,X1)
f1 = model1.fit()


# In[171]:

f1.summary()


# Model 2 with Debt to Income Ratio and Monthly Income vs. Loan Amount

# In[180]:

DtoIncRatio = loansData['Debt.To.Income.Ratio']
MonthlyInc = loansData['Monthly.Income']
x3 = np.array(DtoIncRatio).transpose()
x4 = np.array(MonthlyInc).transpose()
x_2 = np.column_stack([x3,x4])
X2 = sm.add_constant(x_2)


# In[181]:

model2 = sm.OLS(y,X2)
f2 = model2.fit()
f2.summary()


# Model 3 with all variables above

# In[183]:

x_3 = np.column_stack([x1,x2,x3,x4])
X3 = sm.add_constant(x_3)
model3 = sm.OLS(y,X3)
f3 = model3.fit()
f3.summary()

