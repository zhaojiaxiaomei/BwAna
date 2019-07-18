import numpy as np
import pandas as pd

dates=pd.date_range('20180706',periods=6)
print(dates)
# randn函数用于创建随机正态分布数
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('abcd'))
print(df)
df2=pd.DataFrame({'A':np.random.randn(6),})
print(df2)
# 假如字典内的数据长度不同，以最长的数据为准，比如B列有4行
df3=pd.DataFrame({'A':pd.Timestamp('20181119'),'B':pd.Series(1,index=list('zxz'))})
print(df3)
# 可以使用dtypes来查看行每一列的数据格式的数据格式
print(df.dtypes)
# 使用hend查看前几行数据（默认是前5行）也可以指定前几行
print(df.head(2))
# 使用tail查看后5行数据
print(df.tail(2))
# 插卡数据框的索引
print(df.index)
# 查看列名
print(df.columns)
# 查看数据值，用values
print(df.values)
# 查看描述性统计，用describe
print(df.describe())
# 使用T来转置数据，也就是行列转换
print(df.T)



