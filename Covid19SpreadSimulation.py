import warnings
import itertools
import numpy as np
import xlrd
import csv
import math
#from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
from datetime import datetime
import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

def createCountryTrainingTable(countrySF):
    # load the dataset from the CSV file 
    reader = csv.reader(open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/Train.csv", "r"), delimiter=",")
    xx = list(reader)
    xxln = len(xx)
    territoryName = "" 
    for row in range(1, xxln):
        param_country = countrySF.strip()
        train_country = xx[row][3].strip()
        if train_country == param_country:
            targets.append(int(xx[row][1]))
            dates.append(xx[row][4])
            datestr = createDateFormat(xx[row][4])
            countrydate = train_country + ' X ' + datestr
            country_date.append(xx[row][0])
             
    print('country_date: ', country_date)
    #print('targets: ', targets)
    #print('dates: ', dates)

    #input("Press Enter to continue...")
       
def createDateFormat(datstr):
    datstr = datstr.strip()
    dtstrlen = len(datstr.strip())
    # 1/22/20
    if dtstrlen < 10:
        ffslpt1 = datstr.find("/", 0, dtstrlen)
        pt1 = ffslpt1 + 1
        ffslpt2 = datstr.find("/", pt1, dtstrlen)
        pt2 = ffslpt2 + 1
        mm = datstr[0:ffslpt1]
        dd = datstr[pt1:ffslpt2]
        yy = datstr[pt2:]
        #print("datstr: " + str(datstr))
        #print("ffslpt1: " + str(ffslpt1))
        #print("ffslpt2: " + str(ffslpt2))
        #print("mm: " + str(mm))
        #print("dd: " + str(dd))
        #print("yy: " + str(yy))
        mmln = len(mm)
        ddln = len(dd)
        yyln = len(yy)
        if mmln == 1:
            mm = "0" + mm
        if ddln == 1:
            dd = "0" + dd
        if yyln > 2:
            yy = "20"
            #yy = yy + "20"
        datstr = mm + "/" + dd + "/" + yy        
    return datstr

def createDDateFormat(datstr):
    datstr = datstr.strip()
    dtstrlen = len(datstr.strip())
    # 1/22/20
    if dtstrlen < 10:
        ffslpt1 = datstr.find("/", 0, dtstrlen)
        pt1 = ffslpt1 + 1
        ffslpt2 = datstr.find("/", pt1, dtstrlen)
        pt2 = ffslpt2 + 1
        mm = datstr[0:ffslpt1]
        dd = datstr[pt1:ffslpt2]
        yy = datstr[pt2:]
        mm = mm.strip()
        dd = dd.strip()
        yy = yy.strip()
        #print("datstr: " + str(datstr))
        #print("ffslpt1: " + str(ffslpt1))
        #print("ffslpt2: " + str(ffslpt2))
        #print("mm: " + str(mm))
        #print("dd: " + str(dd))
        #print("yy: " + str(yy))
        mmln = len(mm)
        ddln = len(dd)
        yyln = len(yy)
        if mmln == 1:
            mm = "0" + mm
        if ddln == 1:
            dd = "0" + dd
        if yyln > 2:
            yy = "20"            
            #yy = yy + "20"
        datstr = mm + "/" + dd + "/" + yy        
    return datstr

def create8DigitDateFormat(datstr):
    datstr = datstr.strip()
    dtstrlen = len(datstr.strip())
    # 1/22/20
    ffslpt1 = datstr.find("/", 0, dtstrlen)
    pt1 = ffslpt1 + 1
    ffslpt2 = datstr.find("/", pt1, dtstrlen)
    pt2 = ffslpt2 + 1
    mm = datstr[0:ffslpt1]
    dd = datstr[pt1:ffslpt2]
    yy = datstr[pt2:]
    mm = mm.strip()
    dd = dd.strip()
    yy = yy.strip()
    #print("datstr: " + str(datstr))
    #print("ffslpt1: " + str(ffslpt1))
    #print("ffslpt2: " + str(ffslpt2))
    #print("mm: " + str(mm))
    #print("dd: " + str(dd))
    #print("yy: " + str(yy))
    mmln = len(mm)
    ddln = len(dd)
    yyln = len(yy)
    if mmln == 1:
        mm = "0" + mm
    if ddln == 1:
        dd = "0" + dd
    if yyln == 4:
        yy = "20"
    datstr = mm + "/" + dd + "/" + yy
    #print("datstr: " + str(datstr))
    #input("Press Enter to continue...")
    return datstr

def getTailCountryDate():
    #reader = csv.reader(open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/TargetDate.csv", "r"), delimiter=",")
    reader = csv.reader(open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/SampleSubmission.csv", "r"), delimiter=",")
    xx = list(reader)
    xxln = len(xx)
    terrdates = []
    for row in range(1, xxln):
        dterr_datestr = xx[row][0]
        dterr_datestr = dterr_datestr.strip()
        #print("dterr_datestr: " + str(dterr_datestr))
        dtstrlen = len(dterr_datestr)
        pt1 = dterr_datestr.find("X", 0, dtstrlen)
        pt2 = pt1 - 1
        #print("pt1: " + str(pt1))
        #print("pt2: " + str(pt2))
        territory = dterr_datestr[0:pt2]
        #print("territory: " + str(territory))
        #print("(territory == 'Afghanistan'): " + str((territory == 'Afghanistan')))
        #input("Press Enter to continue...")
        startdate = datetime.strptime("04/02/20", "%m/%d/%y")
        if territory == 'Afghanistan':
            #print("Afghanistan seen")
            pt3 = pt1 + 2
            datestr = dterr_datestr[pt3:]
            datestr = createDDateFormat(datestr)
            fteddate = datetime.strptime(datestr, "%m/%d/%y")
            if fteddate >= startdate:                
                terrdates.append(datestr)
        else:
            break
    return terrdates

def get8TailCountryDate():
    #reader = csv.reader(open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/TargetDate.csv", "r"), delimiter=",")
    reader = csv.reader(open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/SampleSubmission.csv", "r"), delimiter=",")
    xx = list(reader)
    xxln = len(xx)
    terrdates = []
    for row in range(1, xxln):
        dterr_datestr = xx[row][0]
        dterr_datestr = dterr_datestr.strip()
        #print("dterr_datestr: " + str(dterr_datestr))
        dtstrlen = len(dterr_datestr)
        pt1 = dterr_datestr.find("X", 0, dtstrlen)
        pt2 = pt1 - 1
        #print("pt1: " + str(pt1))
        #print("pt2: " + str(pt2))
        territory = dterr_datestr[0:pt2]
        #print("territory: " + str(territory))
        #print("(territory == 'Afghanistan'): " + str((territory == 'Afghanistan')))
        #input("Press Enter to continue...")
        startdate = datetime.strptime("04/02/20", "%m/%d/%y")
        if territory == 'Afghanistan':
            #print("Afghanistan seen")
            pt3 = pt1 + 2
            datestr = dterr_datestr[pt3:]
            datestr = createDDateFormat(datestr)
            fteddate = datetime.strptime(datestr, "%m/%d/%y")
            if fteddate >= startdate:                
                terrdates.append(datestr)
        else:
            break
    return terrdates

def getDatePart(datstr):
    fieldlen = len(datstr)
    xpt = datstr.find("/", 0, fieldlen)    
    dtpt = xpt - 2
    datepart = datstr[dtpt:]    
    datepart = createDateFormat(datepart)
    #print("datepart: " + str(datepart))
    #input("Press Enter to continue...")
    fteddate = datetime.strptime(datepart, "%m/%d/%y")
    return fteddate

def createCountriesList(): 
    # load the dataset from the CSV file 
    reader = csv.reader(open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/Train.csv", "r"), delimiter=",")
    xx = list(reader)
    xxln = len(xx)
    all_countries = []
    for row in range(1, xxln):            
        all_countries.append(xx[row][3])
            
    #print('all_countries: ', all_countries)    
    return all_countries

if __name__ == '__main__':
    predicted_targetsFT = []
    predicted_targetsLW = []
    predicted_targetsUP = []
    territories_dates = []
    
    #dates = []
    #target_table = {}        
    #for l in range(0, 185):
    #    target_table[l] = 0
        
    now0 = datetime.now()
    timestamp0 = datetime.timestamp(now0)
    #first_through = False

    countries_all = createCountriesList()
    countriesSF_set = set(countries_all)
    countriesSF = list(sorted(countriesSF_set))    
    contsSFln = len(countriesSF)
    
    #territory_name = ""
    tail_dates = getTailCountryDate()
    #print("tail_dates: " + str(tail_dates))
    #input("Press Enter to continue...")
    #for i in range(contsSFln - 2, contsSFln): 
    for i in range(0, contsSFln):       
        country_date = []
        targets = []
        dates = []        
        countrySF = countriesSF[i]
        #country = ""
        createCountryTrainingTable(countrySF)
            
        country = countrySF

        dates = np.vstack(dates)
        target = np.vstack(targets)

        date_targets = np.concatenate((dates, target), axis=1)

        with open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/Train_Data.csv", "w", newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(['ID', 'Territory X Date', 'Target', 'Territory', 'Date']) 
            writer.writerow(['Date', 'Target']) 
            for row in date_targets:    
                l = list(row)    
                writer.writerow(l)

        print('                           ')    
        print('@@@@@@@@@@@ Model Simulation @@@@@@@@@@@')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    
        # Import Data
        data = pd.read_csv('C:/Users/CONALDES/Documents/Coronavirus/approach_B/Train_Data.csv', parse_dates=['Date'], index_col='Date')
        print('data: ', data)
        targets = data['Target']
        tgtln = len(targets)
        #print('targets: ')
        cv_targets = []        
        for j in range(44, tgtln):            
            predicted_targetsFT.append(int(targets[j]))
            predicted_targetsLW.append(int(targets[j]))
            predicted_targetsUP.append(int(targets[j]))
            cv_targets.append(int(targets[j]))
            #print(targets[j])
            
        #input("Press Enter to continue...")    
        print('targets: ', cv_targets)
        #print('ttargets: ', cv_ttargets)
        try:
            # Seasonal - fit stepwise auto-ARIMA
            smodel = pm.auto_arima(data, start_p=1, start_q=1,
                                 test='adf',
                                 max_p=3, max_q=3, m=12,
                                 start_P=0, seasonal=False,
                                 d=None, D=1, trace=True,
                                 error_action='ignore',  
                                 suppress_warnings=True, 
                                 stepwise=True)

            smodel.summary()        
        
            # Forecast      (Let’s forecast for the next 3 months. )
            n_periods = 67
            fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)
            index_of_fc = pd.date_range(data.index[-1], periods = n_periods, freq='MS')

            # make series for plotting purpose
            fitted_series = pd.Series(fitted, index=index_of_fc)
            lower_series = pd.Series(confint[:, 0], index=index_of_fc)
            upper_series = pd.Series(confint[:, 1], index=index_of_fc)
            fittedseries = []
            fittedserlen = len(fitted_series)
            #print('fitted_series: ')
            for j in range(0, fittedserlen):
                fittedSeries = math.ceil(fitted_series[j])
                if fittedSeries < 0:
                    fittedSeries = 0
                predicted_targetsFT.append(fittedSeries)
                fittedseries.append(fittedSeries)
                #print(fittedSeries)
            print('fitted_series: ', fittedseries)
            
            lowerserlen = len(lower_series)
            #print('ftedseries: ')
            for j in range(0, lowerserlen):
                lowerSeries = math.ceil(lower_series[j])
                if lowerSeries < 0:
                    lowerSeries = 0
                predicted_targetsLW.append(lowerSeries)
                #print(lowerSeries)

            upperserlen = len(upper_series)
            #print('ftedseries: ')
            for j in range(0, upperserlen):
                upperSeries = math.ceil(upper_series[j])
                if upperSeries < 0:
                    upperSeries = 0
                predicted_targetsUP.append(upperSeries)
                #print(upperSeries)
                        
            countln = len(country_date)
            for j in range(44, countln):
                territories_dates.append(country_date[j])

            taildtln = len(tail_dates)
            for j in range(0, taildtln):
                countrystr = country + ' X ' + tail_dates[j].strip() 
                territories_dates.append(countrystr)
            
            #territlen = len(territories_dates)
            #print("territlen: " + str(territlen))
            #print("predtgtln: " + str(predtgtln))
            #print('territories_dates :', territories_dates)
            #print('predicted_targets: ', predicted_targets)
        
            #print('data: ', data)
            #print('fitted_series: ', fitted_series)
            #print('lower_series: ', lower_series)
            #print('upper_series: ', upper_series)
                        
        except:
            print("Exception occured...")
            fittedseries = []
            for j in range(0, 67):
                predicted_targetsFT.append(0)
                predicted_targetsLW.append(0)
                predicted_targetsUP.append(0)
                fittedseries.append(0)

            #print('fitted_series: ')
            print('fitted_series: ', fittedseries)
                
            countln = len(country_date)
            for j in range(44, countln):
                territories_dates.append(country_date[j])

            taildtln = len(tail_dates)
            for j in range(0, taildtln):
                countrystr = country + ' X ' + tail_dates[j].strip() 
                territories_dates.append(countrystr)

            #print('territories_dates :', territories_dates)
            #print('predicted_targets: ', predicted_targets)

        
        print('COVID 19 spread in ' + country + ' simulated')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        
        '''
        # Plot
        plt.plot(data)
        plt.plot(fitted_series, color='darkgreen')
        plt.fill_between(lower_series.index, 
                     lower_series, 
                     upper_series, 
                     color='k', alpha=.15)

        plt.title("SARIMA - Final Forecast of COVID19 Deaths")
        plt.show()
        '''

    '''
    print('                        ')    
    terrdtsln = len(territories_dates)
    print('territories_dates: ')
    for j in range(0, terrdtsln):
        print(territories_dates[j])
    print('                        ')    
    targetsln = len(predicted_targetsFT)
    print('predicted_targetsFT: ')
    for j in range(0, targetsln):
        print(predicted_targetsFT[j])
    
    print('predicted_targetsLW: ')
    for j in range(0, targetsln):
        print(predicted_targetsLW[j])

    print('predicted_targetsUP: ')
    for j in range(0, targetsln):
        print(predicted_targetsUP[j])
    '''
    terrdtsln = len(territories_dates)
    targetsln = len(predicted_targetsFT)
    print("len(territories_dates): " + str(len(territories_dates)))
    print("len(predicted_targetsFT): " + str(len(predicted_targetsFT)))
            
    territoriedates = np.vstack(territories_dates)
    predtargetsFT = np.vstack(predicted_targetsFT)
    predtargetsLW = np.vstack(predicted_targetsLW)
    predtargetsUP = np.vstack(predicted_targetsUP)
    territoty_date_targetsFT = np.concatenate((territoriedates, predtargetsFT), axis=1)
    territoty_date_targetsLW = np.concatenate((territoriedates, predtargetsLW), axis=1)
    territoty_date_targetsUP = np.concatenate((territoriedates, predtargetsUP), axis=1)
    localterritoty_targetsFT = []
    localterritoty_targetsLW = []
    localterritoty_targetsUP = []

    startdate = datetime.strptime("04/02/20", "%m/%d/%y")
    enddate = datetime.strptime("04/08/20", "%m/%d/%y")
    teerdatetgtln = len(territoty_date_targetsFT)   
    for i in range(0, teerdatetgtln):
        teertagetFT = []
        teertagetLW = []
        teertagetUP = []
        localdate = getDatePart(territoty_date_targetsFT[i][0])
        if localdate >= startdate and localdate <= enddate:
            teertagetFT.append(territoty_date_targetsFT[i][0])
            teertagetFT.append(territoty_date_targetsFT[i][1])
            localterritoty_targetsFT.append(teertagetFT)

            teertagetLW.append(territoty_date_targetsLW[i][0])
            teertagetLW.append(territoty_date_targetsLW[i][1])
            localterritoty_targetsLW.append(teertagetLW)

            teertagetUP.append(territoty_date_targetsUP[i][0])
            teertagetUP.append(territoty_date_targetsUP[i][1])
            localterritoty_targetsUP.append(teertagetUP)

    localterritoty_targetsFT = np.vstack(localterritoty_targetsFT)
    localterritoty_targetsLW = np.vstack(localterritoty_targetsLW)
    localterritoty_targetsUP = np.vstack(localterritoty_targetsUP)

    with open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubmissionFT.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Territory X Date', 'Target']) 
        for row in territoty_date_targetsFT:    
            l = list(row)    
            writer.writerow(l)

    print("                                          ")
    print("### C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubmissionFT.csv contains results ###")

    with open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubLocalFT.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Territory X Date', 'Target']) 
        for row in localterritoty_targetsFT:    
            l = list(row)    
            writer.writerow(l)

    print("                                          ")
    print("### C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubLocalFT.csv contains results ###")

    with open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubmissionLW.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Territory X Date', 'Target']) 
        for row in territoty_date_targetsLW:    
            l = list(row)    
            writer.writerow(l)

    print("                                          ")
    print("### C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubmissionLW.csv contains results ###")

    with open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubLocalLW.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Territory X Date', 'Target']) 
        for row in localterritoty_targetsLW:    
            l = list(row)    
            writer.writerow(l)

    print("                                          ")
    print("### C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubLocalLW.csv contains results ###")

    with open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubmissionUP.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Territory X Date', 'Target']) 
        for row in territoty_date_targetsUP:    
            l = list(row)    
            writer.writerow(l)

    print("                                          ")
    print("### C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubmissionUP.csv contains results ###")

    with open("C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubLocalUP.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Territory X Date', 'Target']) 
        for row in localterritoty_targetsUP:    
            l = list(row)    
            writer.writerow(l)

    print("                                          ")
    print("### C:/Users/CONALDES/Documents/Coronavirus/approach_B/ConaldesSubLocalUP.csv contains results ###")

    now1 = datetime.now()
    timestamp1 = datetime.timestamp(now1)
    time_elapsed = timestamp1 - timestamp0
    #print('Time elapsed for computations: ' + str(time_elapsed) + 'seconds')
    print('Time elapsed for computations: ' + str(round(time_elapsed, 2)) + 'seconds')

 
