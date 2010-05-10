#!/usr/bin/python

def tonum(data, start, end):
    """convert to number"""
    num = 0
    for i in data[start:end]:
        n = ord(i)
        num <<= 8 
        num += n

    return num

def tobin(data):
    """ convert to binary list """
    tmp = []
    for dt in data:
        d = ord(dt)
        t = 1
        for i in range(8):
            if d & t:
                tmp.append(1)
            else:
                tmp.append(0)
            t <<= 1
    #tmp.reverse()
    return tmp


if __name__ == '__main__':
    f = file('/usr/local/mysql/var/ibdata1', 'r')
    data = f.read(4096)

    print tonum(data, 0, 4)
    print tonum(data, 4, 8)
    print tonum(data, 8, 12)

    a = tobin(data[334:350])
    print a
    print len(a)



