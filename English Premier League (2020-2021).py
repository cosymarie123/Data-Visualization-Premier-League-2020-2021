#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[11]:


epl_df = pd.read_csv('C:\\Users\\ASUS\\OneDrive\\Desktop\\EPL_20_21.csv') #load tệp csv
epl_df.head()


# In[12]:


epl_df.info()


# In[13]:


epl_df.describe()


# In[14]:


epl_df.isna().sum()


# In[15]:


#Tạo 2 cột mới
#MinsPerMatch(số phút mỗi trận cầu thủ tham gia)
#GoalsPerMatch(số bàn thắng mỗi trận cầu thủ tham gia)
epl_df['MinsPerMatch'] = (epl_df['Mins'] /epl_df['Matches']).astype(int)
epl_df['GoalsPerMatch'] = (epl_df['Goals'] / epl_df['Matches']).astype(float)
epl_df.head()


# In[16]:


#Tổng số bàn thắng đã ghi trong mùa giải 2021
Total_Goals = epl_df['Goals'].sum()
print(Total_Goals)


# In[17]:


#Tổng số bàn thắng nhờ penalty
Total_PenaltyGoals = epl_df['Penalty_Goals'].sum()
print(Total_PenaltyGoals)


# In[18]:


#Tổng số lần sút penalty được thực hiện

Total_PenaltyAttempts = epl_df['Penalty_Attempted'].sum()
print(Total_PenaltyAttempts)


# In[19]:


#Biểu đồ tròn thể hiện số lần sút pen thành bàn thắng và bỏ lỡ

plt.figure(figsize=(13, 6)) #size biểu đồ tròn
plt_not_scored = epl_df['Penalty_Attempted'].sum() - Total_PenaltyGoals #số bàn thắng bị bỏ lỡ = số lần sút - số bàn thắng 
data = [plt_not_scored, Total_PenaltyGoals] #data gồm số bàn thắng bị bỏ lỡ và số bàn thắng
labels = ['Penalties Missed' , 'Penalties Scored'] #tiêu đề
color = sns.color_palette('tab10') #màu
plt.pie(data, labels = labels, colors = color, autopct = '%.0f%%') #biểu đồ tròn gồm data, tiêu đề, màu và bao nhiêu %
plt.show() #show biểu đồ tròn


# In[20]:


#Vị trí duy nhất mà cầu thủ chơi (vd Ronaldo(MU) chỉ chơi vị trí tiền đạo, Phil Poden(MC) chơi được cả tiền đạo và tiền vệ)
epl_df['Position'].unique()


# In[21]:


#Tổng số tiền đạo
epl_df[epl_df['Position'] == 'FW']


# In[22]:


#Tổng số quốc gia khác nhau của cầu thủ
np.size((epl_df['Nationality'].unique()))


# In[23]:


#Cầu thủ đến từ quốc gia nhiều nhất
nationality = epl_df.groupby('Nationality').size().sort_values(ascending = False)
nationality.head(10).plot(kind = 'bar', figsize = (11,5),  color = sns.color_palette('tab10'))


# In[24]:


#Số cầu thủ tối đa có trong đội hình 
epl_df['Club'].value_counts().nlargest(10).plot(kind='bar', color=sns.color_palette("tab10")) #Ta đếm số hàng trong cột Club


# In[31]:


#Số cầu thủ ít nhất của đội hình trong mùa giải
epl_df['Club'].value_counts().nsmallest(10).plot(kind='bar', color=sns.color_palette("tab10")) #Ta đếm số hàng trong cột Club


# In[26]:


#Số tuổi của các cầu thủ
Under20 = epl_df[epl_df['Age'] <=20]
age20_25 = epl_df[(epl_df['Age']>20) & (epl_df['Age']<=25)]
age25_30 = epl_df[(epl_df['Age']>25) & (epl_df['Age']<=30)]
Above30 = epl_df[epl_df['Age'] >30]


# In[32]:


#Tạo biểu đồ tròn thể hiện độ tuổi của các cầu thủ
x = np.array([Under20['Name'].count(), age20_25['Name'].count(), age25_30['Name'].count(), Above30['Name'].count()])
mylabels = ["<=20", ">20 & <=25", ">25 & <=30", ">30"]
plt.title('Total Players with Age Groups', fontsize = 20)
plt.pie(x, labels = mylabels, autopct = "%.2f%%")
plt.show()


# In[42]:


#Tổng số cầu thủ dưới 20 tuổi của mỗi clb
players_under_20 = epl_df[epl_df['Age'] < 20] #Tìm các cầu thủ trong mỗi clb dưới 20 tuổi
players_under_20['Club'].value_counts().plot(kind = 'bar', color = sns.color_palette("tab10")) #Đếm và vẽ biểu đồ cột


# In[43]:


#Số cầu thủ dưới 20 tuổi của MU
players_under_20[players_under_20['Club'] =='Manchester United']


# In[44]:


#Số cầu thủ dưới 20 của Chelsea
players_under_20[players_under_20['Club'] == 'Chelsea']


# In[45]:


#Độ tuổi trung bình của các cầu thủ trong mỗi clb
plt.figure(figsize=(12,6))
sns.boxplot(x = 'Club', y = 'Age', data = epl_df)
plt.xticks(rotation = 90)


# In[64]:


num_player = epl_df.groupby('Club').size()
data = (epl_df.groupby('Club')['Age'].sum())/ num_player
data.sort_values(ascending=False)


# In[102]:


#Tổng số cầu thủ hỗ trợ ghi bàn mỗi clb
Assists_by_clubs = pd.DataFrame(epl_df.groupby('Club',as_index=False) ['Assists'].sum()) #groupby cột Club và cột tổng số hỗ trợ của mỗi clb(Assists)
sns.set_theme(style="whitegrid", color_codes=True) #màu
ax = sns.barplot(x='Club',y='Assists', data=Assists_by_clubs.sort_values(by='Assists'),palette='tab10')
ax.set_xlabel('Club',fontsize=30)
ax.set_ylabel('Assists',fontsize=30)
plt.xticks(rotation=75)
plt.rcParams['figure.figsize'] = (20,8)
plt.title('Plot of Clubs vs Total Assists', fontsize=30)


# In[104]:


#Top 10 cầu thủ hỗ trợ ghi bàn
top_10_assists = epl_df[['Name','Club','Assists','Matches']].nlargest(n=10, columns = 'Assists')
top_10_assists


# In[106]:


#Tổng số bàn thắng của mỗi clb
Goals_by_clubs = pd.DataFrame(epl_df.groupby('Club',as_index=False) ['Goals'].sum()) #groupby cột Club và cột tổng số hỗ trợ của mỗi clb(Assists)
sns.set_theme(style="whitegrid", color_codes=True) #màu
ax = sns.barplot(x='Club',y='Goals', data=Goals_by_clubs.sort_values(by='Goals'),palette='tab10')
ax.set_xlabel('Club',fontsize=30)
ax.set_ylabel('Goals',fontsize=30)
plt.xticks(rotation=75)
plt.rcParams['figure.figsize'] = (20,8)
plt.title('Plot of Clubs vs Total Goals', fontsize=30)


# In[108]:


#Top cầu thủ ghi bàn nhiều nhất
top_10_goals = epl_df[['Name', 'Club', 'Goals', 'Matches']].nlargest(n=10, columns='Goals')
top_10_goals


# In[113]:


#Số bàn thắng mỗi trận
top_10_goals_per_match = epl_df[['Name','GoalsPerMatch','Matches','Goals']].nlargest(n=10,columns='GoalsPerMatch')
top_10_goals_per_match


# In[114]:


#Biểu đồ tròn thể hiên bàn thắng có hỗ trợ hoặc không có hỗ trợ
plt.figure(figsize=(14,7))
assists = epl_df['Assists'].sum()
data = [Total_Goals - assists, assists]#tổng bàn thắng - tổng số lần hỗ trợ = bàn thắng mà k cần hỗ trợ
labels = ['Goals without assists', 'Goals with assists']
color = sns.color_palette('tab10')
plt.pie(data, labels = labels, colors = color, autopct = '%.0f%%')
plt.show()


# In[115]:


#Top 10 cầu thủ bị thẻ vàng nhiều nhất
epl_yellow_card = epl_df.sort_values(by = 'Yellow_Cards', ascending = False)[:10]
plt.figure(figsize=(20,6))
plt.title('Players with the most yellow cards')
c = sns.barplot(x=epl_yellow_card['Name'], y=epl_yellow_card['Yellow_Cards'], label='Players', color = 'yellow')
plt.ylabel('Number of Yellow Cards')
c.set_xticklabels(c.get_xticklabels(),rotation=45)
c


# In[ ]:




