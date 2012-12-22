#!/usr/bin/python

class Record(object):
    def __init__(self):
        pass

    def is_new(self):
        pass

    def show(self):
        pass

    def show_old(self):
        pass

    def show_new(self):
        pass



if __name__ == '__main__':
    import os
    from innodb import *
    from stat import *
    filename = raw_input('filename : ')
    filename = filename.strip()
    f = open(filename,'r')

    size = os.stat(filename).st_size/PAGE_SIZE
    prompt = 'page [0 - %d]: ' % (size-1)
    off = raw_input(prompt)
    try:
        off = int(off)
    except Exception,a:
        continue
    f.seek(off*PAGE_SIZE)
    data = f.read(PAGE_SIZE)

    npage = Page(data)
    npage.show()

    print '\n-------------------------------------\n\n'

