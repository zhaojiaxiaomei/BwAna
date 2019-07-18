import matplotlib.pyplot as plt
from connectMysql.connect import dfInit
from connectMysql.connect import Difuid
from connectMysql.connect import seller
from connectMysql.connect import Difuyhid,payMethod,xzdfyh,pt,xzdfsj
import time

date=input('请输入时间：')
startdate = date + ' 0:0:0'
enddate = date + ' 23:59:59'
starttime = time.strptime(startdate, "%Y-%m-%d %H:%M:%S")
starttime = int(time.mktime(starttime))
endtime = time.strptime(enddate, "%Y-%m-%d %H:%M:%S")
endtime = int(time.mktime(endtime))
wydf = dfInit(starttime, endtime,4)
jddf=dfInit(starttime,endtime,2)
bwdf=dfInit(starttime,endtime,1)
df=dfInit(starttime,endtime,8)
plt.rcParams['font.sans-serif']=['SimHei']

# 京东商品销量前几商品

plt.figure()
ls=Difuid(jddf)
l=ls[0]
xl=l.copy()
goodName=ls[1]
l.reverse()
name=[i[0] for i in l]
colleges=[i[1] for i in l]


fig,ax=plt.subplots()
fig.tight_layout()
b=ax.barh(range(len(name)),colleges)
for rect in b:
    w=rect.get_width()
    ax.text(w,rect.get_y()+rect.get_height()/2,w,ha='left',va='center',color='#008B8B')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xlabel('销售数量')
plt.ylabel('商品id')
plt.title(date+'百望商城京东商品销售量前10商品')
#设置Y轴刻度线标签
ax.set_yticks(range(len(name)))
ax.set_yticklabels(name)
plt.annotate(r'$author:Ariel$',(0,0),color='#C4C4C4')
print('百望商城京东商品销售量前10商品')
print('#########################################')
for i in range(len(goodName)):
    print('销售量第'+str(i+1)+':'+goodName[i]+'     销量：'+str(xl[i][1]))
plt.show()


# 百望商品销量前几商品
plt.figure()
ls=Difuid(bwdf)
l=ls[0]
xl=l.copy()
goodName=ls[1]
l.reverse()
name=[i[0] for i in l]
colleges=[i[1] for i in l]
fig,ax=plt.subplots()
fig.tight_layout()
b=ax.barh(range(len(name)),colleges,color='#4682B4')
for rect in b:
    w=rect.get_width()
    ax.text(w,rect.get_y()+rect.get_height()/2,w,ha='left',va='center',color='#008B8B')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xlabel('销售数量')
plt.ylabel('商品id')
plt.title(date+'百望商城百望商品销售量前10商品')
#设置Y轴刻度线标签
ax.set_yticks(range(len(name)))
ax.set_yticklabels(name)
plt.annotate(r'$author:Ariel$',(0,0),color='#C4C4C4')
print('\n百望商城百望商品销售量前10商品')

for i in range(len(goodName)):
    print('销售量第'+str(i+1)+':'+goodName[i]+'     销量:'+str(xl[i][1]))
plt.show()

# 百望商家销售额高商家
plt.figure()
s=seller(bwdf)
s.reverse()
sname=[i[0] for i in s]
scolleges=[i[1] for i in s]
fig,ax=plt.subplots()
fig.tight_layout()
b=ax.barh(range(len(sname)),scolleges,color='#4682B4')
for rect in b:
    w=rect.get_width()
    ax.text(w,rect.get_y()+rect.get_height()/2,w,ha='left',va='center',color='#008B8B')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xlabel('销售额（元）')
plt.ylabel('商户名称')
plt.title(date+'百望商城销售额前10商家')
ax.set_yticks(range(len(sname)))
ax.set_yticklabels(sname)
plt.annotate(r'$author:Ariel$',(0,0),color='#C4C4C4')
plt.show()

# 参与人数与购买力
plt.figure()
yhs=Difuyhid(df)
yh=yhs[1]
yh.reverse()
yhname=[i[0] for i in yh]
yhcolleges=[i[1] for i in yh]
fig,ax=plt.subplots()
fig.tight_layout()
b=ax.barh(range(len(yhname)),yhcolleges,color='#5F9EA0')
for rect in b:
    w=rect.get_width()
    ax.text(w,rect.get_y()+rect.get_height()/2,w,ha='left',va='center',color='#008B8B')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xlabel('购买金额（元）')
plt.ylabel('账号id')
plt.title(date+'百望商城购买力Max前10用户参与人数：'+str(yhs[0]))
ax.set_yticks(range(len(yhname)))
ax.set_yticklabels(yhname)
plt.annotate(r'$author:Ariel$',(250,0),color='#C4C4C4')
plt.show()


# 支付方式饼状图
plt.figure()
paymethod=payMethod(df)
plt.rcParams['font.sans-serif']=['SimHei']
plt.figure()
plt.pie([i[1] for i in paymethod],labels=[i[0]+str(i[1]) for i in paymethod],startangle=90,autopct='%1.1f%%')
plt.title('百望商城'+date+'支付方式')
plt.annotate(r'$author:Ariel$',(-0.5,0),color='#C4C4C4')
plt.legend()
plt.show()

# 订单量饼状图
plt.figure()
num=[('百望',bwdf.shape[0]),('京东',jddf.shape[0]),('网易',wydf.shape[0])]
sumNum=round(sum([i[1] for i in num]),2)
plt.pie([i[1] for i in num],labels=[i[0]+str(i[1]) for i in num],startangle=90,autopct='%1.1f%%')
plt.title('百望商城'+date+'订单量:'+str(sumNum))
plt.annotate(r'$author:Ariel$',(-0.5,0),color='#C4C4C4')
plt.legend()
plt.show()

plt.figure()
ptnum=pt(df)
plt.pie([i[1] for i in ptnum],labels=[i[0]+':'+str(i[1]) for i in ptnum],startangle=90,autopct='%1.1f%%')
plt.title('百望商城'+date+'订单量来源情况')
plt.annotate(r'$author:Ariel$',(-0.5,0),color='#C4C4C4')
plt.legend()
plt.show()

# 销售额饼状图
plt.figure()
payMoney=[('百望',round(sum(bwdf.org_money),2)),('京东',round(sum(jddf.org_money),2)),('网易',round(sum(wydf.org_money),2))]
sumMoney=round(sum([i[1] for i in payMoney]),2)
plt.pie([i[1] for i in payMoney],labels=[i[0]+str(i[1]) for i in payMoney],startangle=90,autopct='%1.1f%%')
plt.title('百望商城'+date+'销售额:'+str(sumMoney))
plt.annotate(r'$author:Ariel$',(-0.5,0),color='#C4C4C4')
plt.legend()
plt.show()

# 营业额
plt.figure()
rateMoney=[('百望',round(round(sum(bwdf.org_money),2)-round(sum(bwdf.seller_money),2),2))
           ,('京东',round(round(sum(jddf.org_money),2)-round(sum(jddf.seller_money),2),2))
           ,('网易',round(round(sum(wydf.org_money),2)-round(sum(wydf.seller_money),2),2))]
sumrate=round(sum([i[1] for i in rateMoney]),2)
plt.pie([i[1] for i in rateMoney],labels=[i[0]+str(i[1]) for i in rateMoney],startangle=90,autopct='%1.1f%%')
plt.title('百望商城'+date+'平台管理费:'+str(sumrate))
plt.annotate(r'$author:Ariel$',(-0.5,0),color='#C4C4C4')
plt.legend()
plt.show()

# 营业额与利润率分布图
plt.figure()
rate=round(sumrate*100/sumMoney,3)


sellerMoney=[('百望',round(sum(bwdf.seller_money),2))
           ,('京东',round(sum(jddf.seller_money),2))
           ,('网易',round(sum(wydf.seller_money),2))]
plt.bar([i[0] for i in rateMoney],[i[1] for i in rateMoney],label='利润',width=0.3)
for i in rateMoney:
    plt.text(i[0],i[1]+500,i[1],fontsize=8, ha='center', va='center',color='#00CD00')
plt.bar([i[0] for i in sellerMoney],[i[1] for i in sellerMoney],bottom=[i[1] for i in rateMoney],width=0.3)
for i in payMoney:
    plt.text(i[0],i[1]+500,i[1],fontsize=8, ha='center', va='center',color='b')
plt.legend()
bwrate=str(round(rateMoney[0][1]*100/payMoney[0][1],2))+'%'
jdrate=str(round(rateMoney[1][1]*100/payMoney[1][1],2))+'%'
if payMoney[2][1]!=0:
    wyrate=str(round(rateMoney[2][1]*100/payMoney[2][1],2))+'%'
else:
    wyrate=''
plt.ylabel('金额（元）')
plt.xlabel('百望利润率:'+bwrate+' 京东利润率:'+jdrate+' 网易利润率:15%')
plt.annotate(r'$author:Ariel$',(0,0),color='#C4C4C4')
plt.title(date+'百望商城利润率:'+str(rate)+'%')
plt.show()
print(date+'新注册会员人数：'+str(xzdfyh(starttime,endtime)))


df=xzdfsj(starttime,endtime)
if df.shape[0]!=0:
    print('会员升级产品订单：')
    print(df)
else:
    print(date+'号无人购买会员产品')