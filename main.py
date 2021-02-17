import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

df = pd.read_csv("./data/HR.csv")

# pandas
print(df.head(10))

print(type(df))

print(type(df["satisfaction_level"]))

# 求均值
print(df.mean())

print(df["satisfaction_level"].mean())

# 取中值
print(df["satisfaction_level"].median())

# 分位数
print(df["satisfaction_level"].quantile(0.25))

# 众数
print(df["satisfaction_level"].mode())

# 取众数
print(df["department"].mode())

# 标准差
print(df.std())
print(df["satisfaction_level"].std())

# 方差
print(df.var())
print(df["satisfaction_level"].var())

# 求和
print(df.sum())
print(df["satisfaction_level"].sum())

# 偏态系数
print(df.skew())
print(df["satisfaction_level"].skew())

# 峰度系数
print(df.kurt())
print(df["satisfaction_level"].kurt())

# 分布函数
import scipy.stats as ss

print(ss.norm.stats(moments="mvsk"))

# 标准正太分布的0的值
print(ss.norm.pdf(0.0))

# 到概率为1的概率密度函数的取值
print(ss.norm.ppf(0.9))

# 概率密度函数的取值
print(ss.norm.cdf(0.0))

print(ss.norm.cdf(2) - ss.norm.cdf(-2))

# 概率的随机取值
print(ss.norm.rvs(size=10))

# 卡放分布
ss.chi2

# t 分布
ss.t

# f 分布
ss.f

# 抽样
df.sample(n=10)

df.sample(n=0.001)

df["satisfaction_level"].sample(n=0.001)


