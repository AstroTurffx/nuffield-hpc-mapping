import sys
from pyquery import PyQuery
import requests
import sqlite3
import time

DATABASE = "HPCs.db"
TOP500_SYSTEM_URL = "https://www.top500.org/system/"
TOP500_SITE_URL = "https://www.top500.org/site/"
REQUEST_DELAY = 0.5

def scrape_info(url: str):
    page_html = requests.get(url).text
    pq = PyQuery(page_html)

    res = {}
    title_text = pq("title").text()
    res["page_title"] = title_text.replace(" | TOP500", "")

    rows = pq("table.table.table-condensed").eq(0)("tr")
    for row in rows.items():
        key = row("th").text().rstrip(":")
        value = row("td").text()
        if not value:
            continue
        res[key] = value
    return res

def parse_site_info(data):
    res = {}
    res["name"]    = data["page_title"]
    res["segment"] = data["Segment"]
    res["city"]    = data["City"]
    res["country"] = data["Country/Region"]
    res["website"] = data.get("URL", None)
    return res

# messy af, why am I doing it like this :/
def parse_system_info(data):
    try:
        res = {}
        res["manufacturer"] = data["Manufacturer"]
        res["total_cores"] = int(data["Cores"].replace(",", ""))
        res["processor_name"] = data["Processor"]
        res["interconnect"] = data["Interconnect"]
        res["installation_year"] = int(data["Installation Year"])
        res["os"] = data.get("Operating System", None)
        res["r_max"] = float(data["Linpack Performance (Rmax)"].replace("PFlop/s", ""))
        res["r_peak"] = float(data["Theoretical Peak (Rpeak)"].replace("PFlop/s", ""))
        res["n_max"] = int(data.get("Nmax", "0").replace(",", ""))
        res["website"] = data.get("System URL", None)
        res["additional_info"] = get_system_addition_info(data)

        return res
    except Exception as e:
        print("Unable to parse data:", e)
        print(data)
        raise e

# poop code
def get_system_addition_info(data):
    data.pop("page_title",   None)
    data.pop("Site",         None)
    data.pop("System URL",   None)
    data.pop("Manufacturer", None)
    data.pop("Cores", None)
    data.pop("Processor",    None)
    data.pop("Interconnect", None)
    data.pop("Installation Year", None)
    data.pop("Linpack Performance (Rmax)", None)
    data.pop("Theoretical Peak (Rpeak)", None)
    data.pop("Nmax", None)
    data.pop("Operating System", None)
    res = ""
    for (key, value) in data.items():
        res += f"{key}: {value} | "
    return res.rstrip("\n")

def generate_insert_cmd(table: str, data):
    keys = ""
    values = ""
    for (key, value) in data.items():
        keys += key + ","
        v = repr(value)
        if v == "None":
            v = "NULL"
        values += v + ","
    return f"INSERT INTO {table}({keys.rstrip(",")}) VALUES ({values.rstrip(",")});"

# Messy but will do
def scrape():
    print("Scraping UK HPCs from top500.org.uk")

    # ~~POST request for UK HPCs~~
    # Top 500 protects thier API so I can't forge a POST request
    # so I will just download the page for now...
    path_to_scraping = "./"
    if len(sys.argv) > 1:
        path_to_scraping = sys.argv[1]
    file = open(path_to_scraping + "sublist-generator-top500-june-2024.html")
    sublist_html = file.read()
    file.close()

    # Parse HTML and get links to HPC sites
    hpcs = []

    pq = PyQuery(sublist_html)
    tr = pq("tbody > tr")
    for row in tr.items():
        sys_rank = int(row("td").eq(0).text())

        links = row("a")
        sys_id = int(links[0].attrib['href'].replace(TOP500_SYSTEM_URL, ""))
        site_id = int(links[1].attrib['href'].replace(TOP500_SITE_URL, ""))
        sys_name = links.eq(0)("b").text()

        hpc = (sys_id, site_id, sys_name, sys_rank)
        hpcs.append(hpc)

    with sqlite3.connect(path_to_scraping + "../" + DATABASE) as con:
        print(f"Connected to '{DATABASE}'")
        cur = con.cursor()

        # Scrape site info from top500
        print("Exracting site data...")
        visited_sites = []
        for (sys_id, site_id, sys_name, sys_rank) in hpcs:
            # Some sites have multiple HPCs
            if site_id in visited_sites:
                continue

            visited_sites.append(site_id)
            data = scrape_info(TOP500_SITE_URL + str(site_id))
            data = parse_site_info(data)
            data["site_id"] = site_id
            cmd = generate_insert_cmd("sites", data)
            cur.execute(cmd)

            print(f"Inserted data for '{data["name"]}'")
            time.sleep(REQUEST_DELAY)
        
        # Scrape system info from top500
        print("Exracting system data...")
        for (sys_id, site_id, sys_name, sys_rank) in hpcs:
            data = scrape_info(TOP500_SYSTEM_URL + str(sys_id))
            data = parse_system_info(data)
            data["system_id"] = sys_id
            data["site_id"] = site_id
            data["name"] = sys_name
            data["top500_rank"] = sys_rank
            cmd = generate_insert_cmd("hpcs",data)
            cur.execute(cmd)

            print(f"Inserted data for '{sys_name}'")
            time.sleep(REQUEST_DELAY)
        
        con.commit()

if __name__ == "__main__":
    scrape()