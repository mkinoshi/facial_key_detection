from pre_analyze import *
from pre_implentation import *
from implement import *

def main():
	#pre_analyze_preparation()
	trainration = [0.5, 0.6, 0.7, 0.8]
	testratio = 0.1
	eigennum = [10, 20, 30, 40]
	for i in range(len(trainration)):
		tra = trainration[i]
		for j in range(len(eigennum)):
			enum = eigennum[j]
			X_train, X_test, y_train, y_test = pre_analyze_param(tra, testratio)
			X_train = normalize_by_example_m(X_train)
			eigenvectors, eigenvalues, rep_weight = runPCA2_m(X_train, enum)
			eigencatVal = creating_stand_m(y_train, rep_weight)
			X_test = normalize_by_example_m(X_test)
			cat = classify_m(X_test, eigenvectors)
			acc = accuracy(eigencatVal, cat, y_test)
			print "Accuracy is " + str(acc) + ":trainratio = " + str(tra) + ",the number of eigenvectors = " + str(enum)

if __name__ == "__main__":
    main()