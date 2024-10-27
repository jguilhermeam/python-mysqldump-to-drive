Python mysqldump to Google Drive
===

### Install requirements

Python3 is needed.

```
pip install google-api-python-client
sudo apt install mysql-client
```

### Google Cloud console requirements

Enable Google Drive API
Create a Service Account with Actions Admin role
Create a Key for the Service Account in JSON format
Share the folder on Google Drive with the Service Account Principal Email

### To execute

Set database credentials on main.py and configure a Google Service account and export its json key file. Define the json file path in KEY_FILE variable.

The script will first make a dump sql file and then upload it to a backup folder (you name it) on your google drive.
After that it will clear old backups based on the MAX_DUMPS variable value defined.

to run

```
python main.py
```

### Sample cron job

in this sample cron job call, the output will be stored in a log txt file

```
0 3 * * * /usr/bin/python3 /path/to/main.py >> /path/to/log.txt
```
