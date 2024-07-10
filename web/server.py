import json
from flask import Flask, request
import os.path
import sqlite3

DATABASE = "../HPCs.db"

app = Flask(__name__)



# ======================
# ==== Flask Routes ====
# ======================
@app.route('/')
def index():
    with open("./static/index.html") as file:
        return file.read(), 200

@app.route('/static/<path>')
def static_resources(path):
    local_path = "./static/" + path
    status_code = 200
    
    if not os.path.isfile(local_path):
        local_path = "./static/404.html"
        status_code = 404

    with open(local_path) as file:
        return file.read(), status_code

@app.route('/api/hpcs/all', methods=["POST"])
def api_filter_hpcs():
    try:
        raise KeyError('aaa!!!')
        cur = db_con.cursor()
        cur.execute("SELECT name, top500_rank, manufacturer, total_cores, processor_name, installation_year, r_max, addiational_info FROM hpcs")
        result = cur.fetchall()
        return result.dumps(), 200
    except Exception as err:
        return json.dumps(exception_as_dict(err),indent=4), 500



# ==========================
# === Dictionary Helpers ===
# ==========================
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def exception_as_dict(ex):
    return dict(type=ex.__class__.__name__,
                errno=ex.errno, message=ex.message,
                strerror=exception_as_dict(ex.strerror)
                if isinstance(ex.strerror,Exception) else ex.strerror)




if __name__ == "__main__":
    try:
        db_con = sqlite3.connect(DATABASE)
        db_con.row_factory = dict_factory
        app.run(debug=True)
    finally:
        # Clean up code
        db_con.close()