import csv
import pandas as pd
from datetime import timedelta

with open("Attendance.csv","r+")  as csvfile:
        csvreader = csv.reader(csvfile)
        df = pd.read_csv(csvfile)
        #have to convert to timedelta,in order to subtract
        df['Time In'] = pd.to_timedelta(df['Time In'])
        df['Time Out'] = pd.to_timedelta(df['Time Out'])
        a =( df['Time Out'] - df['Time In'])
        # subtracting 1hour of lunch from the total time
        df['Hours Worked'] = (a- timedelta(hours=1))
        #to slice the days from the pd.to_timedelta
        df['Time In'] = df['Time In'].astype(str).map(lambda x: x[7:])
        df['Time Out'] = df['Time Out'].astype(str).map(lambda x: x[7:])
        df['Hours Worked'] = df['Hours Worked'].astype(str).map(lambda x: x[7:])
        print(df)
           
                
                
            


