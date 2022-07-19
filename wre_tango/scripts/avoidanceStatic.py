#!/usr/bin/env python3

import rospy
import math
import sys
from sklearn.neural_network import MLPRegressor
import joblib
import pandas as pd
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

#to run:
#rosrun wre_tango avoidance.py filepath filename
#rosrun wre_tango avoidance.py ~/catkin_ws/bagfiles/final_static/static_thresholded_results/test_train_data/models/3_layers/15_nodes/ model2.pkl

#rosrun wre_tango thresholdAvoidance.py ~/catkin_ws/bagfiles/final_dynamic/dynamic_thresholded_results/test_train_data/models/3_layers/10_nodes/ model4.pkl

directory = sys.argv[1]
filename = sys.argv[2]
model = joblib.load(directory+filename)

def robRead(msg):
	segments = 20
	lasers_per_segment = 720//segments #for real robot
	#lasers_per_segment = 359//segments #for simulation
	current_laser = 0
	thold = 1.5
	
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1000)
	
	segment_vals = []
	for _ in range(segments):
		temp = 1.0
		for y in range(current_laser, current_laser+lasers_per_segment):
			if (math.isinf(msg.ranges[y]) == False):
				if (msg.ranges[y] < thold):
					if (msg.ranges[y] < thold):
						temp += msg.ranges[y]
					else:
						temp += thold
				else:
					temp += thold
		segment_vals.append(temp/lasers_per_segment)
		current_laser+=lasers_per_segment
		
	current_laser = 0
	
	###THIS WORKAROUND IS AWFUL AND I HATE IT
	val_string = ','.join(map(str, segment_vals))
	df = pd.DataFrame([val_string], columns=['0'])
	df = df['0'].astype(str)
	df = df.str.split(',', expand=True)
	df = df.apply(pd.to_numeric)
	###THERE MUST BE A BETTER WAY SOMEHOW
	
	result = model.predict(df)
	#print(segment_vals)
	print(result)
	out = Twist()
	out.linear.x = 0.5 #0.2
	out.angular.z = result[0]
	pub.publish(out)



if __name__ == "__main__":
	rospy.init_node('wreavoid')

	rospy.Subscriber('/scan', LaserScan, robRead)

	rospy.spin()
	
