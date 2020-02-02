import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

df = pd.read_csv("./data/HR.csv")
# Satisfaction Level
sl_s = df["satisfaction_level"]
sl_null = sl_s.isnull()  # 是否为空值
print(df[df["satisfaction_level"].isnull()])
# sl_s = sl_s.dropna()  # 丢弃空值
print(sl_s.mean(), sl_s.std(), sl_s.max(), sl_s.min(), sl_s.median(), sl_s.skew(), sl_s.kurt())

print(np.histogram(sl_s.values, bins=np.arange(0, 1.1, 0.1)))

le_s = df["last_evaluation"]
le_null = le_s[le_s.isnull()]
print(le_null)
# 常见统计项
print(le_s.mean(), le_s.std(), le_s.median(), le_s.max(), \
      le_s.min(), le_s.skew(), le_s.kurt())

q_low = le_s.quantile(q=0.25)  # 下四分位数
q_high = le_s.quantile(q=0.75)  # 上四分位数
print(q_low)
print(q_high)

k = 1.5
q_interval = q_high - q_low

print(q_interval)
print(q_high + k * q_interval, q_low - k * q_interval)
# 异常值过滤
le_s = le_s[le_s < q_high + k * q_interval][le_s > q_low - k * q_interval]

print(len(le_s))
print(np.histogram(le_s.values, bins=np.arange(0.0, 1.1, 0.1)))

# 常见统计项
print(le_s.mean(), le_s.std(), le_s.median(), le_s.max(), \
      le_s.min(), le_s.skew(), le_s.kurt())

# Number Project
np_s = df["number_project"]
print(np_s[np_s.isnull()])
print(np_s.mean(), np_s.std(), np_s.median(), np_s.max(), np_s.min(), np_s.skew(), np_s.kurt())
print(np_s.value_counts(normalize=True).sort_index())

# average_montly_hours
amh_s = df["average_monthly_hours"]
print(amh_s.mean(), amh_s.std(), amh_s.median(), amh_s.max(), amh_s.min(), amh_s.skew(), amh_s.kurt())
print(len(amh_s[amh_s < amh_s.quantile(0.75) + 1.5 * (amh_s.quantile(0.75) - amh_s.quantile(0.25))][
              amh_s > amh_s.quantile(0.25) - 1.5 * (amh_s.quantile(0.75) - amh_s.quantile(0.25))]))
interval = 10
print(np.histogram(amh_s.values, bins=np.arange(amh_s.min(), amh_s.max() + interval, interval)))
print(amh_s.value_counts(bins=np.arange(amh_s.min(), amh_s.max() + interval, interval)))

# Time Spend Company
tsc_s = df["time_spend_company"]
print(tsc_s.value_counts().sort_index())

# Work Accident
wa_s = df["Work_accident"]
print(wa_s.value_counts())
print(wa_s.mean())

# Left
l_s = df["left"]
print(l_s.value_counts())

# promotion_last_5years
pl5_s = df["promotion_last_5years"]
print(pl5_s.value_counts())

# salary
s_s = df["salary"]
print(s_s.value_counts())
s_s = s_s.where(s_s != "nme").dropna()
print(s_s.value_counts())

# department
d_s = df["department"]
print(d_s.value_counts(normalize=True))
print(d_s.where(d_s != "sale").dropna())

# 交叉

df = df.dropna(how="any", axis=0)
df = df[df["last_evaluation"] <= 1][df["salary"] != "nme"][df["department"] != "sale"]

print(df.groupby("department").mean())

sub_df_2 = df.loc[:, ["left", "department"]].groupby("department").mean()

print(sub_df_2)

print("OK")
sub_df_3 = df.loc[:, ["last_evaluation", "department"]]
print(sub_df_3.groupby("department", group_keys=False)["last_evaluation"].apply(lambda x: x.max() - x.min()))
# print(df.groupby("department").mean())

import seaborn as sns
import matplotlib.pyplot as plt

