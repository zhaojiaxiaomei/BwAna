# 春季购物清零节每年的36912月份13-20号统计
# 统计参与人数 并统计购买力前10客户 bar（完成）
# 支付方式 pie （完成）
# 统计每天新注册的客户情况 bar （完成）
# 统计百望自营销售数量前10商品 （完成）
# 统计京东销售数量前10商品 （完成）
# 每天的京东网易百望订单分析 bar (完成)
# 每天的京东网易百望销售额分析 bar（完成）
# 每天的京东网易百望营业额分析 bar（完成）
# 商家销售额前10商家 bar （完成）
# 每日下单人次图 bar(完成)
# 输出每日的利润率及分利润(完成)

import matplotlib.pyplot as plt
from connectMysql.shoppingConnect import reDf,HandleTime,xzdfyh,payMethod,dfqb
from connectMysql.shoppingConnect import difyhid,Difuid,seller,dffk,ord,calLr
import time


# 打印每天的订单量
def printOrNu(date,dfs,num,pay):
    # bwdfs, jddfs, wydfs
    bwdfs=dfs[0]
    jddfs=dfs[1]
    wydfs=dfs[2]
    bw = ord(bwdfs)
    jd = ord(jddfs)
    wy = ord(wydfs)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    # 获取df的df.shape[0]行数
    bwl=bw[0]
    jdl=jd[0]
    wyl=wy[0]
    plt.bar([i[0] - 0.2 for i in bwl], [i[1] for i in bwl], alpha=0.9, width=0.2, edgecolor='white', label='百望',
            lw=1)
    plt.bar([i[0] for i in jdl], [i[1] for i in jdl], alpha=0.9, width=0.2, edgecolor='white', label='京东', lw=1)
    plt.bar([i[0] + 0.2 for i in wyl], [i[1] for i in wyl], alpha=0.9, width=0.2, edgecolor='white', label='网易',
            lw=1)
    for i in bwl:
        plt.text(i[0] - 0.2, i[1] + 10, i[1], color='#00BFFF', fontsize=10, ha='center', va='center')
    for i in jdl:
        plt.text(i[0], i[1] + 10, i[1], color='#FF8C00', fontsize=10, ha='center', va='center')
    for i in wyl:
        plt.text(i[0] + 0.2, i[1] + 10, i[1], color='#006400', fontsize=10, ha='center', va='center')
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.ylabel('数量')
    plt.xlabel('日期')
    plt.title('百望商城'+date + '购物节每日订单情况 总订单量'+str(num))
    plt.legend()
    plt.show()

    plt.figure()
    bwp = bw[1]
    jdp = jd[1]
    wyp = wy[1]
    plt.bar([i[0] - 0.2 for i in bwp], [i[1] for i in bwp], alpha=0.9, width=0.2, edgecolor='white', label='百望',lw=1)
    plt.bar([i[0] for i in jdp], [i[1] for i in jdp], alpha=0.9, width=0.2, edgecolor='white', label='京东', lw=1)
    plt.bar([i[0] + 0.2 for i in wyp], [i[1] for i in wyp], alpha=0.9, width=0.2, edgecolor='white', label='网易',lw=1)
    for i in bwp:
        plt.text(i[0] - 0.2, i[1] + 10, i[1], color='#00BFFF', fontsize=10, ha='center', va='center')
    for i in jdp:
        plt.text(i[0], i[1] + 10, i[1], color='#FF8C00', fontsize=10, ha='center', va='center')
    for i in wyp:
        plt.text(i[0] + 0.2, i[1] + 10, i[1], color='#006400', fontsize=10, ha='center', va='center')
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.ylabel('销售额（元）')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日销售额 总销售额' + str(pay))
    plt.legend()
    plt.show()


def printsj(date,df):
    bwdf=df[df.goods_resource==1]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    s = seller(bwdf)
    s.reverse()
    sname = [i[0] for i in s]
    scolleges = [i[1] for i in s]
    fig, ax = plt.subplots()
    fig.tight_layout()
    b = ax.barh(range(len(sname)), scolleges, color='#4682B4')
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, w, ha='left', va='center', color='#008B8B')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xlabel('销售额（元）')
    plt.ylabel('商户名称')
    plt.title('百望商城'+date + '购物节销售额前10商家')
    ax.set_yticks(range(len(sname)))
    ax.set_yticklabels(sname)
    plt.annotate(r'$author:zxz$', (250, 0), color='#C4C4C4')
    plt.show()

def printbw(date,df):
    bwdf = df[df.goods_resource == 1]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    ls = Difuid(bwdf)
    l = ls[0]
    xl = l.copy()
    goodName = ls[1]
    l.reverse()
    name = [i[0] for i in l]
    colleges = [i[1] for i in l]
    fig, ax = plt.subplots()
    fig.tight_layout()
    b = ax.barh(range(len(name)), colleges)
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, w, ha='left', va='center', color='#008B8B')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xlabel('销售数量')
    plt.ylabel('商品id')
    plt.title('百望商城' + date + '购物节百望商品销售量前10商品')
    # 设置Y轴刻度线标签
    ax.set_yticks(range(len(name)))
    ax.set_yticklabels(name)
    plt.annotate(r'$author:zxz$', (0, 0), color='#C4C4C4')
    print('百望商城百望商品销售量前10商品')
    print('#########################################')
    for i in range(len(goodName)):
        print('销售量第' + str(i + 1) + ':' + goodName[i] + '     销量' + str(xl[i][1]))
    plt.show()

def printjd(date,df):
    jddf = df[df.goods_resource == 2]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    ls = Difuid(jddf)
    l = ls[0]
    xl = l.copy()
    goodName = ls[1]
    l.reverse()
    name = [i[0] for i in l]
    colleges = [i[1] for i in l]
    fig, ax = plt.subplots()
    fig.tight_layout()
    b = ax.barh(range(len(name)), colleges)
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, w, ha='left', va='center', color='#008B8B')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xlabel('销售数量')
    plt.ylabel('商品id')
    plt.title('百望商城'+date+'购物节京东商品销售量前10商品')
    # 设置Y轴刻度线标签
    ax.set_yticks(range(len(name)))
    ax.set_yticklabels(name)
    plt.annotate(r'$author:zxz$', (0, 0), color='#C4C4C4')
    print('百望商城京东商品销售量前10商品')
    print('#########################################')
    for i in range(len(goodName)):
        print('销售量第' + str(i + 1) + ':' + goodName[i] + '     销量' + str(xl[i][1]))
    plt.show()

def printYh(date,df):
    n = difyhid(df)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    yh = n[1]
    yh.reverse()
    yhname = [i[0] for i in yh]
    yhcolleges = [i[1] for i in yh]
    fig, ax = plt.subplots()
    fig.tight_layout()
    b = ax.barh(range(len(yhname)), yhcolleges, color='#5F9EA0')
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, w, ha='left', va='center', color='#008B8B')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xlabel('购买金额（元）')
    plt.ylabel('账号id')
    plt.title('百望商城'+date+'购物节购买力Max前10用户 总参与人次：' + str(n[0]))
    ax.set_yticks(range(len(yhname)))
    ax.set_yticklabels(yhname)
    plt.annotate(r'$author:zxz$', (250, 0), color='#C4C4C4')
    plt.show()

# 支付方式
def printZf(date,df):
    pay = payMethod(df)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    wx = 0
    for i in pay:
        if '微信' in i[0]:
            wx += i[1]
            pay.remove(i)
    pay.append(('微信支付', wx))
    print(pay)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    plt.pie([i[1] for i in pay], labels=[i[0] + str(i[1]) for i in pay], startangle=90, autopct='%1.1f%%')
    plt.title('百望商城' + date + '购物节支付方式')
    plt.annotate(r'$author:zxz$', (-0.5, 0), color='#C4C4C4')
    plt.legend()
    plt.show()


# 绘制每日新注册用户情况
def printXzyh(date,times):
    xz = xzdfyh(times)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    print(xz)
    plt.bar([i[0] for i in xz],[i[1] for i in xz],alpha=0.7,width=0.6,color='#9F79EE')
    for i in xz:
        plt.text(i[0],i[1]+0.5,i[1],fontsize=8, ha='center', va='center')
    plt.ylabel('人数')
    plt.xlabel('日期')
    plt.title('百望商城'+date+'购物节每天新人注册情况，总注册人数：'+str(sum([i[1] for i in xz])))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()


# 每日下单人次图
def printPeryh(date,dfs):
    yhs=[]
    for df in dfs:
        ids = set(df[1].uid)
        yhs.append([df[0],len(ids)])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar([i[0] for i in yhs], [i[1] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[1] + 2.5, i[1], fontsize=10, ha='center', va='center')
    plt.ylabel('人数')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日下单人数 总下单人数：' + str(sum([i[1] for i in yhs])))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

def printlr(date,dfs,dffk):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    jdlr=calLr(dffk[1])
    bwlr=calLr(dffk[0])
    zlr=calLr(dfs)
    plt.bar([i[0] - 0.2 for i in bwlr], [i[3] for i in bwlr], alpha=0.9, width=0.2, edgecolor='white', label='百望', lw=1)
    plt.bar([i[0] for i in jdlr], [i[3] for i in jdlr], alpha=0.9, width=0.2, edgecolor='white', label='京东', lw=1)
    plt.bar([i[0] + 0.2 for i in zlr], [i[3] for i in zlr], alpha=0.9, width=0.2, edgecolor='white', label='总利润', lw=1)
    for i in bwlr:
        plt.text(i[0] - 0.2, i[3]+0.6, i[3], color='#00BFFF', fontsize=10, ha='center', va='center')
    for i in jdlr:
        plt.text(i[0], i[3] , i[3], color='#FF8C00', fontsize=10, ha='center', va='center')
    for i in zlr:
        plt.text(i[0] + 0.2, i[3]+1 , i[3], color='#006400', fontsize=10, ha='center', va='center')
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.ylabel('利润率')
    plt.xlabel('日期'+'   注:网易利润率固定为15%')
    plt.title('百望商城' + date + '购物节每日利润率')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    date1=input('请输入那个季节：')
    s = input('请输入年及月份：')
    s = s + '-13' + ' 0:0:0'
    starttime = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    starttime = int(time.mktime(starttime))
    times = HandleTime(starttime)
    dfs=reDf(times)
    df=dfqb(dfs)
    num=df.shape[0]
    pay=round(sum(df.org_money),2)
    # 百望 京东 网易
    dffk=dffk(dfs)
    # printsj(date1,df)
    # printbw(date1,df)
    # printjd(date1,df)
    # printOrNu(date1,dffk,num,pay)
    # printXzyh(date1,times)
    # printZf(date1,df)
    # printYh(date1,df)
    printPeryh(date1,dfs)
    # printlr(date1,dfs,dffk)
