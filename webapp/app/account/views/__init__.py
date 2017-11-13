from flask import render_template, jsonify, session, redirect, url_for, request
from flask_login import current_user, login_required
from .. import account
from forms import EventCalendar
import google.oauth2.credentials
import googleapiclient.discovery
import pprint


def get_credentials():
    return google.oauth2.credentials.Credentials(
                            **current_user.credentials)


def get_group_service():
    return googleapiclient.discovery.build(
            'admin', 'directory_v1', credentials=get_credentials())


def get_drive_service():
    return googleapiclient.discovery.build('drive', 'v2',
                credentials=get_credentials())


def get_calendar_service():
    return googleapiclient.discovery.build(
        'calendar', 'v3', credentials=get_credentials())


def search_folder(title):
    drive_service = get_drive_service()
    response = drive_service.files().list(q="title='MISDocs' and trashed = false", spaces='drive').execute()
    folders = response.get('items', [])
    #pprint.pprint(folders)
    return folders


def create_system_folder():
    drive_service = get_drive_service()
    folder_metadata = {
        'title': 'MISDocs',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().insert(body=folder_metadata, fields='id').execute()
    return folder


@login_required
@account.route('/profile')
def view_profile():
    return render_template('account/profile.html')


@login_required
@account.route('/docs')
def view_docs():
    drive_service = get_drive_service()
    folders = []
    folders = search_folder('MISDocs')  # search for system folder
    if not folders:
        # print('MISDocs not found')
        folder = create_system_folder()  # app folder does not exist, create one
    else:
        # print('MISDocs found.')
        folder = folders[0]

    children = drive_service.children().list(folderId=folder['id']).execute()['items']
    files = []
    for child in children:
        f = drive_service.files().get(fileId=child['id']).execute()
        files.append(f)
    return render_template('account/docs.html', folder=folder, files=files)


@login_required
@account.route('/docs/delete')
def delete():
    drive_service = get_drive_service()
    folders = search_folder('MISDocs')
    for f in folders:
        drive_service.files().delete(fileId=f['id']).execute()
        print('deleted %s' % f['id'])
    return 'Done'


@login_required
@account.route('/docs/folder/<folder_title>/<folder_id>')
def open_folder(folder_title, folder_id):
    if not folder_id:
        return redirect(url_for('account.view_docs'))
    else:
        files = get_children_files(folder_id)
        return render_template('account/file_list.html', folder_title=folder_title, files=files)


def get_children_files(folder_id):
    drive_service = get_drive_service()
    children = drive_service.children().list(folderId=folder_id).execute()['items']
    files = []
    for child in children:
        f = drive_service.files().get(fileId=child['id']).execute()
        files.append(f)
    return files


@account.route('/groups')
def manage_groups():
    group_service = get_group_service()
    group_email = current_user.email
    results = group_service.users().list().execute()
    return jsonify(results)


@login_required
@account.route('/cart')
def view_cart():
    file_id = request.args.get('file_id', None)
    cart_view = request.args.get('cart_view', 'event')
    if file_id:
        if 'files_cart' not in session:
            session['files_cart'] = [file_id]
        else:
            _files = session['files_cart']
            if file_id not in _files:
                _files.append(file_id)
                session['files_cart'] = _files
    drive_service = get_drive_service()
    files = []
    for item in session['files_cart']:
        f = drive_service.files().get(fileId=item).execute()
        files.append(f)
    event_form = EventCalendar()
    return render_template('account/cart.html', files=files, cart_view=cart_view, event_form=event_form)


@login_required
@account.route('/create_event_with_files', methods=['GET', 'POST'])
def create_event_with_files():
    drive_service = get_drive_service()
    calendar_service = get_calendar_service()
    attachments = []
    for item in session['files_cart']:
        f = drive_service.files().get(fileId=item).execute()
        attachments.append({
            'fileUrl': f['alternateLink'],
            'mimeType': f['mimeType'],
            'title': f['title']
        })
    form = EventCalendar()
    if form.validate_on_submit():
        summary = form.summary.data
        location = form.summary.data
        description = form.description.data
        startdate = form.startdate.data
        enddate = form.enddate.data
        attendees = [a.strip() for a in form.attendees.data.split(',')]
    else:
        return "form not validated"

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': startdate.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Bangkok',
        },
        'end': {
            'dateTime': enddate.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Bangkok',
        },
        'attendees': attendees,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ]
        },
        'attachments': attachments
    }
    event = calendar_service.events().insert(calendarId='primary',
                                                supportsAttachments=True,
                                                body=event).execute()
    return "Event has been created"