#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Authors: Arnold Jiang and Amanda Chan
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# imports
import sys
import sqlite3
import contextlib
#-----------------------------------------------------------------------
# constants
DATABASE_URL = 'file:reg.sqlite?mode=ro'
#-----------------------------------------------------------------------

def reg_overviews(query):
    try:
        with sqlite3.connect(
            DATABASE_URL,
            isolation_level = None,
            uri = True
        ) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                conditions = []
                descriptors = []
                sql_query = """
SELECT DISTINCT cl.classid, cr.dept, cr.coursenum, c.area, c.title 
                    FROM courses c 
                    JOIN crosslistings cr ON c.courseid = cr.courseid 
                    JOIN classes cl ON c.courseid = cl.courseid
                """
                if query.get("dept"):
                    conditions.append("cr.dept LIKE ? ESCAPE '\\'")
                    descriptor = query[
                        "dept"].lower(
                            ).replace("%", r"\%").replace("_", r"\_")
                    descriptors.append(f"%{descriptor}%")
                if query.get("coursenum"):
                    conditions.append("cr.coursenum LIKE ? ESCAPE '\\'")
                    descriptor = query[
                        "coursenum"].lower(
                            ).replace("%", r"\%").replace("_", r"\_")
                    descriptors.append(f"%{descriptor}%")
                if query.get("area"):
                    conditions.append("c.area LIKE ? ESCAPE '\\'")
                    descriptor = query[
                        "area"].lower(
                            ).replace("%", r"\%").replace("_", r"\_")
                    descriptors.append(f"%{descriptor}%")
                if query.get("title"):
                    conditions.append("c.title LIKE ? ESCAPE '\\'")
                    descriptor = query[
                        "title"].lower(
                            ).replace("%", r"\%").replace("_", r"\_")
                    descriptors.append(f"%{descriptor}%")
                if conditions:
                    sql_query += "WHERE " + " AND ".join(conditions)

                sql_query += "ORDER BY cr.dept ASC,"
                sql_query += "cr.coursenum ASC, cl.classid ASC;"
                cursor.execute(sql_query, descriptors)
                ans = cursor.fetchall()

                result = [
                    {
                        "classid": row[0],
                        "dept": row[1],
                        "coursenum": row[2],
                        "area": row[3],
                        "title": row[4]
                    } for row in ans
                ]

                return [True, result]

    except Exception as e:
        print(f"Error in reg_overviews: {str(e)}", file=sys.stderr)
        return [
            False,
"A server error occurred. Please contact the system administrator."
        ]
#-----------------------------------------------------------------------
def reg_details(query):

    try:
        classid = query["classid"]
        if not classid:
            return [
                        False,
                        "missing classid"
                    ]

        try:
            classid = int(classid)
        except ValueError:
            return [
                        False,
                        "non-integer classid"
            ]
        with sqlite3.connect(
            DATABASE_URL,
            isolation_level = None,
            uri = True
        ) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                class_query = """
SELECT classid, days, starttime, endtime, bldg, roomnum, courseid
                    FROM classes
                    WHERE classid = ?
                """
                course_query = """
SELECT DISTINCT c.courseid, c.area, c.title, c.descrip, c.prereqs
                        FROM courses c
                        WHERE c.courseid = ?
                """
                dept_query = """
                    SELECT DISTINCT cr.dept, cr.coursenum
                        FROM crosslistings cr
                        WHERE cr.courseid = ?
                        ORDER BY cr.dept ASC, cr.coursenum ASC
                """
                prof_query = """
                    SELECT DISTINCT p.profname
                        FROM courses c
                        JOIN coursesprofs cp ON c.courseid = cp.courseid
                        JOIN profs p ON cp.profid = p.profid
                        WHERE c.courseid = ?
                        ORDER BY p.profname ASC
                """

                cursor.execute(class_query, (classid,))
                class_row = cursor.fetchone()
                if not class_row:
                    return [
                        False,
                        f"no class with classid {classid} exists"
                    ]

                cursor.execute(course_query, (class_row[6],))
                course_row = cursor.fetchone()
                if not course_row:
                    return [
                        False,
                        f"no course with classid {class_row[6]} exists"
                    ]

                cursor.execute(dept_query, (class_row[6],))
                dept_row = cursor.fetchall()

                cursor.execute(prof_query, (class_row[6],))
                prof_row = cursor.fetchall()

                result = {
                "classid": class_row[0], 
                "days": class_row[1], 
                "starttime": class_row[2], 
                "endtime": class_row[3], 
                "building": class_row[4],
                "room": class_row[5],
                "courseid": course_row[0],
                "area": course_row[1],
                "title": course_row[2],
                "description": course_row[3],
                "prerequisites": course_row[4],
                "departments": [
                    {
                        "dept": dept[0],
                        "coursenum": dept[1]
                    } for dept in dept_row
                ],
                "professors": [prof[0] for prof in prof_row]
                }
                return [True, result]

    except Exception as e:
        print(f"Error in reg_details: {str(e)}", file=sys.stderr)
        return [
            False,
"A server error occurred. Please contact the system administrator."
        ]

#-----------------------------------------------------------------------
# For testing:
overviews_query = {
        "dept": 'COS',
        "coursenum": '333',
        "area": '',
        "title": 'Advanced'
    }

details_query = {
        "classid":'8134'
    }

def _test():
    print(reg_overviews(overviews_query))
    print()
    print(reg_details(details_query))

if __name__ == '__main__':
    _test()
