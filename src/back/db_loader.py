from src.back.db_connetcion import DBConnection


class DBLoader:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def load_table(self, target, query: str):
        target.delete(*target.get_children())
        cursor = self.db_connection.fetch_data(query)
        if cursor:
            for row in cursor:
                target.insert('', 'end', values=row)
            self.db_connection.close_cursor()

    def load_combobox(self, target, query: str):
        cursor = self.db_connection.fetch_data(query)
        if cursor:
            for row in cursor:
                target.genres[row[1]] = int(row[0])
            self.db_connection.close_cursor()
            target.genre_select_cmbx.config(values=list(target.genres.keys()))
