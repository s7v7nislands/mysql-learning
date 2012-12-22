#!/usr/bin/python

if __name__ == '__main__':
    import os
    from innodb import *
    from stat import *
    filename = raw_input('filename : ')
    filename = filename.strip()
    f = open(filename,'r')

    size = os.stat(filename).st_size/PAGE_SIZE
    while 1:
        prompt = 'page [0 - %d]: ' % (size-1)
        off = raw_input(prompt)
        try:
                off = int(off)
        except Exception,a:
            continue
        f.seek(off*PAGE_SIZE)
        data = f.read(PAGE_SIZE)

        npage = Fil(data)
        npage.show()

        if off == 0 :
            npage = Fsp(data)
            npage.show()

            npage = Extent(data)
            npage.show()

        elif off == 1 :
            npage = Ibuf(data)
            npage.show()

        elif off == 2 :
            npage = Seg_inode(data)
            npage.show()

        else :
            npage = Page(data)
            npage.show()

        print "\n"


