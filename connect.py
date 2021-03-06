import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import time

#engine = create_engine('mysql+pymysql://bwsc:Baiwangr147@rr-2ze2m13n0o7x5cn83zo.mysql.rds.aliyuncs.com:3306/wnmall')
# goods_resource 为1为百望商品  为4为网易商品  为2为京东商品
engine = create_engine('mysql+pymysql://bwsc:Baiwangr147@rm-2ze67hh2abc0d7t0lrw.mysql.rds.aliyuncs.com:3306/wnmall')

def dfInit(starttime,endtime,s):
    # 0.订单号 1.用户下单时间  2买家账号 3店铺名称 4产品名称 5商品id 6商品数量 7商品价格  8运费（元） 9应付金额 7实际支付金额
    #  10抵扣购物积分金额（元） 11优惠金额
    # 12用户付款方式  13赠送银积分数量  14收货省份 15商品结算金额
    # 16平台 0代表微信小程序 5代表ios 6代表安卓 8代表web
    if s==1:
        bwsql = '''select o.order_sn,o.addtime,o.uid,s.store_name,o.seller_id,o.goods_name,o.goods_id,o.quantity,ob.price,o.freight,ob.org_money,o.money,
            ob.integral_cost,ob.platform_coupon_money+ob.dpq_money as discount,
            o.from as payMethod,ob.score_multi_back,o.province,o.seller_money+o.freight seller_money,o.pt
            from wn_order o
            left join 
            wn_seller_info s on o.seller_id = s.seller_id 
        left join
        wn_order_billing ob on o.order_sn=ob.order_sn
        where
        o.goods_id <> 0 and o.goods_resource =  %d AND o.addtime >= %d AND o.addtime<=%d AND o.pay_status = 1 AND o.display_status <> 2 ORDER BY addtime DESC 
            ''' % (s,starttime, endtime)
        df = pd.read_sql_query(bwsql, engine)
    elif s==4:
        wysql = '''select o.order_sn,o.addtime,o.uid,s.store_name,o.seller_id,o.goods_name,o.goods_id,o.quantity,ob.price,o.freight,ob.org_money,o.money,
                    ob.integral_cost,ob.platform_coupon_money+ob.dpq_money as discount,
                    o.from as payMethod,ob.score_multi_back,o.province,o.seller_money+o.freight seller_money,o.pt
                    from wn_order o
                    left join 
                    wn_seller_info s on o.seller_id = s.seller_id 
                left join
                wn_order_billing ob on o.order_sn=ob.order_sn
                where
                o.goods_id <> 0 and o.goods_resource =  %d AND o.addtime >= %d AND o.addtime<=%d AND o.pay_status = 1 AND o.display_status <> 2 ORDER BY addtime DESC 
                    ''' % (s,starttime, endtime)
        df = pd.read_sql_query(wysql, engine)
    elif s == 2:
        jdsql = '''select o.order_sn,o.addtime,o.uid,s.store_name,o.seller_id,o.goods_name,o.goods_id,o.quantity,ob.price,o.freight,ob.org_money,o.money,
                       ob.integral_cost,ob.platform_coupon_money+ob.dpq_money as discount,
                       o.from as payMethod,ob.score_multi_back,o.province,o.seller_money+o.freight seller_money,o.pt
                       from wn_order o
                       left join 
                       wn_seller_info s on o.seller_id = s.seller_id 
                   left join
                   wn_order_billing ob on o.order_sn=ob.order_sn
                   where
                   o.goods_id <> 0 and o.goods_resource = %d AND o.addtime >= %d AND o.addtime<=%d AND o.pay_status = 1 AND o.display_status <> 2 ORDER BY addtime DESC 
                       ''' % (s,starttime, endtime)
        df = pd.read_sql_query(jdsql, engine)
    else:
        qbsql = '''select o.order_sn,o.addtime,o.uid,s.store_name,o.seller_id,o.goods_name,o.goods_id,o.quantity,ob.price,o.freight,ob.org_money,o.money,
                               ob.integral_cost,ob.platform_coupon_money+ob.dpq_money as discount,
                               o.from as payMethod,ob.score_multi_back,o.province,o.seller_money+o.freight seller_money,o.pt
                               from wn_order o
                               left join 
                               wn_seller_info s on o.seller_id = s.seller_id 
                           left join
                           wn_order_billing ob on o.order_sn=ob.order_sn
                           where
                           o.goods_id <> 0 AND o.addtime >= %d AND o.addtime<=%d AND o.pay_status = 1 AND o.display_status <> 2 ORDER BY addtime DESC 
                               ''' % (starttime, endtime)
        df = pd.read_sql_query(qbsql, engine)
    return df




# 统计每日新增用户数量
def xzdfyh(starttime,endtime):

    sql='''SELECT COUNT(1) as c from wn_user as u WHERE u.addtime >= %d and u.addtime <= %d'''%(starttime,endtime)
    df = pd.read_sql_query(sql,engine)
    n=df['c'][0]
    return n
# 统计每日购买会员升级产品数量
def xzdfsj(starttime,endtime):
    sql = '''SELECT order_sn,o.uid from wn_order as o WHERE o.addtime >= %d and o.addtime <= %d and o.pay_status = 1 and o.goods_id=1042106'''%(starttime,endtime)
    df = pd.read_sql_query(sql,engine)
    df.rename(columns={'order_sn': '订单号', 'uid': '用户id'},inplace=True)
    return df

# 通过订单号取日期 返回array类型数据
def difDate(df):
    list1=list(df.order_sn)
    datelist=[]
    for i in range(len(list1)):
        datelist.append(str(list1[i])[6:8])
    datelist=np.array(datelist)
    df['daydate'] = datelist
    return df,list1

def dateAnlysis(df):
    h=difDate(df)
    df=h[0]
    dates=h[1]
    for i in dates:
        dates.append(str(i))
    payMoney=[]
    sellernum=[]
    profit=[]
    for date in dates:
        sellerdf = df[df.daydate == date]
        profit.append(date,(round(round(sum(sellerdf.org_money),2)-round(sum(sellerdf.seller_money),2),2)))
        sellernum.append([date,sellerdf.shape[0]])
        payMoney.append([date,round(sum(sellerdf.payMoney),2)])
    return payMoney,sellernum,profit

def sortDict(t,s):
    l=sorted(t.items(), key=lambda d:d[1], reverse = True)
    ls=[]
    for i in l:
        ls.append([i[0],i[1]])
    if s==0:
        ls=ls[:10]
    return ls

# 不同方式支付的支付金额
def payMethod(df):
    p=df.payMethod
    p=p.where(p.notnull(),'ping_wx')
    p=p.mask(p=='ping_wxxcx','ping_wx')
    p = p.mask(p == 'jsapi', 'ping_wx')
    p = p.mask(p == 'alipay_wap', 'alipay')
    methods=list(set(p))
    df.payMethod=p
    methodnum={}
    for method in methods:
        methoddf=df[df.payMethod==method]
        methodnum[method]=round(sum(methoddf.money),2)
    integral_cost=round(sum(df.integral_cost),2)
    discount=round(sum(df.discount),2)
    if discount!=0:
        methodnum['优惠金额']=discount
    methodnum['购物积分']=integral_cost
    methodnum=sortDict(methodnum,1)
    for meth in methodnum:
        if meth[0]=='erpcoin':
            meth[0]='金积分支付'
        elif meth[0] == 'ping_wx':
            meth[0]='微信支付'
        elif meth[0]=='erpmoney':
            meth[0]='百望余额'
        elif meth[0]=='alipay':
            meth[0]='支付宝支付'
        else:
            meth[0]=meth[0]
    return methodnum

# 商户分析
def seller(df):
    sellers = list(set(df.store_name))
    sellernum={}
    for seller in sellers:
        sellerdf=df[df.store_name==seller]
        sellernum[seller]=round(sum(sellerdf.org_money),2)
    sellernum=sortDict(sellernum,0)
    return sellernum

def sellerMonth(df):
    sellers = list(set(df.store_name))
    sellermoney={}
    sellernum={}
    for seller in sellers:
        sellerdf=df[df.store_name==seller]
        seller=seller+str(sellerdf.iat[0,4])
        sellernum[seller]=sellerdf.shape[0]
        sellermoney[seller]=round(sum(sellerdf.org_money),2)
    sellermoney=sortDict(sellermoney,2)
    sellermoney=sellermoney[:20]
    sellernum = sortDict(sellernum,2)
    sellernum = sellernum[:20]
    return sellermoney,sellernum

def dfqb(dfs):
    df=pd.DataFrame()
    for i in dfs:
        df=df.append(i,ignore_index=True)
    return df
# 统计订单来源
def tjPt(s,e):
    ptsql='''SELECT o.pt ,COUNT(*) as c FROM wn_order o 
          WHERE o.addtime>=%d AND o.addtime<=%d and goods_id!=0 and o.pay_status = 1 GROUP BY o.pt '''%(s,e)
    df = pd.read_sql_query(ptsql, engine)
    pts = list(set(df.pt))
    s=0
    num = [['ios端',0],['web端',0],['安卓端',0],['微信小程序',0],['其他',0]]
    for pt in pts:
        dfpt = df[df.pt == pt]
        if pt == 14 or pt == 0:
            s=s+sum(dfpt.c)
        elif pt == 5:
            num[0]=['ios端',sum(dfpt.c)]
        elif pt == 8:
            num[1]=['web端',sum(dfpt.c)]
        elif pt == 6:
            num[2]=['安卓端', sum(dfpt.c)]
        else:
            num[4]=['其他', sum(dfpt.c)]
    num[3]=['微信小程序',s]
    for i in num:
        if i[1]==0:
            num.remove(i)
    return num

# 统计用户
def tjId(s,e):
    ptsql='''select o.uid,SUM(o.money) as allscore from wn_order o WHERE o.addtime>=%d AND o.addtime<=%d and goods_id!=0 AND o.pay_status = 1 AND o.display_status <> 2 GROUP BY o.uid order by allscore desc '''%(s,e)
    df = pd.read_sql_query(ptsql, engine)
    return df

# 订单来源分析
def pt(df):
    pts=list(set(df.pt))
    num=[]
    for pt in pts:
        dfpt=df[df.pt==pt]
        if pt==14 or pt==0:
            num.append(['微信小程序',dfpt.shape[0]])
        elif pt==5:
            num.append(['ios端',dfpt.shape[0]])
        elif pt==8:
            num.append(['web端',dfpt.shape[0]])
        elif pt==6:
            num.append(['安卓端',dfpt.shape[0]])
        else:
            num.append(['其他',dfpt.shape[0]])
    return num



def sumFun(df):
    # 销售额
    saleMoney=round(sum(df.org_money),2)
    # 订单量
    num=df.shape[0]
    # 营业额
    rateMoney=round(round(sum(df.org_money),2)-round(sum(df.seller_money),2)-round(sum(df.discount),2),2)
    return saleMoney,num,rateMoney

# 查看活动参与人数及支付金额
def Difuyhid(df):
    ids = list(set(df.uid))
    paymoney = {}
    for id in ids:
        sellerdf = df[df.uid == id]
        paymoney[id] = round(sum(sellerdf.org_money),2)
    paymoney = sortDict(paymoney, 0)
    return len(ids),paymoney

# 统计销售前十不同商品id销售数量
def Difuid(df):
    ids = list(set(df.goods_id))
    paymoney = {}
    for id in ids:
        sellerdf = df[df.goods_id == id]
        paymoney[id] = round(sum(sellerdf.quantity),2)
    paymoney = sortDict(paymoney, 1)
    s=1
    if len(paymoney)>=10:
        if paymoney[9][1]:
            s=paymoney[9][1]
        else:
            s=0
    newpay=[]
    if s==1:
        for i in paymoney[:10]:
            if i[1]>1:
                newpay.append(i)
            else:
                break
        paymoney=newpay
    n=0
    if len(paymoney)>10:
        for i in range(9,len(paymoney)+1):
            if paymoney[i][1]==s:
                n=i
            else:
                break
        paymoney=paymoney[:n+1]
    goodNames=[]
    for i in paymoney:
        sellerdf = df[df.goods_id == i[0]]
        s=list(set(sellerdf.goods_name))[0]
        goodNames.append(s)
    return paymoney,goodNames



if __name__ == '__main__':
    # num=xzdfyh(1550160000,1550332800)
    # print(num)
    # df=dfInit(1552924800,1553011199,6)
    # # 1552966817
    # print(payMethod(df))
    date = input('请输入时间：')
    startdate = date + ' 0:0:0'
    enddate = date + ' 23:59:59'
    starttime = time.strptime(startdate, "%Y-%m-%d %H:%M:%S")
    starttime = int(time.mktime(starttime))
    endtime = time.strptime(enddate, "%Y-%m-%d %H:%M:%S")
    endtime = int(time.mktime(endtime))
    df=dfInit(starttime,endtime,7)
    # if df.shape[0] != 0:
    #     print('会员升级产品订单：')
    #     print(df)
    # else:
    #     print(date + '号无人购买会员升级产品')
    m=payMethod(df)
    print(m)