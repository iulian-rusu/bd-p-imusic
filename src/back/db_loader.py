from src.back.db_connection import DBConnection


class DBLoader:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def load_table(self, target, query: str):
        # Loads the main content table for a TableView object
        target.delete(*target.get_children())
        cursor = self.db_connection.fetch_data(query)
        if cursor:
            for row in cursor:
                target.insert('', 'end', values=row)
            self.db_connection.close_cursor()

    def load_combobox(self, target, query: str):
        # Loads the genre select combobox for a SongView object
        cursor = self.db_connection.fetch_data(query)
        if cursor:
            for row in cursor:
                target.genres[row[1]] = int(row[0])
            self.db_connection.close_cursor()
            target.genre_select_cmbx.config(values=list(target.genres.keys()))

    def load_spinbox(self, target, query: str):
        # Loads any spinbox with values fetched from the database
        cursor = self.db_connection.fetch_data(query)
        if cursor:
            spinbox_vals = ''
            for row in cursor:
                spinbox_vals += f'{row[0]} '
            self.db_connection.close_cursor()
            target.config(values=spinbox_vals)
