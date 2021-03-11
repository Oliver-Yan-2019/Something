1. 建立长连接之后, 内存飙升:
    - 定期断开连接: 使用一段时间或程序判断执行过一个占用内存的大查询之后,  
      断开连接, 之后查询再进行重连
    - 5.7或以上版本可以执行mysql_reset_connection重新初始化连接资源


2. WAL: 先写日志, 再写磁盘
    - innoDB的redo log是固定大小循环写的, 是一种物理日志,  
      可以避免数据库异常重启丢失数据, crash-safe(MyISAM没有这个能力)
    - server层的binlog归档日志, 是追加写的, 是一种逻辑日志
    - redo log的prepare和commit阶段成为"两阶段提交"
    - innodb_flush_log_at_trx_commit和sync_binlog建议设置为1,  
      持久化到磁盘
    - redo log: "这个页做了什么改动";  
      binlog两种模式:
        - statement格式记sql,
        - row格式记录行内容, 记两条, 更新前和更新后都有


3. MyISAM不支持事务
    - ACID(Atomicity, Consistency, Isolation, Durability),  
      即原子性/一致性/隔离性/持久性
    - 脏读:  
      不可重复读:  
      幻读:
    - 隔离级别:
        - 读未提交RU: 一个事务还没提交时, 它做的变更就能被别的事务看到
        - 读提交RC: 一个事务提交之后, 它做的变更才会被其他事务看到
        - 可重复读RR: 一个事务执行过程中看到的数据, 总是跟这个事务在启动时  
          看到的数据是一致的. 当然在可重复读隔离级别下，未提交变更对其他事务  
          也是不可见的
        - 串行化Serial: 对于同一行记录, "写"会加"写锁", "读"会加"读锁".  
          当出现读写锁冲突的时候, 后访问的事务必须等前一个事务执行完成,  
          才能继续执行
    - 多版本并发控制(MVCC)
        - RU: 没用视图
        - RC: 每句sql执行前建立视图
        - RR: 事务启动时建立视图
        - Serial: 加锁
    - transaction-isolation
    - 回滚日志
    - 不要使用长事务:
        - 系统会保留很老的视图, 在事务提交前会产生很多回滚日志,  
          占用存储空间
        - 占用锁资源
    - 事务的启动方式:
        - begin或start transaction   
          commit  
          rollback
        - set autocommit=0: 将线程的自动提交关掉 commit  
          rollback
        - commit work and chain: 提交事务并自动启动下一个事务
    - 监控information_schema.innodb_trx: 设置长事务阈值


4. 索引
    - 哈希表这种结构适用于只有等值查询的场景:  
      精确查询O(1), 范围查询不乐观
    - 有序数组在等值查询和范围查询场景中的性能就都非常优秀:  
      精确查询和范围查询O(log n), 更新麻烦, 只适用于静态存储引擎
    - 二叉树查询和更新都是O(log N)
    - innoDB使用了B+树, 每个索引对应一棵B+树
    - 主键索引/聚簇索引: (key: 主键的值, value: 叶子节点整行数据)  
      非主键索引/二级索引: (key: 索引列的值, value: 叶子结点主键的值)
    - 基于非主键索引的查询需要多扫描一棵索引树(回表)
    - 页分裂: 影响性能和空间利用率  
      页合并
    - NOT NULL PRIMARY KEY AUTO_INCREMENT:  
      不会触发页分裂(主键字段需要保证有序插入)  
      主键长度尽量小, 这样普通索引叶子节点占用空间也就越小
    - 覆盖索引: 可以减少树的搜索次数, 显著提升查询性能
    - 最左前缀原则: 可以是联合索引的最左N个字,  
      也可以是字符串索引的最左M个字符.  
      如果通过调整顺序, 可以少维护一个索引,  
      那么这个顺序往往就是需要优先考虑采用的.  
      还要考虑索引占用空间
    - 索引下推: 索引遍历过程中, 对索引中包含的字段先做判断,  
      直接过滤掉不满足条件的记录, 减少回表次数
    - 重建索引: 省空间  
      alter table T drop index k;  
      alter table T add index(k);  
      // 重建主键是不合理的, 会重建表, 用alter table T engine=InnoDB替代  
      alter table T drop primary key;  
      alter table T add primary key(id);