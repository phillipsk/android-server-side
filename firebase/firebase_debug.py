import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def conn():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('fmc1fmc2-ceb13cec2549.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.environ.get('API_FIRE_DB_URL')
    })

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    # ref = db.reference('restricted_access/secret_document')
    ref = db.reference('announcements')
    # users_ref = ref.child('users')
    print(ref.get())

    ref = db.reference('announcements')
    snapshot = ref.get()
    for key, val in snapshot.items():
        print('{0} was {1} meters tall'.format(key, val))


if __name__ == '__main__':
    conn()
