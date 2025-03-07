# imports
import flask
import database

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='.')
#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/getoverviews', methods=['GET'])
def get_overviews():
    query = {"dept": flask.request.args.get("dept"),
             "coursenum": flask.request.args.get("coursenum"),
             "area": flask.request.args.get("area"),
             "title": flask.request.args.get("title")
             }
    
    result = database.get_overviews(query) 
    html_code = flask.render_template('getoverviews.html', 
                                      dept=query["dept"],
                                      coursenum=query["coursenum"],
                                      area = query["area"],
                                      title=query["title"],
                                      result = result)
    response = flask.make_response(html_code)
    response.set_cookie("dept", query["dept"])
    response.set_cookie("coursenum", query["coursenum"])
    response.set_cookie("area", query["area"])
    response.set_cookie("title", query["title"])
    return response
    
#-----------------------------------------------------------------------
@app.route('/getdetails', methods=['GET'])
def get_details():
    query = {"classid": flask.request.args.get("classid")}
    result = database.get_details(query)
    dept = flask.request.cookies.get("dept")
    coursenum = flask.request.cookies.get("coursenum")
    area = flask.request.cookies.get("area")
    title = flask.request.cookies.get("title")
    html_code = flask.render_template('getdetails.html', 
                                      classid=query["classid"],
                                      result = result)
    response = flask.make_response(html_code)
    return response