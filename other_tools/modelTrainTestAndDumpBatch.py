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
import pandas as pd

## FILE PARAMS, edit as needed
trainFile = "train"
testFile = "test"
ext = ".csv"
modelFile = "model"
modelExt = ".pkl"

for run in range(5):

	print("Run "+str(run+1))
	print("Preparing data...")
	trainingDataSet = pd.read_csv(trainFile+str(run+1)+ext)
	trainingDataSet['lidar_array'] = trainingDataSet['lidar_array'].map(lambda x: x.lstrip('[').rstrip(']'))

	testingDataSet = pd.read_csv(testFile+str(run+1)+ext)
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

	model = MLPRegressor(max_iter=300, activation = "relu", hidden_layer_sizes=(15,15,15,)) #defaut was (100,100)

	print("Training model...")
	model.fit(XTrain,YTrain)
	print("Model trained!")

	print("Model accuracy: {0:.2f} %".format(100*model.score(XTest, YTest)))

	print("Generating model file...")
	joblib.dump(model, modelFile+str(run+1)+modelExt)
	print("Model file generated!")
