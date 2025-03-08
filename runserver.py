#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Authors: Arnold Jiang and Amanda Chan
#-----------------------------------------------------------------------
# imports
import sys
import argparse
import reg
#-----------------------------------------------------------------------
# app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------
# flask.request.args.get function - get all of the fields of the query 
#(dept, courseum, area, title), make an empty dictionary called query
# fill in the keys using the flask.request.args.get. Then you feed
# the dictionary into the database.py. Database.py handles all fo the sql
# and returns the response. This is all in reg.py for overviews. app
# route get overviews and get details go into reg.py and the fields would 
# come from the query. flask.request.args.get you would call this 4 times for
# the arguments. You call this in details too. 

#flask.render_template gives the sql response to the html and you need to
# feed in the data (sql response) from database.py 

# cookies is in the specs (if the user clicks back, the database can 
# repopulate the table). Search criteria persists across page reloads for
# overviews. And this goes in the reg.py, which is the flask page. 

# use the query name arguments from reg.py in html files to call it
#-----------------------------------------------------------------------
#put sql logic in database.py. In database.py have 2 functions: getOverviews
    # and getDetails and return 

    #flask communicates between html and sql so frontend and backend
    #create reg.py (flask file) import flask and import database 
    # both functions flask in this file need to go to reg.py


#-----------------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser(
        description = 'Server for the registrar application'
    )
    parser.add_argument(
        'port',
        type = int,
        help = 'the port at which the server is listening'
    )

    args = parser.parse_args()
    try:
        reg.app.run(host='0.0.0.0', port=args.port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
        
#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
