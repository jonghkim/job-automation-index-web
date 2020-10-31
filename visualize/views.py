# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from  matplotlib import ticker

import numpy as np
from io import BytesIO
import base64

from django.http import JsonResponse

from .forms import JobAutomationIndexForm, SkillDNA, AutomationRanking, MapForm

from django.conf import settings as djangoSettings
import pandas as pd

def percentileofscore(a, score, kind='rank'):
    if np.isnan(score):
        return np.nan
    a = np.asarray(a)
    n = len(a)
    if n == 0:
        return 100.0

    if kind == 'rank':
        left = np.count_nonzero(a < score)
        right = np.count_nonzero(a <= score)
        pct = (right + left + (1 if right > left else 0)) * 50.0/n
        return pct
    elif kind == 'strict':
        return np.count_nonzero(a < score) / n * 100
    elif kind == 'weak':
        return np.count_nonzero(a <= score) / n * 100
    elif kind == 'mean':
        pct = (np.count_nonzero(a < score) + np.count_nonzero(a <= score)) / n * 50
        return pct
    else:
        raise ValueError("kind can only be 'rank', 'strict', 'weak' or 'mean'")

def draw_task_automation(year='2019', job='TOTAL AVERAGE'):
    #### TASK AUTOMATION ####
    csvpath = djangoSettings.STATICFILES_DIRS[0]+'/data/csv/Panel 1.csv'
    panel_df = pd.read_csv(csvpath, encoding='ISO-8859-1', dtype={'Year':str})

    if (year=='2019') or (year=='2007'):
        if job=='TOTAL AVERAGE':
            objects = ['Job Automation Index','Annual Wage']
        else:
            objects = ['Job Automation Index', 'Employment','Annual Wage']
    elif year=='2007~2019':
        if job=='TOTAL AVERAGE':
            objects = ['Job Automation Index Change']
        else:
            objects = ['Job Automation Index Change', 'Wage Share Change']

    if (year=='2019') or (year=='2007'):        
        fig, axs = plt.subplots(len(objects), figsize=(7,len(objects)*1.3))
        
        for i, obj in enumerate(objects):
            if obj =='Job Automation Index':
                val = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj].iloc[0].tolist()
                val = val*100
                percentile = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj+' Percentile'].iloc[0]
                #arr = panel_df[(panel_df['Year']==year)][obj].tolist()
                #percentile = percentileofscore(arr, val)

                axs[i].barh(0, val, align='center', alpha=0.5)
                axs[i].set_title(obj+' (%)')
                axs[i].set_yticklabels([])

                axs[i].set_xlim(40, 60)
                axs[i].set_xticks(np.arange(40,65,5))

                plt.setp(axs[i].get_xticklabels(), rotation=30)

                axs[i].text(0.9, 0.5, percentile, horizontalalignment='center',
                            verticalalignment='center', transform=axs[i].transAxes)
                #axs[i].text(0.9, 0.5, 'Top '+str(int(round(percentile/5.0)*5.0))+' %', horizontalalignment='center',
                #            verticalalignment='center', transform=axs[i].transAxes)

            elif obj =='Annual Wage':
                val = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj].iloc[0].tolist()
                percentile = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj+' Percentile'].iloc[0]
                #arr = panel_df[(panel_df['Year']==year)][obj].tolist()
                #percentile = percentileofscore(arr, val)
                
                axs[i].barh(0, val, align='center', alpha=0.5)
                #axs[i].barh(0, np.log2(val), align='center', alpha=0.5)

                #axs[i].set_xscale('log')
                axs[i].set_xscale('log', basex=2)

                axs[i].set_title(obj+' ($)')
                axs[i].set_yticklabels([])

                #axs[i].set_xlim(0, 300000)
                #axs[i].set_xlim(1, 3*1e5)
                axs[i].set_xlim(2**13, 2**18)

                #axs[i].set_xticklabels([format(label, ',.0f') for label in [10000,50000,100000,150000,200000,250000,300000]])
                axs[i].set_xticks([label for label in [10000,50000,100000,150000,200000,250000,300000]])
                axs[i].get_xaxis().set_major_formatter(ticker.ScalarFormatter())

                plt.setp(axs[i].get_xticklabels(), rotation=30)
                
                axs[i].text(0.9, 0.5, percentile, horizontalalignment='center',
                            verticalalignment='center', transform=axs[i].transAxes)
                #axs[i].text(0.9, 0.5, 'Top '+str(int(round(percentile/5.0)*5.0))+' %', horizontalalignment='center',
                #            verticalalignment='center', transform=axs[i].transAxes)

            elif obj == 'Employment':
                val = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj].iloc[0].tolist()
                percentile = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj+' Percentile'].iloc[0]
                #arr = panel_df[(panel_df['Year']==year)][obj].tolist()
                #percentile = percentileofscore(arr, val)

                axs[i].barh(0, val, align='center', alpha=0.5)
                #axs[i].barh(0, val, align='center', alpha=0.5)

                axs[i].set_xscale('log')
                
                axs[i].set_title(obj)
                axs[i].set_yticklabels([])

                #axs[i].set_xlim(0, 5000000)
                #axs[i].set_xlim(1, 5*1e6)
                axs[i].set_xlim(10**2, 10**7)
                #axs[i].set_xlim(100, 1000000)
                
                #axs[i].set_xticklabels([format(label, ',.0f') for label in [100,1000,10000,100000,1000000,10000000,50000000]])
                axs[i].set_xticks([label for label in [100,1000,10000,100000,1000000,10000000,50000000]])
                #axs[i].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
                axs[i].get_xaxis().set_major_formatter(ticker.FormatStrFormatter("%d"))

                plt.setp(axs[i].get_xticklabels(), rotation=30)

                axs[i].text(0.9, 0.5, percentile, horizontalalignment='center',
                            verticalalignment='center', transform=axs[i].transAxes)
                #axs[i].text(0.9, 0.5, 'Top '+str(int(round(percentile/5.0)*5.0))+' %', horizontalalignment='center',
                #            verticalalignment='center', transform=axs[i].transAxes)

        plt.tight_layout()

    elif year=='2007~2019':

        if len(objects) == 2:
            fig, axs = plt.subplots(len(objects), figsize=(7,2*1.3))
            
            for i, obj in enumerate(objects):
                if obj == 'Job Automation Index Change':
                    val = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj].iloc[0].tolist()
                    val = val*100

                    percentile = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj+' Percentile'].iloc[0]
                    #arr = panel_df[(panel_df['Year']==year)][obj].tolist()
                    #percentile = percentileofscore(arr, val)

                    axs[i].barh(0, val, align='center', alpha=0.5)
                    axs[i].set_title(obj+' (%p)')
                    axs[i].set_yticklabels([])

                    axs[i].set_xlim(-5, 5)
                    axs[i].set_xticks(np.arange(-5,6,1))

                    ax_xtick = axs[i].get_xticks().tolist() 
                    ax_xtick[0] = '<-5'
                    ax_xtick[-1] = '5<'
                    axs[i].set_xticklabels(ax_xtick)            
                    
                    plt.setp(axs[i].get_xticklabels(), rotation=30)

                    axs[i].text(0.9, 0.5, percentile, horizontalalignment='center',
                                verticalalignment='center', transform=axs[i].transAxes)
                    #axs[i].text(0.9, 0.5, 'Top '+str(int(round(percentile/5.0)*5.0))+' %', horizontalalignment='center',
                    #            verticalalignment='center', transform=axs[i].transAxes)
                    
                elif obj == 'Wage Share Change':
                    val = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj].iloc[0].tolist()
                    percentile = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][obj+' Percentile'].iloc[0]
                    #arr = panel_df[(panel_df['Year']==year)][obj].tolist()
                    #percentile = percentileofscore(arr, val)

                    axs[i].barh(0, val, align='center', alpha=0.5)
                    axs[i].set_title(obj+' (%p)')
                    axs[i].set_yticklabels([])

                    axs[i].set_xlim(-1, 1)

                    plt.setp(axs[i].get_xticklabels(), rotation=30)

                    axs[i].text(0.9, 0.5, percentile, horizontalalignment='center',
                                verticalalignment='center', transform=axs[i].transAxes)
                    #axs[i].text(0.9, 0.5, 'Top '+str(int(round(percentile/5.0)*5.0))+' %', horizontalalignment='center',
                    #            verticalalignment='center', transform=axs[i].transAxes)

            plt.tight_layout()    

        elif len(objects) == 1:
            fig = plt.figure(figsize=(7, 1*1.3))
            ax = fig.add_subplot(111)
            val = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][objects[0]].iloc[0].tolist()
            val = val*100

            percentile = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][objects[0]+' Percentile'].iloc[0]
            #arr = panel_df[(panel_df['Year']==year)][objects[0]].tolist()
            #percentile = percentileofscore(arr, val)
            
            ax.barh(0, val, align='center', alpha=0.5)

            if objects[0] == 'Job Automation Index':
                ax.set_xlim(40, 60)
                ax.set_xticks(np.arange(40,65,5))
                
                ax.set_title(objects[0]+' (%)')
            elif objects[0] == 'Job Automation Index Change':
                ax.set_xlim(-5,5)
                ax.set_xticks(np.arange(-5,6,1))

                ax_xtick = ax.get_xticks().tolist() 
                ax_xtick[0] = '<-5'
                ax_xtick[-1] = '5<'
                ax.set_xticklabels(ax_xtick)            

                ax.set_title(objects[0]+' (%p)')
            else:    
                ax.set_title(objects[0])

            ax.set_yticklabels([])

            plt.setp(ax.get_xticklabels(), rotation=30)

            ax.text(0.9, 0.5, percentile, horizontalalignment='center',
                        verticalalignment='center', transform=ax.transAxes)

            #ax.text(0.9, 0.5, 'Top '+str(int(round(percentile/5.0)*5.0))+' %', horizontalalignment='center',
            #            verticalalignment='center', transform=ax.transAxes)

            plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    task_automation = base64.b64encode(image_png)
    task_automation = task_automation.decode('utf-8')

    return task_automation

# Create your views here.
def draw_task_importance(year='2019', job='TOTAL AVERAGE'):    
    #### TASK IMPORTANCE ####    
    csvpath = djangoSettings.STATICFILES_DIRS[0] +'/data/csv/Panel 2.csv'
    panel_df = pd.read_csv(csvpath, encoding='ISO-8859-1', dtype={'Year':str})
    
    if year =='2019' or year=='2007':
        """
        labels = np.array(["Operation Monitoring", "System Analysis", "Strategic Thinking","Conflict Resolution", 
                        "Communication", "Managerial Task",  "Clerical Task", "Information Processing", 
                        "Hazardous and Group Task", "Outdoor Labor", "Dynamic Physical Task", "Physical Task", 
                        "Equipment Operation", "Equipment Maintenance"])                    
        """
        labels = np.array(["Race with the Machine",	"Race against the Machine",
                            "Race ahead of the Machine", "Running a Different Race"]) # "Changing the Course of a Race"

        lim_range = False
        if job != 'TOTAL AVERAGE':
            focal_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][labels].iloc[0].tolist()
            focal_stats = np.array(focal_stats)*100

            lim_range = True if max(focal_stats) > 30 else lim_range
            focal_stats=np.concatenate((focal_stats,[focal_stats[0]]))
            
            focal_stats[focal_stats>30] = 30

            total_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']=='TOTAL AVERAGE')][labels].iloc[0].tolist()
            total_stats = np.array(total_stats)*100

            lim_range = True if max(total_stats) > 30 else lim_range
            total_stats=np.concatenate((total_stats,[total_stats[0]]))
            
            total_stats[total_stats>30] = 30

            angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)        
            angles=np.concatenate((angles,[angles[0]]))

            fig = plt.figure(figsize=(8, 8))

            ax = fig.add_subplot(111, polar=True)    

            ax.plot(angles, focal_stats, 'o-', linewidth=2, color='#db3f3f', alpha=0.5)
            ax.fill(angles, focal_stats, alpha=0.25, facecolor='#db3f3f')

            ax.plot(angles, total_stats, 'o-', linewidth=2, color='#1f77b4', alpha=0.5)
            ax.fill(angles, total_stats, alpha=0.25, facecolor='#1f77b4')        

            ax.set_thetagrids(angles * 180/np.pi, labels, fontsize=11)
            ax.grid(True)
            ax.yaxis.grid(False)
            ax.legend([job+' (%)','TOTAL AVERAGE'+' (%)'], loc='upper center', bbox_to_anchor=(0.5, -0.08), shadow=True, ncol=2)

        elif job == 'TOTAL AVERAGE':
            focal_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][labels].iloc[0].tolist()            
            focal_stats = np.array(focal_stats)*100

            lim_range = True if max(focal_stats) > 30 else lim_range
            focal_stats=np.concatenate((focal_stats,[focal_stats[0]]))
            
            focal_stats[focal_stats>30] = 30

            angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)        
            angles=np.concatenate((angles,[angles[0]]))

            fig = plt.figure(figsize=(8, 8))

            ax = fig.add_subplot(111, polar=True)

            if year =='2019' or year=='2007':
                ax.plot(angles, focal_stats, 'o-', linewidth=2, color='#1f77b4', alpha=0.5)
                ax.fill(angles, focal_stats, alpha=0.25, facecolor='#1f77b4')
            else:
                ax.plot(angles, focal_stats, 'o-', linewidth=2, color='#1f77b4', alpha=0.5)

            ax.set_thetagrids(angles * 180/np.pi, labels, fontsize=11)
            ax.grid(True)
            ax.yaxis.grid(False)
            ax.legend(['TOTAL AVERAGE'+' (%)'], loc='upper center', bbox_to_anchor=(0.5, -0.08), shadow=True, ncol=1)

        ax.set_rorigin(0)
        """
        if max_ytick < 70:
            ax.set_ylim(0,70)
            yticks = np.arange(0,80,10)
            ax.set_yticks(yticks)
        else:
        """
        ax.set_ylim(0,30)
        yticks = np.arange(0,35,5)
        ax.set_yticks(yticks)           
        ax_ytick = ax.get_yticks().tolist() 
        #ax_ytick[-1] = '>70'
        #if lim_range == True:
        ax_ytick[-1] = '30<'   
        ax.set_yticklabels(ax_ytick)
        
    elif year=='2007~2019':
        """
        labels = np.array(["Hazardous and Group Task","Outdoor Labor","Dynamic Physical Task", "Physical Task",
                         "Equipment Operation", "Equipment Maintenance", "Operation Monitoring", "System Analysis", "Strategic Thinking", 
                         "Conflict Resolution", "Communication", "Managerial Task", "Clerical Task", "Information Processing"])                    
        """
        labels = np.array(["Running a Different Race", 
                            "Race ahead of the Machine", "Race against the Machine",
                            "Race with the Machine"])          # "Changing the Course of a Race", 

        lim_range = False
        if job != 'TOTAL AVERAGE':
            focal_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][labels]
            focal_stats = focal_stats*100

            lim_range = True if max(focal_stats.max()) > 10 else lim_range
            lim_range = True if min(focal_stats.min()) < -10 else lim_range
            focal_stats[focal_stats>10] = 10
            focal_stats[focal_stats<-10] = -10

            max_xtick = max(focal_stats.iloc[0].tolist())

            total_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']=='TOTAL AVERAGE')][labels]
            total_stats = total_stats*100
            lim_range = True if max(total_stats.max()) > 10 else lim_range
            lim_range = True if min(total_stats.min()) < -10 else lim_range            
            total_stats[total_stats>10] = 10
            total_stats[total_stats<-10] = -10

            barh_df = focal_stats.append(total_stats)
            barh_df.index = [job,'TOTAL AVERAGE']

            barh_df = barh_df.T

            ax=barh_df.plot.barh(figsize=(8, 4), fontsize=10, color=['#db3f3f','#1f77b4'], alpha=0.5)
            ax.legend([job+' (%p)','TOTAL AVERAGE'+' (%p)'], loc='upper center', bbox_to_anchor=(0.5, -0.08), shadow=True, ncol=2)

        elif job == 'TOTAL AVERAGE':
            focal_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][labels]
            focal_stats = focal_stats*100
            max_xtick = max(focal_stats.iloc[0].tolist())

            focal_stats.index=['TOTAL_AVERAGE']
            focal_stats = focal_stats.T
            lim_range = True if max(focal_stats.max()) > 10 else lim_range
            lim_range = True if min(focal_stats.min()) < -10 else lim_range     
            focal_stats[focal_stats>10] = 10
            focal_stats[focal_stats<-10] = -10

            ax = focal_stats.plot.barh(figsize=(8, 4), fontsize=10,  color=['#1f77b4'], alpha=0.5)
            ax.legend(['TOTAL AVERAGE'+' (%p)'], loc='upper center', bbox_to_anchor=(0.5, -0.08), shadow=True, ncol=1)

        if job == 'TOTAL AVERAGE':
            ax.set_xlim(-5,5)
            ax.set_xticks(np.arange(-5,6,1))
        else:
            ax.set_xlim(-10,10)
            ax.set_xticks(np.arange(-10,11,2))
            ax_xtick = ax.get_xticks().tolist() 
            #if lim_range == True:
            ax_xtick[0] = '<-10'
            ax_xtick[-1] = '10<'
            ax.set_xticklabels(ax_xtick)            

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    task_importance = base64.b64encode(image_png)
    task_importance = task_importance.decode('utf-8')
    return task_importance

"""
# Create your views here.
def draw_task_importance(year='2007~2019', job='TOTAL AVERAGE'):    
    #### TASK IMPORTANCE ####    
    csvpath = djangoSettings.STATICFILES_DIRS[0] +'/data/csv/Panel 2.csv'
    panel_df = pd.read_csv(csvpath, encoding='utf-8', dtype={'Year':str})
    labels = np.array(["Hazardous and Group Task","Outdoor Labor", "Dynamic Physical Task", "Physical Task", 
                    "Equipment Operation","Equipment Maintenance", "Operation Monitoring", "System Analysis",
                    "Strategic Thinking", "Conflict Resolution", "Communication", "Managerial Task","Information Processing", "Clerical Task"])

    if job != 'TOTAL AVERAGE':
        focal_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][labels].iloc[0].tolist()
        max_ytick = max(focal_stats)
        focal_stats=np.concatenate((focal_stats,[focal_stats[0]]))

        total_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']=='TOTAL AVERAGE')][labels].iloc[0].tolist()
        total_stats=np.concatenate((total_stats,[total_stats[0]]))

        angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)        
        angles=np.concatenate((angles,[angles[0]]))

        fig = plt.figure(figsize=(8, 8))

        ax = fig.add_subplot(111, polar=True)     

        if year =='2019' or year=='2007':
            ax.plot(angles, focal_stats, 'o-', linewidth=2)
            ax.fill(angles, focal_stats, alpha=0.25)

            ax.plot(angles, total_stats, 'o-', linewidth=2)
            ax.fill(angles, total_stats, alpha=0.25)
        else:
            ax.plot(angles, focal_stats, 'o-', linewidth=2)
            ax.plot(angles, total_stats, 'o-', linewidth=2)
            neg = np.minimum(focal_stats, total_stats)
            pos = np.maximum(focal_stats, total_stats)
            ax.fill_between(angles, 0, neg, alpha=0.25)
            ax.fill_between(angles, 0, pos, alpha=0.25)

        ax.set_thetagrids(angles * 180/np.pi, labels)
        ax.grid(True)
        ax.legend([job,'TOTAL AVERAGE'], loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

    elif job == 'TOTAL AVERAGE':
        focal_stats = panel_df[(panel_df['Year']==year)&(panel_df['Job Title']==job)][labels].iloc[0].tolist()
        max_ytick = max(focal_stats)
        focal_stats=np.concatenate((focal_stats,[focal_stats[0]]))

        angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)        
        angles=np.concatenate((angles,[angles[0]]))

        fig = plt.figure(figsize=(8, 8))

        ax = fig.add_subplot(111, polar=True)

        if year =='2019' or year=='2007':
            ax.plot(angles, focal_stats, 'o-', linewidth=2)
            ax.fill(angles, focal_stats, alpha=0.25)
        else:
            ax.plot(angles, focal_stats, 'o-', linewidth=2)

        ax.set_thetagrids(angles * 180/np.pi, labels)
        ax.grid(True)
        ax.legend(['TOTAL AVERAGE'], loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=1)

    if year =='2019' or year=='2007':
        ax.set_rorigin(0)
        if max_ytick < 100:
            ax.set_ylim(0,100)
            ax.set_yticks(np.arange(0,100,10))
        else:
            ax.set_ylim(0,150)
            ax.set_yticks(np.arange(0,150,10))

    elif year=='2007~2019':
        ax.set_rorigin(-60)
        ax.set_ylim(-60,60)
        ax.set_yticks(np.arange(-60,60,10))

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    task_importance = base64.b64encode(image_png)
    task_importance = task_importance.decode('utf-8')
    return task_importance
"""
def job_description(job='TOTAL AVERAGE'):
    csvpath = djangoSettings.STATICFILES_DIRS[0]+'/data/csv/jobs.csv'
    panel_df = pd.read_csv(csvpath, encoding='ISO-8859-1')

    code = panel_df[(panel_df['Job Title']==job)]['Job Code'].iloc[0]
    job_desc = panel_df[(panel_df['Job Title']==job)]['Description'].iloc[0]

    return code, job_desc

def code_description(code='00-0000'):
    csvpath = djangoSettings.STATICFILES_DIRS[0]+'/data/csv/jobs.csv'
    panel_df = pd.read_csv(csvpath, encoding='ISO-8859-1')

    code_desc = panel_df[panel_df['Job Code']==code]['Description'].iloc[0]
    job = panel_df[panel_df['Job Code']==code]['Job Title'].iloc[0]

    return job, code, code_desc

def contact(request):
    return render(request, 'visualize/contact.html')

def about(request):
    return render(request, 'visualize/about.html')

def sitemap(request):
    return render(request, 'visualize/sitemap.xml')
    
def index(request):
    """
    if request.method == 'POST':
        form = JobAutomationIndexForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            job = form.cleaned_data['occupation']

            code, job_desc = job_description(job)

            task_importance = draw_task_importance(year, job)
            task_automation = draw_task_automation(year, job)
            return render(request, 'visualize/index.html',{'task_importance':task_importance, 
                    'task_automation':task_automation, 'year': year, 'job':job,
                    'form' : form, 'job_description':job_desc,'code':code})
    else:
        form = JobAutomationIndexForm()
        task_importance = draw_task_importance()
        task_automation = draw_task_automation()
        code, job_desc = job_description()

        year='2019'
        job='TOTAL AVERAGE'

        return render(request, 'visualize/index.html',{'task_importance':task_importance, 
                    'task_automation':task_automation, 'year': year, 'job':job,
                    'form' : form, 'job_description':job_desc,'code':code})
    """
    return render(request, 'visualize/index.html')

def automation_index(request):
    if request.method == 'POST':
        form = JobAutomationIndexForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            job = form.cleaned_data['occupation']

            code, job_desc = job_description(job)

            task_importance = draw_task_importance(year, job)
            task_automation = draw_task_automation(year, job)
            return render(request, 'visualize/automation_index.html',{'task_importance':task_importance, 
                    'task_automation':task_automation, 'year': year, 'job':job,
                    'form' : form, 'job_description':job_desc,'code':code})
    else:
        form = JobAutomationIndexForm()
        task_importance = draw_task_importance()
        task_automation = draw_task_automation()
        code, job_desc = job_description()

        year='2019'
        job='TOTAL AVERAGE'

        return render(request, 'visualize/automation_index.html',{'task_importance':task_importance, 
                    'task_automation':task_automation, 'year': year, 'job':job,
                    'form' : form, 'job_description':job_desc,'code':code})

def skill_dna_view(request):
    code = request.GET.get('code', '00-0000')
    job = request.GET.get('job','TOTAL AVERAGE')
    year = request.GET.get('year','2019')

    return render(request, 'visualize/skill_dna_view.html', {'year':year, 'job':job, 'code':code})        

def skill_dna_view_mobile(request):
    code = request.GET.get('code', '00-0000')
    job = request.GET.get('job','TOTAL AVERAGE')
    year = request.GET.get('year','2019')

    return render(request, 'visualize/skill_dna_view_mobile.html', {'year':year, 'job':job, 'code':code})        
  
def skill_dna(request):
    if request.method == 'POST':
        form = SkillDNA(request.POST) 
        if form.is_valid():
            year = form.cleaned_data['year']
            code = form.cleaned_data['occupation']
            job, code, code_desc = code_description(code)

            return render(request, 'visualize/skill_dna.html', {'year':year, 'job':job, 'code':code,
                    'form': form, 'code_description':code_desc})        
    else:
        form = SkillDNA()
        year = '2019'
        code = '00-0000'
        job, code , code_desc = code_description()        
        
        return render(request, 'visualize/skill_dna.html', {'year':year, 'job':job, 'code':code,
                'form': form, 'code_description':code_desc})    

def automation_ranking(request):
    if request.method == 'POST':
        form = AutomationRanking(request.POST) 
        if form.is_valid():
            year = form.cleaned_data['year']
            return render(request, 'visualize/automation_ranking.html',{'year':year, 'form': form})      
    else:
        form = AutomationRanking()
        year = '2019'
        return render(request, 'visualize/automation_ranking.html', {'year':year, 'form' : form})

def task_level_automation(request):
    if request.method == 'POST':
        form = AutomationRanking(request.POST) 
        if form.is_valid():
            year = form.cleaned_data['year']
            return render(request, 'visualize/task_level_automation.html',{'year':year, 'form': form})      
    else:
        form = AutomationRanking()
        year = '2019'
        return render(request, 'visualize/task_level_automation.html', {'year':year, 'form' : form})
        
def map_automation(request):
    if request.method == 'POST':
        form = MapForm(request.POST) 
        if form.is_valid():
            relation_to_automation = form.cleaned_data['relation_to_automation']
            year = form.cleaned_data['year']
            return render(request, 'visualize/map_automation.html',{'relation_to_automation':relation_to_automation, 'year':year,'form': form})      
    else:
        form = MapForm()
        relation_to_automation = u'Race with the Machine'
        year = '2019'
        return render(request, 'visualize/map_automation.html', {'relation_to_automation':relation_to_automation, 'year':year,'form': form})      
         

def city_level_automation(request):
    if request.method == 'POST':
        form = AutomationRanking(request.POST) 
        if form.is_valid():
            year = form.cleaned_data['year']
            return render(request, 'visualize/city_level_automation.html',{'year':year, 'form': form})      
    else:
        form = AutomationRanking()
        year = '2019'
        return render(request, 'visualize/city_level_automation.html', {'year':year, 'form' : form})
                