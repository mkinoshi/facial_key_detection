import data
import csv
import math
import numpy as np
import visualization
import scipy
from sklearn.cross_validation import train_test_split
import random

def csv_pre_train(filename):
	f = file(filename, 'rU')
	reader = csv.reader(f)
	headers = reader.next()
	data = []
	for index, row in enumerate(reader):
		temp = []
		for item in row:
			item = item.strip()
			temp.append(item)
		data.append(temp[:])
	len_pre_train = int(len(data)*1/4)
	s1 = filename[:-4] + "Pre.csv"
	f1 = open(s1, 'ab')
	csvWriter1 = csv.writer(f1)
	csvWriter1.writerow(headers)
	for i in range(len(data[:len_pre_train])):
		csvWriter1.writerow(data[i])
	return s1

def csv_data_key(filename, savefile):
	f1 = file(filename, 'rU')
	f2 = open(savefile, 'ab')
	csvwriter = csv.writer(f2)
	reader = csv.reader(f1)
	headers = reader.next()[:-1]
	typed = []
	for i in range(len(headers)):
		typed.append("numeric")
		d = []
	for index, row in enumerate(reader):
		temp = []
		for item in row[:-1]:
			if item == " ":
				item = np.nan
			item = item.strip()
			temp.append(item)
		d.append(temp[:])
	csvwriter.writerow(headers)
	csvwriter.writerow(typed)
	for i in range(len(d)):
		csvwriter.writerow(d[i])
	

def create_cat(data, column_name):
	col = data.get_data([column_name])
	pixel_li = data.get_image_data()

def determine_eye_size(filename1):
	d1 = data.Data(filename1)
	cx = d1.get_data(["left_eye_center_x"])
	icx = d1.get_data(["left_eye_inner_corner_x"])
	ocx = d1.get_data(["left_eye_outer_corner_x"])
	cy = d1.get_data(["left_eye_center_y"])
	icy = d1.get_data(["left_eye_inner_corner_y"])
	ocy = d1.get_data(["left_eye_outer_corner_y"])
	range_x = ocx - icx
	range_y = ocy -icy
	print "left_eye_inner_corner_x_mean", np.nanmean(icx)
	print "left_eye_outer_corner_x_mean", np.nanmean(ocx)
	print "left_eye_center_x_mean", np.nanmean(cx)
	print "range_x mean", np.nanmean(range_x)
	print "range_x std dev", np.nanstd(range_x)
	print "left_eye_inner_corner_y_mean", np.nanmean(icy)
	print "left_eye_outer_corner_y_mean", np.nanmean(ocy)
	print "left_eye_center_y_mean", np.nanmean(cy)
	print "range_y mean", np.nanmean(range_y)
	print "range_y std dev", np.nanstd(range_y)

def create_data_clustering(data, filenameTrain, filenameCat):
	f = open(filenameTrain, 'ab')
	f2 = open(filenameCat, 'ab')
	csvWriter1 = csv.writer(f)
	csvWriter2 = csv.writer(f2)
	header = []
	category_dic = {}
	typed = []
	for row in range(96):
		for columns in range(96):
			if row+1 < 10:
				sr = str(0) + str(row+1)
			else:
				sr = str(row+1)
			if columns + 1<10:
				sc = str(0) + str(columns+1)
			else:
				sc = str(columns+1)
			s1 = "pixel_" + sr + sc
			header.append(s1)
			typed.append("numeric")
	csvWriter1.writerow(header)
	csvWriter1.writerow(typed)
		

	header2 = ["left_eye_center_x", "left_eye_center_y"]
	typed = ["numeric", "numeric"]
	#I divide image into 36 categories each category has 16*16 pixel
	cat = data.get_data(["left_eye_center_x", "left_eye_center_y"]).tolist()
	csvWriter2.writerow(header2)
	csvWriter2.writerow(typed)
	image  = data.get_image_data()
	#print "image", image
	for i in range(len(image)):
		csvWriter1.writerow(image[i])
		csvWriter2.writerow(cat[i]) 

	#print "data.get_data(["Image"])",data.get_data(["Image"])
	f.close()
	f2.close()

def cross_validation_m(fileData, fileCat, train_ratio, test_ratio):
	dfile = data.Data(fileData)
	catfile = data.Data(fileCat)
	dfile_data = dfile.get_data(dfile.get_headers())
	catfile_data = catfile.get_data(catfile.get_headers())
	X_train, X_test, y_train, y_test = train_test_split( dfile_data, catfile_data, test_size=test_ratio, random_state=0)
	train_num = int(dfile_data.shape[0] * train_ratio)
	train_num_indecies = random.sample(range(X_train.shape[0]), train_num)
	X_train = X_train[train_num_indecies, :]
	y_train = y_train[train_num_indecies, :]
	return X_train, X_test, y_train, y_test

def cross_validation(fileData, fileCat, train_ratio, test_ratio, s1, s2, s3, s4):
	dfile = data.Data(fileData)
	catfile = data.Data(fileCat)
	dfile_data = dfile.get_data(dfile.get_headers())
	catfile_data = catfile.get_data(catfile.get_headers())

	ftrainX = open(s1, 'ab')
	ftrainY = open(s2, 'ab')
	ftestX = open(s3, 'ab')
	ftestY = open(s4, 'ab')
	trainX = csv.writer(ftrainX)
	trainY = csv.writer(ftrainY)
	testX = csv.writer(ftestX)
	testY = csv.writer(ftestY)

	#writing header to trainX and testX
	trainX.writerow(dfile.get_headers())
	testX.writerow(dfile.get_headers())

	#writing types to trainX and testX
	trainX.writerow(dfile.get_raw_types())
	testX.writerow(dfile.get_raw_types())

	#writing header to trainY and testY
	trainY.writerow(catfile.get_headers())
	testY.writerow(catfile.get_headers())

	#writing type to trainY and testY
	trainY.writerow(catfile.get_raw_types())
	testY.writerow(catfile.get_raw_types())

	X_train, X_test, y_train, y_test = train_test_split( dfile_data, catfile_data, test_size=test_ratio, random_state=0)

	#create testX and testY
	testX_list = X_test.tolist()
	testY_list = y_test.tolist()
	for i in range(len(testY_list)):
		testX.writerow(testX_list[i])
		testY.writerow(testY_list[i])

	#create trainX and tainY
	train_num = int(dfile_data.shape[0] * train_ratio)
	train_num_indecies = random.sample(range(X_train.shape[0]), train_num)
	trainX_list = X_train.tolist()
	trainY_list = y_train.tolist()
	for num in train_num_indecies:
		trainX.writerow(trainX_list[num])
		trainY.writerow(trainY_list[num])

	ftrainX.close()
	ftrainY.close()
	ftestX.close()
	ftestY.close()

def pre_analyze_preparation():
	trainingdata = data.FacialData("training.csv")
	create_data_clustering(trainingdata, "dataX.csv", "dataY.csv")


def pre_analyze_param(trainratio, testratio):
	X_train, X_test, y_train, y_test = cross_validation_m("dataX.csv", "dataY.csv", trainratio, testratio)
	return X_train, X_test, y_train, y_test

	

def main():
	#f = csv_pre_train("training.csv")
	#pixelInfo = visualization.show_pictures_data("training.csv")
	#visualization.show_picture(pixelInfo)
	#traingdata = data.FacialData("trainingPre.csv")
	#create_data_clustering(traingdata, "trainingPreX.csv", "trainingPreY.csv")
	#trainingdata = data.FacialData("training.csv")
	#create_data_clustering(trainingdata, "dataX.csv", "dataY.csv")
	d = data.Data("traindataX.csv")
	#pixel = d.get_data(d.get_headers())
	#print "pixel.shape", pixel.shape
	#pixel = pixel.tolist()
	#print "len(pixelInfo)", len(pixelInfo)
	#print "len(pixel)", len(pixel.tolist())
	#print "pixelInfo[0]", pixelInfo[0]
	#print "pixel.tolist()[0]",pixel.tolist()[0]
	#visualization.show_picture(pixel)
	normalize_by_example(d, filename="trainNorm.csv")
	#csv_data_key("training.csv", "trainingKey.csv")
	#determine_eye_size("trainingKey.csv")


if __name__ == "__main__":
    main()