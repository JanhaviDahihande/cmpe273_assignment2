from flask import Flask
from flask_restful import Api
import csv
import sys
import hashlib
import requests

app = Flask(__name__)
api = Api(app)


class Consistent:
    def __init__(self, csv_file=sys.argv[1]):
        self.csv_file = csv_file
        server1 = hashlib.sha512("5000".encode())
        self.server1_hash = server1.hexdigest()

        server2 = hashlib.sha512("5001".encode())
        self.server2_hash = server2.hexdigest()

        server3 = hashlib.sha512("5002".encode())
        self.server3_hash = server3.hexdigest()

        server4 = hashlib.sha512("5003".encode())
        self.server4_hash = server4.hexdigest()

        self.server = [self.server1_hash, self.server2_hash, self.server3_hash, self.server4_hash]
        self.server.sort()

    def load_csv_data(self):
        with open(self.csv_file) as csvDataFile:
            count = 0
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                if count != 0:
                    self.get_curl_cmd(row)
                count = count + 1
            print("Uploaded all " + str(count-1) + " entries.")
            print("Verifying the data.")

    def convert_row_data(self,row):
        rowdata = ""
        if (len(row) == 5):
            rowdata = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4]
        elif (len(row) == 4):
            rowdata = row[0] + "," + row[1] + "," + row[2] + "," + row[3]
        else:
            rowdata = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5]

        return rowdata

    def get_curl_cmd(self, row):
        value = row[0] + ":" + row[2] + ":" + row[3]
        hash_val = hashlib.sha512(value.encode()).hexdigest()

        data = '{"' + hash_val + '":"' + self.convert_row_data(row) + '"}'

        headers = {
            'Content-type': 'application/json',
        }

        url = 'http://localhost:5000/api/v1/entries'

        if self.server[3] < hash_val <= self.server[0]:
            url = 'http://localhost:5000/api/v1/entries'
        elif self.server[0] < hash_val <= self.server[1]:
            url = 'http://localhost:5001/api/v1/entries'
        elif self.server[1] < hash_val <= self.server[2]:
            url = 'http://localhost:5002/api/v1/entries'
        elif self.server[2] < hash_val <= self.server[3]:
            url = 'http://localhost:5003/api/v1/entries'

        response = requests.post(url, headers=headers, data=data)

    def get_data(self):
        nodes = ["5000", "5001", "5002", "5003"]
        for node in nodes:
            url = 'http://localhost:' + node + '/api/v1/entries'
            print("\nGET http://localhost:" + node)
            r = requests.get(url=url)
            print(str(r.text))


def consiste_hash():
    consistent_hash = Consistent('causes-of-death.csv')
    consistent_hash.load_csv_data()
    consistent_hash.get_data()


if __name__ == '__main__':
    consiste_hash()

