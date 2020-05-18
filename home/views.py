from django.shortcuts import render
from django.http import HttpResponse
from home.models import country_wise
import requests
from math import log10
import numpy as np
from scipy.optimize import curve_fit
from time import sleep
import time
import threading
from scipy import interpolate
from django.shortcuts import redirect

# Create your views here.



def setup_database():

    url = "https://api.covid19api.com/summary"

    payload = {}
    headers= {}
    url_flag = "https://restcountries.eu/rest/v2/alpha/"
    params = {'code' : 'IND'}
    response = requests.request("GET", url, headers=headers, data = payload).json()['Countries']
    for country in response:
        country_code = country['CountryCode']
        print(country_code)
        if int(country['TotalConfirmed']) <= 75000:
            continue
        flg_url = requests.get(url_flag + country_code , params = params).json()['flag']
        # url_country = f'https://corona.lmao.ninja/v2/countries/{country['CountryCode'] }?yesterday&strict&query'
        # country_data = requests.get(url_country).json()


        entry = country_wise(name = country['Slug'],
                            total_cases = country['TotalConfirmed'],
                            total_des = country['TotalDeaths'],
                            cases_yesterday = country['NewConfirmed'],
                            des_yesterday = country['NewDeaths'],
                            rec_yesterday = country['NewRecovered'],
                            active_yesterday = country['TotalRecovered'],
                            country_code = country['CountryCode'], 
                            flag_url = flg_url,
                            full_name = country['Country']
                             
        )
        entry.save()


def reload():
    country_wise.objects.all().delete()
    setup_database()

TIC = 1

def needed():
    file = open('home/need_to_update.txt', 'r').read()
    if file == 'yes':
        return True
    else :
        return False

def update_file():
    print("-----------------------------------------------------------------------------------")
    open('home/need_to_update.txt', 'w').write('no')

def index(request) :
    # global TIC
    # print(f"[INFO]############### starting TIC = {TIC}")
    # if TIC == 1:
    #     reload()
    #     TIC = 0

    # print(f"[INFO]###############  TIC = {TIC}")   

    if needed():
        reload()
        update_file()

        


    all_countries = country_wise.objects.all().order_by('-total_cases')[:12]

    
    params = {'all_countries': all_countries}
    

    return render(request, 'index.html', params)

def poly(x, a, b, c, d1):
    return a*x**2.5 + b*x**2 + c*x  + d1
# context = {}

def extrapolate(request, country_name):
    url = f'https://api.covid19api.com/dayone/country/{country_name}'
    covid_data_all = requests.get(url).json()
    data = {
        'Confirmed' : [],
        'Deaths' : [],
        'Recovered' : [],
        'Active' : [],
        'First_Case' : '',
        'flag_url' : '',
        'Full_name' : '',
        'Population' : '',
        'Subregion' : '',
        'Today' : ''
    }
    day = 1
    cur_date = ''

    for daily in covid_data_all :
        if daily['Date'] == cur_date:
            data['Confirmed'][-1][1] +=  int(daily['Confirmed'])
            data['Deaths'][-1][1] += int(daily['Deaths'])
            data['Recovered'][-1][1] += int(daily['Recovered'])
            data['Active'][-1][1] += int(daily['Active'])
            
        else:
            data['Confirmed'].append([day, int(daily['Confirmed'])])
            data['Deaths'].append([day, int(daily['Deaths'])])
            data['Recovered'].append([day, int(daily['Recovered'])])
            data['Active'].append([day, int(daily['Active'])])
            day += 1
            cur_date = daily['Date']

    data['Today'] = len(data['Confirmed'])
    data['First_Case'] = covid_data_all[0]['Date']
    data['flag_url'] = country_wise.objects.get(name = country_name).flag_url
    code = country_wise.objects.get(name = country_name).country_code
    url_for_country_data = f'https://restcountries.eu/rest/v2/alpha/{code}'
    country_data = requests.get(url_for_country_data).json()
    data['Subregion'] = country_data['subregion']
    data['Population'] = country_data['population']
    data['Full_name'] = country_data['name']

    # np_days = np.array(data['Confirmed'])[:,0].astype(int)
    # np_Confirmed = np.array(data['Confirmed'], dtype= object)[:,1].astype(int)
    # #print(np_days)
    # fit = interpolate.interp1d(np_days, np_Confirmed, kind = 'linear', fill_value='extrapolate')
    # pred_conf = fit( np.arange(day + 1, day + 14) )
    # for predicted_day in range(day + 1, day + 14):
    #     if predicted_day == day + 1:
    #         data['Confirmed'].append([predicted_day, pred_conf[predicted_day - day - 1]])
    #     else :
    #         data['Confirmed'].append([predicted_day, pred_conf[predicted_day - day - 1]])


    # np_Deaths = np.array(data['Deaths'], dtype= object)[:,1].astype(int)
    # #print(np_days)
    # fit = interpolate.interp1d(np_days, np_Deaths, kind = 'linear', fill_value='extrapolate')
    # pred_conf = fit( np.arange(day + 1, day + 14) )
    # for predicted_day in range(day + 1, day + 14):
    #     if predicted_day == day + 1:
    #         data['Deaths'].append([predicted_day, pred_conf[predicted_day - day - 1]])
    #     else :
    #         data['Deaths'].append([predicted_day, pred_conf[predicted_day - day - 1]])



    # np_Recovered = np.array(data['Recovered'], dtype= object)[:,1].astype(int)
    # #print(np_days)
    # fit = interpolate.interp1d(np_days, np_Recovered, kind = 'linear', fill_value='extrapolate')
    # pred_conf = fit( np.arange(day + 1, day + 14) )
    # for predicted_day in range(day + 1, day + 14):
    #     if predicted_day == day + 1:
    #         data['Recovered'].append([predicted_day, pred_conf[predicted_day - day - 1]])
    #     else :
    #         data['Recovered'].append([predicted_day, pred_conf[predicted_day - day - 1]])


    # np_Active = np.array(data['Active'], dtype= object)[:,1].astype(int)
    # #print(np_days)
    # fit = interpolate.interp1d(np_days, np_Active, kind = 'linear', fill_value='extrapolate')
    # pred_conf = fit( np.arange(day + 1, day + 14) )
    # for predicted_day in range(day + 1, day + 14):
    #     if predicted_day == day + 1:
    #         data['Active'].append([predicted_day, pred_conf[predicted_day - day - 1]])
    #     else :
    #         data['Active'].append([predicted_day, pred_conf[predicted_day - day - 1]])








    
        


    context = {
        'data' : data
    }

    return render(request, 'extrapolate.html', context)
    


def compare(request):
    
    countries = country_wise.objects.all()[:12]
    context = {
        'countries' : countries
    }
    return render(request, 'compare.html', context)

def analyze(request):

    
    
    country1 = request.GET.get('country1')
    country2 = request.GET.get('country2')

    if country1 == 'Select the first country' or country2 == 'Select the first country' :
        return redirect('/compare')
    


# https://api.covid19api.com/country/south-africa
    url_country1_Active = f'https://api.covid19api.com/country/{country1}'
    url_country2_Active = f'https://api.covid19api.com/country/{country2}'
    
    country1_resp = requests.get(url_country1_Active).json()
    country2_resp = requests.get(url_country2_Active).json()

    countries = country_wise.objects.all()[:12]

    data = {
        'Active' : [],
        'Country1' : [],
        'Country2' : [],
        'FirstDate' : '',
        'countries' : []
    }

    
    data['countries'] = countries

    day = 1

    # for i in range(min(len(country1_resp), len(country2_resp))) :
    #     data['Active'].append([day, country1_resp[i]['Active'], country2_resp[i]['Active'] ])
    #     day += 1

    # if len(country1_resp) <= len(country2_resp):
    #     for i in range(len(country1_resp), len(country2_resp) ):
    #         data['Active'].append([day, 0, country2_resp[i]['Active'] ])
    #         day += 1

    # else :
    #     for i in range(len(country2_resp), len(country1_resp) ):
    #         data['Active'].append([day,  country1_resp[i]['Active'] , 0 ])
    #         day += 1


    # if len(country1_resp) <= len(country2_resp) :
    #     for i in range( len(country2_resp) -  len(country1_resp)):
    #         data['Active'].append([day, 0, country2_resp[i]['Active']])
    #         day += 1

    #      for i in range(len(country1_resp), len(country2_resp) ):
    #         data['Active'].append([day,  country1_resp[i - len(country1_resp) ]['Active'] , country2_resp[i]['Active'] ])
    #         day += 1

    # else :

    #      for i in range(len(country2_resp)):
    #         data['Active'].append([day,  country1_resp[i]['Active'], 0])
    #         day += 1

    #      for i in range(len(country2_resp), len(country1_resp) ):
    #         data['Active'].append([day,    country2_resp[i]['Active']  , country1_resp[i - len(country1_resp) ]['Active'] ])
    #         day += 1

    
    active_country1 = []
    active_country2 = []

    cur_date = ''
    data['FirstDate'] = country2_resp[0]['Date']
    for daily in country1_resp :
        if daily['Date'] == cur_date:
            active_country1[-1] +=  int(daily['Active'])
        else:
            
            active_country1.append( int(daily['Active']))
            
            cur_date = daily['Date']

    cur_date = ''

    for daily in country2_resp :
        if daily['Date'] == cur_date:
            active_country2[-1] +=  int(daily['Active'])
        else:
            
            active_country2.append( int(daily['Active']))
            cur_date = daily['Date']


    
    
    if len(active_country1) > len(active_country2) :
        country1, country2 = country2, country1
        active_country1, active_country2 = active_country2, active_country1




    days1 = len(active_country1)
    days2 = len(active_country2)

    for i in range(days2 - days1) :
        data['Active'].append([ day, 0, active_country2[i] ] ) 
        day += 1



        
    for i in range(days2 - days1, days2) :
        data['Active'].append([ day, active_country1[i - days2 + days1], active_country2[i] ] ) 
        day += 1
    





    
    data['Country1'] = country1
    data['Country2'] = country2

     
    
    context = {
        'data' : data
    }



    return render(request, 'analyze.html', context) 






def alerts(request):
    countries = country_wise.objects.all()[:14]
    data = {
        'Danger' : []
        
    }

    for i in range(14):

        data['Danger'].append([countries[i], int(countries[i].cases_yesterday / countries[i].total_cases * 1000)/10])


    data['Danger'].sort(key = lambda x : -x[1])
    
    context = {
        'data' : data
    }


    return render(request, 'alert.html', context)


