import pandas as pd
import csv
import re
import sqlite3
import json
from lxml import etree
import math

class InputFile():
    def __init__(self, input):
        self.input = input
        self.input_csv = self.input[0] + '[CHECKED].csv'
        self.stripped = self.input[0].rstrip("[CHECKED]")
        self.mistakes_counter = 0
        self.header = None

    def if_csv(self):
        if self.input[1] == 'xlsx':
            self.my_xlsx = pd.read_excel(rf'{".".join(self.input)}', sheet_name='Vehicles', dtype=str)
            self.my_xlsx.to_csv(self.input[0] + '.csv', index=None)
            return open(self.input[0]+'.csv', 'r')
        elif self.input[1] == "s3db":
            return self.input[0]+'.s3db'
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
                   '{} cells were corrected in {}'.format(self.mistakes_counter, input_file_xlsx_csv.input_csv, ), sep='\n')
        elif self.mistakes_counter == 0:
            return False
        else:
            print ('{} cells were corrected in {}'.format(self.mistakes_counter, input_file_xlsx_csv.input_csv))

    def writing_rows(self, file_reader):
        row = 0
        with open(input_file_xlsx_csv.input_csv, "w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
            for line in file_reader:
                if row == 0:
                    row += 1
                    self.header = line
                    continue
                else:
                    for index, el in enumerate(line):
                        result = re.search(r'\d+', el)
                        if result is not None:
                            if result.group() != el:
                                line[index] = int(result.group())
                                input_file_xlsx_csv.mistakes_counter += 1
                file_writer.writerow(line)

class DataBase():
    def __init__(self, headers):
        self.input_file_db = input_file_xlsx_csv.stripped + '.s3db'
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
                {} INTEGER NOT NULL,
                {} INTEGER NOT NULL,
                {} INTEGER NOT NULL)
            """.format(self.header[0], self.header[1], self.header[2], self.header[3]))
        conn.commit()
        cur.close()

    def data_to_db(self):
        conn, cur = self.connection()
        table_info = conn.execute("pragma table_info('convoy')").fetchall()
        if len(table_info) == 4:
            cur.execute("""ALTER TABLE convoy
                            ADD COLUMN {} INTEGER NOT NULL""".format("score"))
        else:
            pass
        insert_stm = f"INSERT OR IGNORE INTO convoy {tuple(self.header+['score'])} VALUES (?, ?, ?, ?, ?)"
        with open(input_file_xlsx_csv.input_csv) as w_file:
            file_read = csv.reader(w_file, delimiter=",")
            for row in file_read:
                self.vehicle_score = 0
                self.record_counters += 1
                pitstop = math.floor(450 / ((int(row[1]) / (int(row[2])) * 100)))
                # print('pitsop', pitstop)
                fuel_consumed = ((int(row[2]) / 100) * 450)
                # print("fuel_consumed", fuel_consumed )
                truck_capacity = int(row[3])
                # print('truck_capacity', truck_capacity)
                if pitstop >= 2:
                    self.vehicle_score += 0
                if pitstop == 1:
                    self.vehicle_score += 1
                if pitstop == 0:
                    self.vehicle_score += 2
                if truck_capacity >= 20:
                    self.vehicle_score += 2
                if truck_capacity < 20:
                    self.vehicle_score += 0
                if fuel_consumed < 230:
                    self.vehicle_score += 2
                if fuel_consumed >= 230:
                    self.vehicle_score += 1
                data_with_score = row + [f'{self.vehicle_score}']
                cur.execute(insert_stm, tuple(data_with_score))
        conn.commit()
        cur.close()

    def if_plural(self):
        if self.record_counters == 1:
            return ' was'
        else:
            return 's were'

    def print_db_status(self):
        print("{} record{} inserted into {}".format(self.record_counters, self.if_plural(), self.input_file_db))

class ToJson():
    def __init__(self, db_name):
        self.db_name = db_name
        self.json_name = input_file_xlsx_csv.stripped + ".json"
        self.json_list = []
        self.json_dict = {}

    def connection(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        return conn, cur

    def records_to_json(self):
        conn, cur = self.connection()
        select_all = "SELECT * from convoy"
        cur.execute(select_all)
        col_name_list = [tuple[0] for tuple in cur.description]
        select_stm = f"SELECT {col_name_list[0]}, {col_name_list[1]}, {col_name_list[2]}, {col_name_list[3]}, {col_name_list[4]} FROM convoy"
        cur.execute(select_stm)
        all = cur.fetchall()
        for el in all:
            if el[4] > 3:
                dict = {}
                for x in zip(col_name_list, el):
                    dict[x[0]] = x[1]
                dict.pop('score')
                self.json_list.append(dict)
        self.json_dict['convoy'] = self.json_list
        conn.commit()
        cur.close()

    def json_dumps(self):
        with open(f"{self.json_name}", "w") as json_file:
            json.dump(self.json_dict, json_file)

    def if_plural(self):
        if len(self.json_list) == 1:
            return ' was'
        else:
            return 's were'

    def print_json_status(self):
        print("{} vehicle{} saved into {}".format(len(self.json_list), self.if_plural(), self.json_name))

class ToXML:
    def __init__(self, db_name):
        self.db_name = db_name
        self.xml_file = input_file_xlsx_csv.stripped + ".xml"
        self.xml_string = ""
        self.vehicle_counter = 0

    def connection(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        return conn, cur

    def records_to_XML(self):
        conn, cur = self.connection()
        select_all = "SELECT * from convoy"
        cur.execute(select_all)
        col_name_list = [tuple[0] for tuple in cur.description]
        select_stm = f"SELECT {col_name_list[0]}, {col_name_list[1]}, {col_name_list[2]}, {col_name_list[3]}, {col_name_list[4]} FROM convoy"
        cur.execute(select_stm)
        all = cur.fetchall()
        self.xml_string += '<convoy>'
        for el in all:
            self.xml_string += " "
            if el[4] <= 3:
                self.xml_string += '<vehicle>'
                self.vehicle_counter += 1
                for x in zip(col_name_list, el[0:4]):
                    self.xml_string += f"<{x[0]}>{x[1]}</{x[0]}>"
                self.xml_string += '</vehicle>'
        self.xml_string += '</convoy>'
        conn.commit()
        cur.close()

    def xml_string_2_xml_file(self):
        root = etree.fromstring(self.xml_string)
        tree = etree.ElementTree(root)
        tree.write(self.xml_file)

    def if_plural(self):
        if self.vehicle_counter == 1:
            return ' was'
        else:
            return 's were'

    def print_xml_status(self):
        print("{} vehicle{} saved into {}".format(self. vehicle_counter, self.if_plural(), self.xml_file))

def main(input_file_xlsx_csv):
    my_csv = input_file_xlsx_csv.if_csv()
    file_reader = csv.reader(my_csv, delimiter=',')

    input_file_xlsx_csv.writing_rows(file_reader)

    csv_to_db = DataBase(input_file_xlsx_csv.header)
    csv_to_db.create_table()
    csv_to_db.data_to_db()

    db_to_json = ToJson(csv_to_db.input_file_db)
    db_to_json.records_to_json()
    db_to_json.json_dumps()

    json_to_XML = ToXML(input_file_xlsx_csv.stripped+'.s3db')
    json_to_XML.records_to_XML()
    json_to_XML.xml_string_2_xml_file()

    input_file_xlsx_csv.print_result()
    csv_to_db.print_db_status()
    db_to_json.print_json_status()
    json_to_XML.print_xml_status()
    my_csv.close()

def main_db_only(input_file_db):
    db_to_json = ToJson(input_file_db+'.s3db')
    db_to_json.records_to_json()
    db_to_json.json_dumps()
    db_to_json.print_json_status()
    json_to_XML = ToXML(input_file_db+'.s3db')
    json_to_XML.records_to_XML()
    json_to_XML.xml_string_2_xml_file()
    json_to_XML.print_xml_status()

input_file_xlsx_csv = InputFile(input('Input file name\n').split('.'))
if 's3db' not in input_file_xlsx_csv.input[1]:
    main(input_file_xlsx_csv)
else:
    main_db_only(input_file_xlsx_csv.input[0])
