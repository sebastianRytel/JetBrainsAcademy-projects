import pandas as pd
import csv
import re
import sqlite3

class InputFile():
    def __init__(self, input):
        self.input = input
        self.input_csv = self.input[0] + '[CHECKED].csv'
        self.counter = 0

    def if_csv(self):
        if self.input[1] == 'xlsx':
            self.my_xlsx = pd.read_excel(rf'{".".join(self.input)}', sheet_name='Vehicles', dtype=str)
            self.my_xlsx.to_csv(self.input[0] + '.csv', index=None)
            return open(self.input[0]+'.csv', 'r')
        else:
            return open(self.input[0]+'.csv', 'r')

    def single_multi(self):
        if self.my_xlsx.shape[0] == 1:
            return ' was'
        else:
            return 's were'

    def print_result(self):
        if self.input[1] == 'xlsx':
            print ('{} line{} added to {}'.format(self.my_xlsx.shape[0], self.single_multi(), self.input[0] + '.csv'),
                   '{} cells were corrected in {}'.format(self.counter, input_file_xlsx_csv.input_csv, ), sep='\n')
        else:
            print ('{} cells were corrected in {}'.format(self.counter, input_file_xlsx_csv.input_csv))

    @staticmethod
    def writing_rows(file_reader):
        row = 0
        with open(input_file_xlsx_csv.input_csv, "w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
            for line in file_reader:
                if row == 0:
                    row += 1
                    continue
                else:
                    for index, el in enumerate(line):
                        result = re.search(r'\d+', el)
                        if result is not None:
                            if result.group() != el:
                                line[index] = int(result.group())
                                input_file_xlsx_csv.counter += 1
                file_writer.writerow(line)

    @staticmethod
    def read_header(file_reader):
        for row in file_reader:
            return row

class DataBase():
    def __init__(self, headers):
        self.input_file_db = input_file_xlsx_csv.input[0] + '.s3db'
        self.header = headers
        self.record_counters = 0

    def connection(self):
        conn = sqlite3.connect(self.input_file_db)
        cur = conn.cursor()
        return conn, cur

    def create_table(self):
        conn, cur = self.connection()
        cur.execute("""CREATE TABLE IF NOT EXISTS convoy (
                {} INTEGER NOT NULL PRIMARY KEY,
                {} INTEGER,
                {} INTEGER,
                {} INTEGER)
            """.format(self.header[0], self.header[1], self.header[2], self.header[3]))
        conn.commit()
        cur.close()

    def data_to_db(self):
        conn, cur = self.connection()
        insert_stm = f"INSERT OR IGNORE INTO convoy {tuple(self.header)} VALUES (?, ?, ?, ?)"
        with open(input_file_xlsx_csv.input_csv) as w_file:
            file_read = csv.reader(w_file, delimiter=",")
            for row in file_read:
                self.record_counters += 1
                cur.execute(insert_stm, tuple(row))
        conn.commit()
        cur.close()

    def print_db_status(self):
        print("{} records were inserted into {}".format(self.record_counters, self.input_file_db))

input_file_xlsx_csv = InputFile(input('Input file name\n').split('.'))
my_csv = input_file_xlsx_csv.if_csv()
file_reader = csv.reader(my_csv, delimiter=',')
headers = input_file_xlsx_csv.read_header(file_reader)

input_file_xlsx_csv.writing_rows(file_reader)
input_file_xlsx_csv.print_result()

csv_to_db = DataBase(headers)
csv_to_db.create_table()
csv_to_db.data_to_db()
csv_to_db.print_db_status()
my_csv.close()
