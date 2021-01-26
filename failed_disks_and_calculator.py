# This was one of my first projects using Python. It was for work and it takes a CSV file that needed to be updated when we would have a failed drive at work.
# I wanted to get a visual representation of the failed drives.
# This goes through and creates two plots:
#       1. Location in each device where the drive failed. The size of the dot grows if multiple disks have failed there.
#       2. Total number of drives in each device that has failed as well as an acceptable amount based on how old the device is.
#
# Since that went so well, I also wanted to include a little "calculator" to determine how much space would be needed for new backup sets after
# deduplication was factored in.

from tkinter import *
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from scipy import stats
from scipy.stats import itemfreq
import collections
from datetime import datetime, timedelta, date
import mplcursors

master = Tk()

def spaceCalculator():

    # This will take the input values and calculate how much disk it will take up.
    def calc_dedup():

        T1 = float(E1.get())
        T2 = float(E2.get())
        T3 = float(E3.get())
        T4 = float(E4.get())
        T5 = float(E5.get())
        E1_ans = round(T1 * (1-.8501), 2)
        E2_ans = round(T2 * (1-.6631), 2)
        E3_ans = round((T3-T4) * (1-.851), 2)
        E4_ans = round(T4 * 1, 2)
        E5_ans = round(T5 * (1-.777), 2)
        E6_ans = round(E1_ans+E2_ans+E3_ans+E4_ans+E5_ans, 2)
        E7_ans = round(((1-(E6_ans/(T1+T2+T3+T4+T5)))*100), 2)
        A1['text'] = str(E1_ans)
        A2['text'] = str(E2_ans)
        A3['text'] = str(E3_ans)
        A4['text'] = str(E4_ans)
        A5['text'] = str(E5_ans)
        A6['text'] = str(E6_ans)
        A7['text'] = str(E7_ans)+"%"

    # This generates the GUI to be able to enter the values
    calculator = Toplevel(master) 
    calculator.title("Space Usage Calculator")

    # This will label each field for what type of data is wanted
    L1 = Label(calculator, text="type1")
    L2 = Label(calculator, text="type1")
    L3 = Label(calculator, text="type1")
    L4 = Label(calculator, text="type1")
    L5 = Label(calculator, text="type1")
    L6 = Label(calculator, text="Storage Needed")
    L7 = Label(calculator, text="Total Savings")
    L8 = Label(calculator, text="Totals are calculated using recent dedup totals for each datatype", justify=CENTER, font="Arial 10 italic")

    # This will create the textboxes to enter the amount of data
    E1 = Entry(calculator)
    E2 = Entry(calculator)
    E3 = Entry(calculator)
    E4 = Entry(calculator)
    E5 = Entry(calculator)

    # This creates a spot to put in the total after deduplication
    A1 = Label(calculator, text="0")
    A2 = Label(calculator, text="0")
    A3 = Label(calculator, text="0")
    A4 = Label(calculator, text="0")
    A5 = Label(calculator, text="0")
    A6 = Label(calculator, text="0")
    A7 = Label(calculator, text="0%")

    # This is for the location for all of the above parts
    L1.grid(row=0, column=0)
    L2.grid(row=1, column=0)
    L3.grid(row=2, column=0)
    L4.grid(row=3, column=0)
    L5.grid(row=4, column=0)
    L6.grid(row=6, column=0)
    L7.grid(row=7, column=0)
    L8.grid(row=8, column=0, columnspan=3)
    E1.grid(row=0, column=1)
    E2.grid(row=1, column=1)
    E3.grid(row=2, column=1)
    E4.grid(row=3, column=1)
    E5.grid(row=4, column=1)
    A1.grid(row=0, column=2)
    A2.grid(row=1, column=2)
    A3.grid(row=2, column=2)
    A4.grid(row=3, column=2)
    A5.grid(row=4, column=2)
    A6.grid(row=6, column=2)
    A7.grid(row=7, column=2)

    # This is for a calculate button as well as a quit button
    Button(calculator, text="Calculate", command=calc_dedup).grid(row=1, column=5)
    Button(calculator, text="Quit", command=calculator.destroy).grid(row=2, column=5)

    calculator.mainloop()

def graphingWindow():
    
    graphing = Toplevel(master) 
    graphing.title("Let us graph!")

    def allowedDeadDrives(loadedDrives,years_since):
        if years_since == 1:
            num_drives = loadedDrives*.05
            num_drives = round(num_drives)
        if years_since == 2:
            num_drives = loadedDrives*.08
            num_drives = round(num_drives)
        if years_since == 3:
            num_drives = loadedDrives*.1
            num_drives = round(num_drives)
        if years_since == 4:
            num_drives = loadedDrives*.2
            num_drives = round(num_drives)
        return(num_drives)

    # This will import the CSV to read and will ignore any rows that have no data
    test = pd.read_csv("/directory/for/file.csv")
    test = test.dropna()

    # This will separate out the library that had the bad disk and the disk that went bad
    Library = test.Library
    Disk = test.Replaced

    # This will take the separated sections and turn them into arrays
    Library = np.array(Library)
    Disk = np.array(Disk)

    # This builds an array with both the library and disk that failed. It makes it so it is 50 rows and 2 columns instead
    # of 50 columns and 2 rows
    TestArray = np.concatenate((Library,Disk))
    TestArray = np.array_split(TestArray,2)
    TestArray = np.transpose(TestArray)

    # This takes the array previously created and makes a turple
    new_array = [tuple(row) for row in TestArray]

    # This will go through and get the unique values including a count for how many times each value appears
    unique = np.unique(new_array,axis=0,return_counts=True)

    # This takes the unique counts and turns it into an array
    counting = unique[1:2:1]
    counting = np.transpose(counting)
    counting = np.array(counting)

    # Do this for counting number of rows needed for first part of the final array
    increment = 0
    for x in counting:
        increment = increment + 1

    # This will get the unique combinations of disk libraries and disks who failed
    library = unique[0:1:1]

    # This builds that array to use
    library = np.transpose(library)
    library = np.array_split(library,1)
    library = np.array(library).reshape(2,increment)
    library = np.transpose(library)

    # This creates a single array that lists the unique library and disk failures and associates it with the number of
    # times a particular slot has failed and then sorts by the disk that failed instead of the array
    concat = np.column_stack((library,counting))
    concat = concat[concat[:,1].argsort()]

    # This gets the variable for the size of the dot placed on the chart
    number_of_disks = concat[:,2]
    number_of_disks = np.transpose(number_of_disks)
    number_of_disks = number_of_disks.astype(int)

    # This generates the x-axis
    library_name = concat[:,0]
    library_name = np.transpose(library_name)

    # This generates the y-axis
    disk_number = concat[:,1]
    disk_number = np.transpose(disk_number)

    sizevalues1 = [(x+2)**3 for x in number_of_disks]

    # This is for charting number of disks for each library
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0
    i = 0
    count = 0

    # Use this to determine how old the disk library is
    curr_date = datetime.date(datetime.now())

    # This builds the number of drive replaced for each disk library as well as the maximum number allowed
    # Allowed number per report on https://www.backblaze.com/blog/how-long-do-disk-drives-last/
    for x in Library:
      if x == "dev1":
        a = a + 1
        inst_date = date(2017,5,12)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name1 = x
        num_drives1 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev02":
        b = b + 1
        inst_date = date(2017,5,19)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name2 = x
        num_drives2 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev03":
        c = c + 1
        inst_date = date(2017,5,12)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name3 = x
        num_drives3 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev04":
        d = d + 1
        inst_date = date(2017,5,19)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name4 = x
        num_drives4 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev05":
        e = e + 1
        inst_date = date(2018,3,18)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name5 = x
        num_drives5 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev06":
        f = f + 1
        inst_date = date(2019,3,25)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name6 = x
        num_drives6 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev07":
        g = g + 1
        inst_date = date(2018,3,20)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name7 = x
        num_drives7 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev08":
        h = h + 1
        inst_date = date(2019,3,25)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 168
        name8 = x
        num_drives8 = allowedDeadDrives(loadedDrives,years_since)
      if x == "dev09":
        i = i + 1
        inst_date = date(2017,6,12)
        diff_date = ((curr_date - inst_date).days)
        years_since = round((diff_date/365))
        loadedDrives = 108
        name9 = x
        num_drives9 = allowedDeadDrives(loadedDrives,years_since)

    # This is going to create arrays for the x-axis and y-axis
    disks = [a,b,c,d,e,f,g,h,i]
    names = [name1,name2,name3,name4,name5,name6,name7,name8,name9]
    ok_disks = [num_drives1,num_drives2,num_drives3,num_drives4,num_drives5,num_drives6,num_drives7,num_drives8,num_drives9]

    # To create one array from two. It will use the previous for statement to determine how long the array is
    array = np.concatenate((disks,names)).reshape(2,9)

    # This is for plotting
    fig = plt.figure(figsize=(15,9))
    plt.subplot(131)
    plt.scatter(library_name, disk_number, c='g', s=sizevalues1)
    plt.xlim(-1,9)
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.subplot(132)
    real_drives = plt.scatter(names, disks, c='g', marker="o", s=100)
    max_drives = plt.scatter(names, ok_disks, c='r', marker="x", s=100)
    plt.legend([real_drives, max_drives], ["Actual drive failure", "Max theoretical failures"], loc="upper right")
    plt.xlim(-1,9)
    plt.xticks(rotation='vertical')
    plt.ylim(0,25)
    plt.yticks(np.arange(0,26,1))
    plt.tight_layout(pad=3.0)

    canvas = FigureCanvasTkAgg(fig, master=graphing)
    canvas.draw()
    mplcursors.cursor(hover=True)
    toolbar = NavigationToolbar2Tk(canvas, graphing)
    toolbar.update()
    canvas.get_tk_widget().pack()
    
    graphing.mainloop()
    
graphButton = Button(master,text="Click for graph", command=graphingWindow)
graphButton.pack()
calcButton = Button(master,text="Click for calculator", command=spaceCalculator)
calcButton.pack()
quitButton = Button(master,text="Quit App", command=master.destroy)
quitButton.pack()

mainloop()
