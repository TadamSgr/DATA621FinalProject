#!/usr/bin/env python
# coding: utf-8

# In[30]:


import numpy as np

import pandas as pd
pd.options.display.max_rows = 4000


# In[31]:


data=pd.read_csv("ADMISSIONS.csv")
icd=pd.read_csv("D_ICD_DIAGNOSES.csv")
diag=pd.read_csv("DIAGNOSES_ICD.csv")


# In[32]:


ldata=pd.merge(icd, diag, on="ICD9_CODE")

ldata= ldata.drop(columns=['ROW_ID_x', 'ICD9_CODE', 'LONG_TITLE', 'ROW_ID_y',
                           'SUBJECT_ID', 'SEQ_NUM'])

ldata=pd.merge(ldata, data, on="HADM_ID")
display(ldata.head())


# Get only data on newborn children admitted to neonatal ICU:

# In[33]:


ndata=ldata[ldata['ADMISSION_TYPE'] == 'NEWBORN']
ndata


# In[34]:


len(ndata['HADM_ID'].unique()) # number of newborns


# In[35]:


#add length of stay to dataframe:

los=pd.read_csv('ICUSTAYS.csv') 
ndata=pd.merge(ndata, los, on="HADM_ID")


# Get only infants whose stay is longer than 2 days. This is to remove most infants who are not admitted to NICU with a serious health insult, such as those going there for a routine circumsision:

# In[36]:


ndata=ndata[ndata['LOS'] >= 48]


# In[37]:


len(ndata['HADM_ID'].unique()) # number after removing those with short stays.


# Get counts of common ailments:

# In[38]:


diagg=pd.DataFrame(ndata['SHORT_TITLE'].value_counts())


# In[39]:


print(diagg)


# Based on the breakdown of aliments affecting newborns, difficulties with the respiratory system and circulatory system are very prevalent among preterm and non-preterm infants as reasons for admission to the ICU. As such, we decided to focus on the effect that these conditions, as well as the degree to which an infant was premature, had on the length of stay in the ICU and their discharge location. As the number of diagnoses is large, we categorized insults to these systems into 5 categories of disease. Only insults that appeared in at least 10 diagnoses overall were included in categorization. These categories are:
# 
# - **cardiac hemorrage (1/0)**: included were conditions such as intraventricular hemorrages, pulmonary hemorrages.
# - **circulatory system malformation (1/0)**: included were conditions such as patent ductus arteriosus, ventricular septal defect.
# - **heart rate/circulation issues (1/0)**: Included were conditons such as neonatal bradycardia, hypotension.
# - **preterm** (0 = not preterm, 1 = preterm, 2 = extreme preterm (defined in database as < 1kg)
# - **respiratory distress (1/0)**: included were conditiions such as atelectasis, apnea, respiratory distress syndrome.
# - **sepsis (1/0)**
# - **jaundice (1/0)**: Though the diagnosis is listed as 'preterm jaundice' this label; is applied to many non-preterm infants, suggesting it is used as a generic jaundice diagnosis for infants. As such, we have considered it as such. 
# 
# Patients can be diagnosed with multiple of the above conditions simultaneously.

# In[40]:


diagg=diagg.reset_index()


# In[41]:


#this is the full list of conditions which had at least 10 occurrences, and were pertinent to the above categories:

dg=['Respiratory distress syn', 'Primary apnea of newborn','Patent ductus arteriosus', 'Neonatal bradycardia', 
    'Anemia of prematurity','Perinatal chr resp dis','Preterm NEC 1000-1249g', 'Extreme immatur 750-999g','Preterm NEC 1250-1499g', 
    'Extreme immatur 500-749g','NB intraven hem,grade i','Secundum atrial sept def', 'Other apnea of newborn',
   'Preterm NEC 1500-1749g','NB interstit emphysema','Cong pulmon valve stenos','Ventricular sept defect',
   'Resp prob after brth NEC', 'Hypotension NOS', 'NB intraven hem,grade ii','Preterm NEC 750-999g', 'NB intraven hem NOS', 
    'Ab ftl hrt rt/rhy NOS','NB transitory tachypnea', 'Preterm NEC 500-749g', 'NB atelectasis NEC/NOS', 
    'NB intravn hem,grade iii','NB pulmonary hemorrhage', 'Neonat jaund preterm del', 'NB septicemia [sepsis]']

diagCat=ndata.query('SHORT_TITLE in @dg')


# In[42]:


#this is how each of the above was categorized:

cat=['respiratory','respiratory','circulatory system malformation',
                     'heart rate/circulation issues','heart rate/circulation issues','respiratory', 'preterm',
                     'extreme preterm','preterm','extreme preterm',
                     'cardiac hemorrage', 'circulatory system malformation', 
                     'respiratory', 'preterm','respiratory', 'circulatory system malformation',
                    'circulatory system malformation', 'respiratory',
                     'heart rate/circulation issues', 'cardiac hemorrage',
                     'preterm', 'cardiac hemorrage','heart rate/circulation issues',
                     'respiratory', 'preterm','respiratory','cardiac hemorrage','cardiac hemorrage', 'jaundice', 'sepsis']
diagCat=diagCat.replace(dg, cat)


# In[43]:


#breakdown of ailment inclusion and categorization:

for i in range(len(dg)):
    print(dg[i], "was categorized as", cat[i])


# In[44]:


drop=['ROW_ID_y', 'ROW_ID_x','ADMISSION_TYPE', 'DBSOURCE', 'INSURANCE','LANGUAGE', 'RELIGION',
       'MARITAL_STATUS', 'ETHNICITY','HAS_CHARTEVENTS_DATA','SUBJECT_ID_y', 'EDREGTIME', 'EDOUTTIME',
     'DIAGNOSIS']
diagCat=diagCat.drop(drop, axis=1)


# Pivot table to get categories in presence/absence format, and get 1 row per patient:

# In[45]:


ccc=diagCat.iloc[:,:2]
ccc=ccc.drop_duplicates()
ccc['val']=1
ccc=ccc.pivot(index='HADM_ID', columns='SHORT_TITLE')['val']
ccc=ccc.fillna(0)
ccc=ccc.reset_index()


# In[46]:


ccc
#we have separate columns for preterm and extreme preterm here, but we collapse this into 1 further down


# In[47]:


g=ndata[['SUBJECT_ID_x','HADM_ID','DISCHARGE_LOCATION', 'LOS']]


# In[48]:


ccc=pd.merge(ccc, g, on="HADM_ID")
ccc=ccc.drop_duplicates()


# In[49]:


#add infant sex to dataframe
ind=pd.read_csv('PATIENTS.csv')


# In[50]:


ccc = ccc.rename(columns={'SUBJECT_ID_x': 'SUBJECT_ID'})


# In[51]:


ccc=pd.merge(ccc, ind, on='SUBJECT_ID')


# In[52]:


drop=['SUBJECT_ID', 'ROW_ID', 'DOB', 'DOD', 'DOD_HOSP', 'DOD_SSN', 'EXPIRE_FLAG']
ccc=ccc.drop(drop, axis=1)


# categorize preterms into 3 categories:

# In[53]:


mask = (ccc['extreme preterm'] == 1)
ccc['preterm'][mask] = 2


# In[54]:


ccc=ccc.drop('extreme preterm', axis=1)


# Add column for censorship. Only 1 death, so only 1 patient in censored in terms of their leaving the ICU:

# In[55]:


ccc['delta']=1
mask = (ccc['DISCHARGE_LOCATION'] == 'DEAD/EXPIRED')
ccc['delta'][mask] = 0


# In[56]:


#Final dataframe:
ccc


# In[57]:


#export_csv = ccc.to_csv ('datadfpretermNew.csv', index = None, 
 #                              header=True)

