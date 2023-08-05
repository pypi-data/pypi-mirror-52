# Episode-Fixer

This is a python script cum package that renames episodes, inside a given TV Show folder into a more readable format. It was created by me to parse filenames of downloaded TV Show episodes, deduce their season and episode number and append their episode titles. It uses the TVDB database to scrape info regarding the titles.

The script currently is **stable**. It can handle formats like  S00E00, s00e00, 0x00 , 0X00, 000/0000 and 00. It will rename the files to "Name of TV SHOW S01E01 - Episode Title .fileformat"  
The format in which season and episode info is outputted is controlled by the user.  The output formats SE, se, x, X and 0.  These result in "S00E00, s00e00, 0x0, 0X00 and 000 respectively. The default format is "SE".

The command line to execute this script is  `PYTHON_PATH "PATH/EpisodeFixer.py"`. It has an interactive command line interface.  This interface asks for inital input as the logging level of code, name of the TV Show and Parent Directory of TV Show. It also asks for Output Format.

It will first go through all files in the folder and subfolders of the directory entered. It will find names for these files and in the end ask the user to input the files,they wish to be renamed. It supports episode selections by range and discrete selections. The interactive terminal explains how to do this.

The Program will ask you to confirm the renames. This is done by pressing Enter. If you do not wish to rename the files. You may skip them by pressing any other key. A Log File is also created which stores the rename history in case you need to reverse a rename.

I have enabled logging in order to explain the user what is happening while program is running. The default logging level is INFO. The other options are DEBUG and WARNING. DEBUG will explain to the user what is happening. INFO is there for previewing and checking fields. WARNING in case user wants to go fast and not print everything.

A rename history file is also generated in the target folder. This is done in case user wants to check for errors or reverse a rename manually.

There is also a utility to embed subtitle files into the main video file. This is slow and still being tested.

Since it is also packaged as a module. You can create a class called TVShow() inside your code and then use the rename method to rename the TV Show and embedShowSubtitles to embed Subs if present into the Show file and generate an .mkv file as a result.
