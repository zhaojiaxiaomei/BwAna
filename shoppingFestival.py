# 1.用户
# 1.1每日新注册人数
# 1.2每日实际下单人数
# 1.3每日每人平均单量
# 1.4每日每人平均消费额
# 1.5每日每人平均营业额
# 1.6购买力max的前10名用户
# 2.订单
# 2.1每日订单京东网易百望拆分情况
# 2.2每笔订单平均销售额
# 2.3每笔订单的平均营业额
# 2.4每日订单总体利润率
# 3.统计
# 3.1百望商城销售额前10商家
# 3.2百望销售数量前10的商品
# 3.3京东销售数量前10的商品
# 3.4支付方式饼状图
# 3.5京东网易百望订单饼状图
# 3.6京东网易百望销售额饼状图
# 3.7京东网易百望营业额饼状图


import matplotlib.pyplot as plt
from connectMysql.shoppingConnect import reDf,HandleTime,xzdfyh,payMethod,dfqb
from connectMysql.shoppingConnect import difyhid,Difuid,seller,dffk,ord,calLr,pt
import time


def printNewYh(date,times,dfs):

    # 1.6购买力max的前10名用户
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 1.1每日新注册人数
    xz = xzdfyh(times)
    plt.bar([i[0] for i in xz], [i[1] for i in xz], alpha=0.7, width=0.6, color='#9F79EE')
    for i in xz:
        plt.text(i[0], i[1] + 0.5, i[1], fontsize=8, ha='center', va='center')
    plt.ylabel('人数')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每天新人注册情况，总注册人数：' + str(sum([i[1] for i in xz])))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    # 1.2每日实际下单人数
    plt.figure()
    yhs = []
    for df in dfs:
        ids = set(df[1].uid)
        num=df[1].shape[0]
        money=round(sum(df[1].org_money),2)
        rate = round(round(sum(df[1].org_money), 2) - round(sum(df[1].seller_money), 2) - round(sum(df[1].discount), 2),2)
        yhs.append([df[0],len(ids),num,round(num/len(ids),2),money,round(money/len(ids),2),rate,round(rate/len(ids),2)])
    plt.bar([i[0] for i in yhs], [i[1] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[1] + 2.5, i[1], fontsize=10, ha='center', va='center')
    plt.ylabel('人数')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日下单人数')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    # 1.3每日每人平均单量
    plt.figure()
    plt.bar([i[0] for i in yhs], [i[2] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[2] + 10, i[2], fontsize=10, ha='center', va='center')
    plt.ylabel('单量')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日订单量 总单量：' + str(sum([i[2] for i in yhs])))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    plt.figure()
    plt.bar([i[0] for i in yhs], [i[3] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[3] + 0.05, i[3], fontsize=10, ha='center', va='center')
    plt.ylabel('单量')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日每人平均订单量')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    # 1.4每日每人平均消费额
    plt.figure()
    plt.bar([i[0] for i in yhs], [i[4] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[4] + 10, i[4], fontsize=10, ha='center', va='center')
    plt.ylabel('金额（元）')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日销售量 总销售额：' + str(sum([i[4] for i in yhs])))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    plt.figure()
    plt.bar([i[0] for i in yhs], [i[5] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[5] + 2, i[5], fontsize=10, ha='center', va='center')
    plt.ylabel('金额（元）')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日每人平均消费额')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    # 1.5每日每人平均营业额
    plt.figure()
    plt.bar([i[0] for i in yhs], [i[6] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[6] + 10, i[6], fontsize=10, ha='center', va='center')
    plt.ylabel('金额（元）')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日平台管理费')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    plt.figure()
    plt.bar([i[0] for i in yhs], [i[7] for i in yhs], alpha=0.7, width=0.6)
    for i in yhs:
        plt.text(i[0], i[7] + 1, i[7], fontsize=10, ha='center', va='center')
    plt.ylabel('金额（元）')
    plt.xlabel('日期')
    plt.title('百望商城' + date + '购物节每日每人平均平台管理费')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.show()

    # 1.6购买力max的前10名用户
    plt.figure()
    df=dfqb(dfs)
    n = difyhid(df)
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
    # plt.xlim([0,max(i[0] for i in yh)]+500)
    plt.title('百望商城' + date + '购物节购买力Max前10用户 总参与人次：' + str(n[0]))
    ax.set_yticks(range(len(yhname)))
    ax.set_yticklabels(yhname)
    plt.annotate(r'$author:zxz$', (250, 0), color='#C4C4C4')
    plt.show()


def printNewDd(date,dfs):
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 2.1每日订单京东百望网易拆分情况
    dffk1 = dffk(dfs)
    bwdfs = dffk1[0]
    jddfs = dffk1[1]
    wydfs = dffk1[2]
    bw = ord(bwdfs)
    jd = ord(jddfs)
    wy = ord(wydfs)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    bwl = bw[0]
    jdl = jd[0]
    wyl = wy[0]
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
    plt.title('百望商城' + date + '购物节每日订单情况 总订单量' + str(num))
    plt.legend()
    plt.show()

    # 2.2每日销售额京东百望网易拆分情况
    plt.figure()
    bwp = bw[1]
    jdp = jd[1]
    wyp = wy[1]
    plt.bar([i[0] - 0.2 for i in bwp], [i[1] for i in bwp], alpha=0.9, width=0.2, edgecolor='white', label='百望', lw=1)
    plt.bar([i[0] for i in jdp], [i[1] for i in jdp], alpha=0.9, width=0.2, edgecolor='white', label='京东', lw=1)
    plt.bar([i[0] + 0.2 for i in wyp], [i[1] for i in wyp], alpha=0.9, width=0.2, edgecolor='white', label='网易', lw=1)
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

    # 2.3每日利润率
    jdlr = calLr(jddfs)
    bwlr = calLr(bwdfs)
    zlr = calLr(dfs)
    plt.bar([i[0] - 0.2 for i in bwlr], [i[3] for i in bwlr], alpha=0.9, width=0.2, edgecolor='white', label='百望', lw=1)
    plt.bar([i[0] for i in jdlr], [i[3] for i in jdlr], alpha=0.9, width=0.2, edgecolor='white', label='京东', lw=1)
    plt.bar([i[0] + 0.2 for i in zlr], [i[3] for i in zlr], alpha=0.9, width=0.2, edgecolor='white', label='总利润', lw=1)
    for i in bwlr:
        plt.text(i[0] - 0.2, i[3] + 0.6, i[3], color='#00BFFF', fontsize=10, ha='center', va='center')
    for i in jdlr:
        plt.text(i[0], i[3], i[3], color='#FF8C00', fontsize=10, ha='center', va='center')
    for i in zlr:
        plt.text(i[0] + 0.2, i[3] + 1, i[3], color='#006400', fontsize=10, ha='center', va='center')
    plt.text(13, 0, r'$author:zxz$', fontdict={'size': 10, 'color': '#C4C4C4'})
    plt.ylabel('利润率')
    plt.xlabel('日期' + '   注:网易利润率固定为15%')
    plt.title('百望商城' + date + '购物节每日利润率')
    plt.legend()
    plt.show()


def printNewTj(date,dfs):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df=dfqb(dfs)

    # 3.1百望商城销售额前10商家
    bwdf = df[df.goods_resource == 1]
    jddf = df[df.goods_resource == 2]
    wydf= df[df.goods_resource==4]
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
    plt.title('百望商城' + date + '购物节销售额前10商家')
    ax.set_yticks(range(len(sname)))
    ax.set_yticklabels(sname)
    plt.annotate(r'$author:zxz$', (250, 0), color='#C4C4C4')
    plt.show()

    # 3.2百望销售数量前10的商品
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

    # 3.3京东销售数量前10的商品
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
    plt.title('百望商城' + date + '购物节京东商品销售量前10商品')
    # 设置Y轴刻度线标签
    ax.set_yticks(range(len(name)))
    ax.set_yticklabels(name)
    plt.annotate(r'$author:zxz$', (0, 0), color='#C4C4C4')
    print('百望商城京东商品销售量前10商品')
    print('#########################################')
    for i in range(len(goodName)):
        print('销售量第' + str(i + 1) + ':' + goodName[i] + '     销量' + str(xl[i][1]))
    plt.show()

    # 3.4支付方式饼状图
    pay = payMethod(df)
    plt.figure()
    plt.pie([i[1] for i in pay], labels=[i[0] + str(i[1]) for i in pay], startangle=90, autopct='%1.1f%%')
    plt.title('百望商城' + date + '购物节支付方式')
    plt.annotate(r'$author:zxz$', (-0.5, 0), color='#C4C4C4')
    plt.legend()
    plt.show()
    # 3.5京东网易百望订单饼状图
    jdnum=jddf.shape[0]
    bwnum=bwdf.shape[0]
    wynum=wydf.shape[0]
    num=[['京东',jdnum],['百望', bwnum],['网易', wynum]]
    plt.figure()
    plt.pie([i[1] for i in num], labels=[i[0] + str(i[1]) for i in num], startangle=90, autopct='%1.1f%%')
    plt.title('百望商城' + date + '购物节订单情况')
    plt.annotate(r'$author:zxz$', (-0.5, 0), color='#C4C4C4')
    plt.legend()
    plt.show()
    # 3.6京东网易百望销售额饼状图
    jdmoney = round(sum(jddf.org_money),2)
    bwmoney =round(sum(bwdf.org_money),2)
    wymoney = round(sum(wydf.org_money),2)
    money = [['京东',jdmoney],['百望', bwmoney],['网易', wymoney]]
    plt.figure()
    plt.pie([i[1] for i in money], labels=[i[0] + str(i[1]) for i in money], startangle=90, autopct='%1.1f%%')
    plt.title('百望商城' + date + '购物节销售额情况')
    plt.annotate(r'$author:zxz$', (-0.5, 0), color='#C4C4C4')
    plt.legend()
    plt.show()
    # 3.7京东网易百望营业额饼状图
    jdseller = round(round(sum(jddf.org_money), 2) - round(sum(jddf.seller_money), 2) - round(sum(jddf.discount), 2),2)
    bwseller = round(round(sum(bwdf.org_money), 2) - round(sum(bwdf.seller_money), 2) - round(sum(bwdf.discount), 2),2)
    wyseller = round(round(sum(wydf.org_money), 2) - round(sum(wydf.seller_money), 2) - round(sum(wydf.discount), 2),2)
    sellera = [['京东', jdseller], ['百望', bwseller], ['网易', wyseller]]
    plt.figure()
    plt.pie([i[1] for i in sellera], labels=[i[0] + str(i[1]) for i in sellera], startangle=90, autopct='%1.1f%%')
    plt.title('百望商城' + date + '购物节平台管理费情况')
    plt.annotate(r'$author:zxz$', (-0.5, 0), color='#C4C4C4')
    plt.legend()
    plt.show()
    # 3.8订单来源饼状图
    plt.figure()
    ptnum = pt(df)
    plt.pie([i[1] for i in ptnum], labels=[i[0] + ':' + str(i[1]) for i in ptnum], startangle=90, autopct='%1.1f%%')
    plt.title('百望商城' + date + '订单量来源情况')
    plt.annotate(r'$author:zxz$', (-0.5, 0), color='#C4C4C4')
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
    printNewYh(date1,times,dfs)
    printNewDd(date1, dfs)
    printNewTj(date1, dfs)
