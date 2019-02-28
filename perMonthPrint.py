# 输出每天的新注册用户情况
# 输出订单分布情况
# 输出每天的销售额情况和利润
import matplotlib.pyplot as plt
from connectMysql.connect import dfInit,xzdfyh
import time
import numpy as np


# 划分功能
def times(starttime,jx):
    times=[]
    if jx==7:
        for i in range(jx):
            times.append([starttime, starttime + 86399, i+1])
            starttime = starttime + 86400
    else:
        for i in range(jx):
            timeArray = time.localtime(starttime)
            otherStyleTime = int(time.strftime("%Y/%m/%d %H:%M:%S", timeArray)[8:10])
            times.append([starttime, starttime+86399,otherStyleTime])
            starttime = starttime + 86400
    return times


def fx(times,lx):
    nums,payMoney,sellerMoney,rateMoney,xznums=[],[],[],[],[]
    for i in times:
        df = dfInit(i[0], i[1], lx)
        nums.append([i[2], df.shape[0]])
        org = round(sum(df.org_money), 2)
        seller = round(sum(df.seller_money), 2)
        payMoney.append([i[2], org])
        rate = round(org - seller, 2)
        sellerMoney.append([i[2], seller])
        rateMoney.append([i[2], rate])
    return nums,payMoney,sellerMoney,rateMoney


def printT(date,bw,jd,wy):
    plt.rcParams['font.sans-serif']=['SimHei']
    bwnums=bw[0]
    bwpayMoney=bw[1]
    bwsellerMoney=bw[2]
    bwrateMoney=bw[3]
    jdnums=jd[0]
    jdpayMoney = jd[1]
    jdsellerMoney = jd[2]
    jdrateMoney = jd[3]
    wynums = wy[0]
    wypayMoney = wy[1]
    wysellerMoney = wy[2]
    wyrateMoney = wy[3]
    plt.figure()
    plt.bar([i[0] for i in bwnums ],[i[1] for i in bwnums],label='百望')
    plt.bar([i[0] for i in jdnums ],[i[1] for i in jdnums],bottom=[i[1] for i in bwnums],label='京东')
    plt.bar([i[0] for i in wynums ],[i[1] for i in wynums],bottom=np.array([i[1] for i in bwnums])+np.array([i[1] for i in jdnums]),label='网易')
    suml=[]
    for i in range(jx):
        suml.append([bwnums[i][0],bwnums[i][1]+jdnums[i][1]+wynums[i][1]])
    for i in suml:
        plt.text(i[0],i[1]+5,i[1],fontsize=8,ha='center',va='center')
    plt.text(min([i[0] for i in suml]),0,r'$author:zxz$',fontdict={'size':10,'color':'#C4C4C4'})
    plt.title(date+'月份百望商城每天订单情况 总订单：'+str(sum([i[1] for i in suml])))
    plt.xlabel('日期')
    plt.xticks([i[0] for i in bwnums])
    plt.ylabel('订单数量')
    plt.savefig(date+'每日订单.png')
    plt.legend()

    plt.figure(figsize=(9,6))
    sumrate=[[bwrateMoney[i][0],round(bwrateMoney[i][1]+jdrateMoney[i][1]+wyrateMoney[i][1],2)] for i in range(jx)]
    sumpay=[[bwpayMoney[i][0],round(bwpayMoney[i][1]+jdpayMoney[i][1]+wypayMoney[i][1],2)] for i in range(jx)]
    sumseller=[[bwsellerMoney[i][0],round(bwsellerMoney[i][1]+jdsellerMoney[i][1]+wysellerMoney[i][1],2)] for i in range(jx)]
    plt.bar([i[0] for i in sumrate],[i[1] for i in sumrate],label='利润')
    plt.bar([i[0] for i in sumseller],[i[1] for i in sumseller],bottom=[i[1] for i in sumrate])
    plt.title(date+'月份百望商城每天销售额情况 总销售额：'+str(round(sum([i[1] for i in sumpay]),2)))
    plt.xlabel('日期')
    for i in sumpay:
        if int(i[0])%2==0:
            plt.text(i[0], i[1] + 2500, i[1], fontsize=6, ha='center', va='center',color='b')
        else:
            plt.text(i[0], i[1] + 1500, i[1], fontsize=6, ha='center', va='center', color='b')
    for i in sumrate:
        plt.text(i[0], i[1] + 2500, i[1], fontsize=6, ha='center', va='center',color='b')
    plt.text(min([i[0] for i in suml]),0,r'$author:zxz$',fontdict={'size':10,'color':'#C4C4C4'})
    plt.ylabel('金额（元）')
    plt.xticks([i[0] for i in sumseller])
    plt.savefig(date+'销售额.png')
    plt.legend()
    plt.show()


# 绘制每日新注册用户情况
def printXzyh(times,d):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    nums=[]
    for i in times:
        s=xzdfyh(i[0],i[1])
        nums.append([i[2],s])
    plt.bar([i[0] for i in nums],[i[1] for i in nums],alpha=0.9, width=0.8)
    for i in nums:
        plt.text(i[0],i[1]+0.5,i[1],fontsize=8, ha='center', va='center')
    plt.ylabel('人数')
    plt.xlabel('日期')
    plt.title(d + '月份百望商城每天新人注册情况 总注册人数：'+str(sum([i[1] for i in nums])))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.xticks([i[0] for i in nums])
    plt.text(1, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

if __name__ == '__main__':
    sdate = input('请输入开始时间：')
    jx = int(input('请输入间隙时间：'))
    date = input('请输入时间：')
    startdate = sdate + ' 0:0:0'
    starttime = time.strptime(startdate, "%Y-%m-%d %H:%M:%S")
    starttime = int(time.mktime(starttime))
    timess = times(starttime,jx)
    # print(timess)
    bw = fx(timess, 1)
    jd = fx(timess, 2)
    wy = fx(timess, 4)
    printT(date,bw,jd,wy)
    printXzyh(timess,date)