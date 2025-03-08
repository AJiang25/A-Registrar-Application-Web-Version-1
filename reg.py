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
@app.route('/getoverviews', methods=['GET'])
def get_overviews():
    query = {
        "dept": flask.request.args.get("dept"),
        "coursenum": flask.request.args.get("coursenum"),
        "area": flask.request.args.get("area"),
        "title": flask.request.args.get("title")
    }

    valid, result = database.get_overviews(query) 
    if not valid:
        return flask.render_template('error.html', message = "Failed to retrieve data.")
    
    
    html_code = flask.render_template(
        'getoverviews.html',
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
@app.route('/getdetails', methods=['GET'])
def get_details():
    
    query = {"classid": flask.request.args.get("classid")}
    valid, result = database.get_details(query)
    if not valid:
        return flask.render_template('error.html', message = "Failed to retrieve data.")
    
    dept = flask.request.cookies.get("dept")
    coursenum = flask.request.cookies.get("coursenum")
    area = flask.request.cookies.get("area")
    title = flask.request.cookies.get("title")

    html_code = flask.render_template(
        'getdetails.html',
        classid=query["classid"],
        result = result
    )
    
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)