from flask import Flask, request, jsonify, make_response, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
import mysql.connector
import trashdata, log_in
import sqlite3
import json
import subprocess



app = Flask(__name__)
app.config["SECRET_KEY"] = "ZMK5HD1f2J3ckoUt"

app.config['MYSQL_HOST'] = 'bi8jjzjpekfiufabfp4u-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'u9vwvlgpxselludx'
app.config['MYSQL_PASSWORD'] = 'SWbvsgDGx7C2PhEGMOS4'
app.config['MYSQL_DB'] = 'bi8jjzjpekfiufabfp4u'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


cloud_connection = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)


cursor = cloud_connection.cursor()


trashdata.check()


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"Alert": "Token is missing!"}), 401

        try:
            token = token.split(' ')[1]
            payload = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"])

            exp = payload['expiration']

            if datetime.now() > datetime.strptime(exp, '%Y-%m-%d %H:%M:%S.%f'):
                raise jwt.ExpiredSignatureError("Token has expired")

            query = ("SELECT * FROM dispatch WHERE dispatch_no = %s")

            cursor.execute(query, (payload['dispatch_no'],))

            current_dispatch = cursor.fetchone()

        except jwt.ExpiredSignatureError:
            return jsonify({"Alert": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"Alert": "Invalid Token!"}), 401

        # Continue with the decorated function
        return func(*args, **kwargs, current_dispatch=current_dispatch)

    return decorated


@app.route('/login', methods=["POST"])
def login():

    data = request.get_json()

    dispatch_no = data.get("dispatch_no")

    query = ("SELECT * FROM dispatch WHERE dispatch_no = %s")

    cursor.execute(query, (dispatch_no,))

    dispatch = cursor.fetchone()

    res = log_in.get_dispatch_details(dispatch_no)

    return res


@app.route('/collection', methods=["POST", "GET"])
@token_required
def collection(current_dispatch):
    current_dispatch = current_dispatch
     
    if request.method == "GET":
        try:
            # return jsonify(trashdata.retrieve_collections())
            return json.dumps(trashdata.retrieve_collections(), indent=2), 200
        except Exception as e:
            return jsonify({'message': e}), 500
        

@app.route('/yolo-output', methods=['POST'])
@token_required
def yolo_output(current_dispatch):
    
    try:
        data = request.get_json()

        time = data.get("time")
        dispatch_no = current_dispatch[2]
        x1 = data.get("x1")
        y1 = data.get("y1")
        x2 = data.get("x2")
        y2 = data.get("y2")
        class_name = data.get("class_name")
        score = data.get("score")
        w = data.get("w")
        h = data.get("h")
        weight = data.get("weight")

        
        trashdata.insert_yolo_output_data(time, dispatch_no, x1, y1, x2, y2, class_name, score, w, h, weight)
        
        trashdata.dynamicc(class_name, weight, dispatch_no)

        return jsonify({"message": "Saved Successfully"}), 200
    
    except Exception as e:
        return jsonify({"message": e}), 500
    

@app.route('/start-model', methods=["POST"])
def start_model():
    file_path = 'sub.py'
    dispatch_no = 202019042
    try:
        result = subprocess.run(['python', file_path], input=str(dispatch_no), capture_output=True, text=True)
        output = result.stdout.strip()
        return jsonify({"output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(debug=True)
