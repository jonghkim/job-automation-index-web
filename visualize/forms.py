from django import forms
from django.conf import settings as djangoSettings
import pandas as pd

class JobAutomationIndexForm(forms.Form):
    csvpath = djangoSettings.STATICFILES_DIRS[0]+'/data/csv/jobs.csv'
    panel_df = pd.read_csv(csvpath, encoding='utf-8', dtype={'Family Code':str})

    panel_df_gp = panel_df.groupby('Family Code')

    JOBS = (u'(SOC 00) TOTAL AVERAGE', ((u'TOTAL AVERAGE', u'TOTAL AVERAGE'),)),

    for code, df in panel_df_gp:
        if code =='00':
            continue

        JOB = ()
        for i, r in df.iterrows():
            JOB = JOB + ((r['Job Title'], r['Job Title']),)

        JOBS = JOBS + (('(SOC '+code+') '+df.iloc[0]['Job Family'], JOB),)
        
    occupation = forms.ChoiceField(choices=JOBS)

    #YEARS = (('2018', '2018'),('2008', '2008'),('2008~2018', '2008~2018'))
    YEARS = (('2018', '2018'),('2008', '2008'),('2008~2018', 'Change between 2008-2018'))
    
    year = forms.ChoiceField(choices=YEARS)

class SkillMap(forms.Form):
    csvpath = djangoSettings.STATICFILES_DIRS[0]+'/data/csv/jobs.csv'
    panel_df = pd.read_csv(csvpath, encoding='utf-8', dtype={'Family Code':str})

    panel_df_gp = panel_df.groupby('Family Code')

    JOBS = (u'(SOC 00) TOTAL AVERAGE', ((u'00-0000', u'TOTAL AVERAGE'),)),

    for code, df in panel_df_gp:
        if code =='00':
            continue

        JOB = ()
        for i, r in df.iterrows():
            JOB = JOB + ((r['Job Code'], r['Job Title']),)
        JOBS = JOBS + (('(SOC '+code+') '+df.iloc[0]['Job Family'], JOB),)

    occupation = forms.ChoiceField(choices=JOBS)

    #YEARS = (('2008_2018', 'Evolution during 2008-2018'),('2018', '2018'),('2008', '2008'))
    YEARS = (('2018', '2018'),('2008', '2008'),('2008_2018', 'Change between 2008-2018'))
    year = forms.ChoiceField(choices=YEARS)

class AutomationRanking(forms.Form):
    YEARS = (('2018', '2018'),('2008', '2008'),('2008~2018', 'Change between 2008-2018'))
    year = forms.ChoiceField(choices=YEARS)        