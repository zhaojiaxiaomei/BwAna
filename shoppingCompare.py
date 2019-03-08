# 和上一个购物节的对比折线图
# 比较下秋冬季两个购物节支付方式比例有没有什么变化
import matplotlib.pyplot as plt
from connectMysql.shoppingConnect import reDf,HandleTime,dfqb
import time


def sortDict(t,s):
    l=sorted(t.items(), key=lambda d:d[1], reverse = True)
    ls=[]
    for i in l:
        ls.append([i[0],i[1]])
    if s==0:
        ls=ls[:10]
    return ls


def payMethod(df):
    methods=list(set(df.payMethod))
    methodnum={}
    for method in methods:
        methoddf=df[df.payMethod==method]
        methodnum[method]=round(sum(methoddf.money),2)
    integral_cost=round(sum(df.integral_cost),2)
    discount=round(sum(df.discount),2)
    if discount!=0:
        methodnum['优惠']=discount
    methodnum['购物积分']=integral_cost
    methodnum=sortDict(methodnum,1)
    for meth in methodnum:
        if meth[0]=='erpcoin':
            meth[0]='金积分'
        elif meth[0]=='jsapi' or meth[0]=='ping_wx':
            meth[0]='微信'
        elif meth[0]=='erpmoney':
            meth[0]='余额'
        elif meth[0]=='alipay' or meth[0]=='alipay_wap':
            meth[0]='支付宝'
        else:
            meth[0]=meth[0]
    wx = 0
    for i in methodnum:
        if '微信' in i[0]:
            wx += i[1]
            methodnum.remove(i)
    methodnum.append(('微信', wx))
    return methodnum

def payMeth(meth):
    new=[['购物积分',0],['微信',0],['支付宝',0],['金积分',0],['优惠',0],['余额',0]]
    summ=sum([i[1] for i in meth])
    for m in meth:
        for j in new:
            if m[0]==j[0]:
                j[1]=round(m[1]/summ*100,2)
    for i in range(6):
        new[i][0]=i+1
    return new
def reNum(dfs):
    # 销售数量
    dfn=[]
    dfp=[]
    dfy=[]
    for df in dfs:
        dfn.append([df[0],df[1].shape[0]])
        dfp.append([df[0],round(sum(df[1].org_money),2)])
        dfy.append([df[0],round(round(sum(df[1].org_money),2)-round(sum(df[1].seller_money),2),2)])
    return dfn,dfp,dfy


def printN(date0,dfn0,date1,dfn1):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    sum0=sum([i[1] for i in dfn0])
    sum1 = sum([i[1] for i in dfn1])
    plt.plot([i[0] for i in dfn0], [i[1] for i in dfn0], alpha=0.7, c='blue',label=date0+':'+str(sum0))
    plt.plot([i[0] for i in dfn1], [i[1] for i in dfn1], alpha=0.7, c='red',label=date1+':'+str(sum1))
    for i in dfn0:
        plt.text(i[0], i[1], i[1], color='b')
    for i in dfn1:
        plt.text(i[0] ,i[1], i[1], color='r')
    plt.xlabel('日期')
    plt.legend()
    plt.ylabel('数量')
    plt.annotate(r'$author:zxz$', (13, 0), color='#C4C4C4')
    plt.title('百望商城'+date0+'|'+date1+'购物节每日订单')
    plt.show()



def printLr(date0,dfn0,date1,dfn1):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    sum0 = sum([i[1] for i in dfn0])
    sum1 = sum([i[1] for i in dfn1])
    plt.plot([i[0] for i in dfn0], [i[1] for i in dfn0], alpha=0.7, c='blue', label=date0 + ':' + str(sum0))
    plt.plot([i[0] for i in dfn1], [i[1] for i in dfn1], alpha=0.7, c='red', label=date1 + ':' + str(sum1))
    for i in dfn0:
        plt.text(i[0]-0.2, i[1]+1, i[1], color='b')
    for i in dfn1:
        plt.text(i[0]-0.2, i[1]+1, i[1], color='r')
    plt.xlabel('日期')
    plt.legend()
    plt.ylabel('金额（元）')
    plt.annotate(r'$author:zxz$', (13, 0), color='#C4C4C4')
    plt.title('百望商城' + date0 + '|' + date1 + '购物节每日利润')
    plt.show()



def printXs(date0,dfn0,date1,dfn1):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    sum0 = sum([i[1] for i in dfn0])
    sum1 = sum([i[1] for i in dfn1])
    plt.plot([i[0] for i in dfn0], [i[1] for i in dfn0], alpha=0.7, c='blue', label=date0 + ':' + str(sum0))
    plt.plot([i[0] for i in dfn1], [i[1] for i in dfn1], alpha=0.7, c='red', label=date1 + ':' + str(sum1))
    for i in dfn0:
        plt.text(i[0]-0.2, i[1]+1, i[1], color='b')
    for i in dfn1:
        plt.text(i[0]-0.2, i[1]+1, i[1], color='r')
    plt.xlabel('日期')
    plt.legend()
    plt.ylabel('金额（元）')
    plt.annotate(r'$author:zxz$', (13, 0), color='#C4C4C4')
    plt.title('百望商城' + date0 + '|' + date1 + '购物节每日销售额')
    plt.show()


def printpayMethod(date0,dfn0,date1,dfn1):
    m0=payMethod(dfn0)
    m0=payMeth(m0)
    m1 = payMethod(dfn1)
    m1 = payMeth(m1)
    plt.bar([i[0]-0.2 for i in m0], [i[1] for i in m0], alpha=0.9, width=0.4, edgecolor='white', label=date0, lw=1)
    plt.bar([i[0]+0.2 for i in m1], [i[1] for i in m1], alpha=0.9, width=0.4, edgecolor='white', label=date1, lw=1)
    for i in m0:
        plt.text(i[0]-0.4, i[1], i[1], color='b')
    for i in m1:
        plt.text(i[0], i[1], i[1], color='r')
    plt.xlabel('支付方式')
    plt.legend()
    plt.ylabel('比例(%)')
    plt.ylim(0,50)
    plt.annotate(r'$author:zxz$', (1, 0), color='#C4C4C4')
    plt.xticks([1,2,3,4,5,6],['购物积分','微信','支付宝','金积分','优惠','余额'])
    plt.title('百望商城' + date0 + '|' + date1 + '购物节支付方式比例')
    plt.show()


if __name__ == '__main__':
    date0 = input('请输入那个季节：')
    s0 = input('请输入年及月份：')
    s0 = s0 + '-13' + ' 0:0:0'
    starttime0 = time.strptime(s0, "%Y-%m-%d %H:%M:%S")
    starttime0 = int(time.mktime(starttime0))
    times0 = HandleTime(starttime0)
    date1 = input('请输入那个季节：')
    s1 = input('请输入年及月份：')
    s1 = s1 + '-13' + ' 0:0:0'
    starttime1 = time.strptime(s1, "%Y-%m-%d %H:%M:%S")
    starttime1 = int(time.mktime(starttime1))
    times1 = HandleTime(starttime1)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    dfs0 = reDf(times0)
    dfs1 = reDf(times1)
    dfqb0=dfqb(dfs0)
    dfqb1 = dfqb(dfs1)
    df0=reNum(dfs0)
    df1=reNum(dfs1)
    printN(date0,df0[0],date1,df1[0])
    printXs(date0,df0[1],date1,df1[1])
    printLr(date0, df0[2], date1, df1[2])
    printpayMethod(date0,dfqb0,date1,dfqb1)
    # h=payMethod(dfqb0)
    # print(h)
    # m=payMeth(h)
    # print(m)
