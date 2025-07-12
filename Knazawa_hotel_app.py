#!/usr/bin/env python
# coding: utf-8

# In[10]:


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False


# In[11]:


df = pd.read_csv("hotel_cleaned.csv")

st.title("金沢酒店数据分析与推荐 🌟")
st.markdown("数据来源：Jalan 网页抓取 | 分析维度：价格、评分、预约时间等")


# In[15]:


df["ホテル名"] = df["タイトル"]  

st.subheader("酒店数据概览")
st.dataframe(df[["ホテル名", "最低価格", "評価スコア", "評価ランク"]])

st.sidebar.title("筛选条件")

min_price = st.sidebar.slider("最低価格（円）", int(df["最低価格"].min()), int(df["最低価格"].max()), int(df["最低価格"].min()))
selected_ranks = st.sidebar.multiselect(
    "选择评价等级",
    options=df["評価ランク"].unique(),
    default=list(df["評価ランク"].unique())
)

filtered_df = df[(df["最低価格"] >= min_price) & (df["評価ランク"].isin(selected_ranks))]


# In[16]:


st.subheader("价格与评分关系散布图")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x="最低価格", y="評価スコア", hue="評価ランク", ax=ax)
plt.xlabel("最低価格（円）")
plt.ylabel("評価スコア")
st.pyplot(fig)


# In[18]:


rank_counts = filtered_df["評価ランク"].value_counts()
fig2, ax2 = plt.subplots()
colors = sns.color_palette("viridis", len(rank_counts))
sns.barplot(x=rank_counts.index, y=rank_counts.values, palette=colors, ax=ax2)
ax2.set_xlabel("評価等级")
ax2.set_ylabel("酒店数量")
st.pyplot(fig2)


# In[19]:


st.subheader("TOP 5 高评分酒店推荐 🏨")
top_hotels = filtered_df.sort_values("評価スコア", ascending=False).head(5)
st.table(top_hotels[["ホテル名", "最低価格", "評価スコア", "評価ランク"]])

