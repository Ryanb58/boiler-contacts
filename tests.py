import os
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from protos import contacts_pb2
import app
from db import *
class TestContacts(unittest.TestCase):

    def setUp(self):

        # Remove the old db.
        if app.CONN:
            app.CONN.close()

        if os.path.exists(app.DB_PATH):
            os.remove(app.DB_PATH)

        # setup the database again.
        self.conn = create_connection(app.DB_PATH)
        create_tables_if_not_exist(self.conn)
        self.contact_id = create_contact(
            self.conn,
            "Michael",
            "Scott",
            "Michael",
            "m.scott@dundermifflin.com",
            "321-555-2122",
            "1"
        )

        self.service = app.ContactServicer()

    def test_list_contacts(self):
        app.CONN = self.conn

        request = MagicMock()
        context = MagicMock()

        resp = self.service.List(request, context)

        self.assertEqual(len(resp.contacts), 1)

    def test_add_contact(self):
        app.CONN = self.conn

        request = MagicMock()
        request.firstname = "Andy"
        request.lastname = "Dwyer"
        request.perfname = "Burt Macklin, FBI"
        request.email = "andy.dwyer@fbi.com"
        request.phone = "123-555-1234"
        request.author = "1"
        context = MagicMock()

        resp = self.service.Create(request, context)

        self.assertEqual(resp.firstname, request.firstname)
        self.assertEqual(resp.lastname, request.lastname)
        self.assertEqual(resp.perfname, request.perfname)
        self.assertEqual(resp.email, request.email)
        self.assertEqual(resp.phone, request.phone)
        self.assertEqual(resp.author, request.author)


    def test_update_contact(self):
        app.CONN = self.conn

        request = MagicMock()
        request.id = "1"
        request.firstname = "Andy"
        request.lastname = "Dwyer"
        request.perfname = "Burt Macklin, FBI"
        request.email = "andy.dwyer@fbi.com"
        request.phone = "123-555-1234"
        request.author = "1"
        context = MagicMock()

        resp = self.service.Update(request, context)

        self.assertEqual(resp.firstname, request.firstname)
        self.assertEqual(resp.lastname, request.lastname)
        self.assertEqual(resp.perfname, request.perfname)
        self.assertEqual(resp.email, request.email)
        self.assertEqual(resp.phone, request.phone)
        self.assertEqual(resp.author, request.author)

    def test_delete_a_contact(self):
        app.CONN = self.conn

        request = MagicMock()
        request.id = 1
        context = MagicMock()

        self.service.Delete(request, context)

        request = MagicMock()
        context = MagicMock()
        resp = self.service.List(request, context)
        self.assertEqual(len(resp.contacts), 0)


if __name__ == '__main__':
    unittest.main()
