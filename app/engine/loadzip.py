#!/usr/bin/env python3
import json
from ..models import Appointment, Startup, Mentor, User
from datetime import date, datetime, timedelta
import string
import pandas as pd
import numpy as np
import time
import os
import glob
import zipfile


def cleaner():
    """ delete files in uploads folder
    """
    fileList = glob.glob('media/*.zip')
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")


def loadzip(filename):
    """
    load zip file and pass info into database
    """
    if not os.path.isdir('data'):
        os.mkdir('data')
    with zipfile.ZipFile('media/'+filename, 'r') as zip_ref:
        zip_ref.extractall('data/')
    # create mentors ans startups
    source = pd.read_html('data/Source Data.html', header=1, index_col=0)[0]
    loaddata(source)
    # create appointments
    for company in Startup.objects.all():
        c_name = company.companyName
        appointment = pd.read_html('data/'+c_name+'.html',
                                   header=2, index_col=0)[0]
        load_appointment(appointment, c_name)

    cleaner()


def load_appointment(data_ap, c_name):
    """
    create an appointment in database
    """
    data_ap = data_ap.drop(['Unnamed: 2'], axis=1, errors='ignore')
    dates = ['2021-02-01',
             '2021-02-02',
             '2021-02-03',
             '2021-02-04',
             '2021-02-05']

    mentors = Mentor.objects.all()
    data_ap
    for i, date in enumerate(dates):
        mentors_day = data_ap.iloc[:, i+1]
        for j, m_d in enumerate(mentors_day):
            if type(m_d) == str:
                try:
                    mentor = Mentor.objects.get(name=m_d)
                except:
                    continue

                time_all = data_ap.iloc[j, 0]
                time_all = time_all.split()
                if time_all[1] == 'PM':
                    time_all[0] = convertPM(time_all[0])
                if time_all[4] == 'PM':
                    time_all[3] = convertPM(time_all[3])
                time = time_all[0]
                end = time_all[3]
                startup = Startup.objects.get(companyName=c_name)
                Appointment.objects.update_or_create(
                                                     mentor=mentor,
                                                     startup=startup,
                                                     defaults={'date': date,
                                                               'time': time,
                                                               'status': 'pending',
                                                               'endtime': end})


def convertPM(hour):
    """
    change hour format
    """
    hour = hour.split(':')
    new_hour = int(hour[0])
    new_hour += 12
    return str(new_hour) + ':' + hour[1]


def loaddata(source):
    """
        loads a dataframe file (source data) into database

        source: dataframe
    """
    men_and_com = source['Name'].values.tolist()
    for i in range(len(men_and_com)):
        if type(men_and_com[i]) != str:
            break
    mentors = men_and_com[:i]
    companies = men_and_com[i+2:]
    for j, c in enumerate(companies):
        # c_lower = c.lower()
        # c_final = c_lower.translate({ord(c): None for c in string.whitespace})
        # c_user, _ = User.objects.get_or_create(username=c_final)
        pic = source.iloc[i+j+2, 4]
        obj, created = Startup.objects.get_or_create(companyName=c, startupPic=pic)
                                                     # user=c_user)

    com = Startup.objects.all()
    for i, m in enumerate(mentors):
        list_startups = source.iloc[i, 5:17]
        st = []
        for s in list_startups:
            startups = Startup.objects.filter(companyName=s)
            if len(startups) != 0:
                st.append(startups[0])
        day = "undefined"
        timeslot = "undefined"
        email = "undefined"
        pic = "undefined"
        if type(source.iloc[i, 4]) == str:
            day = source.iloc[i, 4].split(" - ")[0]
            timeslot = source.iloc[i, 4].split(" - ")[1]
        if type(source.iloc[i, 2]) == str:
            email = source.iloc[i, 2]
        if type(source.iloc[i, 17]) == str:
            pic = source.iloc[i, 17]
        obj, _ = Mentor.objects.update_or_create(name=m,
                                                 defaults={'name': m,
                                                           'email': email,
                                                           'day': day.lower(),
                                                           'timeSlot': timeslot,
                                                           'mentorPic': pic,
                                                           })
        obj.startup.add(*st)
        obj.save()
