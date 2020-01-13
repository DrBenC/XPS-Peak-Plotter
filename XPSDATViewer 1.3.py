"""
This script will take all .dat files in from its directory and output a figure showing all peaks and residuals
"""

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sbn
import glob
import os
import openpyxl
import numpy as np

abspath = os.path.abspath("XPSDATViewer 1.3.py")
path = os.path.dirname(abspath)

#Finds and retrieves all .dat files 
filenames1 = glob.glob(path + "/*.dat")
filenames2 = [os.path.split(y)[1] for y in filenames1]
filenames = [os.path.splitext(os.path.basename(z))[0] for z in filenames2]

#Finds and retrieves .xls file to use as FILENAME - if no .xls will simply name the files 'sample'
core_file_extpath = glob.glob(path + "/*.xls")
core_fileext = [os.path.split(h)[1] for h in core_file_extpath]
core_file = [os.path.splitext(os.path.basename(j))[0] for j in core_fileext]
if len(core_file) != 0:
    core_file_s = core_file[0]
else:
    core_file_s = "sample"

#Parses through each file
for file in filenames:
    title = str(file)+" region in "+str(core_file_s)
    sn = pd.read_fwf(file+".dat", delim_whitespace=True)

    #This is used later to set the x limits for the graph
    energy = list(sn["B.E.(eV)"])
    energy_reverse = list(reversed(energy))


    #Sometimes the residuals are output as strings, this fixes that  
    differences_raw = list(sn["difference"])
    differences = ([float(diff) if type(diff)==float else float(diff[:5]) for diff in differences_raw])
    
    
    #loading message to show data has been taken in and processed successfully
    print("Drawing "+file)

    #draws shortlist of column headings in dataframe
    heads = list(sn.columns)

    #confirms no open plot and sets figure size
    plt.close()
    fig = plt.figure(figsize = (8, 6))

    #works through each peak within the file
    for entry in sn.columns:

        #Sets off first subplot (data), and plots all series except B.E. and Difference, sets x limits to reverse x axis
        ax_signal = plt.subplot(4,2,(1,6), label=file+" signal plot").set_xlim(energy[0], energy_reverse[0])
        if entry != "B.E.(eV)":
            if entry != "difference":
              

                #If Peak Sum data, will be a dashed line to aid visualisation
                if entry == "Peak Sum ":
                    ax_signal = plt.plot(energy_reverse, sn[entry], label=entry, linestyle="--")
                else:
                    ax_signal = plt.plot(energy_reverse, sn[entry], label=entry)

                #Formats first subplot
                plt.tick_params(labelleft=False, left=False)
                plt.legend()
                plt.xticks(fontsize=12)
                plt.ylabel("Counts / Arbitrary", fontsize = 14)                   
                plt.title(title, fontsize = 16)
                plt.ytick_labels=False
                
                #Plots second subplot (residuals from fit) and formats
            else:
                print((differences))
                ax_difference = plt.subplot(4,2,(7,8), label=entry+" difference plot").set_xlim(energy[0], energy_reverse[0])
                ax_difference = plt.plot(energy_reverse, list(differences))
                plt.tick_params(labelleft=False, left=False)
                plt.xticks(fontsize=12)
                plt.xlabel("Binding Energy / eV", fontsize = 14)
                plt.ylabel("Residuals", fontsize = 14)
                       
    #final layout fixing, showing and saving data
    fig.tight_layout()
    plt.pause(1)
    fig.savefig(title+".png")
    plt.close()
    
    
