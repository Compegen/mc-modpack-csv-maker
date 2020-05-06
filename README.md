# mc-modpack-csv-maker
Tries to automatically make a csv file based on the contents of the mcmod.info of all mods inside your mods folder

<h2> What this does: </h2>

- Allows user to open a 'mods' folder directory & reads contents of that folder
- All .jar files in that folder are opened and searched for a 'mcmod.info'
- If there is a 'mcmod.info', it tries to get a mod name & link from the file
- After going through all available files, it exports a dictionary to an auto-named .csv file in your working directory

<h3> What this doesn't do </h3>

- Be efficient
- List author names
- Handle malformed json's
- Handle really long mod descriptions on multiple lines

_____
This was made as a realitively simple project to make generating the modlist to my custom modpacks easier. 

I'd love to see a fancier version of this if someone made one.
