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
trainFile = "train"
testFile = "test"
ext = ".csv"
modelFile = "finalVizModel"
modelExt = ".pkl"
iterations = 170
fileSet = 3
results = np.zeros(iterations)

for run in range(iterations):

	print("Training iteration "+str(run+1))
	print("Preparing data...")
	trainingDataSet = pd.read_csv(trainFile+str(fileSet)+ext)
	trainingDataSet['lidar_array'] = trainingDataSet['lidar_array'].map(lambda x: x.lstrip('[').rstrip(']'))

	testingDataSet = pd.read_csv(testFile+str(fileSet)+ext)
	testingDataSet['lidar_array'] = testingDataSet['lidar_array'].map(lambda x: x.lstrip('[').rstrip(']'))

	XTrain = trainingDataSet.lidar_array
	XTrain = XTrain.str.split(',', expand=True)
	XTrain = XTrain.apply(pd.to_numeric)
	YTrain = trainingDataSet.angular_velocity #.linear_velocity

	#print(XTrain)

	XTest = testingDataSet.lidar_array
	XTest = XTest.str.split(',', expand=True)
	XTest = XTest.apply(pd.to_numeric)
	YTest = testingDataSet.angular_velocity #.linear_velocity

	model = MLPRegressor(max_iter=run+1, random_state=1, hidden_layer_sizes=(15,15,)) #defaut was (100,100)

	print("Training model...")
	model.fit(XTrain,YTrain)
	print("Model trained!")

	print("Model accuracy: {0:.2f} %".format(100*model.score(XTest, YTest)))
	
	results[run] = (100*model.score(XTest, YTest)).round(2)

	if(run==iterations-1):
		print(results)
		plt.figure(figsize=(45,10))
		plt.plot(np.arange(1,iterations+1,1),results,'ro')
		plt.xticks(np.arange(1,iterations+1,1))
		plt.grid()
		plt.savefig('result_graph.png', dpi=100)
		
		print("Generating model file...")
		joblib.dump(model, modelFile+modelExt)
		print("Model file generated!")
