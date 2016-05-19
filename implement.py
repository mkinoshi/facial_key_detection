import classifier
import data
import sys
import numpy as np
import scipy
import math


def classify(testfilename, eigenf):
	d = data.Data(testfilename)
	pictures = d.get_data(d.get_headers())
	cat = np.zeros((pictures.shape[0], 1))
	for i,each_pic in enumerate(pictures):
		c_ind = 0
		min_d = float("inf")
		for index, eigenface in enumerate(eigenf):
			dis = scipy.spatial.distance.euclidean(eigenface, each_pic)
			if dis < min_d:
				c_ind = index
				min_d = dis
		cat[i] = c_ind
	return cat

def classify_m(pictures, eigenf):
	cat = np.zeros((pictures.shape[0], 1))
	for i,each_pic in enumerate(pictures):
		c_ind = 0
		min_d = float("inf")
		for index, eigenface in enumerate(eigenf):
			dis = scipy.spatial.distance.euclidean(eigenface, each_pic)
			if dis < min_d:
				c_ind = index
				min_d = dis
		cat[i] = c_ind
	return cat

def accuracy(eigenval, catsresult, trucats):
	error_sum = 0.0
	catsresult = catsresult.tolist()
	trucats = trucats.tolist()
	eigenval = eigenval.tolist()
	num = len(catsresult)
	for index, item in enumerate(catsresult):
		error1 = (eigenval[int(item[0])][0] - trucats[index][0])
		error2 = (eigenval[int(item[0])][1] - trucats[index][1])
		error_t = error1*error1 + error2*error2
		if np.isnan(error_t):
			error_t = 0
		error_sum = error_sum + error_t
	error = math.sqrt(error_sum/num)
	return error

def implment(testdata, testcat, eigenf, eigenvalf):
	test = data.Data(testcat)
	eigenf_d = data.Data(eigenf)
	eigenv = data.Data(eigenvalf)
	test_c = test.get_data(test.get_headers())
	eigenface = eigenf_d.get_data(eigenf_d.get_headers())
	eigenval = eigenv.get_data(eigenv.get_headers())
	category_test = classify(testdata, eigenface)
	print accuracy(eigenval, category_test, test_c)


def implement_analysis(trainingdata,  testdata, trainingcat, testcat, eigenfile, method="Naive",filename=None):
	traindata = data.Data(trainingdata)
	catdata = data.Data(trainingcat)
	testdata = data.Data(testdata)
	cattestdata = data.Data(testcat)
	eigenvalues = data.Data(eigenfile)

	traincats = catdata.get_data([catdata.get_headers()[0]])
	testcats = cattestdata.get_data(cattestdata.get_headers())
	train = traindata.get_data(traindata.get_headers())
	test = testdata.get_data(testdata.get_headers())
	eigenval = eigenvalues.get_data(eigenvalues.get_headers())

	if method == "Naive":
		nbc = classifier.NaiveBayes()
		#nbc_t = classifier.NaiveBayes()
		nbc.build( train, traincats )
		#nbc_t.build(test, testcats)
		ctraincats, ctrainlabels = nbc.classify( train )
		print "accuracy is ", accuracy(eigenval, ctraincats, traincats)
		ctestcats, ctestlabels = nbc.classify(test)
		print "accuracy is ", accuracy(eigenval, ctestcats, testcats)
		"""
		print nbc.confusion_matrix_str(nbc.confusion_matrix(traincats, ctraincats))
		ctestcats, ctestlabels = nbc.classify(test)
		print nbc.confusion_matrix_str(nbc.confusion_matrix(testcats, ctestcats))
		"""
	elif method == "KNN":
		knnctrain = classifier.KNN()
		knnctrain.build(train, traincats)

		ctraincats, ctrainlabels = knnctrain.classify(train)
		print "accuracy is ", accuracy(eigenval, ctraincats, traincats)
		#print knnctrain.confusion_matrix_str(knnctrain.confusion_matrix(traincats, ctraincats))
		ctestcats, ctestlabels = knnctrain.classify(test)
		print "accuracy is ", accuracy(eigenval, ctestcats, testcats)
		#print knnctrain.confusion_matrix_str(knnctrain.confusion_matrix(testcats, ctestcats))
	#testdata.adding_column("category", "numeric", ctestcats)
	#testdata.write(filename)
def main(argv):
	"""
	if len(argv) < 3:
		print 'Usage: python %s <training data file> <test data file> <training category file> <test category file> <method> <filename>' % (argv[0])
		exit(-1)

	implement_analysis(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7])
	"""
	implment("testdataX.csv", "testdataY.csv", "eigenFace.csv", "eigenCatVal.csv")
if __name__ == "__main__":
    main(sys.argv)
