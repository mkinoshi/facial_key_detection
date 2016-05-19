#analysis.py
#Makoto Kinoshita
#02/22/16
import data
import numpy as np
from scipy import stats
import scipy.cluster.vq as vq
import random
import math

#returns the range of data in a specified columns
def data_range(data, header_names_list):
	target = data.get_data(header_names_list)
	#print target
	minlist = target.min(0)
	maxlist = target.max(0)
	#print "maslist and minlist are", maxlist, minlist
	result = np.concatenate((minlist.T, maxlist.T), axis=1)
	return result.tolist()

#returns the mean of data in columns which are specified by header_name_list
def mean(data, header_names_list):
	target = data.get_data(header_names_list)
	return np.mean(target, axis = 0).tolist()

#returns the standard deviation of data in columns which are specified by header_name_list
def stdev(data, header_names_list):
	target = data.get_data(header_names_list)
	return np.std(target, axis = 0, ddof=1).tolist()

#nomalizes each columns so that minimum number is 0 and the max number is 1
def normalize_columns_separately(data, header_names_list):
	target = data.get_data(header_names_list)
	minC = np.min(target, axis=0)
	maxC = np.max(target, axis=0)
	rangeC = maxC - minC
	new_matrix = 1- ((maxC - target)/rangeC)
	return new_matrix

#for matrix
def normalize_columns_separately_m(dmatrix):
	target = dmatrix
	minC = np.min(target, axis=0)
	maxC = np.max(target, axis=0)
	rangeC = maxC - minC
	new_matrix = 1- ((maxC - target)/rangeC)
	return new_matrix

#nomalizes all columns together so that minimum number is 0 and the max number is 1
def normalize_columns_together(data, header_names_list):
	target = data.get_data(header_names_list)
	minA = np.min(target)
	maxA = np.max(target)
	rangeA = maxA - minA
	new_matrix = 1 - ((maxA - target)/rangeA)
	return new_matrix

#This fucntion implemets linear regression and return coeffiients, sse, R2, t-value, p-value
def linear_regression(d, ind, dep):
	y = d.get_data(dep)
	A = d.get_data(ind)
	N = d.get_raw_num_rows()
	ones = np.ones([N, 1])
	A = np.column_stack((A, ones))
	AAinv = np.linalg.inv(np.dot(A.T,A))
	x = np.linalg.lstsq(A,y)
	b = x[0]
	C = len(b)
	df_e = N-C
	df_r = C-1
	error = y - np.dot(A, b)
	sse = np.dot(error.T, error) / df_e
	stderr = np.sqrt( np.diagonal( sse[0, 0] * AAinv ) )
	t = b.T / stderr
	p = 2*(1 - stats.t.cdf(abs(t), df_e))
	r2 = 1 - error.var() / y.var()
	#print [var for sublist in b.tolist() for var in sublist], [var for sublist in sse.tolist() for var in sublist], r2, [var for sublist in t.tolist() for var in sublist], [var for sublist in p.tolist() for var in sublist]
	return [var for sublist in b.tolist() for var in sublist], [var for sublist in sse.tolist() for var in sublist], r2, [var for sublist in t.tolist() for var in sublist], [var for sublist in p.tolist() for var in sublist]
	

#This pca funtion uses SVD to get eigenvectors and eigenvalues
def pca(d, headers_list, p_norm=True,filename=None, savefile = None):
	if p_norm == True:
		A = normalize_columns_separately(d, headers_list)
	else:
		A = d.get_data(headers_list)
	print "A.shape", A.shape
	N = d.get_raw_num_rows()
	m = A.mean(axis = 0)
	print "m.shape", m.shape
	D = A.copy()
	for i in range(A.shape[0]):
		D[i] = D[i] - m
	U, S, V = np.linalg.svd(D, full_matrices=False)
	eigenvalues = np.asmatrix((S*S)/(N-1))
	eigenvectors = V
	pdata = (V*D.T).T
	print "pdata.shape", pdata.shape
	return data.PCAData(D, headers_list, pdata, eigenvalues, eigenvectors, m, filename, savefile)

#This pca function uses SVD to get eigenvectors and eigenvalues of given matrix
def pca_m(dmatrix, headers_list, p_norm=True,filename=None, savefile = None):
	if p_norm == True:
		A = normalize_columns_separately_m(dmatrix)
	else:
		A = dmatrix
	N = dmatrix.shape[0]
	m = A.mean(axis = 0)
	D = A.copy()
	for i in range(A.shape[0]):
		D[i] = D[i] - m
	U, S, V = np.linalg.svd(D, full_matrices=False)
	eigenvalues = np.asmatrix((S*S)/(N-1))
	eigenvectors = V
	pdata = (V*D.T).T
	return data.PCAData(D, headers_list, pdata, eigenvalues, eigenvectors, m, filename, savefile)

#This pca function is to compress the data of columns
def pca_c(d, headers_list, p_norm=True, filename=None, savefile=None):
	if p_norm == True:
		A = normalize_columns_separately(d, headers_list)
	else:
		A = d.get_data(headers_list)
	print "A.shape", A.shape
	N = d.get_raw_num_rows()
	m = A.mean(axis = 0)
	print "m.shape", m.shape
	D = A.copy()
	for i in range(A.shape[0]):
		D[i] = D[i] - m
	U, S, V = np.linalg.svd(D.transpose(), full_matrices=False)
	eigenvalues = np.asmatrix((S*S)/(N-1))
	eigenvectors = V
	pdata = V*D.T
#this function implemnts kmeans function by using kmeans function on numpy
def kmeans_numpy( d, headers, K, whiten = True):
    '''Takes in a Data object, a set of headers, and the number of clusters to create
    Computes and returns the codebook, codes, and representation error.
    '''
    
    # assign to A the result of getting the data from your Data object
    A = d.get_data(headers)
    # assign to W the result of calling vq.whiten on A
    W = vq.whiten(A)
    # assign to codebook, bookerror the result of calling vq.kmeans with W and K
    codebook, bookerror = vq.kmeans(W, K)
    # assign to codes, error the result of calling vq.vq with W and the codebook
    codes, error = vq.vq(W,codebook)
    # return codebook, codes, and error
    return codebook, codes, error

#This fucntion configures necessary input for kmean function
def kmeans_init(data, K, clabels = ''):
	ret = []
	tdata = data.tolist()
	cluster_lables = []
	if clabels == '':
		for i in range(K):
			element = tdata.pop(random.randint(0,len(tdata)))
			ret.append(element)
		return np.asmatrix(ret)
	else: 
		kval = np.max(clabels, axis = 0)
		f_num = data.shape[1]
		ret = np.zeros((kval+1, f_num))
		for kind in range(kval+1):
			count = 0
			temp = np.zeros((1,f_num))
			for i,item in enumerate(clabels.tolist()):
				if kind == item[0]:
					temp += data[i]
					count += 1
			temp = temp / count
			ret[kind] = np.asmatrix(temp)
		return np.asmatrix(ret)

#This fucntion classifies data points and returns cluster mean, list of ID, and distance
def kmeans_classify(data, c_mean, metric="SSD"):
	if metric == "SSD":
		ret = np.zeros((data.shape[0], 1))
		ret2 = np.zeros((data.shape[0], 1))
		for row in range(data.shape[0]):
			temp = np.zeros((c_mean.shape[0], 1))
			for c_row in range(c_mean.shape[0]):
				ssd = (data[row] - c_mean[c_row])*(data[row] - c_mean[c_row]).T
				temp[c_row] = np.sqrt(ssd)
			cluster = np.argmin(temp)
			dist = np.min(temp)
			ret[row] = int(cluster)
			ret2[row] = dist
		return ret, ret2 
	elif metric == "Cosine":
		ret = np.zeros((data.shape[0], 1))
		ret2 = np.zeros((data.shape[0], 1))
		for row in range(data.shape[0]):
			temp = np.zeros((c_mean.shape[0], 1))
			for c_row in range(c_mean.shape[0]):
				drow = np.asmatrix([data[row].tolist()])
				dot = drow * c_mean[c_row].T
				lengthD = np.sqrt(drow*drow.T)
				lengthC = np.sqrt(c_mean[c_row]*c_mean[c_row].T)
				temp[c_row] = 1.0 - dot/(lengthD*lengthC)
			cluster = np.argmin(temp)
			dist = np.min(temp)
			ret[row] = int(cluster)
			ret2[row] = dist
		return ret, ret2 
	elif metric == "correlation":
		ret = np.zeros((data.shape[0], 1))
		ret2 = np.zeros((data.shape[0], 1))
		for row in range(data.shape[0]):
			temp = np.zeros((c_mean.shape[0], 1))
			N = data.shape[1]
			for c_row in range(c_mean.shape[0]):
				drow = np.asmatrix([data[row].tolist()])
				sumxy = drow * c_mean[c_row].T
				avgx = np.sum(drow)
				avgy = np.sum(c_mean[c_row])
				sumx2 = drow * drow.T
				sumy2 = c_mean[c_row]*c_mean[c_row].T
				avgx = avgx / N
				avgy = avgy / N
				r = (sumxy[0][0] - N * avgx * avgy) / (math.sqrt(sumx2[0][0] - N*avgx*avgx) * math.sqrt(sumy2[0][0] - N*avgy*avgy))
				temp[c_row] = 1.0 - 0.5 * (1 + r)
			cluster = np.argmin(temp)
			dist = np.min(temp)
			ret[row] = int(cluster)
			ret2[row] = dist
		return ret, ret2 
#This is the core function of kmean
def kmeans_algorithm(A, means, metric, min_num, max_ite):
    # set up some useful constants
    MIN_CHANGE = min_num
    MAX_ITERATIONS = max_ite
    D = means.shape[1]
    K = means.shape[0]
    N = A.shape[0]

    # iterate no more than MAX_ITERATIONS
    for i in range(MAX_ITERATIONS):
        # calculate the codes
        codes, errors = kmeans_classify( A, means, metric )

        # calculate the new means
        newmeans = np.zeros_like( means )
        counts = np.zeros( (K, 1) )
        for j in range(N):
            newmeans[codes[j,0],:] += A[j,:]
            counts[codes[j,0],0] += 1.0

        # finish calculating the means, taking into account possible zero counts
        for j in range(K):
            if counts[j,0] > 0.0:
                newmeans[j,:] /= counts[j, 0]
            else:
                newmeans[j,:] = A[random.randint(0,A.shape[0]),:]

        # test if the change is small enough
        diff = np.sum(np.square(means - newmeans))
        means = newmeans
        if diff < MIN_CHANGE:
            break

    # call classify with the final means
    codes, errors = kmeans_classify( A, means )

    # return the means, codes, and errors
    return (means, codes, errors)

#The top level function of kmeans algorithm
def kmeans(d, headers, K, whiten=True, categories = '', metric = 'SSD', min_num = 1e-9, max_ite = 100):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	Computes and returns the codebook, codes and representation errors. 
	If given an Nx1 matrix of categories, it uses the category labels 
	to calculate the initial cluster means.
	'''

	# assign to A the result getting the data given the headers
	A = d.get_data(headers)
	# if whiten is True
	if whiten == True:
	  # assign to W the result of calling vq.whiten on the data
		W = vq.whiten(A)
	else:
	  # assign to W the matrix A
		W = A
	# assign to codebook the result of calling kmeans_init with W, K, and categories
	codebook = kmeans_init(W, K, categories)
	# assign to codebook, codes, errors, the result of calling kmeans_algorithm with W and codebook        
	codebook, codes, errors = kmeans_algorithm(W, codebook, metric, min_num, max_ite)
	# return the codebook, codes, and representation error
	return codebook, codes, errors

	
def main():
	testdata = data.Data("testdata.csv")
	labels = np.matrix([[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1],[1],[1],[1],[1],[1],[1]])
	clustered_d, data1 = kmeans_init(testdata.get_data(['thing1','thing2']), 3, labels)
	print "clustered_d, data1", clustered_d, data1
	#testdata = data.Data("cars.csv")
	#coeff, sse, R2, t, p = linear_regression(testdata, ["speed"], ["dist"])
	#print "coefficient: " + coeff[0] + coeff[1] + ", sse: " + sse[0] + ",R2: " + str(R2) + ",t: " + t[0] + t[1] + t[2] + ",p: " + p[0] + p[1] + p[2]
if __name__ == "__main__":
	main()

