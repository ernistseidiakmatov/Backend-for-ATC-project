import json, jwt 
from datetime import datetime, timedelta
import mysql.connector

secret_key = "ZMK5HD1f2J3ckoUt"

cloud_connection = mysql.connector.connect(
    host='bi8jjzjpekfiufabfp4u-mysql.services.clever-cloud.com',
    user='u9vwvlgpxselludx',
    password='SWbvsgDGx7C2PhEGMOS4',
    database='bi8jjzjpekfiufabfp4u'
    )

def get_dispatch_details(dispatch_no):

  conn = cloud_connection.cursor()

  # Query dispatch table
  query = "SELECT * FROM dispatch WHERE dispatch_no = %s"
  conn.execute(query, (dispatch_no,))
  dispatch = conn.fetchone()

  if not dispatch:
    return {"message": "Dispatch not found"}, 404

  # Fetch details from other tables
  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[3],)) 
  dispatch_mgr = conn.fetchone()[0]

  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[4],))
  approval_mgr = conn.fetchone()[0]

  conn.execute("SELECT area_name FROM area WHERE area_id = %s", (dispatch[5],))
  area = conn.fetchone()[0]

  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[7],))
  driver = conn.fetchone()[0]

  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[8],))
  crew1 = conn.fetchone()[0]

  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[9],))
  crew2 = conn.fetchone()[0]

  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[10],))
  alt_driver = conn.fetchone()[0]

  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[11],))
  alt_crew1 = conn.fetchone()[0]

  conn.execute("SELECT name FROM staff WHERE staff_id = %s", (dispatch[12],))
  alt_crew2 = conn.fetchone()[0]

  token = jwt.encode({"dispatch_no": dispatch_no, "expiration": str(datetime.now() + timedelta(seconds=43200))},
                       secret_key)
  
  response = {
    "token": token,
    "dispatch_no": dispatch[2],
    "dispatch_mgr": dispatch_mgr, 
    "approval_mgr": approval_mgr,
    "area": area,
    "vehicle": dispatch[6],
    "driver": driver,
    "crew1": crew1,
    "crew2": crew2,
    "alt_driver": alt_driver,
    "alt_crew1": alt_crew1,
    "alt_crew2": alt_crew2,
    # other details
  }

  return json.dumps(response, indent=2, ensure_ascii=False)