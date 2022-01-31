#!.venv/bin/python

import os
import json
import tempfile
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, storage, firestore, messaging
from doc_generator.generator import DocumentGenerator
from doc_generator.data_class import (
    DataItem,
    Metadata,
    SectionData,
    SubsectionData
)


BASE_DIR = Path(tempfile.gettempdir())
FILEPATH = BASE_DIR / "test.txt"
TEMPLATE = "template.docx"

cred = credentials.Certificate("firebase-admin-cred.cred.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "peritax-auditing.appspot.com",
})
db = firestore.client()


def get_user(uid: str):
    doc = db.collection("users").document(uid)
    return doc.get().to_dict()


def create_document(data: dict, uuid: str):
    metadata_dict = data["metadata"]
    metadata = Metadata(metadata_dict["date"], metadata_dict["client_name"], metadata_dict["location"])

    section_list = data["sectionDataList"]
    section_data_list = []
    for d in section_list:
        section = SectionData(**d)
        section_data_list.append(section)

    subsection_list = data["subsectionDataList"]
    subsection_data_list = []
    for d in subsection_list:
        subsection = SubsectionData(**d)
        subsection_data_list.append(subsection)

    data = DataItem(metadata, section_data_list, subsection_data_list)
    output_filepath = BASE_DIR / f"{uuid}.docx"
    DocumentGenerator(TEMPLATE, output_filepath, data).go()
    return output_filepath


def generate_document(request):
    data = request.get_json()
    user, uuid = get_user(data["user"]), data["uuid"]

    doc_path = create_document(data["dataItem"], uuid)

    # # upload document to the bucket
    bucket = storage.bucket()
    blob = bucket.blob(f"documents/{user}/{uuid}.docx")
    blob.upload_from_filename(doc_path)
    os.remove(doc_path)

    # Test user hYJ1MIa9datBz8YPtwq5

    if "devices" in user:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title='Document created',
                body='Document is ready.',
            ),
            data={'docx_uuid': uuid},
            tokens=user["devices"],
        )
        messaging.send_multicast(message)
    return json.dumps(user)


if __name__ == "__main__":
    class JsonData:
        def __init__(self, data):
            self.data = data

        def get_json(self):
            return self.data

    with open("test_data.json", "r") as json_data_test:
        data = json.load(json_data_test)
        request = JsonData(data)
        resp = generate_document(request)
        print(resp)
