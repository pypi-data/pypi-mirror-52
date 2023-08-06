def lol(cast,indent=False,level=0,fh=sys.stdout):
    for i in cast:
        if isinstance(i, list):
            lol(i,indent,level+1,fh)
        else:
            for j in range(level):
                    print("\t",end='',file=fh)
            print(i,fh)
