#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:26:39 2018

@author: lishuo
"""

import Backtest_Platform as bp
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# turn off the warning in backtesting
pd.options.mode.chained_assignment = None  # default='warn'


#===================================== Part 1: Read data =====================================

fname1 = "mkt_dat_dict_Recent_Output.pkl"
dir_path1 = ""
markets = bp.read_pickle_file(dir_path1, fname1)
fname2 = "ContractSpecificationsRecent.xlsx"
df_spec = pd.read_excel(fname2, header = 0)
df_spec.set_index('BLOOMBERG TICKER', inplace=True)

fname3 = "CorrelatedMktsRecent.xlsx"
corr_mkts = pd.read_excel(fname3, header = None)
corr_mkts = corr_mkts.T

fname4 = "Risk Free Rate and CTA Index Data.xlsx"
df_rf = pd.read_excel(fname4, skiprows=1, 
                      usecols=[0,1,2], index_col=0, 
                      names=["PX_LAST","rf"])
df_cta = pd.read_excel(fname4, skiprows=1, 
                       usecols=[4,5,6], index_col=0,
                       names=["PX_LAST","CTA Return"]).dropna()
df_rf['index'] = [str(cur)[:7] for cur in df_rf.index.tolist()]
df_rf.set_index('index', inplace=True)

#===================================== Part 2: Backtest =====================================
# Specify the backtest period
start_date = datetime(2014, 1, 1)
end_date = datetime(2018, 2, 1)
total_capital = 1000000
# Specify the information, i.e. columns in the history
port_col_list = ['Units', 'Contracts', 'Stop Level', 'Unrealized PnL', 'Realized PnL', 'LongOrNot']
# sys_index = System 1, sys_index2 = System 2
sys_index, sys_index2 = [8, 9, 10, 11], [12, 13, 14, 15]
# Specify the information, i.e. columns in the blotter
col_list = ['MktID', 'Entry Date', 'LongOrNot', 'Live', 'Entry Price', 'N', 
            'Unit Size', 'Units', 'Stop Level', 'Exit Price', 'Exit Date', 
            'StopOrExit', 'Realized PnL', 'Nth Unit']
# Limits for single market, direction, closely and loosely correlated markets
switch = [True, True, True, True]
limits = [4, 12, 6, 10]

# Recent data stop_level_factor = 1
#=======================
stop_level_factor = 1 #=
#=======================

t = time.time()

print("Backtest Started...")
blotter1, history   = bp.Backtest(markets, df_spec, total_capital, col_list, start_date, 
                               end_date, port_col_list, sys_index, bp.whipsaw_stop_level, 
                               switch, limits, corr_mkts, stop_level_factor)
print("Backtest Finished.")
print("Time used = ", time.time() - t, "seconds.")

#=========================== Part 3: Performance Analysis ===========================
#=========================== 3.1 Portfolio NAV ===========================
#total_capital = 1000000
_,port_nav = bp.get_portfolio_nav(history, total_capital)
temp_index = [pd.Timestamp(cur) for cur in port_nav.index]
port_nav_copy = port_nav.copy()
port_nav_copy.index = temp_index
#print("Portfolio NAV Plot")
port_nav_copy.plot(title="Portfolio NAV Plot")

# =========================== 3.2 NAVs by Markets ===========================
navs_by_markets = bp.get_nav(history, total_capital)
df_navs = pd.DataFrame(navs_by_markets, index=temp_index)
#print("NAV Plot by markets")
ax = df_navs.plot(title="NAV by Markets",legend=True)
ax.legend(bbox_to_anchor=(1, 1.2))

# =========================== 3.3 Statistics Calculation ===========================
mon_ret = bp.get_monthly_return(navs_by_markets, history, total_capital)
df_stat = bp.get_stats(mon_ret, history, total_capital, df_rf)
#print("Performance Statistics")
print(df_stat)

#=========================== 3.4 Drawdown Analysis ===========================
dd, mdd = bp.get_drawdown(mon_ret.iloc[:,0], total_capital)
#print("Maximum Drawdown")
print(mdd)

#=========================== 3.5 Correlation Check ===========================
#print("Monthly Portfolio NAV vs. CTA Plot")
df_port_temp = pd.DataFrame(port_nav, index=temp_index, columns=['NAV'])
mon_index = bp.get_month_index(port_nav)
df_port_temp.iloc[mon_index,:].plot(title="Portfolio NAV")
new_mon_ret = bp.get_ret(port_nav[mon_index])[1:]
fig, ax = plt.subplots()
ax = df_cta['PX_LAST']['2014-01':'2018-02'].plot(title="Monthly NAV vs CTA Index",legend=False, style='r-')
ax2 = ax.twinx()
df_port_temp.iloc[mon_index,:].plot(ax=ax2)
ax2.legend([ax.get_lines()[0], ax2.get_lines()[0]], ['CTA Index','System 1'])

# The correlation between system 1 and CTA during 1986 to 1989 is 0.71.
sys1_corr = np.corrcoef(df_cta['CTA Return']['2014-01':'2018-01'].tolist(), new_mon_ret.tolist())
print("Correlation with CTA = ",sys1_corr[0,1])


#=========================== Get as of date blotter =========================== 
test_blotter = bp.get_blotter(blotter1, history, markets, df_spec, '2014-04-09')

#===========================  Get history Summary ===========================
#NOTE: This function require a recent version of pandas 
#test_profile = bp.get_profile(test_blotter, history, markets, df_spec, '1984-04-09', show_details = False)









