Python mysqldump to Google Drive
===

### Install requirements

```
pip install google-api-python-client
sudo apt install mysql-client
```

### To execute

Set database credentials on main.py and configure a Google Service account and export its json key file. Define the json file path in KEY_FILE variable.

The script will first make a dump sql file and then upload it to a backup folder (you name it) on your google drive.
After that it will clear old backups based on the MAX_DUMPS variable value defined.

to run

```
python main.py
```

