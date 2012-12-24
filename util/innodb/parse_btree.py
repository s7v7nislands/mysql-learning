#!/usr/bin/python

if __name__ == '__main__':
    import os
    import sys
    from innodb import *
    from stat import *
    from collections import defaultdict
    filename = sys.argv[1].strip()
    f = open(filename,'r')

    size = os.stat(filename).st_size/PAGE_SIZE

    page_types = defaultdict(int)
    index_level = defaultdict(int)
    while 1:
        data = f.read(PAGE_SIZE)

        if not data:
            break

        page = Fil(data)

        page_types[page.type] += 1

        if page.type == 17855:
            p = Page(data)
            index_level[p.index_id, p.level] += 1


    for k in page_types:
        print PAGE_TYPE[k], page_types[k]

    print '-' * 40
    print 'index', 'level'
    for k in sorted(index_level):
        print k, index_level[k]
