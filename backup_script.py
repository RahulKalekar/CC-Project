import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging
from kubernetes import client, config

# Load Kubernetes configuration
config.load_incluster_config()

# Create Kubernetes API client
core_api = client.CoreV1Api()

# Retrieve secret
secret_name = 'api-credentials'
secret = core_api.read_namespaced_secret(secret_name, 'default')

# Get API credentials from secret
client_id = secret.data['client_id'].decode('utf-8')
client_secret = secret.data['client_secret'].decode('utf-8')

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """
    Authenticate with Google Drive API using OAuth2 credentials.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def upload_file(file_path):
    """
    Upload a file to Google Drive.
    """
    # Authenticate with Google Drive API
    creds = authenticate()

    # Build Google Drive API service
    service = build('drive', 'v3', credentials=creds)

    # Define file metadata
    file_metadata = {'name': os.path.basename(file_path)}

    # Upload file to Google Drive
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Log file ID
    logging.info('Uploaded file %s to Google Drive. File ID: %s', file_path, file.get('id'))

if __name__ == '__main__':
    # Log backup process start
    logging.info('Backup process started...')

    # Upload file to Google Drive
    upload_file('file1.txt')  # Replace with the correct path to your file

    # Log backup process completion
    logging.info('Backup process completed successfully.')
