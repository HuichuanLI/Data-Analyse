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
MONTH ( pay_time );

-- step3 在2的基础上应用窗口函数实现需求

SELECT
a.MONTH,-- 月份
a.pay_amount,-- 当月总支付金额
sum( a.pay_amount ) over ( ORDER BY a.MONTH ) -- 就是2019年的数据，所以
不用分组
-- --此时没有使用rows指定窗口数据范围，默认当前行及其之前的所有行
FROM
(
SELECT MONTH
( pay_time ) MONTH,
sum( pay_amount ) pay_amount
FROM
user_trade
WHERE
YEAR ( pay_time ) = 2019
GROUP BY
MONTH ( pay_time )
) a