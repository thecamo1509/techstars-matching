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


def cleaner():
    """ delete files in uploads folder
    """
    fileList = glob.glob('media/*.csv')
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")


def loaddata(filename):
    """
        loads a csv file (source data) into database

        filename: file name of cvs file located in /media
    """
    source = pd.read_csv('media/'+filename)
    men_and_com = source['Name'].values.tolist()
    for i in range(len(men_and_com)):
        if type(men_and_com[i]) != str:
            break
    mentors = men_and_com[:i]
    companies = men_and_com[i+2:]
    for c in companies:
        c_lower = c.lower()
        c_final = c_lower.translate({ord(c): None for c in string.whitespace})
        print(c_final)
        c_user, _ = User.objects.get_or_create(username=c_final)
        obj, created = Startup.objects.get_or_create(companyName=c, user=c_user)

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
        if type(source.iloc[i, 4]) == str:
            day = source.iloc[i, 4].split(" - ")[0]
            timeslot = source.iloc[i, 4].split(" - ")[1]
        if type(source.iloc[i, 2]) == str:
            email = source.iloc[i, 2]
        obj, _ = Mentor.objects.update_or_create(name=m,
                                                 defaults={'name': m,
                                                           'email': email,
                                                           'day': day.lower(),
                                                           'timeSlot': timeslot
                                                           })
        obj.startup.add(*st)
        obj.save()
    cleaner()
