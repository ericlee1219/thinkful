
# coding: utf-8

# In[43]:

import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import collections
get_ipython().magic('matplotlib inline')


# In[16]:

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')
loansData.head()


# In[17]:

loansData.dropna(inplace = True)


# In[27]:

loansData.boxplot(column="Amount.Funded.By.Investors")
plt.show()
loansData.boxplot(column='Amount.Requested')
plt.show()


# In[25]:

loansData.hist(column='Amount.Funded.By.Investors')
loansData.hist(column='Amount.Requested')
plt.show()


# In[24]:

plt.figure()
graph1 = stats.probplot(loansData['Amount.Funded.By.Investors'], dist="norm", plot=plt)
plt.show()
graph2 = stats.probplot(loansData['Amount.Requested'], dist='norm',plot=plt)
plt.show()


# In[32]:

freq = collections.Counter(loansData['Open.CREDIT.Lines'])


# In[55]:

len(freq)


# In[50]:

x = freq.values()
list_values = [ v for v in freq.values() ]
list_values


# In[35]:

plt.figure()
plt.bar(freq.keys(), freq.values(), width=1)
plt.show()


# In[52]:

chi, x = stats.chisquare(list_values)


# In[53]:

chi


# In[54]:

x

