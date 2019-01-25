import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("SQL Error:")
        print(e)


def create_tables_if_not_exist(conn):
    sql_contacts_table = '''
CREATE TABLE IF NOT EXISTS contacts (
    id integer PRIMARY KEY,
    firstname text,
    lastname text,
    perfname text,
    email text,
    phone text,
    date_updated text,
    date_created text,
    author text
)'''
    if conn is not None:
        # create contacts table
        create_table(conn, sql_contacts_table)
    else:
        print("Error! cannot create the database connection.")


# CONTACT FUNCTIONS:

def select_all_contacts(conn):
    """
    Query all rows in the contacts table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")

    rows = cur.fetchall()

    for row in rows:
        yield row


def select_contact_by_id(conn, id):
    """
    Query contacts by id
    :param conn: the Connection object
    :param id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE id=?", (id,))

    return cur.fetchone()


def create_contact(conn, firstname, lastname, perfname, email, phone, author):
    """
    Create a new contact.
    :param conn:
    :param contact:
    :return: contact id
    """
    sql = ''' INSERT INTO contacts(firstname, lastname, perfname, email, phone, date_created, author)
              VALUES(?,?,?,?,?,datetime('now'),?) '''
    cur = conn.cursor()
    cur.execute(sql, [firstname, lastname, perfname, email, phone, author])
    conn.commit()
    return cur.lastrowid


def update_contact(conn, id, firstname, lastname, perfname, email, phone, author):
    """
    update a contacts
    :param conn:
    :param contact:
    :return: contact id
    """
    sql = ''' UPDATE contacts
              SET firstname = ? ,
                  lastname = ? ,
                  perfname = ? ,
                  email = ? ,
                  phone = ? ,
                  author = ? ,
                  date_updated = datetime('now')
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, [firstname, lastname, perfname, email, phone, author, id])
    conn.commit()


def delete_contact(conn, id):
    """
    Delete a specific contacts
    :param conn: the Connection object
    :param id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
