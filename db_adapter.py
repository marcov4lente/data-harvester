import sqlite3

class DBAdapter:


    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()


    def __generate_field_str(self, fields):
        field_str = ''
        field_count = len(fields)
        i = 1

        for field in fields:
            field_str += field
            if(i < field_count):
                field_str += ', '
            i = i + 1

        return field_str


    def __generate_placeholder_str(self, fields):
        placeholder_str = ''
        field_count = len(fields)
        i = 1

        for field in fields:
            placeholder_str += ' ? '
            if(i < field_count):
                placeholder_str += ', '
            i = i + 1

        return placeholder_str


    def create_table_if_not_exists(self, table_name, fields):
        query = 'CREATE TABLE IF NOT EXISTS '+table_name+' ( '
        query += self.__generate_field_list(fields)
        query += ' ) '
        self.cursor.execute(query)
        self.connection.commit()


    def insert(self, table_name, data):
        field_count = len(data)

        query = ' INSERT INTO '+table_name+' ( '
        query += self.__generate_field_list(data.keys())
        query += ' ) VALUES ( '
        query += self.__generate_placeholder_list(data)
        query += ' ) '

        params = list(data.values())

        self.cursor.execute(query, params)
        self.connection.commit()
