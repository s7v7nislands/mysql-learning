import sys

def tonum(data, start, end):
    """convert to number"""
    num = 0
    for k,v in enumerate(data[start:end]):
        n = ord(v) << (8*k)
        num += n

    return num

def main(frm):
    with open(frm) as f:
        fileinfo = f.read(64)
        format(fileinfo, headers)

        tmp = f.read(32)

        pos = tonum(tmp, 3, 7)
        print 'forminfo pos: ', pos
        f.seek(pos)

        tmp = f.read(288)
        format(tmp, forminfos)


def html(func):
    def _(*arg):
        print "<html><body>"
        print "<h1>mysql frm file format</h1>"
        print '<table border="1">'
        print '<tr><th>offset</th><th>name</th><th>value</th></tr>'
        func(*arg)
        print "</table>"
        print "</body></html>"
    return _

@html
def format(fileinfo, fields):
    offset = 0
    for name, length in fields:
        print "<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (offset, name, tonum(fileinfo, offset, offset+length))
        offset += length

forminfos = [
        ('length',2),
        ('xxx',254),
        ('screens',2),
        ('elements',2),
        ('info_length',2),
        ('totlength',2),
        ('no_empty',2),
        ('reclength',2),
        ('n_length',2),
        ('int_count',2),
        ('int_parts',2),
        ('int_length',2),
        ('time_stamp_pos',2),
        ('columns',2),
        ('rows',2),
        ('null_fields',2),
        ('com_length',2),
        ]

headers = [
    ('const', 1),
    ('const', 1),
    ('version', 1),
    ('db_type', 1),
    ('total form name length', 2),
    ('next block', 2), # Next block starts here
    ('form names', 2),
    ('next next block', 4), # begine is form pos, after is next pos
    ('tmp_key_length', 2),
    ('reclength', 2),
    ('max_rows', 4),
    ('min_rows', 4),
    ('one-record-database/crypted', 1),
    ('long pack-fields', 1),
    ('key_info_length', 2),
    ('table_options', 2),
    ('const', 1), #NO filename anymore, New frm file in 3.23
    ('const', 1), #Mark for 5.0 frm file
    ('avg_row_length', 4),
    ('csid', 1),
    ('const', 1),
    ('row_type', 1),
    ('raid: csid>>8', 1),
    ('const', 1),
    ('const', 1),
    ('const', 1),
    ('const', 1),
    ('const', 1),
    ('key_length', 4),
    ('MYSQL_VERSION_ID', 4),
    ('extra_size', 4),
    ('extra_rec_buf_length', 2),
    ('part_db_type', 1),
    ('key_block_size', 2),
]


if __name__ == '__main__':
    main(sys.argv[1])
