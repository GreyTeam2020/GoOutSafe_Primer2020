from .table import Table


class Restaurant:

    def __init__(self, filename):
        self.tables = []
        self.name = None
        self.lat = None
        self.lon = None
        self.like = 0

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        self.name = lines[0].strip()
        self.lat = lines[1].strip()
        self.lon = lines[2].strip()

        for line in lines[3:]:
            table_name, table_capacity = line.split()
            self.tables.append(Table(table_name, int(table_capacity)))
