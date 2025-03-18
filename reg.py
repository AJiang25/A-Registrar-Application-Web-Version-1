#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Authors: Arnold Jiang and Amanda Chan
#-----------------------------------------------------------------------
# imports
import flask
import database

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    query = {
        "dept": flask.request.args.get("dept"),
        "coursenum": flask.request.args.get("coursenum"),
        "area": flask.request.args.get("area"),
        "title": flask.request.args.get("title")
    }

    valid, result = database.reg_overviews(query)
    if not valid:
        result = {"error": result}

    html_code = flask.render_template(
        'regoverviews.html',
        dept=query["dept"],
        coursenum=query["coursenum"],
        area = query["area"],
        title=query["title"],
        result = result
    )

    response = flask.make_response(html_code)

    if query["dept"] is not None:
        response.set_cookie("dept", query["dept"])
    if query["coursenum"] is not None:
        response.set_cookie("coursenum", query["coursenum"])
    if query["area"] is not None:
        response.set_cookie("area", query["area"])
    if query["title"] is not None:
        response.set_cookie("title", query["title"])
    return response

#-----------------------------------------------------------------------
@app.route('/regdetails', methods=['GET'])
def reg_details():

    query = {"classid": flask.request.args.get("classid")}
    valid, result = database.reg_details(query)
    if not valid:
        result = {"error": result}

    dept = flask.request.cookies.get("dept","")
    coursenum = flask.request.cookies.get("coursenum","")
    area = flask.request.cookies.get("area","")
    title = flask.request.cookies.get("title","")

    html_code = flask.render_template(
        'regdetails.html',
        classid=query["classid"],
        result = result,
        dept = dept,
        coursenum = coursenum,
        area = area,
        title = title
    )

    response = flask.make_response(html_code)

    return response

#-----------------------------------------------------------------------
# For testing:

def _test():
    print(index())
    print()
    print(reg_details())

if __name__ == '__main__':
    _test()
