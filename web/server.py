import json
import math
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
def api_all_hpcs():
    global db_con
    try:
        req_data = request.get_json()

        cur = db_con.cursor()
        cur.execute(\
            """SELECT hpcs.name as 'hpc_name', top500_rank, manufacturer,
            total_cores, processor_name, installation_year, interconnect,
            r_max, additional_info, sites.name as 'site_name', city, country,
            hpcs.website as 'hpc_website', sites.website as 'site_website',
            system_tier, system_status, segment, system_id, total_nodes,
            system_type, longitude, latitude
            FROM hpcs, sites
            WHERE hpcs.site_id = sites.site_id
            ORDER BY top500_rank ASC
            LIMIT ? OFFSET ?""",\
            (req_data["limit"],req_data["offset"])
        )
        rows = cur.fetchall()
        html = ""
        pins = ""

        for row in rows:
            html += render_hpc(row)
            pins += render_pin(row)
        
        result = {
            "length": len(rows),
            "start_range": req_data["offset"],
            "pins": pins,
            "html": html
        }
        return result, 200
    except Exception as err:
        print(err)
        result = { "error_name": err.__class__.__name__ }
        return result, 500


@app.route('/api/hpcs/node_details/<system_id>', methods=["GET"])
def api_node_details(system_id):
    global db_con
    try:
        cur = db_con.cursor()
        cur.execute("SELECT number, processor_name, node_cores, accelerator, memory FROM node_details WHERE system_id = ?", (system_id,))
        rows = cur.fetchall()
        return render_template("node-detail-card.html", rows=rows), 200
    except Exception as err:
        print(err)
        result = { "error_name": err.__class__.__name__ }
        return result, 500


@app.route('/api/hpcs/filter', methods=["POST"])
def api_filter_hpcs():
    global db_con
    try:
        req_data = request.get_json()
        computed_filters = compute_filters(req_data)

        cur = db_con.cursor()
        cur.execute(\
            f"""SELECT hpcs.name as 'hpc_name', top500_rank, manufacturer,
            total_cores, processor_name, installation_year, interconnect,
            r_max, additional_info, sites.name as 'site_name', city, country,
            hpcs.website as 'hpc_website', sites.website as 'site_website',
            system_tier, system_status, segment, system_id, total_nodes,
            system_type, longitude, latitude
            FROM hpcs, sites
            WHERE hpcs.site_id = sites.site_id
            {computed_filters}
            ORDER BY top500_rank ASC
            LIMIT ? OFFSET ?""",\
            (req_data["limit"],req_data["offset"])
        )
        rows = cur.fetchall()
        html = ""
        pins = ""

        for row in rows:
            html += render_hpc(row)
            pins += render_pin(row)
        
        result = {
            "length": len(rows),
            "start_range": req_data["offset"],
            "pins": pins,
            "html": html
        }
        return result, 200
    except Exception as err:
        print(err)
        result = { "error_name": err.__class__.__name__ }
        return result, 500


# @app.route('/api/hpcs/all/count', methods=["GET"])
# def api_all_hpcs_count():
#     global db_con
#     try:
#         cur = db_con.cursor()
#         cur.execute("SELECT COUNT(*) FROM hpcs")
#         length = cur.fetchone()[0]
#         result = { "length": length }
#         return result, 200
#     except Exception as err:
#         print(err)
#         result = { "error_name": err.__class__.__name__ }
#         return result, 500

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
    
def compute_filters(data):
    res = ""
    for (key, value) in data.items():
        match key:
            case "r_max_1":
                res += f"AND r_max > {value} "
            case "r_max_2":
                res += f"AND r_max < {value} "
            case "total_cores_1":
                res += f"AND total_cores > {value} "
            case "total_cores_2":
                res += f"AND total_cores < {value} "

        if value == "Any":
            continue

        match key:
            case "cpu_family":
                res += f"AND processor_name LIKE '%{value}%' "
            case "system_status":
                res += f"AND system_status = '{value}' "
            case "system_tier":
                res += f"AND system_tier = {value} "
    return res

MAP_BOUNDS_LAT_1 = 60.846142
MAP_BOUNDS_LAT_2 = 49.162600
MAP_BOUNDS_LNG_1 = -10.476361
MAP_BOUNDS_LNG_2 = 1.765083

def merc_y(lat):
    return math.log(math.tan((lat * math.pi)/360.0 + math.pi/4.0))

def render_pin(row):
    if not row["latitude"] or not row["longitude"]:
        return ""
    proj_lat = merc_y(row["latitude"])
    ymax = merc_y(MAP_BOUNDS_LAT_1)
    ymin = merc_y(MAP_BOUNDS_LAT_2)
    t = 100.0 * (ymax - proj_lat) / (ymax - ymin)
    l = 100.0 * (row["longitude"]-MAP_BOUNDS_LNG_1) / (MAP_BOUNDS_LNG_2-MAP_BOUNDS_LNG_1)
    tooltip = f"""data-bs-toggle="tooltip" data-bs-title="{row["hpc_name"]}" """ \
        if row["hpc_name"] else ""
    return f"""<img style="display: none; top: {t}%; left: {l}%;" id="sys-id-{row["system_id"]}"
                {tooltip}
                class="map-pin" src="icons/map_pin.svg" onload="SVGInject(this)">"""

def render_hpc(row):
    # Compute values
    add_i = []
    for x in row["additional_info"].split(" | "):
        if not x:
            continue
        scndsplt = x.split(": ")
        add_i.append(scndsplt)

    tier_color = tier_to_color_class(row["system_tier"])
    status_color = status_to_color_class(row["system_status"])

    return render_template("results-card.html",\
                                tier_color=tier_color,\
                                status_color=status_color,\
                                add_i=add_i,\
                                **row)


if __name__ == "__main__":
    try:
        db_con = sqlite3.connect(DATABASE, autocommit=True, check_same_thread = False)
        db_con.row_factory = dict_factory
        app.run(debug=True)
    finally:
        # Clean up code
        print("Exiting...")
        db_con.close()