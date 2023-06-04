import sqlite3


class DuplicateContactException(Exception):
    pass


class InvalidContactException(Exception):
    pass


def create_contacts_table():
    connection = sqlite3.connect('contacts.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                phone_number TEXT
            )
    ''')
    connection.commit()
    connection.close()


class ContactService:
    @staticmethod
    def is_contact_exists(user_id, name):
        connection = sqlite3.connect('contacts.db')
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM contacts WHERE user_id = ? AND LOWER(name) = LOWER(?)",
                       (user_id, name.lower()))
        count = cursor.fetchone()[0]
        connection.close()
        return count > 0

    @staticmethod
    def add_contact(user_id, name, phone_number):
        if ContactService.is_contact_exists(user_id, name):
            raise DuplicateContactException(f'Contact with name {name} already exists in your contacts book')

        connection = sqlite3.connect('contacts.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO contacts (user_id, name, phone_number) VALUES (?, LOWER(?), ?)',
                       (user_id, name, phone_number))
        connection.commit()
        connection.close()

    @staticmethod
    def get_contacts(user_id):
        connection = sqlite3.connect('contacts.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id, UPPER(substring(name, 1, 1)) || LOWER(substring(name, 2)) AS name,'
                       ' phone_number FROM contacts WHERE user_id = ?', (user_id,))
        contacts = cursor.fetchall()
        connection.close()
        return contacts

    @staticmethod
    def delete_contact(user_id, name):
        if not ContactService.is_contact_exists(user_id, name):
            raise InvalidContactException(f"No contact with name {name} in contacts book")
        ContactService.is_contact_exists(user_id, name)
        connection = sqlite3.connect('contacts.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM contacts WHERE user_id = ? AND LOWER(name) = LOWER(?)', (user_id, name))
        connection.commit()
        connection.close()

