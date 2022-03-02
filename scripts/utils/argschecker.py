import sys

def argschecker(args):

    if True not in list(vars(args).values()):
        print('ValueError: No arguments passed.')
        sys.exit()

    if args.filename is None:
        print('ValueError: A input filename has not been passed.')
        sys.exit()

    if args.manual:
        if args.d is None and args.n is None:
            print('ValueError: Please specify the distance between profiles and the number of profiles to manually analyse.')
            sys.exit()

    if args.misfit or args.morphology:
        if args.d is None:
            print('ValueError: Please specify the distance between profiles.')
            sys.exit()