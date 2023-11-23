import sqlite3

import os

def check():

    create_dispatch_table = '''
        CREATE TABLE IF NOT EXISTS dispatch(
            time TIMESTAMP, 
            dispatch_no INTEGER PRIMARY KEY, 
            dispatch_mgr_id INTEGER, 
            approval_mgr_id INTEGER, 
            area_id INTEGER, 
            vehicle_id VARCHAR, 
            driver_id INTEGER,
            crew1_id INTEGER, 
            crew2_id INTEGER, 
            alt_driver_id INTEGER, 
            alt_crew1_id INTEGER, 
            alt_crew2_id INTEGER
        );'''
    
    create_collection_table = '''
        CREATE TABLE IF NOT EXISTS collection(
            time TIMESTAMP,
            dispatch_no INTEGER PRIMARY KEY,
            bag_5L INTEGER,
            bag_10L INTEGER,
            bag_20L INTEGER,
            bag_30L INTEGER,
            bag_50L INTEGER,
            bag_75L INTEGER,
            bag_etc INTEGER,
            others INTEGER,
            weight INTEGER
        );'''
    
    create_yolo_outout_table = '''
        CREATE TABLE IF NOT EXISTS yolo_output(
            time TIMESTAMP,
            dispatch_no INTEGER,
            x1 INTEGER,
            y1 INTEGER,
            x2 INTEGER,
            y2 INTEGER,
            class_name CHAR(255),
            score FLOAT,
            w INTEGER,
            h INTEGER,
            weight INTEGER
        );'''

    if os.path.exists('localDatabase.db'):
        print("The database already exists.")
    else:
        conn = sqlite3.connect('localDatabase.db')
        cursor = conn.cursor()
        
        cursor.execute(create_dispatch_table)
        cursor.execute(create_collection_table)
        cursor.execute(create_yolo_outout_table)

        print("The database and tables have been created.")
        
        conn.commit()
        conn.close()

    conn = sqlite3.connect('localDatabase.db')
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('dispatch', 'collection', 'yolo_output')")
    existing_tables = cursor.fetchall()
    
    if len(existing_tables) < 3:
        cursor.execute(create_dispatch_table)
        cursor.execute(create_collection_table)
        cursor.execute(create_yolo_outout_table)
        
        print("The missing tables have been created.")
    else:
        print("All required tables already exist.")
    
    conn.commit()
    conn.close()



def start_collection_table():
    # query of create collection table
    create_collectiontable_query = '''
    CREATE TABLE IF NOT EXISTS collection(
        time TIMESTAMP,
        dispatch_no INTEGER PRIMARY KEY,
        bag_5L INTEGER,
        bag_10L INTEGER,
        bag_20L INTEGER,
        bag_30L INTEGER,
        bag_50L INTEGER,
        bag_75L INTEGER,
        bag_etc INTEGER,
        others INTEGER,
        weight INTEGER
    );'''

    check()
    conn = sqlite3.connect('localDatabase.db')
    cursor = conn.cursor()

    # checking made table
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='collection';")
    if cursor.fetchone() is None:
        # create table
        cursor.execute(create_collectiontable_query)
        conn.commit()
    conn.close()


# save collection data
def insert_collection_data(time, dispatch_no, bag_5L, bag_10L, bag_20L, bag_30L, bag_50L, bag_75L, bag_etc, others, weight):
    # start_collection_table()
    conn = sqlite3.connect("localDatabase.db")
    cursor = conn.cursor()

    insert_data_query = '''
    INSERT INTO collection (time, dispatch_no, bag_5L, bag_10L, bag_20L, 
    bag_30L, bag_50L, bag_75L, bag_etc, others, weight)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    # value for insert
    data_to_insert = (time, dispatch_no, bag_5L, bag_10L, bag_20L,
                      bag_30L, bag_50L, bag_75L, bag_etc, others, weight)

    # runing insert
    cursor.execute(insert_data_query, data_to_insert)

    conn.commit()
    conn.close()


def update_collections_data(time, dispatch_no, bag_5L, bag_10L, bag_20L, bag_30L, bag_50L, bag_75L, bag_etc, others, weight):
    # start_collection_table()
    conn = sqlite3.connect("localDatabase.db")
    cursor = conn.cursor()
    update_data_query = "UPDATE collection SET time=?, bag_5L=?, bag_10L=?, bag_20L=?, bag_30L=?, bag_50L=?, bag_75L=?, bag_etc=?, others=?, weight=? WHERE dispatch_no=?"

    cursor.execute(update_data_query, (time, bag_5L, bag_10L, bag_20L, bag_30L,
                   bag_50L, bag_75L, bag_etc, others, weight, dispatch_no))

    conn.commit()
    conn.close()

def retrieve_collections():
    # Remove unnecessary function call
    # start_collection_table()

    with sqlite3.connect("localDatabase.db") as conn:

        cur = conn.cursor()
        cur.execute('SELECT * FROM collection')

        rows = cur.fetchall()

        if len(rows) == 0:
            return {"message": "No collection data!"}

        data = []

        for row in rows:
            data.append(row)

        result = {'data': []}

        for i in range(len(data)):


            bag_volumes = {
                "bag_5L": data[i][2],
                "bag_10L": data[i][3],
                "bag_20L": data[i][4],
                "bag_30L": data[i][5],
                "bag_50L": data[i][6],
                "bag_75L": data[i][7]
            }

            total_volume = 0

            for bag, quantity in bag_volumes.items():
                volume = int(bag.split("_")[1].replace("L", ""))
                total_volume += volume * quantity

            r = {   
                    # "time": data[i][0],
                    # "dispatch_no": data[i][1],
                    "bag_5L": data[i][2],
                    "bag_10L": data[i][3],
                    "bag_20L": data[i][4],
                    "bag_30L": data[i][5],
                    "bag_50L": data[i][6],
                    "bag_75L": data[i][7],
                    "bag_etc": data[i][8],
                    "others": data[i][9],
                    "weight": data[i][10],
                    "volume": total_volume
                }
            result['data'].append(r)
        

        
        return result
    


def delete_collection_data():
    conn = sqlite3.connect("localDatabase.db")
    cursor = conn.cursor()

    delete_collection_query = "DELETE FROM collection"

    cursor.execute(delete_collection_query)
    conn.commit()
    conn.close()
    return print("Done")


def start_yolo_output_table():
    # query of create yolo_output table
    create_yolo_output_query = '''
    CREATE TABLE IF NOT EXISTS yolo_output(
        time TIMESTAMP,
        dispatch_no INTEGER PRIMARY KEY,
        x1 INTEGER,
        y1 INTEGER,
        x2 INTEGER,
        y2 INTEGER,
        class_name CHAR(255),
        score FLOAT,
        w INTEGER,
        h INTEGER,
        weight INTEGER
    );'''

    # check()
    conn = sqlite3.connect('localDatabase.db')
    cursor = conn.cursor()

    # checking made table
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='yolo_output';")
    if cursor.fetchone() is None:
        # create table
        cursor.execute(create_yolo_output_query)
        conn.commit()
    conn.close()


def dynamicc(class_name, weight, dispatch_no):

    conn = sqlite3.connect("localDatabase.db")
    cursor = conn.cursor()

    # class_name = request.json_get("class_name")
    # weight = request.json_get("weight")

    select_query = "SELECT COUNT(*) FROM collection WHERE dispatch_no = ?"
    cursor.execute(select_query, (dispatch_no,))
    result = cursor.fetchone()

    if result[0] == 0:
        # Insert a new row into the collection table
        class_names = ["bag_5L", "bag_10L", "bag_20L", "bag_30L", "bag_50L", "bag_75L", "bag_etc","others"]
        class_values = [1 if name == class_name else 0 for name in class_names]
        class_values_str = ', '.join(str(value) for value in class_values)

        insert_query = f"INSERT INTO collection (dispatch_no, {', '.join(class_names)}, weight) VALUES (?, {class_values_str}, ?)"

        values = (dispatch_no, weight)
        cursor.execute(insert_query, values)
    else:
        # Update the existing row
        update_coll_query = "UPDATE collection SET {} = {} + 1, weight = weight + ? WHERE dispatch_no = ?".format(class_name, class_name)
        values = (weight, dispatch_no)
        cursor.execute(update_coll_query, values)


    conn.commit()
    conn.close()

# save yolo_output data
def insert_yolo_output_data(time, dispatch_no, x1, y1, x2, y2, class_name, score, w, h, weight):
    # start_yolo_output_table()
    conn = sqlite3.connect("localDatabase.db")
    cursor = conn.cursor()

    insert_data_query = '''
    INSERT INTO yolo_output (time, dispatch_no, x1, y1, x2, 
    y2, class_name, score, w, h, weight)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    data_to_insert = (time, dispatch_no, x1, y1, x2, y2,
                      class_name, score, w, h, weight)

    cursor.execute(insert_data_query, data_to_insert)

    conn.commit()
    conn.close()




def delete_yolo_output_data():
    conn = sqlite3.connect("localDatabase.db")
    cursor = conn.cursor()

    delete_yolo_output_query = "DELETE FROM yolo_output"

    cursor.execute(delete_yolo_output_query)
    conn.commit()
    conn.close()
    return print("Done")

