1. 需求1： 查询线索(二级渠道jdsc)后续转化成交车型详情

SELECT
c.clue_id,
ca_n,
chexing_id
FROM
clue_day c,
order_day o
WHERE
c.clue_id = o.clue_id
AND ca_n = 'jdsc';



SELECT
c.clue_id,
ca_n,
chexing_id
FROM
clue_day c

INNER JOIN order_day o ON c.clue_id = o.clue_id
WHERE
ca_n = 'jdsc';

2. 需求2：统计所有渠道（按照二级渠道）的转化率
解析：

SELECT
c.ca_n,
count(o.clue_id)/count(c.clue_id) sale_rate
FROM
clue_day c
LEFT OUTER JOIN
order_day o
ON o.clue_id = c.clue_id
GROUP BY c.ca_n
order by sale_rate desc
limit 6;


3. 需求3：查询各城市线索数并计算所有城市线索总数

select city_id,count(clue_id) as clue_count from clue_day group by city_id
union all
select '总计' as city_id,count(clue_id) clue_count from clue_day;




WITH ca_value AS (
SELECT
	ca_n,
	avg( DATEDIFF( created_at, clue_created_at ) ) avg_time,
	count( o.clue_id ) clue_num 
FROM
	clue_day c
	LEFT JOIN order_day o ON c.clue_id = o.clue_id 
WHERE
	o.created_at IS NOT NULL 
	AND c.clue_created_at IS NOT NULL 
GROUP BY
	ca_n 
	) SELECT
	ca_n,
	avg_time,
	clue_num 
FROM
	ca_value 
WHERE
	avg_time < (-- 整体线索平均转化周期
SELECT
	avg( DATEDIFF( created_at, clue_created_at ) ) 
FROM
	clue_day c
	LEFT JOIN order_day o ON c.clue_id = o.clue_id 
WHERE
	o.created_at IS NOT NULL 
	AND c.clue_created_at IS NOT NULL 
	) 
	AND clue_num > ( -- 二级渠道平均线索量（需要基于上面select查询进一步avg处理）
	SELECT ceil( avg( clue_num ) ) FROM ca_value );、、、、、、、、、、、、、、、、、、、、