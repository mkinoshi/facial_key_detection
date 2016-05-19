import data
import random
import csv
import analysis
import numpy as np
import visualization
import math
from scipy.spatial.distance import euclidean



def normalize_by_example_m(dmatrix):
	data_m = dmatrix
	max_m = np.amax(data_m, axis=1)
	min_m = np.amin(data_m, axis=1)
	range_m = max_m-min_m
	inv_range_m = 1/range_m
	inv_range_m = inv_range_m * 255.0
	data_sub_min = data_m - min_m
	normalized = []
	for i in range(data_m.shape[0]):
		temp = inv_range_m[i] * data_sub_min[i]
		normalized.append(temp.tolist()[0])
	return np.asmatrix(normalized)

def normalize_by_example(d, dmatrix=None, filename=None):
	if filename != None:
		f = open(filename, 'ab')
		csvWriter = csv.writer(f)
	if filename != None:
		header = d.get_headers()
		typed = d.get_raw_types()
		csvWriter.writerow(header)
		csvWriter.writerow(typed)
	if dmatrix != None:
		data_m = dmatrix
	else:
		data_m = d.get_data(d.get_headers())
	max_m = np.amax(data_m, axis=1)
	min_m = np.amin(data_m, axis=1)
	range_m = max_m-min_m
	inv_range_m = 1/range_m
	inv_range_m = inv_range_m * 255.0
	data_sub_min = data_m - min_m
	normalized = []
	for i in range(data_m.shape[0]):
		temp = inv_range_m[i] * data_sub_min[i]
		normalized.append(temp.tolist()[0])
		if filename != None:
			csvWriter.writerow(temp.tolist()[0])
	if filename != None:
		f.close()
	if dmatrix != None:
		return np.asmatrix(normalized)

def runPCA(filename, savefile,representing_ratio):
	d = data.Data(filename)
	f = open(savefile, 'ab')
	csvwriter = csv.writer(f)
	pcadata = analysis.pca(d, d.get_headers())
	eigenvectors = pcadata.get_eigenvectors()
	eigenvalues = pcadata.get_eigenvalues()
	weights = pcadata.get_data_r()
	v_sum = np.sum(eigenvalues)
	s=0.0
	count = 0
	e_val = eigenvalues.tolist()
	#print "e_val", e_val
	while (s/v_sum < 0.9):
		s += e_val[0][count]
		count += 1

	print "count", count
	ind = []
	for i in range(count):
		ind.append(i)

	print "weights.shape",weights.shape
	rep_weight = weights[:,ind]
	eigenvectors = eigenvectors[ind,:]
	eigenvalues = eigenvalues.tolist()[:count]
	header =[]
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
	csvwriter.writerow(header)
	csvwriter.writerow(typed)
	eigenvec_data = eigenvectors.tolist()
	for i in range(len(eigenvec_data)):
		csvwriter.writerow(eigenvec_data[i])
	f.close()
	return eigenvectors, eigenvalues, rep_weight

def runPCA2_m(d, eigennum):
	header = []
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
	pcadata = analysis.pca_m(d, header)
	eigenvectors = pcadata.get_eigenvectors()
	eigenvalues = pcadata.get_eigenvalues()
	weights = pcadata.get_data_r()
	v_sum = np.sum(eigenvalues)
	s=0.0
	e_val = eigenvalues.tolist()
	#print "e_val", e_val
	for i in range(eigennum):
		s += e_val[0][i]
	ind = []
	for i in range(eigennum):
		ind.append(i)
	rep_weight = weights[:,ind]
	eigenvectors = eigenvectors[ind,:]
	eigenvalues = eigenvalues[:eigennum]
	
	return eigenvectors, eigenvalues, rep_weight

def runPCA2(filename,savefile,eigennum):
	d = data.Data(filename)
	f = open(savefile, 'ab')
	csvwriter = csv.writer(f)
	pcadata = analysis.pca(d, d.get_headers())
	eigenvectors = pcadata.get_eigenvectors()
	eigenvalues = pcadata.get_eigenvalues()
	weights = pcadata.get_data_r()
	v_sum = np.sum(eigenvalues)
	s=0.0
	e_val = eigenvalues.tolist()
	#print "e_val", e_val
	for i in range(eigennum):
		s += e_val[0][i]

	print "count", s/v_sum
	ind = []
	for i in range(eigennum):
		ind.append(i)

	print "weights.shape",weights.shape
	rep_weight = weights[:,ind]
	eigenvectors = eigenvectors[ind,:]
	eigenvalues = eigenvalues[:eigennum]
	header = []
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
	csvwriter.writerow(header)
	csvwriter.writerow(typed)
	eigenvec_data = eigenvectors.tolist()
	for i in range(len(eigenvec_data)):
		csvwriter.writerow(eigenvec_data[i])
	f.close()
	return eigenvectors, eigenvalues, rep_weight


def create_cat(filename, catfile, rep_weight, eigenvectors, savefile_cat, savefile_eig):
	d = data.Data(filename)
	x_mean, y_mean = creating_stand(catfile, rep_weight)
	f = open(savefile_cat, 'ab')
	f2 = open(savefile_eig, 'ab')
	writer = csv.writer(f)
	writer2 = csv.writer(f2)
	writer.writerow(["category"])
	writer.writerow(["numeric"])

	writer2.writerow(["x", "y"])
	writer2.writerow(["numeric", "numeric"])

	pictures = d.get_data(d.get_headers())
	cat = np.zeros((pictures.shape[0], 1))
	for i,each_pic in enumerate(pictures):
		c_ind = 0
		min_d = float("inf")
		for index, eigenface in enumerate(eigenvectors):
			dis = euclidean(eigenface, each_pic)
			if dis < min_d:
				c_ind = index
				min_d = dis
		cat[i] = c_ind
	cat = cat.tolist()
	for i in range(len(cat)):
		writer.writerow(cat[i])
	f.close()

	x_mean = x_mean.tolist()
	y_mean = y_mean.tolist()
	for i in range(len(x_mean)):
		dlist = []
		dlist.append(x_mean[i])
		dlist.append(y_mean[i])
		writer2.writerow(dlist)
	f2.close()


def calculate_stand_pixel(filename, catfile, rep_weight):
	d = data.Data(filename)
	d2 = data.Data(catfile)
	ori_d = d.get_data(d.get_headers())
	cat = d2.get_data(d2.get_headers())
	true = np.floor(cat)
	index = true[:,0]+true[:,1]*96
	print "index", index

def creating_stand(catfile, rep_weight):
	minR = np.min(rep_weight, axis=0)
	maxR = np.max(rep_weight, axis=0)
	rangeR = maxR - minR
	rep_weight_norm = 1-((maxR - rep_weight)/rangeR)
	rep_weight_sum = np.sum(rep_weight_norm, axis=0)
	rep_weight_norm = rep_weight_norm/rep_weight_sum

	#calculating the mean of the center
	d2 = data.Data(catfile)
	left_center_xmean = d2.get_data(["left_eye_center_x"])
	temp_x = np.zeros((rep_weight_norm.shape[0], rep_weight_norm.shape[1]))
	for i in range(rep_weight_norm.shape[1]):
		temp_x[:,i] = np.squeeze(np.multiply(rep_weight_norm[:,i],left_center_xmean))
	temp_c_x = np.nansum(temp_x, axis=0)
	temp_c_xm = np.asmatrix(temp_c_x)
	sum_all_x = np.nansum(temp_c_xm)

	left_center_ymean = d2.get_data(["left_eye_center_y"])
	temp_y = np.zeros((rep_weight_norm.shape[0], rep_weight_norm.shape[1]))
	for i in range(rep_weight_norm.shape[1]):
		temp_y[:,i] = np.squeeze(np.multiply(rep_weight_norm[:,i],left_center_ymean))
	temp_c_y = np.nansum(temp_y, axis=0)
	temp_c_ym = np.asmatrix(temp_c_y)
	sum_all_y = np.nansum(temp_c_ym)
	#adding some margins to search
	
	
	return temp_c_x, temp_c_y

def creating_stand_m(d, rep_weight):
	minR = np.min(rep_weight, axis=0)
	maxR = np.max(rep_weight, axis=0)
	rangeR = maxR - minR
	rep_weight_norm = 1-((maxR - rep_weight)/rangeR)
	rep_weight_sum = np.sum(rep_weight_norm, axis=0)
	rep_weight_norm = rep_weight_norm/rep_weight_sum

	left_center_xmean = d[:,0]
	temp_x = np.zeros((rep_weight_norm.shape[0], rep_weight_norm.shape[1]))
	for i in range(rep_weight_norm.shape[1]):
		temp_x[:,i] = np.squeeze(np.multiply(rep_weight_norm[:,i],left_center_xmean))
	temp_c_x = np.nansum(temp_x, axis=0)
	temp_c_xm = np.asmatrix(temp_c_x)
	sum_all_x = np.nansum(temp_c_xm)

	left_center_ymean = d[:,1]
	temp_y = np.zeros((rep_weight_norm.shape[0], rep_weight_norm.shape[1]))
	for i in range(rep_weight_norm.shape[1]):
		temp_y[:,i] = np.squeeze(np.multiply(rep_weight_norm[:,i],left_center_ymean))
	temp_c_y = np.nansum(temp_y, axis=0)
	temp_c_ym = np.asmatrix(temp_c_y)
	sum_all_y = np.nansum(temp_c_ym)

	cat = np.zeros((rep_weight_norm.shape[1],2))
	cat[:,0] = temp_c_x
	cat[:,1] = temp_c_y
	
	return cat

def calculate_error(testcatfile, estimate):
	d = data.Data(testcatfile)
	left_eye_center = d.get_data(d.get_headers())
	estimate_m = np.asmatrix(estimate)
	error = np.zeros((left_eye_center.shape[0],1))
	for i in range(left_eye_center.shape[0]):
		temp = left_eye_center[i] - estimate_m
		temp = np.multiply(temp, temp)
		temp = np.sum(temp)
		error[i] = temp
	error_sum = np.nansum(error)
	error_squared = error_sum/left_eye_center.shape[0]
	error_ret = math.sqrt(error_squared)
	print error_ret


 	#streching eigen faces
	#eigenfaces = pre_analyze.normalize_by_example(pcadata, eigenvectors)
	#print "eigenvectors", eigenvectors


	#visualization.show_picture(eigenfaces.tolist())
	"""
	#f = open(savefile, 'ab')
	#savedfile = csv.writer(f)
	#savedfile.writerow(pcadata.get_data_headers())
	#savedfile.writerow(pcadata.get_raw_types())
	evals = pcadata.get_eigenvalues().tolist()
	sum_evals = np.sum(evals)
	s = 0.0
	count = 0
	while(s/sum_evals < representing_ratio):
		s += evals[0][count]
		count += 1

	#Eigen faces
	datam = pcadata.get_data_row().tolist()
	temp = []
	#for i in range(count):
		#savedfile.writerow(datam[i])

	#reconstructing 
	print "sum_evals", sum_evals
	print "s", s
	print "s/sum_evals", s/sum_evals
	print "count", count
	f.close()
	"""

def main():
	#eigvec, eigval, weight = runPCA("trainNorm.csv", "PCA90trainNorm.csv", 0.9)
	#calculate_stand_pixel("trainNorm.csv", "traindataY.csv", weight)
	#creating_stand( "traindataY.csv", weight)
	#runPCA2("trainNorm.csv", 20)
	#calculate_error("testdataY.csv", [66,37])
	#d = data.Data("testdataX.csv")
	#pixel = d.get_data(d.get_headers())
	#pixel = pixel.tolist()
	#visualization.show_picture_estimate(pixel, [66,37])
	#eigenvectors, eigenvalues, rep_weight = runPCA2("trainNorm.csv", 20)
	#create_cat("trainNorm.csv", "traindataY.csv", rep_weight, eigenvectors, "eigenCat.csv", "eigenCatVal.csv")
	eigenvectors, eigenvalues, rep_weight = runPCA2("trainNorm.csv", "eigenFace.csv", 20)
if __name__ == "__main__":
    main()