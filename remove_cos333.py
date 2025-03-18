import sqlite3
import contextlib

DATABASE_URL = 'file:reg.sqlite?mode=rw'

def remove_cos333():
    try:
        with sqlite3.connect(
            DATABASE_URL,
            isolation_level=None,
            uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                sql_query = "SELECT courseid FROM crosslistings WHERE dept = 'COS' AND coursenum = '333'"
                cursor.execute(sql_query)
                courseid_row = cursor.fetchone()
                courseid = courseid_row[0]
                cursor.execute(
                    "DELETE FROM classes WHERE courseid = ?",
                    (courseid,)
                )
                cursor.execute(
                    "DELETE FROM crosslistings WHERE courseid = ?",
                    (courseid,)
                )
                cursor.execute(
                    "DELETE FROM coursesprofs WHERE courseid = ?",
                    (courseid,)
                )
                cursor.execute(
                    "DELETE FROM courses WHERE courseid = ?",
                    (courseid,)
                )
                print("deleted COS 333 data")
    except Exception as e:
        print(f"Error deleting COS 333 data: {str(e)}")

if __name__ == '__main__':
    remove_cos333()
