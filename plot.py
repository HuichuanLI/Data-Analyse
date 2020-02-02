import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

import numpy as np

sns.set_style(style="darkgrid")  # 配置样式
# sns.set_context(context="poster")  # 配置字体
# sns.set_palette(sns.color_palette("RdBu", n_colors=7))  # 配置色板

pd.set_option('display.max_columns', None)

df = pd.read_csv("./data/HR.csv")
df = df.dropna(how="any", axis=0)
df = df[df["last_evaluation"] <= 1][df["salary"] != "nme"][df["department"] != "sale"]

# 柱状图
print(df["salary"].value_counts())
plt.title("Salary")
plt.xlabel("salary")
plt.ylabel("Number")
plt.xticks(np.arange(len(df["salary"].value_counts())) + 0.5, df["salary"].value_counts().index)
plt.axis([0, 3, 0, 9000])

plt.bar(np.arange(len(df["salary"].value_counts())) + 0.5, df["salary"].value_counts(), width=0.5)
for x, y in zip(np.arange(len(df["salary"].value_counts())) + 0.5, df["salary"].value_counts()):
    plt.text(x, y, y, ha="center", va="bottom")
plt.show()

sns.countplot(x="salary", hue="department", data=df)
plt.show()

# 直方图
f = plt.figure(0)
f.add_subplot(1, 3, 1)
sns.distplot(df["satisfaction_level"], bins=10)
f.add_subplot(1, 3, 2)
sns.distplot(df["last_evaluation"], bins=10)
f.add_subplot(1, 3, 3)
sns.distplot(df["average_monthly_hours"], bins=10)
plt.show()

# 箱线图
sns.boxplot(y=df["last_evaluation"], saturation=0.75, whis=3)
plt.show()

# 点线图（折线图）
sub_df = df.groupby("time_spend_company").mean()
# print(sub_df["left"])
sns.pointplot(sub_df.index, sub_df["left"])
plt.show()

sns.pointplot(x="time_spend_company", y="left", data=df)
plt.show()
# 饼图
lbs = df["department"].value_counts().index
explodes = [0.1 if i == "sales" else 0 for i in lbs]
plt.pie(df["department"].value_counts(normalize=True), explode=explodes, autopct='%1.1f%%',
        colors=sns.color_palette("Reds", n_colors=7), labels=df["department"].value_counts().index)
plt.show()
plt.pie(df["number_project"].value_counts(normalize=True), labels=df["number_project"].value_counts().index)
plt.show()

# PIE
lbs = df["department"].value_counts().index
lbs_name = df["department"].value_counts()
print("ok")
print(lbs_name.keys())
plt.pie(df["department"].value_counts(normalize=True), labels=lbs_name.keys(), autopct='%1.1f%%')
plt.show()
