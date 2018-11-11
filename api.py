from flask import Flask, request, Response
from flask_restful import Api
import sys

app = Flask(__name__)
api = Api(app)


list_values = {}
my_list = []


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_parser():
    args = request.get_json()
    # print("Args: " + str(args))
    for k, v in args.items():
        my_list.append({k: v})
    return my_list


@app.route('/api/v1/entries', methods=['POST'])
def put_item():
    args = get_parser()
    list_values.update({'num_entries': len(args), 'entries': args})
    return Response(status=201)


@app.route('/api/v1/entries', methods=['GET'])
def return_item():
    return Response(response="{0}".format(list_values), status=200)


if __name__ == '__main__':
    app.run(port=sys.argv[1], debug=True)