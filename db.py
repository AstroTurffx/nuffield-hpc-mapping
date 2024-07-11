import sqlite3
import sys
import os.path

DATABASE = "HPCs.db"

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# Temporary script to run SQL files
def main():
    if len(sys.argv) < 2:
        print("Missing argument: file")
        return
    
    fpath = sys.argv[1]
    if not os.path.isfile(fpath):
        print(f"Can't find file '{fpath}'")
        return
    
    
    file = open(fpath, "r")
    contents = file.read()
    file.close()

    with sqlite3.connect(DATABASE, autocommit=True) as connection:
        
        if len(sys.argv) > 2:
            connection.row_factory = dict_factory
            

        cursor = connection.cursor()
        sql_cmds = contents.rstrip(';').split(';')
        print(f"Running {len(sql_cmds)} commands...")
        for sql in sql_cmds:
            res = cursor.execute(sql)
            rows = res.fetchall()
            [print(row) for row in rows]
            connection.commit()


if __name__ == "__main__":
    main()