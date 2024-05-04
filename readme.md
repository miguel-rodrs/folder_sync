# Folder Synchronization

**Folder Synchronization** that synchronizes the files in two folders, being one of them the source folder and the other
one the replica folder. The synchronization happens only in one way, being the replica the one who will have the content
changed by this script.

The only requirement to run this script is having python installed. The python version used to create this script was 3.12.0
 and so is recommended in order to run this script.

usage: SyncDir [-h] [-v] [-s SOURCE] [-r REPLICA] [-l LOG] [-i INTERVAL]

## Description

This script synchronizes 2 directories, one of them being the source folder and the other one being the replica folder using an interval between each synchronization and
logging every operation to a log file.

options:

-  -h, --help            
&nbsp;&nbsp;&nbsp;&nbsp;
show this help message and exit


-  -v, --version         
&nbsp;&nbsp;&nbsp;&nbsp;
show program's version number and exit


-  -s SOURCE, --source SOURCE          
&nbsp;&nbsp;&nbsp;&nbsp;
File path to the source folder. The path can be relative or absolute. This argument is optional 
and the default path is './src_path'.
 

- -r REPLICA, --replica REPLICA         
&nbsp;&nbsp;&nbsp;&nbsp;
File path to the replica folder. The path can be relative or absolute. This argument is optional and the default path is './rep_path'.
 

- -l LOG, --log LOG     
&nbsp;&nbsp;&nbsp;&nbsp;
Path where the log will be created and written. The path can be relative or absolute. This argument is optional and the default path is './log.log'.
 

- -i INTERVAL, --interval INTERVAL         
&nbsp;&nbsp;&nbsp;&nbsp;
Interval between each synchronization in seconds. This argument is optional and the default interval is '60' seconds.