import pandas as pd
import matplotlib.pyplot as plt
import os 
import random

df = pd.read_csv("Voters.csv")

for i in range(len(df["Stake(MKR)"])):
    df["Stake(MKR)"][i] = df["Stake(MKR)"][i].replace(',', "")

df = df.astype({'Stake(MKR)': 'float'})
total_governance_stake = sum(df["Stake(MKR)"])

df["NormalizedStake"] = df["Stake(MKR)"]/total_governance_stake

## creating a plot of voter activity 
## for the top 10 addresses in the dataframe
smalldf = df[0:10]

smalldf['Datetime'] = pd.to_datetime(smalldf['Last voting'])

smalldf = smalldf.set_index(['Datetime'])


fig, ax = plt.subplots(2)
fig.set_figheight(10)
fig.set_figwidth(16)


colors = []
for i in range(10):
    c = (random.random(), random.random(), random.random())
    colors.append(c)


smalldf = smalldf.sort_values(by=['NormalizedStake'], ascending=True)
smalldf['shortAddress'] = smalldf['Address']

for i in range(len(smalldf)):
    smalldf['shortAddress'][i] =  smalldf['shortAddress'][i][0:10]
ax[0].bar(smalldf['shortAddress'], smalldf["NormalizedStake"], color=colors)
ax[0].set_title("Governance token distribution for the 10 largest individual stakeholders")
ax[0].set_ylabel(r'Relative Stake ($\alpha \in [0,1]$)')
ax[0].set_xlabel('Voter address')
plt.setp(ax[0].get_xticklabels(), rotation=30, horizontalalignment='right')

plt.subplots_adjust(bottom=-.2, right=0.8, top=1)

ax[1].set_title("Voting Activity for Top 10 MKR Stakeholders")
ax[1].set_ylabel('Total Voting Activity')
ax[1].set_xlabel('Date')
    

whalenames = []
j = 0 # tmp var just to track color 

## Reading in each of the 10 csv files 
for fp in os.listdir("whales"):
    
    tmp = pd.read_csv(f"whales/{fp}")
    name = fp.split(".")[0]
    whalenames.append(name)
    for i in range(len(tmp["Time"])):
        tmp["Time"][i] = tmp["Time"][i].split(' ')[0] + " " + tmp["Time"][i].split(' ')[1]
        
    tmp['Datetime'] = pd.to_datetime(tmp['Time'])
    tmp = tmp.sort_values(by=['Datetime'])
    tmp = tmp.set_index(['Datetime'])

    tmp["activity"] = [i for i in range(1,len(tmp)+1)]
    ax[1].plot_date(tmp.index, tmp["activity"], linestyle='solid', label=name[0:10], color = colors[len(colors)-1-j])
    j+=1
ax[1].legend()

## one whale has never voted! 
non_voting_whale = [x for x in smalldf["Address"] if x not in whalenames][0]
non_voting_stake = 0
whale_ownership = 0
for i in range(len(smalldf)):
    whale_ownership += smalldf["NormalizedStake"][i]
    if smalldf["Address"][i] == non_voting_whale:
        non_voting_stake = smalldf["NormalizedStake"][i]
print(f"address {non_voting_whale} owns {non_voting_stake}!")
print(f"total ownership by top 10 addresses is {whale_ownership}!")
