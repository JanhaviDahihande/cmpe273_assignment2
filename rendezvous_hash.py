from flask import Flask
from flask_restful import Api
import csv
import sys
import hashlib
import requests

app = Flask(__name__)
api = Api(app)


class Rendezvous:
    def __init__(self, csv_file=sys.argv[1]):
        self.csv_file = csv_file
        self.nodes = ["5000", "5001", "5002", "5003"]

    def get_csv_data(self):
        with open(self.csv_file) as csvDataFile:
            count = 0
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                if count != 0:
                    self.get_curl_cmd(row)
                count = count + 1
            print("Uploaded all " + str(count-1) + " entries.")
            print("Verifying the data.")

    def convert_row_data(self, row):
        rowdata = ""
        if (len(row) == 5):
            rowdata = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4]
        elif (len(row) == 4):
            rowdata = row[0] + "," + row[1] + "," + row[2] + "," + row[3]
        else:
            rowdata = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5]

        return rowdata

    def get_curl_cmd(self, row):
        list_items = self.get_hash_value(row)
        sorted_list = sorted(list_items.values(), reverse=True)

        data = '{"' + sorted_list[0] + '":"' + self.convert_row_data(row) + '"}'

        headers = {
            'Content-type': 'application/json',
        }
        url = 'http://localhost:5000/api/v1/entries'
        for k, v in list_items.items():
            if v == sorted_list[0]:
                url = 'http://localhost:' + k + '/api/v1/entries'
                break

        response = requests.post(url, headers=headers, data=data)

    def get_hash_value(self, row):
        dictofvalues = {}
        key = row[0]+":"+row[2]+":"+row[3]
        for node in self.nodes:
            final_key = key + "," + node
            hashid = hashlib.sha512(final_key.encode())
            dictofvalues.update({node: hashid.hexdigest()})
        return dictofvalues

    def get_data(self):
        nodes = ["5000", "5001", "5002", "5003"]
        for node in nodes:
            url = 'http://localhost:' + node + '/api/v1/entries'
            print("\nGET http://localhost:" + node)
            r = requests.get(url=url)
            print(str(r.text))


def rendev_hash():
    rendezvous_hash = Rendezvous('causes-of-death.csv')
    rendezvous_hash.get_csv_data()
    rendezvous_hash.get_data()


if __name__ == '__main__':
    rendev_hash()

