# DATA621FinalProject
Modelling for Newborn Length of Stay in Intensive Care Units based on Diagnoses

Authors: Luke Larter and Trevor Seeger


# Background/Rationale
Newborn infants are particularly vulnerable to health upsets, thus understanding the determinants of intensive care unit (ICU) outcomes for newborns is integral for predicting how patients will recover. Additionally, complexity and duration of care received in neonatal intensive care unit (NICU) can be predictive of long-term effects on developmental outcomes (Subedi, Deboer, & Scharf, 2017). As such, much research has addressed the factors shaping the health outcomes and survival prospects of newborns admitted to the ICU (Foglia et al., 2017; Kurek Eken, Tüten, Özkaya, Karatekin, & Karateke, 2017; Meadow, Lagatta, Andrews, & Lantos, 2012). As prematurity is a common condition requiring hospitalization in the NICU, many studies have specifically looksed at the NICU outcomes for premature infants (e.g. Manktelow et al., 2010; Kono et al., 2011). However, many health conditions may also require NICU admission for infants who have been brought to term. As infants at differing levels of prematurity will differ in their levels of physiological development, health conditions may interact with levels of prematurity to determine health outcomes (sengupta, 2013). As such, the current study aims to assess NICU patient health outcomes based on level of prematurity in addition to the combination of diagnoses patients have received using the MIMIC-III database. 
The Multiparameter Intelligent Monitoring in Intensive Care (MIMIC)-III dataset (Johnson et al., 2016) is an freely-accessible, de-identified, ICU-specific dataset with records spanning 10 years. As such, it has been extensively used to test big data solutions in ICU situations. However, to our knowledge there have been no studies that focus completely on the newborns that go to the NICU using this data. 
While medically, it makes sense that different diagnoses leading to NICU admission will lead to differences in outcome and length of stay, being able to predict the length of stay has not been thoroughly researched. A 2015 systematic literature review found only 9 studies predicting length of stay (Seaton et al., 2016), but of these, only one study included the reason for admission as a predictor, and they studied 4702 very premature infants (23-32 weeks gestation) (Manktelow, Draper, Field, & Field, 2010). Other studies included other conditions of the baby, mother, and other factors. Therefore, it is important to gain the predictive insight into when any baby may be discharged either to other units or home. For parents, having this insight may be beneficial to their engagement and preventing caregiver burnout, as a parent that knows their baby is likely to not be in hospital long will likely suffer less stress, and a parent that knows their baby may be in the hospital longer will be able to find support systems and manage their stress (Peebles-Kleiger, 2000).  

# Research Question/Objective 
## Research Question 
We posed the research question: Can the duration and discharge location of a newborns’s ICU stay be modelled based on the diagnoses that led to their admission?  


## Aim 1
Using a Cox proportional hazards model, We will investigate how combinations of different health issue diagnoses influence the likelihood of infants being discharge from NICU over time.

## Aim 2
As many health conditions may be commonly associated with premature birth, we will also see whether the prevalence of certain health conditions differs among infants who differ in their level of prematurity.

## Aim 3
We will investigate how patients' health outcomes (i.e. discharged to home, to further hospitalization, etc.) are influenced by the combination of health issues they are diagnosed with when entering NICU. 

## Hypotheses: 
We hypothesize that the causes for admission to the NICU will influence the length of stay in NICU and the discharge location. Specifically, we hypothesize that the presence of sepsis and prematurity will be most useful in predicting the outcomes due to the multi-system nature of these diagnoses. For example, a premature (or extremely premature) newborn will be a more complex case because they have not reached certain developmental milestones within the entire individual, whereas a malformation may only affect one part of one organ. Therefore, we believe it is prudent to test for interactions with prematurity across all of the other variables, because those organ-specific issues may be triggered or exacerbated by the newborn being born too early in their developmental process. 



# Methods



The MIMIC data set includes patients admitted to critical care units consisting of records for 7830 neonates admitted to NICU between 2001 and 2008 in the United States (Johnson et al., 2016). In building our final data set for analysis, demographic information was extracted from the PATIENTS table. The outcomes of interest for our study were the length of patients' stay at the NICU, as well as the location to which a patient was discharged to after their stay at NICU. These data were included in the ADMISSIONS and ICUSTAYS tables. To examine how diagnoses with different health conditions influenced the outcome of interest, we used diagnoses present in the DIAGNOSIS_ICD table. 

## Patient recruitment and inclusion/exclusions criteria

This study utilized newborn infants recorded in the MIMIC-III database who had been admitted to NICU immediately subsequent to their birth (n=7830). As we were interested in duration of stay in NICU, we narrowed our data set down to only contain infants whose stay in NICU was longer than 48 hours (n=450). This was to ensure than we only had cases requiring prolonged hospitalization.

We wanted to determine how infants' combinations of diagnoses affected their health outcomes, however there were a total of 389 unique diagnoses applied to the 450 newborns in our data set. In looking at counts of diagnoses, many of the most common diagnoses (with > 10 occurrences) could be grouped into 7 broad diagnosis categories (exact categorizations can be seen in the python data wrangling file). These are: 

i) Cardiac hemorrhages (e.g. intraventricular hemorrhages, pulmonary hemorrhages) 
ii) Malformations of the circulatory system (e.g. patent ductus arteriosus, ventricular septal defect)
iii) Anomalous heart rates or blood pressure (e.g. neonatal bradycardia, hypotension)
iv) Prematurity (3 levels: full-term, preterm, extreme preterm (<1kg; this cutoff is coded in the MIMIC data set))
v) Respiratory issues (e.g. atelectasis, apnea, respiratory distress syndrome)
vi) Sepsis
vii) Jaundice

As these were the largest sensible groupings of diagnoses that emerged among the most common diagnoses, we then included any male and female infants who were diagnosed with 1 or more of these conditions in our data set. The above diagnoses are not mutually exclusive, and indeed many are commonly comorbid. For example, malformations of the circulatory system and anomalous heart rate are often found together, but they are not inextricably linked. As such, many patients had multiple of the above conditions. These categories are not all encompassing, for example conditions such as hernias, retrolental fibroplasia, and metabolic acidosis appeared as somewhat common diagnoses. However, these and other diagnoses not fitting the scheme above could not be meaningfully grouped together, and so were dropped to avoid an excessive number of categories. Each of the 450 patients whose stay exceeded 48 hours had at least one diagnosis fitting into the above categorization scheme, meaning our final number of subjects was 450 infants.


## General outline of analysis

Aim 1 was be addressed via a Cox proportional hazards regression modelling approach in R. The full model included presence/absence of all categories of health issue mentioned above, gender, and interactions between level of prematurity and all other health conditions. We decided to include this because preterm infants, especially extreme preterm, are less robust than infants brought to term, and so are often more vulnerable to health upsets (Platt, 2014). Thus, there are clinical grounds for including an interaction between preterm and other health variables. This full model was then pared down by removing non-significant interactions, then non-significant main effects until only significant variables remained. At each stage of model reduction, proportional hazards assumptions were checked via Schoenfeld plots, likelihood ratio tests were preformed to confirm variable removal would not worsen the model, and the lack of a confounding effect of removed variables was checked (removal did not change betas of remaining variables by > 10%).

Aim 2 was addressed via proportion tests in R. Significant differences in disease prevalence among prematurity groups were investigated with post-hoc pairwise proportion tests, with Bonferroni corrections for multiple comparisons. 

Aim 3 was addressed by multinomial modelling in R. After data cleaning, there were only one individual in each of the death, long term care, and cancer groups, therefore these patients were removed as the groups could not be meaningfully combined with others. Testing was carried on with patients who were discharged to short term care, home health care, and home. We first tested interactions between prematurity and other factors, as they are clinically likely to share some overlap, which will extend to the complexity of each case, and through to whether a patient can be discharged home or require more complex care after their NICU stay.Likelihood ratio tests were performed on each interaction, and if these interactions were significant a larger model would have been built. After model building for the interactions was complete, all main effects that did not have main effects estimates that we could conclude were non-zero were removed from the model, one at a time, tested with a likelihood ratio test, and the main effect with the least effect on the model was removed. The updated model followed the same process until all variables had at least one non-zero estimate or the likelihood ratio test, which indicates that removing the variable significantly reduced the variability captured by the model. 


## Analysis
Analyses were performed under in R version 3.6.2 (R Core Team, 2007) using RStudio (RStudio Team, 2015), using data wrangling processes from tidyr (Wickham & Henry, 2020) and dplyr (Wickham, François, Henry, & Müller, 2020). Figures will be made in ggplot (Wickam, 2009) and ggfortify (Tang, Horikoshi, & Li, 2016).

```{r setup, include=FALSE}
rm(list = ls())
knitr::opts_chunk$set(echo = TRUE, include = TRUE, warning = FALSE, message = FALSE)

```

```{r include=F}
# Install any previously uninstalled packages
list.of.packages <- c("ggplot2", 'ggfortify', "VGAM", "survival", "KMsurv", "survminer", "survivalMPL", "biostat3", "tidyr", "dplyr", "table1")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)


# load packages
if(!is.loaded("VGAM")) library(VGAM,quietly=T)
if(!is.loaded("survival")) library(survival,quietly=T)
if(!is.loaded("survminer")) library(survminer,quietly=T)
if(!is.loaded("survivalMPL")) library(survivalMPL,quietly=T)
if(!is.loaded("biostat3")) library(biostat3,quietly=T)
if(!is.loaded("ggplot2")) library(ggplot2,quietly=T)
if(!is.loaded("ggfortify")) library(ggfortify,quietly=T)
if(!is.loaded("tidyr")) library(tidyr,quietly=T)
if(!is.loaded("dplyr")) library(dplyr,quietly=T)
if(!is.loaded("table1")) library(table1,quietly=T)


options(scipen=999)
```
