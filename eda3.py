import numpy as np
import scipy.stats as ss

norm_dist = ss.norm.rvs(size=20)
print(norm_dist)

print(ss.normaltest(norm_dist))

# 卡方检验 判断相关
ss.chi2_contingency([[15, 96], [85, 5]])

# 均值相等
print(ss.ttest_ind(ss.norm.rvs(size=10), ss.norm.rvs(size=20)))

print(ss.ttest_ind(ss.norm.rvs(size=100), ss.norm.rvs(size=200)))

# f 分布 === > anova
print(ss.f_oneway([49, 50, 39, 40, 43], [28, 32, 30, 36, 34], [38, 40, 45, 42, 48]))

from statsmodels.graphics.api import qqplot
from matplotlib import pyplot as plt

qqplot(ss.norm.rvs(size=100))
plt.show()

import pandas as pd

s1 = pd.Series([0.1, 0.2, 1.1, 2.4, 1.3, 0.3, 0.5])
s2 = pd.Series([0.5, 0.4, 1.2, 2.5, 1.1, 0.7, 0.1])

print(s1.corr(s2, method="spearman"))

print(s1.corr(s2, method="pearson"))

df = pd.DataFrame(np.array([s1, s2]).T)
print(df.corr())

# 回归
x = np.arange(10).astype(np.float).reshape((10, 1))

y = x * 3 + 4 + np.random.random((10, 1))

from sklearn.linear_model import LinearRegression

reg = LinearRegression()

res = reg.fit(x, y)

y_pred = reg.predict(x)

# PCA

# PCA降维
df = pd.DataFrame(np.array([np.array([2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2, 1, 1.5, 1.1]),
                            np.array([2.4, 0.7, 2.9, 2.2, 3, 2.7, 1.6, 1.1, 1.6, 0.9])]).T)
from sklearn.decomposition import PCA

lower_dim = PCA(n_components=1)
lower_dim.fit(df.values)
print(lower_dim.transform(df.values))
print("PCA")
print(lower_dim.explained_variance_ratio_)
print(lower_dim.explained_variance_)

## 实现PCA
from scipy import linalg


def pca(data_mat, topNfeat=1000000):
    mean_vals = np.mean(data_mat, axis=0)
    mid_mat = data_mat - mean_vals
    # 按照列协方差矩阵
    cov_mat = np.cov(mid_mat, rowvar=False)
    eig_vals, eig_vects = linalg.eig(np.mat(cov_mat))
    eig_val_index = np.argsort(eig_vals)
    eig_val_index = eig_val_index[:-(topNfeat + 1):-1]
    eig_vects = eig_vects[:, eig_val_index]
    low_dim_mat = np.dot(mid_mat, eig_vects)
    # ret_mat = np.dot(low_dim_mat,eig_vects.T)
    return low_dim_mat, eig_vals


data = np.array([np.array([2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2, 1, 1.5, 1.1]),
                 np.array([2.4, 0.7, 2.9, 2.2, 3, 2.7, 1.6, 1.1, 1.6, 0.9])]).T

print(pca(data, topNfeat=1))
