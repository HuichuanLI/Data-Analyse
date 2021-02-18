需求1: 查询出2019年每月的支付总额和当年累积支付总额
/*
需求1: 查询出2019年每月的支付总额和当年累积支付总额
*/

-- step1 过滤出2019年数据
select * from user_trade where year(pay_time)=2019;
-- step2 在1的基础上，按照月份进行group by 分组，统计每个月份的支付总额
SELECT MONTH
	( pay_time ),
	sum( pay_amount ) 
FROM
	user_trade 
WHERE
	YEAR ( pay_time ) = 2019 
GROUP BY
	MONTH ( pay_time );-- step3 在2的基础上应用窗口函数实现需求
SELECT
	a.MONTH,-- 月份
	a.pay_amount,-- 当月总支付金额
	sum( a.pay_amount ) over ( ORDER BY a.MONTH ) -- 就是2019年的数据，所以
	不用分组-- --此时没有使用rows指定窗口数据范围，默认当前行及其之前的所有行
	
FROM
	( SELECT MONTH ( pay_time ) MONTH, sum( pay_amount ) pay_amount FROM user_trade WHERE YEAR ( pay_time ) = 2019 GROUP BY MONTH ( pay_time ) ) a


需求2：查询出2018-2019年每月的支付总额和当年累积支付总额

SELECT a.year,
a.month,
a.pay_amount,
sum(a.pay_amount) over(partition by a.year order by a.month)
FROM
(SELECT year(pay_time) year,
month(pay_time) month,
sum(pay_amount) pay_amount
FROM user_trade
WHERE year(pay_time) in (2018,2019)
GROUP BY year(pay_time),
month(pay_time))a;

需求3: 查询出2019年每个月的近三月移动平均支付金额

SELECT a.month,
a.pay_amount,
avg(a.pay_amount) over(order by a.month rows between 2 preceding
and current row)
FROM
(SELECT month(pay_time) month,
sum(pay_amount) pay_amount
FROM user_trade
WHERE year(pay_time)=2019
GROUP BY month(pay_time))a;


需求4: 查询出每四个月的最大月总支付金额
SELECT a.month,
a.pay_amount,
max(a.pay_amount) over(order by a.month rows between 3 preceding
and current row)
FROM
(SELECT substr(pay_time,1,7) as month,
sum(pay_amount) as pay_amount
FROM user_trade
GROUP BY substr(pay_time,1,7))a;







需求5: 2020年1月，购买商品品类数的用户排名

SELECT
user_name,
count( DISTINCT goods_category ) category_count,
row_number() over(order by count( DISTINCT goods_category ) desc) order1,
-- row_number生成了行的编号从1开始
rank() over(order by count( DISTINCT goods_category ) desc ) order2,
dense_rank() over(order by count( DISTINCT goods_category ) desc) order3
FROM
user_trade
WHERE
substring( pay_time, 1, 7 ) = '2020-01'
GROUP BY
user_name

需求6: 查询出将2020年2月的支付用户，按照支付金额分成5组后的结果
SELECT user_name,
sum(pay_amount) pay_amount,
ntile(5) over(order by sum(pay_amount) desc) level
FROM user_trade
WHERE substr(pay_time,1,7)='2020-02'
GROUP BY user_name;


需求7: 查询出2020年支付金额排名前30%的所有用户
SELECT a.user_name,
a.pay_amount,
a.level
FROM
(SELECT user_name,
sum(pay_amount) pay_amount,
ntile(10) over(order by sum(pay_amount) desc) level
FROM user_trade
WHERE year(pay_time)=2020
GROUP BY user_name)a
WHERE a.level in (1,2,3);

需求10: 查询出支付时间间隔超过100天的用户数
SELECT count(distinct user_name)
FROM
(SELECT user_name,
pay_time,
lead(pay_time) over(partition by user_name order by
pay_time) lead_dt
FROM user_trade)a
WHERE a.lead_dt is not null
and datediff(a.lead_dt,a.pay_time)>100;