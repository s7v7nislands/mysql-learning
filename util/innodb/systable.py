#!/usr/bin/python

if __name__ == '__main__':
    import os
    from innodb import *
    from stat import *
    filename = raw_input('filename : ')
    filename = filename.strip()
    f = open(filename,'r')

    while 1:
    	size = os.stat(filename).st_size/PAGE_SIZE
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

	elif off == 3:
	    npage = Ibuf_header(data)
	    npage.show()

	elif off == 4:
	    print 'SYS_IBUF_TABLE_0 (PAGE_NO, TYPES)'
	    npage = Page(data)
	    npage.show()

	elif off == 5 :
	    npage = Trx(data)
	    npage.show()

	elif off == 6 :
	    npage = Rseg(data)
	    npage.show()

        elif off == 7 :
	    npage = Dict(data)
	    npage.show()

	else :
	    print '''
which type:
1). normal page
2). undo page
choose no:'''
	    pagetype = raw_input()
	    if pagetype == '1':
		    ptype = 1
            elif pagetype == '2':
		    ptype = 2
	    else:
		print 'bad choose!'
		continue
	    
            if ptype == 1:
		npage = Page(data)
	    elif ptype == 2:
	    	npage = Undo(data)

	    npage.show()
	
	print "\n"


