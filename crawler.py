import centipede

with open('jobs', 'w') as fp:
    fp.write('http://unix.stackexchange.com/questions/tagged/security\tstackexchange.unix.questions\n')


cl = centipede.Centipede('jobs', debug=True, debug_level=2)
cl.run()

