#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:39:26 2018

@author: lishuo
"""

import Backtest_Platform as bp
import pandas as pd
import pickle
#===================================== Read Files ===================================== 
fname1 = "DataValuesNEW.xlsx"
data_to_parse = pd.read_excel(fname1, header = None)
fname2 = "ContractSpecifications.xlsx"
df_spec = pd.read_excel(fname2, header = 0)
df_spec.set_index('ID', inplace=True)
fname3 = "Systems.xlsx"
df_sys = pd.read_excel(fname3, header = 0)

total_capital = 1000000
sys_list = bp.get_system_dict_list(df_sys)
markets = bp.get_market_data(data_to_parse, window=6)
mkt_keys = list(markets.keys())

markets= bp.process_market_data(mkt_keys, markets, total_capital, df_spec, sys_list)

#=====================================  write python dict to a file ======================
output_fname= "mkt_dat_dict_Output.pkl"
output_dir = "./"
output = open(output_dir + output_fname, 'wb')
pickle.dump(markets, output)
output.close()
print("Export Finished.")

#===================================== Test: read pickle file back ======================
pkl_file = open(output_dir + output_fname, 'rb')
tmp = pickle.load(pkl_file)
pkl_file.close()
len(tmp.keys())

print(tmp['US1 Comdty'].head())