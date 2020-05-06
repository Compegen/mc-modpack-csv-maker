'''
Created 2020-05-06 by Derek R / Compegen

Automated Minecraft modpack list generator
------------------------------------------

Used to generate a list of mods & their websites from their JARs inside a mods folder

TODO:
! Possible GUI?
! Be able to select mods folder to try and open
! Open & read all files in a folder
! zipfile
! Check for when a file cannot be opened & skip it

'''
# For GUI
from tkinter import *
import tkinter.filedialog

# For file handling
import zipfile, csv, json
'''
# .jar's are archive files and must be unzipped
# We are exporting the final list into a formatted .csv
# The mcmod.info inside the jar's are just json files
'''

# For file opening
import os, ntpath, glob
'''
# ntpath allows us to handle file names no matter the file system architecture
# glob allows us to get a list of paths based on regex
'''

# For filename
import time


# Folder to look for mods. Default to working directory
folder = os.getcwd()+"\mods"
# Current modlist
modlist = []


# Set working folder to directory user gives
def fillDirectory():
    global folder

    print("Getting user directory")
    folder = tkinter.filedialog.askdirectory()
    browseBar['text'] = str(folder)
    print("Directory set to "+str(folder))


# When we hit run, do things.    
def getItGoing():
    global modlist
    global folder

    # Update GUI to reflect current state
    runB['state'] = "disable"

    statustag['text'] = "Running"
    statustag['bg'] = "red"
    master.update()

    # Make sure we start with a fresh modlist every run
    modlist.clear()

    # Do that thing we do
    runFolder()


    # Create final modlist & export it to a .csv file
    filename = "MODLIST-"+time.strftime("%Y.%m.%d-%H%M%S"+".csv")
    try:
        with open(filename, "w", newline='') as sheet:
            fields = ['modname', 'link', 'filename']
            writer = csv.DictWriter(sheet, fieldnames=fields)
            writer.writeheader()

            
            for row in modlist:
                writer.writerow( row )
        print("File exported!")
    except Exception as exc:
        print("Could not save file")
        print("    ", end="")
        print(exc)

    #Update the GUI to reflect the current state
    statustag['text'] = "Finished"
    statustag['bg'] = "Green"
    master.update()

    time.sleep(2)
    runB['state'] = "normal"

    statustag['text'] = "Idle"
    statustag['bg'] = "black"
    master.update()


# Open folder & start getting information
def runFolder():
    global folder
    print("Opening "+str(folder))
    #Are there jar files to analyze?
    try:
        for filename in glob.glob(os.path.join(folder, '*.jar')):

            #Unzip file
            try:
                with zipfile.ZipFile(filename) as jar:
                    extractMODINFO(jar)
            except Exception as exc:
                print("Couldn't unzip "+filename)
                print("    ", end="")
                print(exc)
                

    except Exception as exc:
        print("Couldn't find any jar files to open")
        print("    ", end="")
        print(exc)

# Open the modinfo & get attributes we want
def extractMODINFO(jar):
    global modlist

    # Base entry
    entry = {"modname" : "", "link":"", "filename": ntpath.basename(jar.filename)}

    # Does a mcmod.info exist
    try:
        with jar.open('mcmod.info') as mod:
            mcinfo_raw = json.loads(mod.read())

            # Check for mcinfo version
            if isinstance(mcinfo_raw[0], object):
                mcinfo = mcinfo_raw[0]
            else:
                mcinfo = mcinfo[1][0]


            mcinfo = mcinfo_raw[0]
            #print("\n---MCINFO---\n"+str(mcinfo))

 
            # Isn't it fun that the name & link attributes aren't required as part of the mcp standard
            try:
                entry['modname'] = str(mcinfo['name'])
            except:
                #print("NO_NAME")
                entry['modname'] = "NO_NAME"
            try:
                entry['link'] = str(mcinfo['url'])
            except:
                #print("NO_URL")
                entry['link'] = "NO_URL"
                

            
    except Exception as exc:
        print("Couldn't find 'mcmod.info' in "+entry['filename'])
        print("    ", end="")
        print(exc)

    #print("\n----ENTRY----\n"+str(entry))
    modlist.append(entry)

        


### GUI ###

master = Tk(className="Modpack list Generator")
master.geometry("600x200")
master.columnconfigure([0,1], weight=1, minsize=50)
master.rowconfigure(3, weight=1, minsize=50)

browseLabel = Label(master, text="Browse for 'mods' folder")
browseLabel.grid(columnspan=2, padx=5, pady=5, sticky=NW)

browseBt = Button(master, text="Browse...", command=fillDirectory)
browseBt.grid(row=1, column=0, padx=5, pady=5, sticky=NW)


browseBar = Label(master, text=folder)
browseBar.grid(row=1, column=1, padx=5, pady=5, stick=NW)

runB = Button(master, text="Run", command=getItGoing)
runB.grid(row=2, columnspan=2, padx=5, pady=5, sticky=N)

statustag = Label(master, text="Idle", fg="white", bg="black", width=7, height=2)
statustag.grid(row=3, columnspan=2, padx=5, pady=5)

master.mainloop()

### ##### ###



