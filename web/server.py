import json
from flask import Flask, render_template, request
import os.path
import sqlite3

DATABASE = "../HPCs.db"

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')



# ======================
# ==== Flask Routes ====
# ======================
@app.route('/')
def index():
    with open("./static/index.html") as file:
        return file.read(), 200

@app.route('/api/hpcs/all', methods=["POST"])
def api_filter_hpcs():
    global db_con
    try:
        req_data = request.get_json()

        cur = db_con.cursor()
        cur.execute(\
            """SELECT hpcs.name as 'hpc_name', top500_rank, manufacturer,
            total_cores, processor_name, installation_year, interconnect,
            r_max, additional_info, sites.name as 'site_name', city, country,
            hpcs.website as 'hpc_website', sites.website as 'site_website',
            system_tier, system_status
            FROM hpcs, sites
            WHERE hpcs.site_id = sites.site_id
            ORDER BY top500_rank ASC
            LIMIT ? OFFSET ?""",\
            (req_data["limit"],req_data["offset"])
        )
        rows = cur.fetchall()
        result = ""
        for row in rows:
            add_i = []
            for x in row["additional_info"].split(" | "):
                if not x:
                    continue
                scndsplt = x.split(": ")
                add_i.append(scndsplt)

            tier_color = tier_to_color_class(row["system_tier"])
            status_color = status_to_color_class(row["system_status"])


            result += render_template("results-card.html",\
                                        tier_color=tier_color,\
                                        status_color=status_color,\
                                        add_i=add_i,\
                                        **row)
        return result, 200
    except Exception as err:
        print(err)
        result = {
            "error_name": err.__class__.__name__
        }
        return result, 500



# ====================
# === HTML Helpers ===
# ====================


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



# =====================
# === Miscellaneous ===
# =====================
def tier_to_color_class(tier):
    match tier:
        case 1:
            return "text-bg-info"
        case 2:
            return "text-bg-primary"
        case _:
            return "text-bg-secondary"

def status_to_color_class(status):
    match status:
        case "Active":
            return "text-bg-success"
        case "Out of Service" | "Under Maintenance":
            return "text-bg-warning"
        case "EOL":
            return "text-bg-danger"
        case _:
            return "text-bg-secondary"


if __name__ == "__main__":
    try:
        db_con = sqlite3.connect(DATABASE, autocommit=True, check_same_thread = False)
        db_con.row_factory = dict_factory
        app.run(debug=True)
    finally:
        # Clean up code
        print("Exiting...")
        db_con.close()