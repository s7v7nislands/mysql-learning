#!/usr/bin/python

from utility import tonum, tobin
from const import *

class Fsp(object):
    header_offset = 38
    header_size   = 112
    def __init__(self, data):
        if len(data) != PAGE_SIZE:
            raise Exception
        self.data = data[38:38+112]

        self.space_id   = tonum(self.data, 0, 4)
        self.not_use    = tonum(self.data, 4, 8)
        self.size       = tonum(self.data, 8, 12)
        self.free_limit         = tonum(self.data, 12, 16)
        self.lowest_no_write    = tonum(self.data, 16, 20)
        self.frag_n_used        = tonum(self.data, 20, 24)

        self.free_cnt           = tonum(self.data, 24, 28)
        self.free_first         = tonum(self.data, 28, 34)
        self.free_last          = tonum(self.data, 34, 40)

        self.free_frag_cnt          = tonum(self.data, 40, 44)
        self.free_frag_first        = tonum(self.data, 44, 50)
        self.free_frag_last         = tonum(self.data, 50, 56)

        self.full_frag_cnt          = tonum(self.data, 56, 60)
        self.full_frag_first        = tonum(self.data, 60, 66)
        self.full_frag_last         = tonum(self.data, 66, 72)

        self.seg_id                 = tonum(self.data, 72, 80)

        self.seg_inodes_full_cnt    = tonum(self.data, 80, 84)
        self.seg_inodes_full_first  = tonum(self.data, 84, 90)
        self.seg_inodes_full_last   = tonum(self.data, 90, 96)

        self.seg_inodes_free_cnt    = tonum(self.data, 96, 100)
        self.seg_inodes_free_first  = tonum(self.data, 100, 106)
        self.seg_inodes_free_last   = tonum(self.data, 106, 112)

    def show(self):
        print '-------- FSP HEADER --------'
        print 'space id                         :', self.space_id
        print 'not use                          :', self.not_use
        print 'space size (pages)               :', self.size
        print 'free pages limit                 :', self.free_limit
        print 'lowest pages no write            :', self.lowest_no_write
        print 'partial extent list used pages   :', self.frag_n_used

        print 'free extent list length          :', self.free_cnt
        print 'first node addr(page off)        :', self.free_first >> 16, self.free_first & 0x00000000FFFF
        print 'last  node addr(page off)        :', self.free_last  >> 16, self.free_last  & 0x00000000FFFF

        print 'partial extent list length       :', self.free_frag_cnt
        print "first node addr(page off)        :", self.free_frag_first >> 16, self.free_frag_first & 0x00000000FFFF
        print "last  node addr(page off)        :", self.free_frag_last  >> 16, self.free_frag_last  & 0x00000000FFFF

        print 'full extent list length          :', self.full_frag_cnt
        print 'fisrt node addr(page off)        :', self.full_frag_first >> 16, self.full_frag_first & 0x00000000FFFF
        print 'last  node addr(page off)        :', self.full_frag_last  >> 16, self.full_frag_last  & 0x00000000FFFF

        print 'first unused segment id          :', self.seg_id

        print 'segment inodes full list length  :', self.seg_inodes_full_cnt
        print 'first node addr(page off)        :', self.seg_inodes_full_first >> 16, self.seg_inodes_full_first & 0x00000000FFFF
        print 'last  node addr(page off)        :', self.seg_inodes_full_last  >> 16, self.seg_inodes_full_last  & 0x00000000FFFF

        print 'segment inode free list length   :', self.seg_inodes_free_cnt
        print 'fisrt node addr(page off)        :', self.seg_inodes_free_first >> 16, self.seg_inodes_free_first & 0x00000000FFFF
        print 'last  node addr(page off)        :', self.seg_inodes_free_last  >> 16, self.seg_inodes_free_last  & 0x00000000FFFF
        print '-------- END OF FSP HEADER --------'
        print

class Fil(object):
    header_offset = 0
    header_size   = 38

    tailer_offset = PAGE_SIZE - 8
    tailer_size   = 8
    def __init__(self, data):
        if len(data) != PAGE_SIZE:
            raise Exception 
        self.data = data

        self.newsum = tonum(self.data, 0, 4)
        self.offset = tonum(self.data, 4, 8)
        self.prev   = tonum(self.data, 8, 12)
        self.next   = tonum(self.data, 12, 16)
        self.lsn    = tonum(self.data, 16, 24)
        self.type   = tonum(self.data, 24, 26)
        self.flsn   = tonum(self.data, 26, 34)
        self.sid    = tonum(self.data, 34, 38)

        self.oldsum = tonum(self.data, PAGE_SIZE-8, PAGE_SIZE-4)
        self.olsn   = tonum(self.data, PAGE_SIZE-4, PAGE_SIZE)

    def show(self):
        print '-------- FIL HEADER AND TAILER --------'
        print 'new checksum  : ', self.newsum
        print 'page offset   : ', self.offset
        print 'prev page no  : ', self.prev
        print 'next page no  : ', self.next
        print 'page lsn      : ', self.lsn
        print 'page  type    : ', 
        for k in PAGE_TYPE:
            if k == self.type:
                print PAGE_TYPE[k]
                find = True
        if not find:
            print 'UNKNOW'
        print 'file lsn      : ', self.flsn
        print 'space id      : ', self.sid
        print 'old checksum  : ', self.oldsum
        print 'log sequence  : ', self.olsn

        print '-------- END FIL HEADER AND TAILER --------'
        print

class Extent(object):
    def __init__(self, data):
        if len(data) != PAGE_SIZE:
            raise Exception
        self.data = data[XDES_ARR_OFFSET:10240+XDES_ARR_OFFSET]

        self.ext = [] 
        self.tmp = {}
        for i in range(XDES_ARR_SIZE/XDES_SIZE):
            self.tmp['xdes_id']         = tonum(self.data, i*XDES_SIZE+0, i*XDES_SIZE+8)
            self.tmp['flst_node_prev']  = tonum(self.data, i*XDES_SIZE+8, i*XDES_SIZE+14)
            self.tmp['flst_node_next']  = tonum(self.data, i*XDES_SIZE+14, i*XDES_SIZE+20)
            self.tmp['xdes_status']     = tonum(self.data, i*XDES_SIZE+20, i*XDES_SIZE+24)
            self.tmp['bitmaps']         = self.data[i*XDES_SIZE+24:i*XDES_SIZE+40]
            self.ext.append(self.tmp.copy())

    def show(self):
        print '-------- EXTENT DESCRIPTOR --------'
        print 'total pages          :', XDES_DESCRIBED_PER_PAGE
        print 'total extents        :', XDES_ARR_SIZE/XDES_SIZE
        print
        for i in range(XDES_ARR_SIZE/XDES_SIZE):
            if self.ext[i]['flst_node_next'] == 0x000000000000:
                continue
            print 'xdes it          :', self.ext[i]['xdes_id']
            print 'node offset page :', 150 + i*XDES_SIZE + 8, ',extent no', i
            print 'flst node prev   :', self.ext[i]['flst_node_prev'] >> 16, self.ext[i]['flst_node_prev'] & 0x00000000FFFF
            print 'flst node next   :', self.ext[i]['flst_node_next'] >> 16, self.ext[i]['flst_node_next'] & 0x00000000FFFF
            print 'xdes status      :', self.ext[i]['xdes_status'],
            if self.ext[i]['xdes_status'] == XDES_FREE:
                print 'free extent in space list' 
            elif self.ext[i]['xdes_status'] == XDES_FREE_FRAG:
                print 'partial free extent in space list'
            elif self.ext[i]['xdes_status'] == XDES_FULL_FRAG:
                print 'full extent in space list'
            elif self.ext[i]['xdes_status'] == XDES_FSEG:
                print 'extent belongs to segment'
            else:
                print 'UNKNOWN XDES TYPE' 
            print 'xdes bitmaps     : free_bit clean_bit' , 
            bits = tobin(self.ext[i]['bitmaps'])
            for i in range(0, len(bits), 2):
                if not (i % 16):
                    print "\n                  ", 
                print '%d%d' % (bits[i], bits[i+1]),
            print
        print '-------- END EXTENT DESCRIPTOR --------'

class Seg_inode(object):
    def __init__(self, data):
        if len(data) != PAGE_SIZE:
            raise Exception
        self.data = data[FSEG_INODE_PAGE_NODE:FSEG_INODE_PAGE_NODE+FLST_NODE_SIZE+FSP_SEG_INODES_PER_PAGE*FSEG_INODE_SIZE]

        self.seg_inodes_prev = tonum(self.data, 0, 6)
        self.seg_inodes_next = tonum(self.data, 6, 12)

        self.seg = []
        self.tmp = {}
        for i in range(FSEG_INODE_PAGE_NODE):
            self.tmp['fseg_id']             = tonum(self.data, 12+i*FSEG_INODE_SIZE+0, 12+i*FSEG_INODE_SIZE+8)
            self.tmp['fseg_not_full_used']  = tonum(self.data, 12+i*FSEG_INODE_SIZE+8, 12+i*FSEG_INODE_SIZE+12)
            self.tmp['fseg_free_cnt']       = tonum(self.data, 12+i*FSEG_INODE_SIZE+12, 12+i*FSEG_INODE_SIZE+16)
            self.tmp['fseg_free_first']     = tonum(self.data, 12+i*FSEG_INODE_SIZE+16, 12+i*FSEG_INODE_SIZE+22)
            self.tmp['fseg_free_last']      = tonum(self.data, 12+i*FSEG_INODE_SIZE+22, 12+i*FSEG_INODE_SIZE+28)
            self.tmp['fseg_not_full_cnt']   = tonum(self.data, 12+i*FSEG_INODE_SIZE+28, 12+i*FSEG_INODE_SIZE+32)
            self.tmp['fseg_not_full_first'] = tonum(self.data, 12+i*FSEG_INODE_SIZE+32, 12+i*FSEG_INODE_SIZE+38)
            self.tmp['fseg_not_full_last']  = tonum(self.data, 12+i*FSEG_INODE_SIZE+38, 12+i*FSEG_INODE_SIZE+44)
            self.tmp['fseg_full_cnt']       = tonum(self.data, 12+i*FSEG_INODE_SIZE+44, 12+i*FSEG_INODE_SIZE+48)
            self.tmp['fseg_full_first']     = tonum(self.data, 12+i*FSEG_INODE_SIZE+48, 12+i*FSEG_INODE_SIZE+54)
            self.tmp['fseg_full_last']      = tonum(self.data, 12+i*FSEG_INODE_SIZE+54, 12+i*FSEG_INODE_SIZE+60)
            self.tmp['fseg_magic']          = tonum(self.data, 12+i*FSEG_INODE_SIZE+60, 12+i*FSEG_INODE_SIZE+64)
            self.tmp['fseg_array']          = self.data[12+i*FSEG_INODE_SIZE+64:12+i*FSEG_INODE_SIZE+192]
            self.seg.append(self.tmp.copy())
    
    def show(self):
        print '-------- SEGMENT INODE -------'
        print 'segment inodes prev:', self.seg_inodes_prev >> 16, self.seg_inodes_prev & 0x00000000FFFF 
        print 'segment inodes next:', self.seg_inodes_next >> 16, self.seg_inodes_next & 0x00000000FFFF 
        for i in range(FSEG_INODE_PAGE_NODE):
            if self.seg[i]['fseg_id'] == 0:
                continue
            print 'segment id               :', self.seg[i]['fseg_id'], ',page offset', FSEG_PAGE_DATA+12+i*FSEG_INODE_SIZE 
            print 'segment used in partial  :', self.seg[i]['fseg_not_full_used']
            print 'segment free number      :', self.seg[i]['fseg_free_cnt']
            print 'segment node first       :', self.seg[i]['fseg_free_first'] >> 16, self.seg[i]['fseg_free_first'] & 0x00000000FFFF
            print 'segment node last        :', self.seg[i]['fseg_free_last'] >> 16, self.seg[i]['fseg_free_last'] & 0x00000000FFFF
            print 'segment partial number   :', self.seg[i]['fseg_not_full_cnt']
            print 'segment node first       :', self.seg[i]['fseg_not_full_first'] >> 16, self.seg[i]['fseg_not_full_first'] & 0x00000000FFFF
            print 'segment node last        :', self.seg[i]['fseg_not_full_last'] >> 16, self.seg[i]['fseg_not_full_last'] & 0x00000000FFFF
            print 'segment full number      :', self.seg[i]['fseg_full_cnt']
            print 'segment node first       :', self.seg[i]['fseg_full_first'] >> 16, self.seg[i]['fseg_full_first'] & 0x00000000FFFF
            print 'segment node last        :', self.seg[i]['fseg_full_last'] >> 16, self.seg[i]['fseg_full_last'] & 0x00000000FFFF
            print 'segment magic number     :', self.seg[i]['fseg_magic']
            print 'segment array            :', 
            for j in range(32):
                if not(j % 4) :
                    print '\n                           ',
                print '%10d' % tonum(self.seg[i]['fseg_array'], j*4, j*4+4),
            print
        print '-------- END OF SEGMENT INODE --------'    

class Page(object):
    def __init__(self, data):
        if len(data) != PAGE_SIZE:
            raise Exception
        self.data = data[FIL_SIZE:PAGE_SIZE-8]

        self.dir_slots      = tonum(self.data, 0, 2)
        self.heap_top       = tonum(self.data, 2, 4)
        self.heap_cnt       = tonum(self.data, 4, 6)
        self.new_format     = self.heap_cnt & 0x8000
        self.heap_cnt       = self.heap_cnt & 0x7FFF
        self.page_free      = tonum(self.data, 6, 8)
        self.page_garbage   = tonum(self.data, 8, 10)
        self.last_insert    = tonum(self.data, 10, 12)
        self.direction      = tonum(self.data, 12, 14)
        self.direction_cnt  = tonum(self.data, 14, 16)
        self.record_cnt     = tonum(self.data, 16, 18)
        self.max_trxid      = tonum(self.data, 18, 26)
        self.level          = tonum(self.data, 26, 28)
        self.index_id       = tonum(self.data, 28, 36)
        self.btr_seg_leaf   = tonum(self.data, 36, 46)
        self.btr_seg_top    = tonum(self.data, 46, 56)
        
        self.slots          = self.data[-2*self.dir_slots:]

    def show(self):
        print '-------- PAGE HEADER --------'
        print 'dirctory slot number         :', self.dir_slots
        print 'heap top offset              :', self.heap_top
        print 'record format                :',
        if self.new_format:
            print 'new'
        else:
            print 'old'
        print 'heap record number           :', self.heap_cnt
        print 'free record list pointer     :', self.page_free
        print 'garbage number (bytes)       :', self.page_garbage
        print 'last insert heap offset      :', self.last_insert
        print 'direction                    :', self.direction
        print 'consecutive direction number :', self.direction_cnt
        print 'records number               :', self.record_cnt
        print 'max trx id                   :', self.max_trxid
        print 'page level                   :', self.level
        print 'index id                     :', self.index_id >> 32, self.index_id & 0x00000000FFFFFFFF
        print 'leaf btree segment           :', self.btr_seg_leaf >> 48, (self.btr_seg_leaf >> 16) & 0x000000000000FFFFFFFF, self.btr_seg_leaf & 0x0000000000000000FFFF 
        print 'top btree segment            :', self.btr_seg_top >> 48, (self.btr_seg_top >> 16) & 0x000000000000FFFFFFFF, self.btr_seg_top & 0x0000000000000000FFFF
        for i in range(self.dir_slots):
            print 'slot pointer   :', tonum(self.slots, len(self.slots)-2*(i+1), len(self.slots)-2*i)
        print '-------- END PAGE HEADER --------'

        
class Ibuf(object):
	def __init__(self, data):
        	if len(data) != PAGE_SIZE:
            		raise Exception
        	self.data = data[FIL_SIZE:]

	def show(self):
		print '-------- INSERT BUFFER BITMAP --------'
		for i in range(XDES_DESCRIBED_PER_PAGE):
			bits = self._getindex(i)
			if '1' in bits:
				print 'ibuf (%d) bitmap free     :' % i, bits[0:2]
				print 'ibuf (%d) bitmap buffered :' % i, bits[2:3]
				print 'ibuf (%d) bitmap ibuf     :' % i, bits[3:4]
			
		print 
		print 'total have 16K bitmaps.we only print some used bitmaps, for more you should use hexdump to see detail.'
		print 'maybe: hexdump -C -s 16422 ibdata1 -n 1024 -v'
		print '-------- END INSERT BUFFER BITMAP --------'

	def _getindex(self, index):
		o = index/2 
		p = index%2

		bitmap = self.data[o]
		bitmap = tobin(bitmap)
		if p:
			bits = bitmap[0:4]
		else:
			bits = bitmap[4:8] 

		return bits

class Ibuf_header(object):
	def __init__(self, data):
		if (len(data) != PAGE_SIZE):
			raise Exception
		self.data = data[PAGE_DATA:PAGE_DATA+10]

	def show(self):
		print '-------- INSERT BUFFER SEGMENT --------'
		print 'ibuf header segment space : ', tonum(self.data, 0, 4)
		print 'ibuf header segment page  : ', tonum(self.data, 4, 8)
		print 'ibuf header segment offset: ', tonum(self.data, 8, 10)
		print '-------- END INSERT BUFFER SEGMENT --------'



class Trx(object):
	def __init__(self, data):
		if (len(data) != PAGE_SIZE):
			raise Exception
		self.data = data

	def show(self):
		print '-------- TRANSACTION  --------'
		data = self.__getsys()
		print 'sys trx id     : ', tonum(data, 0, 8)
		print 'segment space  : ', tonum(data, 8, 12)
		print 'segment page   : ', tonum(data, 12, 16)
		print 'segment offset : ', tonum(data, 16, 18)
		print
		print 'total have 256 rollback segment slots (but use only one, xtradb has the patch):'
		for i in range(256):
			space = tonum(data, i*8+18, i*8+22)
			page = tonum(data, i*8+22, i*8+26)
			if space != 4294967295:
				print 'segment header space:', space
				print 'segmnet header page :', page
		print

		data = self.__getmaster()
		print 'log magic      : ', tonum(data, 0, 4)
		print 'log high offset: ', tonum(data, 4, 8)
		print 'log low offset : ', tonum(data, 8, 12)
		print 'log file name  : ', 
		for k,v in enumerate(data[12:]):
			if v == '\x00':
				break;
		print data[12:12+k]
		print
		
		data = self.__getlog()
		print 'log magic      : ', tonum(data, 0, 4)
		print 'log high offset: ', tonum(data, 4, 8)
		print 'log low offset : ', tonum(data, 8, 12)
		print 'log file name  : ', 
		for k,v in enumerate(data[12:]):
			if v == '\x00':
				break;
		print data[12:12+k]
		print

		data = self.__getdwseg()
		print 'double write seg header space: ', tonum(data, 0, 4)
		print 'double write seg header page : ', tonum(data, 4, 8)
		print 'double write seg header off  : ', tonum(data, 8, 10)
		print 'double write magic           : ', tonum(data, 10, 14)
		print 'double write block1 page     : ', tonum(data, 14, 18)
		print 'double write block2 page     : ', tonum(data, 18, 22)
		print 'double write magic           : ', tonum(data, 22, 26)
		print 'double write block1 page     : ', tonum(data, 26, 30)
		print 'double write block2 page     : ', tonum(data, 30, 34)
		print 'double write space id(dummy) : ', tonum(data, 34, 38)
		print '--------  END TRANSACTION  --------'

	def __getsys(self):
		return self.data[FIL_SIZE:FIL_SIZE+256*8+18]

	def __getmaster(self):
		return self.data[TRX_SYS_MYSQL_MASTER_LOG_INFO:TRX_SYS_MYSQL_MASTER_LOG_INFO+TRX_SYS_MYSQL_LOG_NAME_LEN+12]

	def __getlog(self):
		return self.data[TRX_SYS_MYSQL_LOG_INFO:TRX_SYS_MYSQL_LOG_INFO+TRX_SYS_MYSQL_LOG_NAME_LEN+12]

	def __getdwseg(self):
		return self.data[TRX_SYS_DOUBLEWRITE:TRX_SYS_DOUBLEWRITE+34]

class Rseg(object):
	def __init__(self, data):
		if (len(data) != PAGE_SIZE):
			raise Exception
		self.data = data[TRX_RSEG:TRX_RSEG+TRX_RSEG_UNDO_SLOTS+TRX_RSEG_N_SLOTS*TRX_SEG_SLOT_SIZE]

	def __getslots(self):
		return self.data[TRX_RSEG_UNDO_SLOTS:]

	def show(self):
		print '-------- ROLLBACK SEGMENT  --------'
		print 'rseg max size         : ', tonum(self.data, 0, 4)
		print 'rseg history size     : ', tonum(self.data, 4, 8)
		print 'rseg undo list num    : ', tonum(self.data, 8, 12)
		print 'rseg undo list first  : ', tonum(self.data, 12, 16), tonum(self.data, 16, 18)
		print 'rseg undo list last   : ', tonum(self.data, 18, 22), tonum(self.data, 22, 24)
		print 'rseg header seg space : ', tonum(self.data, 24, 28)
		print 'rseg header seg page  : ', tonum(self.data, 28, 32)
		print 'rseg header seg offset: ', tonum(self.data, 32, 34)

		data = self.__getslots()
		print 'innodb total has 1024 slots'
		for i in range(TRX_RSEG_N_SLOTS):
			num = tonum(data, i*4, i*4+4)
			if num != 4294967295:
				print 'rseg slot %4d: ' % i, num, ' page'
		print '-------- END ROLLBACK SEGMENT  --------'

class Dict(object):
	def __init__(self, data):
		if (len(data) != PAGE_SIZE):
			raise Exception
		self.data = data[DICT_HDR:DICT_HDR+66]

	def show(self):
		print '------- META DICTIONARY -------'
		print 'lastest row id        : ', tonum(self.data, 0, 8)
		print 'lastest table id      : ', tonum(self.data, 8, 16)
		print 'lastest index id      : ', tonum(self.data, 16, 24)
		print 'lastest max id        : ', tonum(self.data, 24, 32), 'Obsolete, always DICT_HDR_FIRST_ID = 10'
		print 'lastest table root    : ', tonum(self.data, 32, 36)
		print 'lastest table id root : ', tonum(self.data, 36, 40)
		print 'lastest column id     : ', tonum(self.data, 40, 44)
		print 'lastest index id      : ', tonum(self.data, 44, 48)
		print 'lastest field id      : ', tonum(self.data, 48, 52)
		print 'dict header seg space : ', tonum(self.data, 56, 60)
		print 'dict header seg page  : ', tonum(self.data, 60, 64)
		print 'dict header seg offset: ', tonum(self.data, 64, 66)
		print '------- END META DICTIONARY -------'

class Undo(object):
	__stat = ('TRX_UNDO_ACTIVE','TRX_UNDO_CACHED','TRX_UNDO_TO_FREE','TRX_UNDO_TO_PURGE','TRX_UNDO_PREPARED')
	def __init__(self, data):
		if (len(data) != PAGE_SIZE):
			raise Exception
		self.data = data
	
	def show_page_hdr(self):
		data = self.data[TRX_UNDO_PAGE_HDR:TRX_UNDO_PAGE_HDR+TRX_UNDO_PAGE_HDR_SIZE]
		_type = tonum(data, 0, 2)
		print '----------------undo log page header--------------------'
		print 'undo log type      : ', _type , ' ,insert undo log' if _type == 1 else ' ,update undo log' 
		print 'undo page start    : ', tonum(data, 2, 4)
		print 'undo page free     : ', tonum(data, 4, 6)
		print 'undo page list prev: ', tonum(data, 6, 10), ' page', tonum(data, 10, 12), ' offset'
		print 'undo page list next: ', tonum(data, 12, 16), ' page', tonum(data, 16, 18), ' offset'

	def show_seg_hdr(self):
		data = self.data[TRX_UNDO_SEG_HDR:TRX_UNDO_SEG_HDR+TRX_UNDO_SEG_HDR_SIZE]
		_stat= tonum(data, 0, 2)
		print '----------------undo segment header--------------------'
		print 'undo log stat          : ', _stat, '  ', self.__stat[_stat] 
		print 'undo last insert offset: ', tonum(data, 2, 4)
		print 'undo fseg header space : ', tonum(data, 4, 8)
		print 'undo fseg header page  : ', tonum(data, 8, 12)
		print 'undo fseg header offset: ', tonum(data, 12, 14)
		print 'undo page list base    : ', tonum(data, 14, 18)
		print 'undo page list first   : ', tonum(data, 18, 22), ' page', tonum(data, 22, 24), ' offset'
		print 'undo page list last    : ', tonum(data, 24, 28), ' page', tonum(data, 28, 30), ' offset'

	def show_undo_hdr(self):
		data = self.data[:]
		last = tonum(data, TRX_UNDO_SEG_HDR+2, TRX_UNDO_SEG_HDR+4)
		print '----------------undo log header--------------------'
		while last :
			hdr = data[last:last+TRX_UNDO_LOG_OLD_HDR_SIZE]
			print 'undo trx id      : ', tonum(hdr, 0, 4), tonum(hdr, 4, 8)
			print 'undo trx num     : ', tonum(hdr, 8, 12), tonum(hdr, 12, 16)
			print 'undo del mark    : ', tonum(hdr, 16, 18)
			print 'undo first start : ', tonum(hdr, 18, 20)
			print 'undo xid exist   : ', tonum(hdr, 20, 21)
			print 'undo dict trx    : ', tonum(hdr, 21, 22)
			print 'undo table id    : ', tonum(hdr, 22, 30)
			print 'undo next log    : ', tonum(hdr, 30, 32)
			print 'undo prev log    : ', tonum(hdr, 32, 34)
			print 'undo history prev: ', tonum(hdr, 34, 38), ' page', tonum(hdr, 38, 40), ' offset'
			print 'undo history next: ', tonum(hdr, 40, 44), ' page', tonum(hdr, 44, 42), ' offset'
			print '----------------------------------'
			last = tonum(hdr, 32, 34)


	def show(self):
		self.show_page_hdr()
		print '\n-----------------------\n'
		self.show_seg_hdr()
		print '\n-----------------------\n'
		self.show_undo_hdr()



if __name__ == '__main__':
    import os
    from stat import *
    filename = raw_input('filename : ')
    filename = filename.strip()
    f = open(filename,'r')
    size = os.stat(filename).st_size/PAGE_SIZE
    prompt = 'page [0 - %d]: ' % (size-1)

    while 1:
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
	    print '''which type:
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


