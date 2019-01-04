import pandas as pd
import numpy as np

def OrderInit(strl):
    # 读取文件 并得到相应的数值
    # 2用户下单时间 3买家手机号 4买家账号 8店铺名称 9产品类型（一级类目） 13商品id 16商品数量 17商品总价（元） 18应付金额 19运费（元） 23抵扣购物积分金额（元） 24实付现金金额（元）
    # 25用户付款方式  29赠送银积分数量  41收货省份 45商品结算金额
    listread = [2, 3, 4, 6, 8, 9, 13, 16, 17, 18, 19, 22, 23, 24, 25, 29, 41, 45]
    df=pd.DataFrame()
    for str in strl:
        df0 = pd.read_csv(str+'.csv', usecols=listread)
        df0.dropna(axis=0, how='any', inplace=True)
        df.append(df0)
    df.rename(columns={'用户下单时间':'dateTime','买家手机号': 'mobile', '买家账号': 'uid', '订单编号':'orderId','店铺名称': 'sellername',
                       '产品类型(一级类目)': 'goodType', '商品id': 'goodId', '商品数量（件）': 'goodNum',
                       '商品总价（元）': 'goodPrice', '应付金额': 'payMoney',
                       '运费（元）': 'freight','优惠金额':'discount', '抵扣购物积分金额（元）': 'shopIntergration',
                       '实付现金金额（元）': 'realPaymoney', '用户付款方式': 'payMethod',
                       '赠送银积分数量': 'giveIntegration', '收货省份': 'recivePrivince', '商户结算金额': 'settlement'},
              inplace=True)
    return df

def initJd():
    strljd=['jd13-16','jd17-18','jd19','jd20']
    jddf=OrderInit(strljd)
    return jddf

def initBw():
    strlbw=['bw13-18','bw19-20']
    bwdf=OrderInit(strlbw)
    num=bwdf.shape[0]
    bwdf=bwdf[bwdf['sellername'] != '赵家小妹']
    num1=bwdf.shape[0]
    num2=num-num1
    return num,num2,bwdf

# 查看新人有礼商品购买情况 df为百望bwdf
def newGood(df):
    df=df[df.goodId==1030552]
    num1=df.shape[0]
    df2=df[df.giveIntegration==180000]
    num2=df2.shape[0]
    return num1,num2

def initWy():
    strlwy=['wy13-20']
    wydf=OrderInit(strlwy)
    return wydf

def initFull():
    jddf=initJd()
    bwdf=initBw()[2]
    wydf=initWy()
    df=jddf.append(bwdf)
    df=df.append(wydf)
    return df

# 对字典数据进行降序排序 并返回字典
def sortDict(t,s):
    l=sorted(t.items(), key=lambda d:d[1], reverse = True)
    if s==0:
        l=l[:10]
    newDict={}
    for i in l:
        newDict[i[0]]=i[1]
    return newDict

def resortDict(t):
    l=sorted(t.items(), key=lambda d:d[1], reverse = False)
    return l

def DictToList(t):
    l=sorted(t.items(), key=lambda d:d[1], reverse = True)
    return l

# 求和统计
def sumCal(df):
    # 赠送银积分
    integration=round(sum(df.giveIntegration),2)
    # 使用购物积分抵扣金额
    shopIntergration=round(sum(df.shopIntergration),2)
    # 商品数量
    goodNum=round(sum(df.goodNum),2)
    # 应付金额
    payMoney=round(sum(df.payMoney),2)
    # 实付现金金额
    realPaymoney=round(sum(df.realPaymoney),2)
    # 优惠金额
    discount=round(sum(df.discount),2)
    # 商家结算金额
    settlement=round(sum(df.settlement),2)
    return integration,shopIntergration,discount,goodNum,payMoney,realPaymoney,settlement

 # 不同方式支付的支付金额
def payMethod(df):
    methods=list(set(df.payMethod))
    methodnum={}
    for method in methods:
        methoddf=df[df.payMethod==method]
        methodnum[method]=round(sum(methoddf.realPaymoney),2)
    methodnum=sortDict(methodnum,1)
    return methodnum

# 查看活动参与人数及支付金额
def Difuid(df):
    ids = list(set(df.uid))
    paymoney = {}
    for id in ids:
        sellerdf = df[df.uid == id]
        paymoney[id] = round(sum(sellerdf.payMoney),2)
    paymoney = sortDict(paymoney, 0)
    return len(ids),paymoney

# 通过订单号取日期 返回array类型数据
def difDate(df):
    list1=list(df.orderId)
    datelist=[]
    for i in range(len(list1)):
        datelist.append(str(list1[i])[6:8])
    datelist=np.array(datelist)
    return datelist


def dataAnlysis(df):
    df['daydate']=difDate(df)
    dates=[]
    for i in range(13,21):
        dates.append(str(i))
    payMoney=[]
    sellernum=[]
    profit={}
    for date in dates:
        sellerdf = df[df.daydate == date]
        # settlement payMoney
        profit[date]=round(round(sum(sellerdf.payMoney),2)-round(sum(sellerdf.settlement),2),2)
        sellernum.append((date,sellerdf.shape[0]))
        payMoney.append((date,round(sum(sellerdf.payMoney),2)))
    return payMoney,sellernum,profit

# 收货省份分析
def provinceAna(df):
    ids = list(set(df.recivePrivince))
    num={}
    for id in ids:
        dfp=df[df.recivePrivince==id]
        num[id]=dfp.shape[0]
    num=resortDict(num)
    return num

if __name__ == '__main__':
    pass