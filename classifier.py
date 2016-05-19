# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import analysis as an
import numpy as np
import scipy.cluster.vq as vq

class Classifier:

    def __init__(self, type):
        '''The parent Classifier class stores only a single field: the type of
        the classifier.  A string makes the most sense.

        '''
        self._type = type

    def type(self, newtype = None):
        '''Set or get the type with this function'''
        if newtype != None:
            self._type = newtype
        return self._type

    def confusion_matrix( self, truecats, classcats ):
        '''Takes in two Nx1 matrices of zero-index numeric categories and
        computes the confusion matrix. The rows represent true
        categories, and the columns represent the classifier output.

        '''
        
        unique, mapping = np.unique( np.array(truecats.T), return_inverse=True)
        unique2, mapping2 = np.unique(np.array(classcats.T), return_inverse=True)
        confusion = np.zeros((unique.shape[0], unique.shape[0]))
        conf = []
        for i in range(unique.shape[0]):
            temp = []
            for j in range(unique.shape[0]):
                temp.append(0)
            conf.append(temp)
        for i in range(truecats.shape[0]):
            conf[int(mapping[i])][int(mapping2[i])] += 1
        return np.asmatrix(conf)

    def accuracy (self, truecats, classcats):
        '''return the overall accuracy of prediction'''
        overall_num = truecats.shape[0]
        accurate_pred = 0
        print "trucats", truecats
        print "classcats", classcats
        for i in range(truecats.shape[0]):
            if truecats[i][0] == classcats[i][0]:
                accurate_pred += 1
        return float(accurate_pred) / float(overall_num)
    def confusion_matrix_str( self, cmtx ):
        '''Takes in a confusion matrix and returns a string suitable for printing.'''
        cmtx = cmtx.tolist()
        s = "\nConfusion Matrix\n" 
        s += 'Actual->     '
        for i in range(len(cmtx)):
            s += 'Cluster %d   ' % (i)
        for i in range(len(cmtx)):
            s += '\nCluster %d' % (i)
            for val in cmtx[i]:
                s += "%12d" % (val)
        return s

    def __str__(self):
        '''Converts a classifier object to a string.  Prints out the type.'''
        return str(self._type)



class NaiveBayes(Classifier):
    '''NaiveBayes implements a simple NaiveBayes classifier using a
    Gaussian distribution as the pdf.

    '''

    def __init__(self, dataObj=None, headers=[], categories=None):
        '''Takes in a Data object with N points, a set of F headers, and a
        matrix of categories, one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'Naive Bayes Classifier')
        self.dataObj = dataObj
        # store the headers used for classification
        self.headers = headers
        # number of classes and number of features
        self.num_classes = 0
        self.num_features = len(headers)
        # original class labels
        self.class_labels = categories
        # unique data for the Naive Bayes: means, variances, scales
        self.class_means = 0
        self.class_vars = 0
        self.class_scales = 0
        # if given data,
        if self.dataObj != None:
            # call the build function
            self.build(dataObj, categories)

    def build( self, A, categories ):
        '''Builds the classifier give the data points in A and the categories'''
        
        # figure out how many categories there are and get the mapping (np.unique)
        unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
        self.class_unique = unique
        self.num_classes = unique.shape[0]
        self.num_features = A.shape[1]
        self.class_labels = categories
        # create the matrices for the means, vars, and scales
        #print "self.num_classes, self.num_features",self.num_classes, self.num_features
        self.class_means = np.zeros((self.num_classes, self.num_features))
        self.class_vars = np.zeros((self.num_classes, self.num_features))
        self.class_scales = np.zeros((self.num_classes, self.num_features))
        # the output matrices will be categories (C) x features (F)
        # compute the means/vars/scales for each class
        for index, label in enumerate(unique):
            #print "label is",label,A[(mapping == label),:]
            cat_data = A[(unique[mapping] == label),:]
            #print "shape is ",label, cat_data.shape
            self.class_means[index] = np.mean(cat_data, axis=0)
            #print "self.class_means", label, self.class_means.shape
            #print "np.var(cat_data, 0).shape", np.var(cat_data, 0).shape
            self.class_vars[index] = np.var(cat_data, 0, ddof=1)
            self.class_scales[index] = np.asmatrix((1/np.sqrt(2*np.pi*self.class_vars[index])))
        # store any other necessary information: # of classes, # of features, original labels

        return 

    def classify( self, A, return_likelihoods=False ):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_likelihoods
        is True, it also returns the NxC likelihood matrix.

        '''

        # error check to see if A has the same number of columns as
        # the class means
        if A.shape[1] != self.class_means.shape[1]:
            print "the number of columns of A doesn't much with that of mean matrix"
        
        # make a matrix that is N x C to store the probability of each
        # class for each data point
        P = np.zeros((A.shape[0], self.num_classes)) # a matrix of zeros that is N (rows of A) x C (number of classes)

        # calculate the probabilities by looping over the classes
        #  with numpy-fu you can do this in one line inside a for loop
        for i in range(self.num_classes):
        #print "A - self.class_means[i]",A - self.class_means[i]
        #print "np.prod(A - self.class_means[i], A - self.class_means[i])",np.multiply(A - self.class_means[i], A - self.class_means[i]
            prod = np.exp(-(np.multiply(A - self.class_means[i], A - self.class_means[i])/(2*self.class_vars[i])))
            prod2 = self.class_scales[i]
            #print "(prod * prod2.T).shape",            
            P.T[i] = (prod2 * prod.T)
        # calculate the most likely class for each data point
        #print "P", P
        cats = np.reshape(np.nanargmax(P, axis=1), (A.shape[0], 1)) # take the argmax of P along axis 1
        #print "cats", cats
        #print "self.calss_labels", self.class_labels
        # use the class ID as a lookup to generate the original labels
        labels = self.class_labels[cats]

        if return_likelihoods:
            return cats, labels, P

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nNaive Bayes Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Mean  : ' + str(self.class_means[i,:]) + "\n"
            s += 'Var   : ' + str(self.class_vars[i,:]) + "\n"
            s += 'Scales: ' + str(self.class_scales[i,:]) + "\n"

        s += "\n"
        return s
        
    def write(self, filename):
        '''Writes the Bayes classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the Bayes classifier from the file'''
        # extension
        return

    
class KNN(Classifier):

    def __init__(self, dataObj=None, headers=[], categories=None, K=None):
        '''Take in a Data object with N points, a set of F headers, and a
        matrix of categories, with one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'KNN Classifier')
        
        # store the headers used for classification
        self.headers = headers
        # number of classes and number of features
        self.num_classes = K
        self.num_features = 0
        # original class labels
        self.class_labels = categories
        # unique data for the KNN classifier: list of exemplars (matrices)
        self.exemplars = []
        # if given data,
            # call the build function
        if dataObj != None:
            self.build(dataObj.get_data(headers), categories, K)

    def build( self, A, categories, K = None ):
        '''Builds the classifier give the data points in A and the categories'''

        # figure out how many categories there are and get the mapping (np.unique)
        unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
        self.num_classes = unique.shape[0]
        self.num_features = A.shape[1]
        self.class_means = np.zeros((self.num_classes, self.num_features))
        self.class_unique = unique
        # for each category i, build the set of exemplars
        print "A.shape", A.shape
        for index, label in enumerate(unique):
            # if K is None
            if K == None:
                # append to exemplars a matrix with all of the rows of A where the category/mapping is i
                self.exemplars.append(A[(unique[mapping] == label),:])
            # else
            else:
                # run K-means on the rows of A where the category/mapping is i
                # append the codebook to the exemplars
                #print "unique[mapping], label", unique[mapping], label
                """
                print "unique", unique
                print "mapping", mapping.shape
                print "label", label
                print "A.shape[0]", A.shape[0]
                print "unique[mapping]", unique[mapping].shape
                print "A[(unique[mapping] == label), :]", A[(unique[mapping] == label), :]
                """
                data = A[(unique[mapping] == label), :]
                #W = vq.whiten(data)
                codebook, bokerror = vq.kmeans(data,K)
                self.exemplars.append(codebook)
            self.class_means[index] = np.mean(self.exemplars[index], axis=0)
        # store any other necessary information: # of classes, # of features, original labels
        self.class_labels = categories
        print "finished building"
        return

    def classify(self, A, K=3, return_distances=False):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_distances is
        True, it also returns the NxC distance matrix.

        The parameter K specifies how many neighbors to use in the
        distance computation. The default is three.'''

        # error check to see if A has the same number of columns as the class means
        if A.shape[1] != self.class_means.shape[1]:
           print "the number of columns of A doesn't much with that of mean matrix"
        

        # make a matrix that is N x C to store the distance to each class for each data point
        D = np.zeros((A.shape[0], self.num_classes)) # a matrix of zeros that is N (rows of A) x C (number of classes)
        # for each class i
        for i, label in enumerate(self.class_unique):
            temp = np.zeros((A.shape[0], self.exemplars[i].shape[0]))
            # make a temporary matrix that is N x M where M is the number of examplars (rows in exemplars[i])
            for row in range(A.shape[0]):
                for row_M in range(self.exemplars[i].shape[0]):
                    temp[row, row_M] = (A[row]-self.exemplars[i][row_M])*(A[row]-self.exemplars[i][row_M]).T
            #print "temp", temp
            temp = np.sort(temp, axis=1)
            column = []
            for item in range(K):
                column.append(item)
            if temp.shape[1] > K:
                D.T[i] = np.asmatrix(np.sum(temp[:,column], axis=1))
            else:
                D.T[i] = np.asmatrix(np.sum(temp, axis=1))
            per = float(i+1) / float(self.num_classes)
            print "About " + str(100*per) + " is done"
            # calculate the distance from each point in A to each point in exemplar matrix i (for loop)
            # sort the distances by row
            # sum the first K columns
            # this is the distance to the first class

        # calculate the most likely class for each data point
        cats = np.reshape(np.argmin(D, axis=1), (A.shape[0], 1)) # take the argmin of D along axis 1
        # use the class ID as a lookup to generate the original labels
        labels = self.class_labels[cats]

        if return_distances:
            return cats, labels, D

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nKNN Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
            s += 'Mean of Exemplars  :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

        s += "\n"
        return s


    def write(self, filename):
        '''Writes the KNN classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the KNN classifier from the file'''
        # extension
        return
    
