import pandas as pd
import numpy as np
import scipy.stats as ss
import seaborn as sns

# sns.set_context(context="poster", font_scale=1.2)
import matplotlib.pyplot as plt
import math
from sklearn.decomposition import PCA

df = pd.read_csv("./data/HR.csv")
df = df.dropna(how="any", axis=0)
df = df[df["last_evaluation"] <= 1][df["salary"] != "nme"][df["department"] != "sale"]

sns.barplot(x="salary", y="left", hue="department", data=df)

plt.show()

sl_s = df["satisfaction_level"]
sns.barplot(list(range(len(sl_s))), sl_s.sort_values())
plt.show()