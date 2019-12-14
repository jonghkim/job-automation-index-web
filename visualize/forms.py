from django import forms
from django.conf import settings as djangoSettings
import pandas as pd

class JobAutomationIndexForm(forms.Form):
    csvpath = djangoSettings.STATICFILES_DIRS[0]+'/data/csv/jobs.csv'
    panel_df = pd.read_csv(csvpath, encoding='ISO-8859-1', dtype={'Family Code':str})

    panel_df_gp = panel_df.groupby('Family Code')

    JOBS = (u'(SOC 00) TOTAL AVERAGE', ((u'TOTAL AVERAGE', u'TOTAL AVERAGE'),)),

    for code, df in panel_df_gp:
        if code =='00':
            continue

        JOB = ()
        for i, r in df.iterrows():
            JOB = JOB + ((r['Job Title'], r['Job Title']),)

        JOBS = JOBS + (('(SOC '+code+') '+df.iloc[0]['Job Family'], JOB),)
        
    occupation = forms.ChoiceField(choices=JOBS, widget=forms.Select(attrs={'style': 'width:300px'}))

    #YEARS = (('2018', '2018'),('2008', '2008'),('2008~2018', '2008~2018'))
    YEARS = (('2018', '2018'),('2008', '2008'),('2008~2018', 'Change during 2008-2018'))
    
    year = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'style': 'width:200px'}))

class SkillMap(forms.Form):
    csvpath = djangoSettings.STATICFILES_DIRS[0]+'/data/csv/jobs.csv'
    panel_df = pd.read_csv(csvpath, encoding='ISO-8859-1', dtype={'Family Code':str})

    panel_df_gp = panel_df.groupby('Family Code')

    JOBS = (u'(SOC 00) TOTAL AVERAGE', ((u'00-0000', u'TOTAL AVERAGE'),)),

    for code, df in panel_df_gp:
        if code =='00':
            continue

        JOB = ()
        for i, r in df.iterrows():
            JOB = JOB + ((r['Job Code'], r['Job Title']),)
        JOBS = JOBS + (('(SOC '+code+') '+df.iloc[0]['Job Family'], JOB),)

    occupation = forms.ChoiceField(choices=JOBS, widget=forms.Select(attrs={'style': 'width:300px'}))

    #YEARS = (('2008_2018', 'Evolution during 2008-2018'),('2018', '2018'),('2008', '2008'))
    YEARS = (('2018', '2018'),('2008', '2008'),('2008_2018', 'Change during 2008-2018'))
    year = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'style': 'width:200px'}))

class AutomationRanking(forms.Form):
    YEARS = (('2018', '2018'),('2008', '2008'),('2008~2018', 'Change during 2008-2018'))
    year = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'style': 'width:200px'}))        

class MapForm(forms.Form):
    TYPES = (("Race ahead of the Machine","Race ahead of the Machine"),("Race with the Machine","Race with the Machine"),
              ("Race against the Machine","Race against the Machine"),("Running a Different Race","Running a Different Race"))
        
    relation_to_automation = forms.ChoiceField(choices=TYPES, widget=forms.Select(attrs={'style': 'width:300px'}))

    YEARS = (('2018', '2018'),('2008', '2008'),('2008~2018', 'Change during 2008-2018'))
    
    year = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'style': 'width:200px'}))