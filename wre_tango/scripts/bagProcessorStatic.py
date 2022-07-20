#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : William Robert Evans [wre]
# Created Date: 20/07/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Description, to be added"""
# ---------------------------------------------------------------------------

import rospy
import math
import sys
import os
import csv
import rosbag

#to run:
#rosrun wre_tango thresholdBagProcessor.py ~/catkin_ws/bagfiles/final_static run1...bag

segments = 20
#segments start from 0, make an option to start segments not from 0 maybe?
lasers_per_segment = 720//segments
#print(lasers_per_segment)
current_laser = 0
thold = 1


filename = sys.argv[2]
directory = sys.argv[1]

print("Reading the rosbag file...")
if not directory.endswith("/"):
	directory += "/"
extension = ""
if not filename.endswith(".bag"):
	extension = ".bag"
bag = rosbag.Bag(directory + filename + extension)

# Create directory with name filename (without extension)
#results_dir = directory + filename[:-4] + "_results"
#change this for left and right
results_dir = directory + "static_thresholded" + "_results" ###change this line as needed
if not os.path.exists(results_dir):
	os.makedirs(results_dir)

print("Processing Lidar data...")

def get_closest_vel(time):
	for topic, msg, t in bag.read_messages(topics=['/cmd_vel']):
		if (t < time):
			continue
		else:
			return round(msg.angular.z, 5) #.angular.z , .linear.x
	return 0.0

with open(results_dir +"/"+filename+'_processed.csv', mode='w') as data_file:
	data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	data_writer.writerow(['time', 'lidar_array', 'angular_velocity'])
	# Get all message on the /scan topic
	for topic, msg, t in bag.read_messages(topics=['/scan']):
		### PROCESSING OF LIDAR GOES HERE
		segment_vals = []
		for _ in range(segments):
			temp = 0.0
			for y in range(current_laser, current_laser+lasers_per_segment): #count is not needed, apply a threshold instead - any value over 1 gets assigned the value of 1
				if (math.isinf(msg.ranges[y]) == False):
					if (msg.ranges[y] < thold):
						temp += msg.ranges[y]
					else:
						temp += thold
				else:
					temp += thold
			segment_vals.append(temp/lasers_per_segment)
			current_laser+=lasers_per_segment
		data_writer.writerow([t, segment_vals, get_closest_vel(t)])
		current_laser = 0
		###

print("Finished creating csv file!")
bag.close()
