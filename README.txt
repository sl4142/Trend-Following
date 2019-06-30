1. Introduction:
The main file is Backtest_Platform.py which contains all the functionalities of the backtest platform. It contains two parts, the Data Handler and the Backtest. 

Data Handler (DH) will preprocess raw market data and prepare the input for the backtest main function. DH can exclude bad data, calculate N, TR, Unit Size, etc. Then, it can transform the data into a dictionary of market data and export to a pickle file. 

Backtest (BT) contains three parts, Reading Data, Backtest main function, and performance analysis. First read in the output, the pickle file, from the Data Handler and other datasets such as the Contract Specification, Risk Free Rate and CTA Index Data, and Correlated Markets. 

Second, set the Backtest parameters (See Backtest_1980.py or Backtest_Recent.py for details) and run the backtest.

Finally, use the supporting functions to analysis the performance.

2. General Instructions:
(1). Run Data Handler and get the pickle file containing the processed market data.
(2). Read in the pickle file and prepare for the input for backtest main function
(3). Set backtest parameters and run the backtest
(4). Performance Analysis

3. Examples:
We provide examples for both Data Handler and backtest. See Data_Handler.py, Backtest_1980.py and Backtest_Recent.py for details.

NOTE:
(1). Please put Backtest_Platform.py in the same folder as Data_Handler.py, Backtest_1980.py and Backtest_Recent.py.
(2). The stop level factors are DIFFERENT for 1980's data and recent data. Please see Backtest_1980.py and Backtest_Recent.py for details. 