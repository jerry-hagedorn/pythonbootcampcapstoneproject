

class Lot:

    _subdivision_name: str
    _lot_num: str
    _records: list


    def __init__(self, subdivision_name, lot_num):

        self._subdivision_name = subdivision_name
        self._lot_num = lot_num
        self._records = []


    def add_records(self, records: list):
        self._records.extend(records)


    @property
    def get_records(self):
        return self._records

    @property
    def get_subdivision_name(self):
        return self._subdivision_name

    @property
    def get_lot_num(self):
        return self._lot_num

