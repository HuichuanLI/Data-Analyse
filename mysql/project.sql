增加新列date_time（datetime）,dates（char，年⽉⽇），便于后续时间维度分析；

-- 增加新列date_time、dates
alter table o_retailers_trade_user add column date_time datetime null;
update o_retailers_trade_user
set date_time =str_to_date(time,'%Y-%m-%d %H') ;
-- %H可以表示0-23；⽽%h表示0-12
alter table o_retailers_trade_user add column dates char(10) null;
update o_retailers_trade_user
set dates=date(date_time);
desc o_retailers_trade_user;
select * from o_retailers_trade_user limit 5;

重复值处理：创建新表a，并插⼊5W条⽆重复数据
create table temp_trade like o_retailers_trade_user;
insert into temp_trade select distinct * from o_retailers_trade_user limit
50000;

uv、pv、留存率（按⽇）统计
-- pv 进⾏cout时候，如果behavior_type=1进⾏计算，如果不是，不进⾏计算
select
dates,
count( distinct user_id ) as 'uv',
count( if(behavior_type=1,user_id,null)) as 'pv',
count( if(behavior_type=1,user_id,null))/count( distinct user_id ) as
'pv/uv'
from
temp_trade
group by
dates;

-- ⽤户留存
with temp_table_trades as
(select a.dates
,count(distinct b.user_id) as device_v
,count(distinct if(datediff(b.dates,a.dates)=0,b.user_id,null)) as
device_v_remain0
,count(distinct if(datediff(b.dates,a.dates)=1,b.user_id,null)) as
device_v_remain1
,count(distinct if(datediff(b.dates,a.dates)=2,b.user_id,null)) as
device_v_remain2
,count(distinct if(datediff(b.dates,a.dates)=3,b.user_id,null)) as
device_v_remain3
,count(distinct if(datediff(b.dates,a.dates)=4,b.user_id,null)) as
device_v_remain4
,count(distinct if(datediff(b.dates,a.dates)=5,b.user_id,null)) as
device_v_remain5
,count(distinct if(datediff(b.dates,a.dates)=6,b.user_id,null)) as
device_v_remain6
,count(distinct if(datediff(b.dates,a.dates)=7,b.user_id,null)) as
device_v_remain7
,count(distinct if(datediff(b.dates,a.dates)=15,b.user_id,null)) as
device_v_remain15
,count(distinct if(datediff(b.dates,a.dates)=30,b.user_id,null)) as
device_v_remain30
from
(select
user_id
,dates
from
temp_trade
group by
user_id
,dates ) a
left join
(
select
dates
,user_id
from temp_trade
GROUP BY dates,user_id
) b on a.user_id = b.user_id
where b.dates >= a.dates
group by a.dates)
select dates, device_v_remain0,
concat(cast((device_v_remain1/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_1%',
concat(cast((device_v_remain2/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_2%',
concat(cast((device_v_remain3/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_3%',
concat(cast((device_v_remain4/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_4%',
concat(cast((device_v_remain5/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_5%',
concat(cast((device_v_remain6/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_6%',
concat(cast((device_v_remain7/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_7%',
concat(cast((device_v_remain15/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_15%',
concat(cast((device_v_remain30/device_v_remain0)*100 as DECIMAL(18,2)),'%') as
'day_30%'
from temp_table_trades;



1.RFM模型：R部分

-- RFM模型
-- 1.建⽴r视图，将近期购买时间提取到R临时表中
drop view if EXISTS user_recency;
create view user_Recency
as
select user_id ,max(dates) as rec_buy_time
from temp_trade
where behavior_type='2'
group by user_id
order by rec_buy_time desc;
--