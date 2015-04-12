#mysql开发应用

介绍在平时开发中,使用mysql的注意事项.

---

**强烈建议:** 升级到**mysql5.6**,增加了很多功能!

-	[BKA](http://dev.mysql.com/doc/refman/5.6/en/bnl-bka-optimization.html)
-	[MRR](http://dev.mysql.com/doc/refman/5.6/en/mrr-optimization.html)
-	[ICP](http://dev.mysql.com/doc/refman/5.6/en/index-condition-pushdown-optimization.html)

mysql5.7也已经发布RC版本,功能强大!!!

-	[JSON]

---

##存储引擎

mysql自带的存储引擎

-	**innodb**
-	myisam
-	memeory(heap)

第三方的存储引擎

-	xtradb
-	tokudb
	-	Fractal Tree

---

##索引

mysql支持的索引

-	btree
-	hash
-	rtree
-	fulltext

###myisam的index存储

-	数据是heap存储
-	所有的所以都是一样的

###innodb的index存储

-	cluster index
-	secondary index包括primary key
	-	如果不知道primary key,innodb会选取第一个unique index或者自己生成6 bytes的主键
	-	在选取primary key的时候尽量保持primary key的长度

###选择合适的字段

-	anlysn

###索引使用原则

-	只使用一个索引
	-	index merge
-	leftmost原则
-	什么时候增加索引?
	-	只在read的时候有帮助, write, update的时候会带来额外的开销
-	ANALYZE TABLE

combined index

prefix index

-	怎么选取prefix长度
	-	count(distinct left(field_name, 10))/count(distinct field_name)

covered index

###join

(todo)

join_buffer_size(BKA)

###explain的使用

Using temporary

-	memory
-	on-disk(myisam)
	-	tmp_table_size
	-	max_heap_table_size
	-	blob/text, 长的char

Using filesort

###sql注意点

-	subquery
	-	[mysql5.6改进对subquery的优化](dev.mysql.com/doc/refman/5.6/en/subquery-optimization.html)
-	创建表的时候增加注释
-	字段的选择
-	strict_mode
	-	(todo) mysql5.6
-	autocommit
-	select \*
	-	使用列名,避免出现修改表结构的时候需要修改sql
-	group by
	-	(todo): mysql5.6已经修改默认行为
	-	loose, tight index scan
-	sum返回的类型
-	优化器提示
	-	use index, force index, straight index
-	union, distinct union
-	limit的使用
-	ORM
-	backup

###诊断慢查询

slow log

###getlock()问题

(todo): memcache in mysql5.6?

##sql driver

####python

-	[**mysqlclient-python**](https://github.com/PyMySQL/mysqlclient-python)
-	[pymysql](https://github.com/PyMySQL/PyMySQL)
-	[MySQLdb](https://github.com/farcepest/MySQLdb1)
-	[connector-python](http://dev.mysql.com/doc/connector-python/en/index.html)
-	[ultramysql](https://github.com/esnme/ultramysql)
-	[Tornado-MySQL](https://github.com/PyMySQL/Tornado-MySQL)

####golang

-	[**mysql**](https://github.com/go-sql-driver/mysql)
-	[mymysql](https://github.com/ziutek/mymysql)

##工具

-	[percona xtrabackup](http://www.percona.com/software/percona-xtrabackup)
-	[percona toolkit](http://www.percona.com/software/percona-toolkit)
-	[mysqlsandbox](http://mysqlsandbox.net/)
-	[mysql-sys](https://github.com/MarkLeith/mysql-sys/)
-	[dbahelper](https://github.com/MarkLeith/dbahelper)
-	[mydumper](https://launchpad.net/mydumper)
-	[mysql-mmm](http://mysql-mmm.org/doku.php)
-	[Databene Benerator](http://databene.org/databene-benerator.html)
-	[Percona Playback](http://www.percona.com/doc/percona-playback/)

##mysql衍生版本

-	[mariadb](https://mariadb.com/)
-	[percona server](http://www.percona.com/)

##参考资料

book

-	[High Performance MySQL](http://www.highperfmysql.com/)
-	[SQL Antipatterns](https://pragprog.com/book/bksqla/sql-antipatterns)

blog

-	[mysql performance blog](http://www.mysqlperformanceblog.com/)
