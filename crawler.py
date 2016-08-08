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

def get_dirs():
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

    return (cur_dir, tmp_dir, log_dir, output_dir)

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
             "help",            # -h
             "resume=",         # -r
            ]

        opts, args = getopt.getopt(argv, "o:f:hcr:", l)
    except getopt.GetoptError as e:
        # print help information and exit:
        # print str(e)
        usage()
        sys.exit(2)

    # defults of options
    dir = 'centipede_data'
    debug = False
    debug_level = 2
    selenium = False
    file = '' if not args else args[0]
    archive = False
    task = None
    resume_task = False

    for opt, val in opts:
        if opt in ("-o", "--dir", "--directory"):
            dir = val
        elif opt == "--debug":
            debug = True
        elif opt == "--debug-level":
            debug_level = int(val)
        elif opt == "--selenium":
            selenium = True
        elif opt in ("-f", "--job"):
            file = val
        elif opt in ("-c", "--compress"):
            archive = True
        elif opt in ("-r", "--resume"):
            task = val
            resume_task = True
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(2)
        else:
            assert False, "unhandled option"

    if not os.path.isfile(file) and not resume_task:
        usage()
        sys.exit(2)

    if resume_task:
        pass
    else:
        task = file + '.' + time.strftime("%Y-%m-%d", time.gmtime())

    try:
        cur_dir, tmp_dir, log_dir, output_dir = get_dirs()

        task_dir = os.path.join(tmp_dir, task)
        jobs = os.path.join(cur_dir, task + '.jobs')
        logfile = os.path.join(log_dir, task + '.log')

        if not resume_task:
            shutil.copy(file, jobs)

        cl = centipede.Centipede(
               jobs, \
               selenium=selenium, \
               debug=debug, \
               debug_level=debug_level, \
               dir=task_dir, \
               logfile=logfile                   
             )

        cl.run()

        if archive:
            shutil.make_archive(
              os.path.join(output_dir, task), \
              'gztar', \
              tmp_dir, task
            )
            shutil.rmtree(task_dir)
        else:
            shutil.move(task_dir, output_dir)

    except centipede.Error as e:
        print str(e)
        sys.exit(2)
    except OSError as e:
        print str(e)
        sys.exit(2)
    except Exception as e:
        print str(e)    
        raise
        sys.exit(2)
    finally:
        cl.close()
        # sys.exit(2)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))