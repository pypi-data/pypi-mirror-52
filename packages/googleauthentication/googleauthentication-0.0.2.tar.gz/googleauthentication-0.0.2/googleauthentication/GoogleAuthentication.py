import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build


def _write_cred(cred, file_path):
    f = open(file_path, "w")
    f.write(json.dumps(cred))
    f.close()


class GoogleAuthentication:
    def __init__(self, client_secret_file_path):
        self.client_secret_file_path = client_secret_file_path

    def credentials(self):
        f = open(self.client_secret_file_path, "r")
        cred = json.load(f)
        f.close()
        cred["private_key"] = os.environ["GOOGLE_PRIVATE_KEY"]
        _write_cred(cred, self.client_secret_file_path)
        credentials = service_account.Credentials.from_service_account_file(self.client_secret_file_path)
        del cred["private_key"]
        _write_cred(cred, self.client_secret_file_path)
        return credentials

    def get_account(self, api, version="v4"):
        credentials = self.credentials()
        account = build(api, version, credentials=credentials)
        return account
