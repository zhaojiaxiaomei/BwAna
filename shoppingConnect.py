# 返回每天的df
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import time

engine = create_engine('mysql+pymysql://bwsc:Baiwangr147@rr-2ze2m13n0o7x5cn83zo.mysql.rds.aliyuncs.com:3306/wnmall')

def HandleTime(starttime):
    times=[]
    for i in range(13,21):
        times.append([starttime, starttime + 86399,i])
        starttime = starttime + 86400
    return times

def sortDict(t,s):
    l=sorted(t.items(), key=lambda d:d[1], reverse = True)
    ls=[]
    for i in l:
        ls.append([i[0],i[1]])
    if s==0:
        ls=ls[:10]
    return ls

def reDf(times):
    dfs=[]
    for i in times:
    # goods_resource为1是百望 为4网易 为2为京东
        qbsql = '''select o.order_sn,o.addtime,o.uid,s.store_name,o.goods_name,o.goods_id,o.quantity,ob.price,o.freight,ob.org_money,o.money,
                                   ob.integral_cost,ob.platform_coupon_money+ob.dpq_money as discount,
                                   o.from as payMethod,ob.score_multi_back,o.province,o.seller_money+o.freight seller_money,o.goods_resource
                                   from wn_order o
                                   left join 
                                   wn_seller_info s on o.seller_id = s.seller_id 
                               left join
                               wn_order_billing ob on o.order_sn=ob.order_sn
                               where
                               o.goods_id <> 0 AND o.addtime >= %d AND o.addtime<=%d AND o.pay_status = 1 AND o.display_status <> 2 ORDER BY addtime DESC 
                                   ''' % (i[0], i[1])
        df = pd.read_sql_query(qbsql, engine)
        df['date']=i[2]
        dfs.append([i[2],df])
    return dfs

def dfqb(dfs):
    df=pd.DataFrame()
    for i in dfs:
        df=df.append(i[1],ignore_index=True)
    return df


# 统计百望自营销售数量前10商品
# 统计京东销售数量前10商品
# 统计销售前十不同商品id销售数量
def Difuid(df):
    ids = list(set(df.goods_id))
    paymoney = {}
    for id in ids:
        sellerdf = df[df.goods_id == id]
        paymoney[id] = round(sum(sellerdf.quantity),2)
    paymoney = sortDict(paymoney, 1)
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
        for i in range(10,len(paymoney)+1):
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


# 统计参与人数 并统计购买力前10客户 bar
def difyhid(df):
    ids = list(set(df.uid))
    paymoney = {}
    for id in ids:
        sellerdf = df[df.uid == id]
        paymoney[id] = round(sum(sellerdf.org_money), 2)
    paymoney = sortDict(paymoney, 0)
    return len(ids), paymoney

# 支付方式 pie
def payMethod(df):
    methods=list(set(df.payMethod))
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
        elif meth[0]=='jsapi' or meth[0]=='ping_wx':
            meth[0]='微信支付'
        elif meth[0]=='erpmoney':
            meth[0]='百望余额'
        elif meth[0]=='alipay' or meth[0]=='alipay_wap':
            meth[0]='支付宝支付'
        else:
            meth[0]=meth[0]
    return methodnum



def dffk(dfs):
    jddfs=[]
    bwdfs=[]
    wydfs=[]
    for i in dfs:
        jddfs.append([i[0],i[1][i[1].goods_resource==2]])
        bwdfs.append([i[0],i[1][i[1].goods_resource==1]])
        wydfs.append([i[0],i[1][i[1].goods_resource==4]])
    return bwdfs,jddfs,wydfs

def seller(df):
    sellers = list(set(df.store_name))
    sellernum={}
    for seller in sellers:
        sellerdf=df[df.store_name==seller]
        sellernum[seller]=round(sum(sellerdf.org_money),2)
    sellernum=sortDict(sellernum,0)
    return sellernum




# 统计每日新增用户数量
def xzdfyh(times):
    xz=[]
    for i in times:
        sql='''SELECT COUNT(1) as c from wn_user as u WHERE u.addtime >= %d and u.addtime <= %d'''%(i[0],i[1])
        df = pd.read_sql_query(sql,engine)
        n=df['c'][0]
        xz.append([i[2],n])
    return xz

def ord(dfl):
    newl=[]
    orgMoney=[]
    for d in dfl:
        newl.append([d[0],d[1].shape[0]])
        orgMoney.append([d[0],round(sum(d[1].org_money),2)])
    return newl,orgMoney

def calLr(dfs):
    lr=[]
    for df in dfs:
        rate=round(round(sum(df[1].org_money),2)-round(sum(df[1].seller_money),2)-round(sum(df[1].discount),2),2)
        money=round(sum(df[1].org_money),2)
        if rate!=0:
            lr.append([df[0],rate,money,round(rate/money*100,2)])
    return lr

if __name__ == '__main__':
    s=input('请输入年及月份：')
    s=s+'-13'+' 0:0:0'
    starttime = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    starttime = int(time.mktime(starttime))
    times=HandleTime(starttime)
    # xz=xzdfyh(times)
    # print(xz)
    # dfs=reDf(times)
    # df=dfqb(dfs)
    # yh=difyhid(df)
    # print(yh[0])
    # print(yh[1])
    # 分析购买力最高的客户的购物的支付方式 pie
    # maxdf=df[df.uid == yh[1][0][0]]
    # pay=payMethod(maxdf)
    # print(pay)
    print(xzdfyh(times))