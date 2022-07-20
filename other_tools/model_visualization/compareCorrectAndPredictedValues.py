#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : William Robert Evans [wre]
# Created Date: 20/07/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Description, to be added"""
# ---------------------------------------------------------------------------

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import joblib
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

## FILE PARAMS, edit as needed
testFile = "test"
ext = ".csv"
modelFile = "finalVizModel"
modelExt = ".pkl"
fileSet = 3

print("Preparing data...")

testingDataSet = pd.read_csv(testFile+str(fileSet)+ext)
testingDataSet['lidar_array'] = testingDataSet['lidar_array'].map(lambda x: x.lstrip('[').rstrip(']'))

XTest = testingDataSet.lidar_array
XTest = XTest.str.split(',', expand=True)
XTest = XTest.apply(pd.to_numeric)
YTest = testingDataSet.angular_velocity #.linear_velocity

model = joblib.load(modelFile+modelExt)

iterations = len(YTest)
results = np.zeros(iterations)

print("Running predictions...")
for run in range(iterations):
	
	results[run] = model.predict(XTest.iloc[[run]]).round(2)

	if(run==iterations-1):
		print(results)
		print(YTest.to_numpy())
		print("Creating graph...")
		plt.figure(figsize=(45,10))
		plt.plot(np.arange(1,iterations+1,1),results,'ro', label="Predicted value")
		plt.plot(np.arange(1,iterations+1,1),YTest.to_numpy(),'bs', label="Actual value")
		#plt.xticks(np.arange(1,iterations+1,1))
		plt.grid()
		plt.xlabel("Data instance")
		plt.ylabel("Angular velocity")
		plt.legend(loc="upper left")
		plt.savefig('compare_result_graph.png', dpi=100)
		print("Done!!")
