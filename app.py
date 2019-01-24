from concurrent import futures
import os
import time
import random

import grpc
from google.protobuf import empty_pb2

# import your gRPC bindings here:
from protos import contacts_pb2
from protos import contacts_pb2_grpc

from db import *


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
DB_PATH = "app.sqlite"
CONN = None

class ContactServicer(contacts_pb2_grpc.ContactServiceServicer):

    def GetByID(self, request, context):
        contact = select_contact_by_id(CONN, request.id)
        if contact:
            return contacts_pb2.Contact(
                id=str(contact[0]),
                firstname=str(contact[1]),
                lastname=str(contact[2]),
                perfname= str(contact[3]),
                email= str(contact[4]),
                phone= str(contact[5]),
                date_updated= str(contact[6]),
                date_created= str(contact[7]),
                author= str(contact[8])
            )
        context.set_code(grpc.StatusCode.NOT_FOUND)

    def List(self, request, context):
        contacts = select_all_contacts(CONN)

        serialized_contacts = []
        for contact in contacts:
            serialized_contacts.append(
                contacts_pb2.Contact(
                    id=str(contact[0]),
                    firstname=str(contact[1]),
                    lastname=str(contact[2]),
                    perfname= str(contact[3]),
                    email= str(contact[4]),
                    phone= str(contact[5]),
                    date_updated= str(contact[6]),
                    date_created= str(contact[7]),
                    author= str(contact[8])
                )
            )

        print("List Action")

        return contacts_pb2.ListContactsResponse(
            contacts=serialized_contacts
        )

    def Create(self, request, context):
        contact_id = create_contact(
            CONN,
            request.firstname,
            request.lastname,
            request.perfname,
            request.email,
            request.phone,
            request.author
        )

        print("Contact Created: {}".format(contact_id))

        return contacts_pb2.Contact(
            id=str(contact_id),
            firstname=str(request.firstname),
            lastname=str(request.lastname),
            perfname= str(request.perfname),
            email= str(request.email),
            phone= str(request.phone),
            date_updated= "",
            date_created= "",
            author= str(request.author)
        )

    def Update(self, request, context):
        # Check to see if they already exist:
        if not select_contact_by_id(CONN, request.id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return

        update_contact(
            CONN,
            request.id,
            request.firstname,
            request.lastname,
            request.perfname,
            request.email,
            request.phone,
            request.author
        )

        contact = select_contact_by_id(CONN, request.id)

        print("Contact Updated: {}".format(request.id))
        return contacts_pb2.Contact(
            id=str(contact[0]),
            firstname=str(contact[1]),
            lastname=str(contact[2]),
            perfname= str(contact[3]),
            email= str(contact[4]),
            phone= str(contact[5]),
            date_updated= str(contact[6]),
            date_created= str(contact[7]),
            author= str(contact[8])
        )

    def Delete(self, request, context):
        if not select_contact_by_id(CONN, request.id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return

        delete_contact(CONN, request.id)

        print("Deleted contact {}".format(request.id))
        return empty_pb2.Empty()


def serve():
    print("Starting server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    contacts_pb2_grpc.add_ContactServiceServicer_to_server(ContactServicer(), server)
    server.add_insecure_port('[::]:22222')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def setUpDB():
    CONN = create_connection(DB_PATH)
    create_tables_if_not_exist(CONN)
    contact = select_contact_by_id(CONN, 1)
    if not contact:
        contact_id = create_contact(
            CONN,
            "Michael",
            "Scott",
            "Michael",
            "m.scott@dundermifflin.com",
            "321-555-2122",
            "1"
        )
        print("Contact ID: {}".format(contact_id))


if __name__ == '__main__':
    # setup database.
    setUpDB()

    # Start gRPC server.
    serve()
