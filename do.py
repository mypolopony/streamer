def dothings():
    '''
    This is an obnoxiously easy way to suggest command line arguments and avoid 
    argparse, which is usually recommended. I kind of like it, though. It's essentially
    a parser of a different sort, because it doesn't look like standard language, but
    it is, which makes it kind of brilliant.

    Usage:
        managelog.py [options] process -- <logfile>...
        managelog.py [options] upload -- <logfile>...
        managelog.py [options] process upload -- <logfile>...
        managelog.py -h

    Options:
        -V, --verbose      Be verbose
        -U, --user <user>  Username
        -P, --pswd <pswd>  Password

    Manage log file by processing and/or uploading it.
    If upload requires authentication, you shall specify <user> and <password>
    '''

if __name__ == "__main__":
    dothings()
    from docopt import docopt
    args = docopt(__doc__)
    print(args)