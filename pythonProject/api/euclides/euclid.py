
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from database.connection_db import Connection
from flask_cors import CORS
from json import loads

app = Flask(__name__)
CORS(app)

parser = reqparse.RequestParser()

def gcd(n1, n2):
    if (n1 == 0):
        return n2
    else:
        return gcd(n2 % n1, n1)

@app.route("/euclid/", methods = ['POST'])
def post():
    data = request.json
    print(data)
    inteligence_types = []
    results = {}
    [inteligence_types.append(i['inteligence_type']) for i in data if i['inteligence_type'] not in inteligence_types]
    for x in inteligence_types:
        questions = [q['value'] for q in data if q['inteligence_type'] == x]
        print(x)
        print(questions)
        greatest_common_divisor = gcd(int(questions[0]), gcd(int(questions[1]), int(questions[2])))
        results.update({x: greatest_common_divisor})
    print(results)
    max_value = max(results, key=results.get)
    print("Maximum value = ", max_value)
    return jsonify(max_value), 201

@app.route("/users/", methods = ['GET'])
def get_users():
    conn = Connection()
    df = conn.get_users()
    res = df.to_json(orient="records")
    parsed = loads(res)
    return parsed, 200

@app.route("/users/inteligence/", methods = ['GET'])
def get_users_by_inteligence():
    args = request.args
    conn = Connection()
    df = conn.get_users_by_inteligence(args.get("inteligence"))
    res = df.to_json(orient="records")
    parsed = loads(res)
    return parsed, 200

@app.route("/users/", methods = ['POST'])
def add_user():
    data = request.json
    conn = Connection()
    conn.add_user(data['username'], data['inteligence'], data['pass'])
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(debug=True)