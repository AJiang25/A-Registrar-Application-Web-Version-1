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
