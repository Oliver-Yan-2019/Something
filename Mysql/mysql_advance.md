### 普通索引和唯一索引

1. 普通索引和唯一索引的查询性能几乎一样, 但是写性能是普通索引快. 因为可以用到change buffer, 唯一索引会导致内存命中率下降.
2. change buffer用的是buffer pool里的内存(`innodb_change_buffer_max_size`).
3. 使用change buffer的场景: 写多读少.
4. redo log主要节省的是随机写磁盘的IO消耗(转成顺序写), 而change buffer主要节省的则是随机读磁盘的IO消耗.

### MySQL 是怎样得到索引的基数的

1. 采样, `innodb_stats_persistent`:
    - on: 表示统计信息会持久化存储. 默认的N是20, M是10.
    - off: 表示统计信息只存储在内存中. 默认的N是8, M是16.
2. mysql选错索引, 解决方法：
    - 使用`show index from table_name`命令, 查看表索引的基数.
    - 使用`analyze table table_name`命令, 重新统计索引信息, 解决采样导致的扫描行数出错的问题.
    - `force index`

### 怎么给字符串字段加索引？

1. 前缀索引(增加扫描行数).
2. 倒序索引(增加扫描行数).
3. 哈希索引(不支持范围).
4. 完整索引(占用空间).

### MySQL 突然抖一下

1. 在刷脏页.
2. 场景:
    - InnoDB的redo log写满了: 尽量避免, 所有的更新都会堵住.
    - 系统内存不足.
    - MySQL认为系统"空闲"的时候.
    - MySQL正常关闭.

3. InnoDB用缓冲池(buffer pool)管理内存, 缓冲池中的内存页有三种状态:
    - 还没有使用的.
    - 使用了并且是干净页.
    - 使用了并且是脏页

4. 要避免:
    - 一个查询要淘汰的脏页个数太多, 会导致查询的响应时间明显变长.
    - 日志写满, 更新全部堵住, 写性能跌为0.

5. InnoDB刷脏页的控制策略:
    - 磁盘能力`innodb_io_capacity`: 设置成磁盘的IOPS(
      fio工具: `fio -filename=$filename -direct=1 -iodepth 1 -thread -rw=randrw -ioengine=psync -bs=16k -size=500M -numjobs=10 -runtime=10 -group_reporting -name=mytest`
      ).
    - 脏页比例上限`innodb_max_dirty_pages_pct`: 75%.
    - SSD设置`innodb_flush_neighbors`为0.

6. 脏页比例:

```mysql
use performance_schema;

select VARIABLE_VALUE
into @a
from global_status
where VARIABLE_NAME = 'Innodb_buffer_pool_pages_dirty';

select VARIABLE_VALUE
into @b
from global_status
where VARIABLE_NAME = 'Innodb_buffer_pool_pages_total';

select @a / @b;
```

### 为什么表数据删掉一半, 表文件大小不变?

1. `innodb_file_per_table`:
    - OFF: 表的数据放在系统共享表空间.
    - ON: 每个InnoDB表数据存储在一个以.ibd为后缀的文件中.

2. 重建表: `alter table A engine=InnoDB`或`optimize table A`.
3. gh-ost: github开源的一个工具.

### count(*)

1. 不同引擎:
    - MyISAM.
    - InnoDB.

2. count(字段) < count(主键 id) < count(1) ≈ count(*).

### "order by"是怎么工作的

1. 全字段排序
    - MySQL会给每个线程分配一块内存用于排序, 称为sort_buffer.
    - `sort_buffer_size`:
        - 在内存中: 快速排序.
        - 临时文件辅助排序: 归并排序(外部排序), 查看`number_of_tmp_files`.
         ```mysql
         /* 打开optimizer_trace，只对本线程有效 */
         SET optimizer_trace = 'enabled=on';
         
         /* @a保存Innodb_rows_read的初始值 */
         select VARIABLE_VALUE
         into @a
         from performance_schema.session_status
         where variable_name = 'Innodb_rows_read';
         
         /* 执行语句 */
         select city, name, age
         from t
         where city = '杭州'
         order by name
         limit 1000;
         
         /* 查看 OPTIMIZER_TRACE 输出 */
         SELECT *
         FROM `information_schema`.`OPTIMIZER_TRACE`\G
         
         /* @b保存Innodb_rows_read的当前值 */
         select VARIABLE_VALUE
         into @b
         from performance_schema.session_status
         where variable_name = 'Innodb_rows_read';
         
         /* 计算Innodb_rows_read差值 */
         select @b - @a;
         ```
      
2. rowid排序
   - `max_length_for_sort_data`: 控制用于排序的行数据的长度.
   
3. 如果内存够, 就要多利用内存, 尽量减少磁盘访问.
4. 优化: 联合索引vs覆盖索引.

### 如何正确地显示随机消息?

1. 内存临时表`tmp_table_size`.
2. `order by rand()`
   - 创建内存临时表, 其中一个字段是rand()生成的随机小数, 另一个字段是rowid.
   - 使用rowid排序, 之后取出前limit行, 在内存里找到对应字段值.
   
3. 磁盘临时表(超过`tmp_table_size`).
   - 引擎: `internal_tmp_disk_storage_engine`.
   
4. 优先队列排序算法

### 不走索引的情况(函数操作)

1. 对索引字段做函数操作, 可能会破坏索引值的有序性, 因此优化器就决定放弃走树搜索功能.
2. 隐式类型转换(函数操作), 注: 字符串和数字做比较, 会默认把字符串转为数字.
3. 隐式字符编码转换(CONVERT).

### 为什么我只查一行的语句, 也执行这么慢? (`show processlist`命令)

1. 查询长时间不返回.
   - 大概率是表t被锁住了. 
   - 等MDL锁.
   - 等flush.
   - 等行锁: 
      - ```select * from t sys.innodb_lock_waits where locked_table='`test`.`t`'\G```
      - ```KILL blocking_pid;```
   
2. 查询慢.
   - 扫描行数多.
   - 有事务的undo log过长, 当前查询需要遍历undo log.
   
### 第20讲