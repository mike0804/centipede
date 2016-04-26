import sys
import getopt
import centipede

def main(argv = None):
    argv = sys.argv if argv is None else argv

    try:
        l = ["dir=", \
             "directory=", \
             "debug", \
             "debug-level=", \
             "job="]
        
        opts, args = getopt.getopt(argv, "o:f:", l)
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        # usage()
        sys.exit(2)

    debug = False
    debugLevel = 2
    dir = 'centipede_data'
    jobFile = '' if not args else args[0]
    
    for opt, val in opts:
        if opt in ("-o", "--dir", "--directory"):
            dir = val
        elif opt == "--debug":
            debug = True
        elif opt == "--debug-level":
            debugLevel = int(val)
        elif opt in ("-f", "--job"):
            jobFile = val
        else:
            assert False, "unhandled option"
    
    cl = centipede.Centipede(jobFile, debug=debug, debug_level=debugLevel, dir=dir)
    cl.run()
            
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))