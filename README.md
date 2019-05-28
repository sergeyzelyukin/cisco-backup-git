# cisco-backup-git
Automate the backup process for all CDP discoverable devices using GIT subsystem

First of all, please, install "ciscotelnet" module:
<pre>
pip install git+https://github.com/sergeyzelyukin/cisco-telnet.git
pip install git+https://github.com/sergeyzelyukin/cisco-mapper.git
</pre>
Now you can use this script.


Just modify BACKUP_PATH variable inside the script to any existing directory,<br>
prefill auth_choices.conf file with all authentication credentials that could be met in the network and<br> 
then add the script to crontab:
<pre>
0        */4     *       *       *       root    /root/cisco-backup-git/browse-and-backup.py /root/cisco-backup-git/auth_choices.conf R1
</pre>
and it will browse all CDP neighbors at regular intervals, from R1 downwards the tree, saving router's configs to the backup directory.<br> 
If there is at least one difference in comparison to the previous run, the script will make new GIT commit, specifying changed hostnames.


IMPORTANT: Before running this, please make sure that CDP is disabled on all untrusted ports. If someone pretends as a CDP neighbor, he/she can steal all your passwords! Use this approach at your own risk!


