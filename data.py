#data.py
#Makoto Kinoshita
#02/22/16
import numpy as np
import csv
from datetime import datetime
import xlrd
import pandas as pd
import math


class Data:
	def __init__ (self, filename = None, sheetname = None):
		self.matrix_data = np.matrix([])
		self.header2matrix = {}
		self.raw_headers = []
		self.raw_types = []
		self.raw_data = []
		self.headers = []
		self.header2raw = {}
		self.enumDictionary = {}
		self.cluster = {}
		self.IDs_counter = 0
		if (filename != None):
			self.read(filename)


	#This function reads the file which specified by filename, convert numeric,
	# enum, date type to float numbers and store them in the matrix object of numpy.
	#Also it fills the necessary fields.
	def read(self, filename):
		self.file = file(filename, 'rU')
		reader = csv.reader(self.file)

		self.raw_headers = reader.next()
		self.raw_types = reader.next()
		#print "self.raw_headers,self.raw_types",self.raw_headers,self.raw_types
		index_dic=0
		for row in reader:
			#print "row", row
			self.raw_data.append(row)
		for header in self.raw_headers:
			self.header2raw[header] = index_dic
			index_dic += 1
		
		#match the index to the column name whose type is numeric
		columnIndexinMatrix=0
		matrix = []
		for columnIndex in range(self.get_raw_num_columns()):
			if self.raw_types[columnIndex] == "numeric":
				self.header2matrix[self.raw_headers[columnIndex]] = columnIndexinMatrix
				row_data = []
				for i in range(self.get_raw_num_rows()):
					#print "i, self.raw_headers[columnIndex]", i, self.raw_headers[columnIndex]
					#print "self.get_raw_value(i,self.raw_headers[columnIndex])", self.get_raw_value(i,self.raw_headers[columnIndex])
					if self.get_raw_value(i,self.raw_headers[columnIndex]) == " ":
						row_data.append(float(np.nan))
					else:
						row_data.append(float(self.get_raw_value(i,self.raw_headers[columnIndex])))
				columnIndexinMatrix += 1
				matrix.append(row_data)
				self.headers.append(self.raw_headers[columnIndex])
			elif self.raw_types[columnIndex] == "enum":
				self.header2matrix[self.raw_headers[columnIndex]] = columnIndexinMatrix
				matrix.append(self.parse_enum(self.raw_headers[columnIndex]))
				columnIndexinMatrix += 1
				self.headers.append(self.raw_headers[columnIndex])
			elif self.raw_types[columnIndex] == "date":
				self.header2matrix[self.raw_headers[columnIndex]] = columnIndexinMatrix
				matrix.append(self.parse_date(self.raw_headers[columnIndex]))
				columnIndexinMatrix += 1
				self.headers.append(self.raw_headers[columnIndex])
		self.matrix_data = np.asmatrix(matrix).transpose()
		#print self.matrix_data
			#from here
		self.file.close()

	def write(self, name, columns=None):
		print "self.headers", self.headers
		f = open(name, 'ab')
		csvWriter = csv.writer(f)
		types = []
		if columns == None:
			csvWriter.writerow(self.headers)
			for i in range(self.matrix_data.shape[1]):
				types.append('numeric')
			csvWriter.writerow(types)
			for i in range(self.matrix_data.shape[0]):
				csvWriter.writerow(self.matrix_data[i].tolist()[0])
		else:
			csvWriter.writerow(columns)
			for i in range(len(columns)):
				types.append('numeric')
			csvWriter.writerow(types)
			for i in range(self.get_data(columns).shape[0]):
				csvWriter.writerow(self.get_data(columns)[i].tolist()[0])
		
		f.close()


	#returns the header of raw_data as a list
	def get_raw_headers(self):
		return self.raw_headers

	#returns the type of each column of raw data as a list
	def get_raw_types(self):
		return self.raw_types

	#returns the number of columns of raw data
	def get_raw_num_columns(self):
		return len(self.raw_headers)

	#returns the number of rows of raw data
	def get_raw_num_rows(self):
		return len(self.raw_data)

	#returns the row of raw data as a list whose location isspecified by rownum 
	#variable
	def get_raw_row(self, rownum):
		return self.raw_data[rownum]

	#returns the raw data value whose location is specified by row index and headerName
	def get_raw_value(self,index, headerName):
		colnum = self.header2raw[headerName]
		if headerName == "pixel_111" and index == 0:
			print "colnum", colnum
		return self.raw_data[index][colnum]

	#returns the headers of stored data as a list
	def get_headers(self):
		return self.headers

	#returns the number of columns of sotred data 
	def get_num_columns(self):
		return len(self.header2matrix)

	#returns the row of sotred data whose location is specified by index 
	def get_row(self, index):
		return self.matrix_data[index]

	#returns the data point of stored data whose location if specified by index
	#and headerName
	def get_values(self, index, headerName):
		colnum = self.header2matrix[headerName]
		return self.matrix_data.item(index, colnum)

	#returns the data as matrix whose columns are specified by the list of headers
	def get_data(self, column_header_list):
		matrixRet = []
		transposedData = np.asarray(self.matrix_data.transpose())
		for col_name in column_header_list:
			matrixRet.append(transposedData[self.header2matrix[col_name]])
		matrixRet = np.asmatrix(matrixRet)
		return matrixRet.transpose()

	#return the matrix object of data
	def get_data_ori(self):
		return self.matrix_data
	#returns the data as the transposed matrix whose columns are specified by the 
	#list of headers
	def get_data_transposed(self, column_header_list):
		matrixRet = []
		transposedData = np.asarray(self.matrix_data.transpose())
		for col_name in column_header_list:
			matrixRet.append(transposedData[self.header2matrix[col_name]])
		matrixRet = np.asmatrix(matrixRet)
		return matrixRet

	#converts  enum data to numeric data, and returns that data column as a list
	def parse_enum(self, header_name):
		itemCount = 0
		data_column = []
		for i in range(self.get_raw_num_rows()):
			if not (self.get_raw_value(i, header_name) in self.enumDictionary.keys()):
				#print self.get_raw_value(i, header_name), itemCount
				self.enumDictionary[self.get_raw_value(i, header_name)] = itemCount
				itemCount += 1
			data_column.append(float(self.enumDictionary[self.get_raw_value(i, header_name)]))
		return data_column

	#converts date type to numpy dateint64 type data, and returns that data column as a list
	def parse_date(self, header_name):
		itemCount = 0
		data_column = np.empty(self.get_raw_num_rows(), dtype='datetime64[us]')
		for i in range(self.get_raw_num_rows()):
			try:
				date_time = datetime.strptime(self.get_raw_value(i, header_name), '%m/%d/%Y')
			except ValueError:
				try:
					date_time = datetime.strptime(self.get_raw_value(i, header_name), '%d/%m/%y')
				except ValueError:
					try:
						date_time = datetime.strptime(self.get_raw_value(i, header_name), '%B/%d/%y')
					except ValueError:
						try:
							ate_time = datetime.strptime(self.get_raw_value(i, header_name), '%b/%d/%y')
						except:
							date_time = datetime.strptime(self.get_raw_value(i, header_name), '%m/%d/%y')
			date_time = np.datetime64(date_time)
			data_column[i] = date_time
		return data_column.tolist()

	#return the cluster Ids number
	def get_IDs_counter(self):
		return self.IDs_counter

	#incrementing cluster Ids number
	def increment_IDs_counter(self):
		self.IDs_counter += 1
		

	#This function adds the data to both raw data and the matrix. It also fills necessary information
	def adding_column(self,header,header_type,item_list):
		if len(item_list) != self.get_raw_num_rows():
			print "Invalid number of the items", len(item_list), self.get_raw_num_rows()
			return
		self.raw_headers.append(header)
		self.headers.append(header)
		self.raw_types.append(header_type)
		for i in range(len(item_list)):
			self.raw_data[i].append(item_list[i])
		#print self.raw_data
		col_num = len(self.header2raw.keys())
		self.header2raw[header] = col_num
		if header_type == "numeric":
			col_matrix_num = len(self.header2matrix.keys())
			self.header2matrix[header] = col_matrix_num
			appending_data = []
			for item in item_list:
				appending_data.append(float(item))
			appending_data = np.asmatrix(appending_data)
			self.matrix_data = np.concatenate((self.matrix_data, appending_data.T), axis = 1)
			#print self.matrix_data
		elif header_type == "enum":
			col_matrix_num = len(self.header2matrix.keys())
			index = len(self.raw_headers)
			index -= 1
			self.header2matrix[header] =  col_matrix_num
			appending_data = self.parse_enum(self.raw_headers[index])
			appending_data = np.asmatrix(appending_data)
			self.matrix_data = np.concatenate((self.matrix_data, appending_data.T), axis=1)
			#print self.matrix_data
		elif header_type == "date":
			col_matrix_num = len(self.header2matrix.keys())
			index = len(self.raw_headers)
			index -= 1
			self.header2matrix[header] =  col_matrix_num
			appending_data = self.parse_date(self.raw_headers[index])
			appending_data = np.asmatrix(appending_data)
			self.matrix_data = np.concatenate((self.matrix_data, appending_data.T), axis=1)


class PCAData(Data):
	def __init__(self, ori_d, headers, data, eigenvalues, eigenvectors, dmean, filename=None, savefile = None):
		Data.__init__(self)
		self.filename = filename
		self.savefile = savefile
		self.headers = headers
		self.matrix_data = data
		self.header2matrix_S = {}
		self.original = ori_d
		self.raw_data = data
		for i in range(self.raw_data.shape[1]):
			if len(headers) == self.raw_data.shape[1]:
				s = "PCA%02d" % (i)
			else:
				s = "Column%02d" % (i)
			self.raw_headers.append(s)
			self.raw_types.append('numeric')
			self.header2matrix_S[str(i)] = i
			self.header2matrix[s] = i
			self.header2raw[s] = self.raw_data[:,i]
		self.headers = self.raw_headers
		self.eigenvalues = eigenvalues
		self.eigenvectors = eigenvectors
		self.dmean = dmean
		self.dheader = headers

	def get_original(self):
		return self.original

	def get_eigenvalues(self):
		return self.eigenvalues

	def get_eigenvectors(self):
		return self.eigenvectors

	def get_data_means(self):
		return self.dmean

	def get_data_headers(self):
		return self.headers

	def get_data_row(self):
		return self.raw_data

	def get_data_r(self):
		return self.matrix_data

	def get_h_data(self):
		return self.header2matrix

	def get_data_s(self, column_header_list):
		matrixRet = []
		transposedData = np.asarray(self.matrix_data.transpose())
		for col_name in column_header_list:
			matrixRet.append(transposedData[self.header2matrix_S[col_name]])
		matrixRet = np.asmatrix(matrixRet)
		return matrixRet.transpose()

	def get_file_name(self):
		return self.filename

	def get_save_file(self):
		return self.savefile
	#convert xml file to csv file
	# def xls_to_csv(self,filename, sheetname = 'sheet1'):
	# 	data_xls = pd.ExcelFile(filename)
	# 	df = data_xls.parse(sheetname, index_col=None)
	# 	print df
	# 	df.to_csv(''.join(filename[:,-4],'csv'),sep='\t', encoding='utf-8')
	# 	print data_xls

class FacialData(Data):

	def __init__(self, filename=None):
		Data.__init__(self)
		self.image_data = []
		if (filename != None):
			self.read(filename)

	def read(self, filename):
		self.file = file(filename, 'rU')
		reader = csv.reader(self.file)

		self.raw_headers = reader.next()
		for row in reader:
			#print "row", row
			self.raw_data.append(row)

		#print "self.raw_headers", self.raw_headers
		index_dic=0
		for header in self.raw_headers:
			self.header2raw[header] = index_dic
			index_dic += 1

		for index,item in enumerate(self.raw_headers):
			self.raw_types.append("numeric")

		#match the index to the column name whose type is numeric
		columnIndexinMatrix=0
		matrix = []
		for columnIndex in range(self.get_raw_num_columns()):
			if self.raw_types[columnIndex] == "numeric":
				self.header2matrix[self.raw_headers[columnIndex]] = columnIndexinMatrix
				row_data = []
				for i in range(self.get_raw_num_rows()):
					if columnIndex != self.get_raw_num_columns()-1:
						if self.get_raw_value(i,self.raw_headers[columnIndex]) == '':
							row_data.append(float('nan'))
						else:
							row_data.append(float(self.get_raw_value(i,self.raw_headers[columnIndex])))
						columnIndexinMatrix += 1
						matrix.append(row_data)
						self.headers.append(self.raw_headers[columnIndex])
					else:
						vlist = self.get_raw_value(i,self.raw_headers[columnIndex]).split()
						for index, item in enumerate(vlist):
							vlist[index] = float(item)
						self.image_data.append(vlist)
	
		self.matrix_data = np.asmatrix(matrix).transpose()
		#print self.matrix_data
			#from here
		self.file.close()

	def get_image_data(self):
		return self.image_data
def main():
	testdata = Data("testdata.csv")
	testdata.write("sample.csv", ['thing1'])

if __name__ == "__main__":
    main()
