import shelve

class DBService:

    @staticmethod
    def insert_data(key: str, obj: object, path: str):
        with shelve.open(path) as db:
            db[key] = obj
            db.sync()

    @staticmethod
    def select_data(key: str, path: str) -> object:
        with shelve.open(path) as db:
            return db[key]

    @staticmethod
    def multi_select_data(keys: list, path: str) -> dict:
        result_data = {}
        with shelve.open(path) as db:
            for key in keys:
                if key in db:
                    result_data[key] = db[key]
        return result_data

    @staticmethod
    def export_all_data(path: str) -> dict:
        all_data = {}
        with shelve.open(path) as db:
            for key in db:
                all_data[key] = db[key]
        return all_data
