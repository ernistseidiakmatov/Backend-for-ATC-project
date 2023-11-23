# test-capstone

log-in POST request /login
{
  "dispatch_no": "20231030001"
}

log-in Response 
{
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
  
}


collection GET request /collection
{
    "bag_5L": 0,
    "bag_10L": 0,
    "bag_20L": 0,
    "bag_30L": 0,
    "bag_50L": 0,
    "bag_75L": 0,
    "bag_etc": 0,
    "others": 0,
    "weight": 0,
    "volume": 9
}


yolo-output POST request /yolo-output

{
    "time": "2023-11-2",
    "dispatch_no": 20231030001,
    "x1": 100,
    "y1": 200,
    "x2": 300,
    "y2": 400,
    "class_name": "bag_etc",
    "score": 0.8,
    "w": 20,
    "h": 40,
    "weight": 10
}


