from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os
import time

HOST='127.0.0.1'
DB_USER='username'
DB_PASS='password'
DB_NAME='database'
KEY_FILE='key.json'
MAX_DUMPS = 7
BACKUPS_FOLDER='backups'

def get_dump():
    print('dumping database...')
    filestamp = time.strftime('%Y-%m-%d-%I-%M')
    os.popen("mysqldump --column-statistics=0 -h %s -u %s -p%s %s > %s.sql" % (HOST,DB_USER,DB_PASS,DB_NAME,DB_NAME+"_"+filestamp))
    dump_filename = DB_NAME+"_"+filestamp+".sql"
    print("Database dumped to "+dump_filename)
    return dump_filename

def clear_old_backups(service):
    print("searching for old backups to delete (MAX="+str(MAX_DUMPS)+")")

    results = service.files().list(fields="files(id, name, createdTime)").execute()
    items = results.get('files', [])
    sqls = [item for item in items if item['name'].endswith('.sql')]

    if len(sqls) > MAX_DUMPS:
        sqls.sort(key = lambda x: x['createdTime'], reverse=True)
        for file in sqls[MAX_DUMPS:]:
            delete_file(service, file['name'], file['id'])
    else:
        print('not going to delete')


def delete_file(service, filename, file_id):
    print('deleting file '+filename+" (id="+file_id+")")
    file = service.files().delete(fileId=file_id).execute()
    print("delete successful")

def upload_basic(service, filename, mime, folder_id):
    try:
        file_metadata = {'name': filename, 'parents': [folder_id]}
        media = MediaFileUpload(filename, mimetype=mime)
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print("uploading "+filename)
        print(F'File ID: {file.get("id")}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        exit('STOPPING -> upload failed')
        file = None

    return {'name': filename, 'id': file.get('id'), 'createdTime': file.get('createdTime')}


def main():
    dump_file = get_dump()

    creds = service_account.Credentials.from_service_account_file(KEY_FILE)
    service = build('drive', 'v3', credentials=creds)

    try:
        results = service.files().list(fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return

        folder_id = None
        print('Files:')
        for item in items:
            print(str(item))
            if item['name'] == BACKUPS_FOLDER:
                folder_id = item['id']
                print(BACKUPS_FOLDER+" folder id = "+folder_id)

        if folder_id == None:
            exit('ERROR no backups folder was found')

        upload_basic(service, dump_file, 'application/sql', folder_id)
        clear_old_backups(service)
        os.remove(dump_file)

    except HttpError as error:
        print(f'An error occurred: {error}')



if __name__ == '__main__':
    main()
