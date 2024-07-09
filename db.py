import sqlite3
import sys
import os.path

DATABASE = "HPCs.db"

# Temporary script to run SQL files
def main():
    if len(sys.argv) < 3:
        print("Arguments:")
        print("1 Command type: execute/select")
        print("2 File path")
        return
    
    cmd = sys.argv[1].lower()
    if cmd != "execute" and cmd != "select":
        print(f"Unknown command '{cmd}'")
        return
    
    fpath = sys.argv[2]
    if not os.path.isfile(fpath):
        print(f"Can't find file '{fpath}'")
        return
    
    file = open(fpath, "r")
    contents = file.read()
    file.close()

    with sqlite3.connect(DATABASE, autocommit=True) as connection:
        cursor = connection.cursor()
        sql_cmds = contents.split(';')
        print(f"Running {len(sql_cmds)} commands...")
        for sql in sql_cmds:
            res = cursor.execute(sql)
            if cmd == "select":
                rows = res.fetchall()
                [print(row) for row in rows]
            else:
                connection.commit()


if __name__ == "__main__":
    main()