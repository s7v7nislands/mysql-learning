#!/usr/bin/python

PAGE_TYPE = {
        17855 : 'B-tree node',
        2     : 'Undo log page',
        3     : 'Index node',
        4     : 'Insert buffer free list',
        0     : 'Freshly allocated page',
        5     : 'Insert buffer bitmap',
        6     : 'System page',
        7     : 'Transaction system data',
        8     : 'File space header',
        9     : 'Extent descriptor page',
        10    : 'Uncompressed BLOB page',
        11    : 'First compressed BLOB page',
        12    : 'First compressed BLOB page'}

#page size = 16k
PAGE_SIZE = 16 * 1024
UNIV_PAGE_SIZE = 16 * 1024

#address size = 6
FIL_ADDR_SIZE = 6


#list size
FLST_BASE_NODE_SIZE = 4 + 2 * FIL_ADDR_SIZE
FLST_NODE_SIZE = 2 * FIL_ADDR_SIZE

#fil header
FIL_OFFSET = 0
FIL_SIZE   = 38

#fsp header
FSP_OFFSET = FIL_SIZE
FSP_SIZE   = 32 + 5 * FLST_BASE_NODE_SIZE
FSP_EXTENT_SIZE = 64

#extend header
XDES_BITMAP         = 24

XDES_BITS_PER_PAGE  = 2
XDES_FREE_BIT       = 0
XDES_CLEAN_BIT      = 1

# States of a descriptor
XDES_FREE           = 1
XDES_FREE_FRAG      = 2
XDES_FULL_FRAG      = 3
XDES_FSEG           = 4

XDES_SIZE           = 40
XDES_ARR_SIZE       = 10240

XDES_ARR_OFFSET = FIL_SIZE + FSP_SIZE

XDES_DESCRIBED_PER_PAGE = PAGE_SIZE

# segment inode
FSEG_PAGE_DATA          = FIL_SIZE
FSEG_INODE_PAGE_NODE    = FSEG_PAGE_DATA
FSEG_ARR_OFFSET         = FSEG_PAGE_DATA + FLST_NODE_SIZE

FSEG_FRAG_SLOT_SIZE     = 4
FSEG_FRAG_ARR_N_SLOTS   = FSP_EXTENT_SIZE / 2

FSEG_INODE_SIZE         = 16 + 3 * FLST_BASE_NODE_SIZE + FSEG_FRAG_ARR_N_SLOTS * FSEG_FRAG_SLOT_SIZE
FSP_SEG_INODES_PER_PAGE = (UNIV_PAGE_SIZE - FSEG_ARR_OFFSET - 10) / FSEG_INODE_SIZE
FSEG_MAGIC_N_VALUE      = 97937874
FSEG_FILLFACTOR         = 8
FSEG_FRAG_LIMIT         = FSEG_FRAG_ARR_N_SLOTS
FSEG_FREE_LIST_LIMIT    = 40
FSEG_FREE_LIST_MAX_LEN  = 4
FSEG_HEADER_SIZE        = 10

# page
PAGE_HEADER = FIL_SIZE
PAGE_DATA   = PAGE_HEADER + 36 + 2 * FSEG_HEADER_SIZE

# ibuf bitmap
IBUF_BITMAP         = PAGE_DATA
IBUF_BITS_PER_PAGE  = 4

IBUF_BITMAP_FREE    = 0
IBUF_BITMAP_BUFFERED    = 2
IBUF_BITMAP_IBUF    = 3

# ibuf header
IBUF_HEADER     = PAGE_DATA

# ibuf root


# trx 
TRX_SYS         = FSEG_PAGE_DATA
TRX_SYS_N_RSEGS     = 256

TRX_SYS_MYSQL_MASTER_LOG_INFO   = UNIV_PAGE_SIZE - 2000 + FSEG_PAGE_DATA
TRX_SYS_MYSQL_LOG_INFO          = UNIV_PAGE_SIZE - 1000 + FSEG_PAGE_DATA
TRX_SYS_DOUBLEWRITE             = UNIV_PAGE_SIZE - 200

TRX_SYS_MYSQL_LOG_NAME_LEN  = 256

# trx rseg
TRX_RSEG            = FSEG_PAGE_DATA
TRX_RSEG_N_SLOTS    = 1024

TRX_SEG_SLOT_SIZE   = 4
TRX_RSEG_UNDO_SLOTS     = 8 + FLST_BASE_NODE_SIZE + FSEG_HEADER_SIZE

# dict 
DICT_HDR       = FSEG_PAGE_DATA


# undo segment
TRX_UNDO_PAGE_HDR           = FSEG_PAGE_DATA
TRX_UNDO_PAGE_HDR_SIZE      = (6 + FLST_NODE_SIZE)
TRX_UNDO_SEG_HDR            = (TRX_UNDO_PAGE_HDR + TRX_UNDO_PAGE_HDR_SIZE)
TRX_UNDO_SEG_HDR_SIZE       = (4 + FSEG_HEADER_SIZE + FLST_BASE_NODE_SIZE)

TRX_UNDO_LOG_OLD_HDR_SIZE   = (34 + FLST_NODE_SIZE)
TRX_UNDO_XA_FORMAT          =(TRX_UNDO_LOG_OLD_HDR_SIZE)
