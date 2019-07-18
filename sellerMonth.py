# 输出商家销售额高的前20商家
# 输出商家单量高的前20商家
from connectMysql.connect import dfInit,dfqb,sellerMonth
import time
import matplotlib.pyplot as plt

def times(starttime,jx):
    times=[]
    for i in range(jx):
        timeArray = time.localtime(starttime)
        otherStyleTime = int(time.strftime("%Y/%m/%d %H:%M:%S", timeArray)[8:10])
        times.append([starttime, starttime+86399,otherStyleTime])
        starttime = starttime + 86400
    return times

def printSeller(seller,date):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    s=seller[0]
    sname = [i[0] for i in s]
    scolleges = [i[1] for i in s]
    smax=max(scolleges)
    fig, ax = plt.subplots()
    fig.tight_layout()
    b = ax.barh(range(len(sname)), scolleges, color='#9ACD32')
    for rect in b:
        w = rect.get_width()
        if w==smax:
            ax.text(w-15000, rect.get_y() + rect.get_height() / 2, w, ha='left', va='center', color='#C71585')
        else:
            ax.text(w, rect.get_y() + rect.get_height() / 2, w, ha='left', va='center', color='#C71585')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xlabel('销售额（元）')
    plt.ylabel('商户名称+ID')
    # plt.xlim([0,int(max(scolleges))+23000])
    plt.title(date + '月份百望商城销售额前20商家')
    ax.set_yticks(range(len(sname)))
    ax.set_yticklabels(sname)
    plt.annotate(r'$author:zxz$', (250, 0), color='#C4C4C4')
    plt.show()

    # plt.figure()
    # s = seller[1]
    # sname = [i[0] for i in s]
    # scolleges = [i[1] for i in s]
    # fig, ax = plt.subplots()
    # fig.tight_layout()
    # b = ax.barh(range(len(sname)), scolleges, color='#4682B4')
    # for rect in b:
    #     w = rect.get_width()
    #     ax.text(w, rect.get_y() + rect.get_height() / 2, w, ha='left', va='center', color='#008B8B')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.xlabel('订单量')
    # plt.ylabel('商户名称+ID')
    # plt.title(date + '月份百望商城订单量前20商家')
    # ax.set_yticks(range(len(sname)))
    # ax.set_yticklabels(sname)
    # plt.annotate(r'$author:zxz$', (250, 0), color='#C4C4C4')
    # plt.show()

if __name__ == '__main__':
    sdate = input('请输入开始时间：')
    jx = int(input('请输入间隙时间：'))
    date = input('请输入时间：')
    startdate = sdate + ' 0:0:0'
    starttime = time.strptime(startdate, "%Y-%m-%d %H:%M:%S")
    starttime = int(time.mktime(starttime))
    timess = times(starttime, jx)
    dfs=[]
    for t in timess:
        dfs.append(dfInit(t[0],t[1],1))
    dfqb=dfqb(dfs)
    seller=sellerMonth(dfqb)
    print('销售额：')
    print(seller[0])
    print('订单量：')
    print(seller[1])
    printSeller(seller,date)
