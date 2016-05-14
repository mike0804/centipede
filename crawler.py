import sys
import os
import getopt
import shutil
import time
import centipede

def usage():
  # print "\nThis is the usage function\n"
  print 'Usage: '+sys.argv[0]+' [OPTION] jobfile'
  print '  or   '+sys.argv[0]+' [OPTION] -f jobfile\n'
  print 'Options'
  print ' -o, --dir           path to working directory'
  print '     --debug         turn on debugging messages'
  print '     --debug-level   debug level (max 3)'
  print ' -c, --compress      archive the result directory into gzib tarball'
  print '     --selenium      enable selenium'
  print ' -f, --job           path to job file\n'

def main(argv = None):
    argv = sys.argv if argv is None else argv

    try:
        l = ["dir=", \
             # "directory=", \
             "debug", \
             "debug-level=", \
             "selenium", \
             "job=",            # -f
             "compress",        # -c
            ]

        opts, args = getopt.getopt(argv, "o:f:", l)
    except getopt.GetoptError as e:
        # print help information and exit:
        # print str(e) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    # defults of options
    dir = 'centipede_data'
    debug = False
    debug_level = 2
    file = '' if not args else args[0]
    archive = False

    for opt, val in opts:
        if opt in ("-o", "--dir", "--directory"):
            dir = val
        elif opt == "--debug":
            debug = True
        elif opt == "--selenium":
            selenium = True
        elif opt == "--debug-level":
            debug_level = int(val)
        elif opt in ("-f", "--job"):
            file = val
        elif opt in ("-c", "--compress"):
            archive = True
        else:
            assert False, "unhandled option"

    # task - file + current timestamp
    task = file + '.' + time.strftime("%Y-%m-%d", time.gmtime())

    try:
        cur_dir = sys.path[0]
        tmp_dir = os.path.join(cur_dir, 'tmp')
        log_dir = os.path.join(cur_dir, 'log')
        output_dir = os.path.join(cur_dir, 'output')

        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        jobs = os.path.join(cur_dir, task + '.jobs')
        logfile = os.path.join(cur_dir, task + '.log')

        shutil.copy(file, jobs)

    except OSError as e:
        print str(e)
        sys.exit(2)

    job_dir = os.path.join(tmp_dir, task)

    try:
        cl = centipede.Centipede(jobs, \
                                 debug=debug, \
                                 debug_level=debug_level, \
                                 dir=os.path.join(tmp_dir, task), \
                                 logfile=logfile, \
                                 selenium=selenium \
                                 )
        cl.run()
    except Centipede.Error as e:
        # do something
        pass
    except Exception as e:
        print str(e)
    finally:
        cl.close()
        sys.exit(2)

    try:
        if archive:
            shutil.make_archive(os.path.join(output_dir, task), \
                                'gztar', \
                                tmp_dir, task)
        else:
            shutil.move(job_dir, output_dir)

        shutil.rmtree(job_dir)
    except OSError as e:
        print str(e)
        sys.exit(2)



if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))