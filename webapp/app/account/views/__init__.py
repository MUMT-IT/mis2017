from flask import render_template
from flask_login import current_user, login_required
from .. import account
import google.oauth2.credentials
import googleapiclient.discovery
import pprint

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'


def get_service():
    credentials = google.oauth2.credentials.Credentials(
        **current_user.login.credentials
    )
    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials
    )
    return drive


def search_folder(title):
    drive = get_service()
    response = drive.files().list(q="title='MISDocs' and trashed = false", spaces='drive').execute()
    folders = response.get('items', [])
    pprint.pprint(folders)
    return folders


def create_system_folder():
    drive = get_service()
    folder_metadata = {
        'title': 'MISDocs',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive.files().insert(body=folder_metadata, fields='id').execute()
    return folder


@account.route('/profile')
def view_profile():
    return render_template('account/profile.html')


@login_required
@account.route('/docs')
def view_docs():
    drive = get_service()
    folders = []
    folders = search_folder('MISDocs')  # search for system folder
    if not folders:
        print('MISDocs not found')
        folder = create_system_folder()  # app folder does not exist, create one
    else:
        print('MISDocs found.')
        folder = folders[0]

    children = drive.children().list(folderId=folder['id']).execute()['items']
    files = []
    for child in children:
        f = drive.files().get(fileId=child['id']).execute()
        pprint.pprint(f)
        files.append(f)
    return render_template('account/docs.html', folder=folder, files=files)

@account.route('/docs/delete')
def delete():
    drive = get_service()
    folders = search_folder('MISDocs')
    for f in folders:
        drive.files().delete(fileId=f['id']).execute()
        print('deleted %s' % f['id'])
    return 'Done'

