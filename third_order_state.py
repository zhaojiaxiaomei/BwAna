from sqlalchemy import create_engine
import time
import pandas as pd
engine = create_engine('mysql+pymysql://bwsc:Baiwangr147@rr-2ze2m13n0o7x5cn83zo.mysql.rds.aliyuncs.com:3306/wnmall')
starttime = input('请输入开始时间：')
starttime=starttime+' 0:0:0'
starttime = time.strptime(starttime, "%Y-%m-%d %H:%M:%S")
starttime = int(time.mktime(starttime))
endtime=input('请输入结束时间：')
endtime=endtime+' 23:59:59'
# print(endtime)
endtime=time.strptime(endtime,"%Y-%m-%d %H:%M:%S")
endtime=int(time.mktime(endtime))
jdsql = '''select o.order_sn,o.addtime,o.uid,s.store_name,o.goods_name,o.goods_id,o.quantity,ob.price,o.freight,ob.org_money,o.money,
                       ob.integral_cost,ob.platform_coupon_money+ob.dpq_money as discount,
                       o.from as payMethod,ob.score_multi_back,o.province,o.seller_money+o.freight seller_money
                       from wn_order o
                       left join 
                       wn_seller_info s on o.seller_id = s.seller_id 
                   left join
                   wn_order_billing ob on o.order_sn=ob.order_sn
                   where
                   o.goods_id <> 0 and o.goods_resource = 2 and o.third_order_state=2 AND o.addtime >= %d AND
                    o.addtime<=%d AND o.pay_status = 1 AND o.display_status <> 2 ORDER BY addtime DESC 
                       ''' % (starttime,endtime)
df = pd.read_sql_query(jdsql, engine)
print(round(sum(df.seller_money),2))
