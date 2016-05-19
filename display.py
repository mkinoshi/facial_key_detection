# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
#
# CS 251
# Spring 2015

import Tkinter as tk
import tkFont as tkf
import math
import random
import view
import numpy as np
import sys
import data
import tkFileDialog
import tkMessageBox
import colorsys
import os
import analysis
from scipy import stats
import csv
import matplotlib.colors as colors


class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+200,
                                  parent.winfo_rooty()+200))

        self.initial_focus.focus_set()
        self.cancel_sig = 0

        self.wait_window(self)


    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()
        self.cancel_sig = 0

    def cancel(self, event=None):
        self.cancel_sig = 1
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

#This dialog makes it possible to choose the spped of movement of the graph.
class MyDialog(Dialog):
    #init function of MyDialog
    def __init__(self, parent):
        Dialog.__init__(self, parent)
        
    #this overrides the body function of Dialog class
    def body(self, master):
        tk.Label(master, text="The speed of translation").grid(row=0, column=0)
        tk.Label(master, text="The speed of scaling").grid(row=1, column=0)
        tk.Label(master, text="The speed of rotating").grid(row=2, column=0)

        self.liTrans = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0,height= 5)
        self.liTrans.grid(row=0, column=1)
        self.Trans = [0.1, 0.5, 1.0, 2.0, 5.0]
        for i in self.Trans:
            self.liTrans.insert(tk.END, i)
        self.liTrans.select_set(2)

        self.liScale = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0,height= 5)
        self.liScale.grid(row=1, column=1)
        self.Scale = [0.1, 0.5, 1.0, 2.0, 5.0]
        for i in self.Scale:
            self.liScale.insert(tk.END, i)
        self.liScale.select_set(2)

        self.liRotate = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0,height= 5)
        self.liRotate.grid(row=2, column=1)
        self.Rotate = [0.1, 0.5, 1.0, 2.0, 5.0]
        for i in self.Rotate:
            self.liRotate.insert(tk.END, i)
        self.liRotate.select_set(2)

    #this overrides the apply function of Dialog class
    def apply(self):
        item1 = self.liTrans.curselection()
        item2 = self.liScale.curselection()
        item3 = self.liRotate.curselection()
        
        element1 = int(item1[0])
        element2 = int(item2[0])
        element3 = int(item3[0])
        
        self.dataTrans = self.Trans[element1]
        self.dataScale = self.Scale[element2]
        self.dataRotate = self.Rotate[element3]
        print "element, self.dataTrans are", element2, self.dataScale

#this creates the column choosing set up dialog.
class DataDialog(Dialog):
    def __init__(self, parent, filename):
        self.selectedFile = filename
        print filename
        Dialog.__init__(self, parent)

    def body(self, master):
        tk.Label(master, text="The column of x axis").grid(row=0, column=0)
        tk.Label(master, text="The column of y axis").grid(row=1, column=0)
        tk.Label(master, text="The column of z axis").grid(row=2, column=0)
        tk.Label(master, text="The column of color axis").grid(row=3, column=0)
        tk.Label(master, text="The column of size axis").grid(row=4, column=0)
        if self.master.dataFile == None:
            tkMessageBox.showinfo("error", "Slect File first")
            self.cancel()
        else:
            self.headers = self.master.dataFile[self.selectedFile].get_headers()[:]
            num_h = len(self.headers)
            self.liX = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
            self.liX.grid(row=0, column=1)
            for i in self.headers:
                self.liX.insert(tk.END, i)
            self.liY = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
            self.liY.grid(row=1, column=1)
            for i in self.headers:
                self.liY.insert(tk.END, i)
            self.headers.append("None")
            self.liZ = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
            self.liZ.grid(row=2, column=1)
            for i in self.headers:
                self.liZ.insert(tk.END, i)
            self.liColor = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
            self.liColor.grid(row=3, column=1)
            for i in self.headers:
                self.liColor.insert(tk.END, i)
            self.liSize = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
            self.liSize.grid(row=4, column=1)
            for i in self.headers:
                self.liSize.insert(tk.END, i)

    def apply(self):
        item1 = self.liX.curselection()
        item2 = self.liY.curselection()
        item3 = self.liZ.curselection()
        item4 = self.liColor.curselection()
        item5 = self.liSize.curselection()
        
        element1 = int(item1[0])
        element2 = int(item2[0])
        element3 = int(item3[0])
        element4 = int(item4[0])
        element5 = int(item5[0])
        
        if element1 == element2 or element1 == element3 or element2 == element3:
            tkMessageBox.showinfo("error", "you can't choose the same column for two axes")
            return
        self.datacoX = self.headers[element1]
        self.datacoY = self.headers[element2]
        self.datacoZ = self.headers[element3]
        self.datacoC = self.headers[element4]
        self.datacoS = self.headers[element5]
        
#This creates file managing dialog.
class FileManagementDialog(Dialog):
    def __init__(self, parent):
        Dialog.__init__(self, parent)

    def body(self, master):
        tk.Label(master, text="Choose the file to delete").grid(row=0, column=0)
        file_num = len(self.master.filenames)
        if file_num == 0:
            tkMessageBox.showinfo("error", "No File selected")
            self.cancel()
        self.filelist = self.master.filenames.keys()
        self.lifiles = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=file_num)
        self.lifiles.grid(row=0, column=1)
        for i in self.filelist:
            self.lifiles.insert(tk.END, i)

    def apply(self):
        item1 = self.lifiles.curselection()
        element1 = int(item1[0])
        self.filenames = self.filelist[element1]

#This creates the dialog to change the columns
class ChoosingData(Dialog):
    def __init__(self, parent):
        Dialog.__init__(self, parent)

    def body(self, master):
        tk.Label(master, text="Choose the data file to select column").grid(row=0, column=0)
        file_num = len(self.master.filenames)
        if file_num == 0:
            tkMessageBox.showinfo("error", "No File selected")
            self.cancel()
        self.filelist = self.master.filenames.keys()
        self.lifiles = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=file_num)
        self.lifiles.grid(row=0, column=1)
        for i in self.filelist:
            self.lifiles.insert(tk.END, i)

    def apply(self):
        item1 = self.lifiles.curselection()
        element1 = int(item1[0])
        self.filenames = self.filelist[element1]

#This creates dialog to choose a file for linear regression
class ChoosingFile_forReg(Dialog):
    def __init__(self, parent):
        Dialog.__init__(self, parent)

    def body(self, master):
        tk.Label(master, text="Choose the data file to operate linear regression").grid(row=0, column=0)
        file_num = len(self.master.filenames)
        if file_num == 0:
            tkMessageBox.showinfo("error", "No File selected")
            self.cancel()
        self.filelist = self.master.filenames.keys()
        self.lifiles = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=file_num)
        self.lifiles.grid(row=0, column=1)
        for i in self.filelist:
            self.lifiles.insert(tk.END, i)

    def apply(self):
        item1 = self.lifiles.curselection()
        element1 = int(item1[0])
        self.filenames = self.filelist[element1]

#this dialog makes it possible to choose variables and axes for linear regression.
class LinearDialog(Dialog):
    def __init__(self, parent, filename):
        print "filename is", filename
        self.selectedFile = filename
        Dialog.__init__(self, parent)

    def body(self, master):
        if self.master.dataFile == None:
            tkMessageBox.showinfo("error", "Slect File first")
            self.cancel()
        else:
            self.headers = self.master.dataFile[self.selectedFile].get_headers()
            header_num = len(self.headers)
            tk.Label(master, text="Independent Variable").grid(row=0, column=0)
            tk.Label(master, text="Dependent variable").grid(row=header_num+1, column=0)
            #tk.Label(master, text="The column of z axis").grid(row=header_num+2, column=0)
            #tk.Label(master, text="The column of color axis").grid(row=header_num+3, column=0)
            #tk.Label(master, text="The column of size axis").grid(row=header_num+4, column=0)
            num_h = len(self.headers)
            self.var_headers = {}
            for index, i in enumerate(self.headers):
                self.var_headers[index] = tk.IntVar()
                self.liX = tk.Checkbutton(master, text=i, variable=self.var_headers[index])
                #self.liX.insert(tk.END, i)
                self.liX.grid(row=index/4, column=index%4+1)
            self.liY = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
            self.liY.grid(row=header_num+1, column=1)
            for i in self.headers:
                self.liY.insert(tk.END, i)

    def apply(self):
        item2 = self.liY.curselection()
        
        
        element2 = int(item2[0])
        
        self.linearInd = []
        for i in range(len(self.headers)-1):
            if self.var_headers[i].get() == 1:
                self.linearInd.append(self.headers[i])
        self.linearcoY = self.headers[element2]

class LinearDialog2(Dialog):
    def __init__(self, parent, headers):
        self.headers = headers
        Dialog.__init__(self, parent)
        
    def body(self, master):
        self.headers.append("None")
        tk.Label(master, text="The column of x axis").grid(row=0, column=0)
        tk.Label(master, text="The column of y axis").grid(row=1, column=0)
        tk.Label(master, text="The column of z axis").grid(row=2, column=0)
        tk.Label(master, text="The column of color axis").grid(row=3, column=0)
        tk.Label(master, text="The column of size axis").grid(row=4, column=0)
        self.liX = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liX.grid(row=0, column=1)
        for i in self.headers:
            self.liX.insert(tk.END, i)
        self.liY = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liY.grid(row=1, column=1)
        for i in self.headers:
            self.liY.insert(tk.END, i)
        self.liZ = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liZ.grid(row=2, column=1)
        for i in self.headers:
            self.liZ.insert(tk.END, i)
        self.liColor = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liColor.grid(row=3, column=1)
        for i in self.headers:
            self.liColor.insert(tk.END, i)
        self.liSize = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liSize.grid(row=4, column=1)
        for i in self.headers:
            self.liSize.insert(tk.END, i)

    def apply(self):
        item1 = self.liX.curselection()
        item2 = self.liY.curselection()
        item3 = self.liZ.curselection()
        item4 = self.liColor.curselection()
        item5 = self.liSize.curselection()
        
        element1 = int(item1[0])
        element2 = int(item2[0])
        element3 = int(item3[0])
        element4 = int(item4[0])
        element5 = int(item5[0])
        
    
        self.linearcoX = self.headers[element1]
        self.linearcoY = self.headers[element2]
        self.linearcoZ = self.headers[element3]
        self.linearcoC = self.headers[element4]
        self.linearcoS = self.headers[element5]

#This creates the dialog to iplement PCA analysis
class PCADialog(Dialog):
    def __init__(self, parent, filename):
        self.selectedFile = filename
        Dialog.__init__(self, parent)

    def body(self, master):
        if self.master.dataFile == None:
            tkMessageBox.showinfo("error", "Slect File first")
            self.cancel()
        else:
            self.headers = self.master.dataFile[self.selectedFile].get_headers()
            header_num = len(self.headers)
            tk.Label(master, text="Choose the columns to implement PCA").grid(row=0, column=0)
            self.var_headers = {}
            for index, i in enumerate(self.headers):
                self.var_headers[index] = tk.IntVar()
                self.liX = tk.Checkbutton(master, text=i, variable=self.var_headers[index])
                self.liX.grid(row=index, column=1)
            self.e = tk.Entry(master)
            tk.Label(master, text="Type the analysis name").grid(row=len(self.headers)+1, column=0)
            self.e.grid(row=len(self.headers)+1, column=1)


    def apply(self):
        self.pca_header = []
        for i in range(len(self.headers)):
            if self.var_headers[i].get() == 1:
                self.pca_header.append(self.headers[i])
        self.savefile = self.e.get()
        if self.savefile == '':
            tkMessageBox.showinfo("error", "Type the name of the analysis")
        else:
            self.savefile = self.e.get()

#This create the dialog to implement plot the result of PCA
class PCAplotDialog(Dialog):
    def __init__(self, parent, headers_list):
        self.headers = headers_list
        Dialog.__init__(self, parent)

    def body(self, master):
        header_num = len(self.headers)
        tk.Label(master, text="The column of x axis").grid(row=0, column=0)
        tk.Label(master, text="The column of y axis").grid(row=header_num+1, column=0)
        tk.Label(master, text="The column of z axis").grid(row=header_num+2, column=0)
        tk.Label(master, text="The column of color axis").grid(row=header_num+3, column=0)
        tk.Label(master, text="The column of size axis").grid(row=header_num+4, column=0)
        self.var_headers = {}
        
        self.liX = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liX.grid(row=0, column=1)
        for i in self.headers:
            self.liX.insert(tk.END, i)
        self.liY = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liY.grid(row=header_num+1, column=1)
        for i in self.headers:
            self.liY.insert(tk.END, i)
        self.headers.append("None")
        self.liZ = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liZ.grid(row=header_num+2, column=1)
        for i in self.headers:
            self.liZ.insert(tk.END, i)
        self.liColor = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liColor.grid(row=header_num+3, column=1)
        for i in self.headers:
            self.liColor.insert(tk.END, i)
        self.liSize = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liSize.grid(row=header_num+4, column=1)
        for i in self.headers:
            self.liSize.insert(tk.END, i)

    def apply(self):
        item1 = self.liX.curselection()
        item2 = self.liY.curselection()
        item3 = self.liZ.curselection()
        item4 = self.liColor.curselection()
        item5 = self.liSize.curselection()
        
        element1 = int(item1[0])
        element2 = int(item2[0])
        element3 = int(item3[0])
        element4 = int(item4[0])
        element5 = int(item5[0])
        
        if element1 == element2 or element1 == element3 or element2 == element3:
            tkMessageBox.showinfo("error", "you can't choose the same column for two axes")
            return
        self.datacoX = self.headers[element1]
        self.datacoY = self.headers[element2]
        self.datacoZ = self.headers[element3]
        self.datacoC = self.headers[element4]
        self.datacoS = self.headers[element5]

#This create the detail window od the PCA result
class PCAresultWindow(Dialog):
    def __init__(self, parent, data, eigenvalues, eigenvectors, headers):
        self.data = data
        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors
        self.headers = headers
        Dialog.__init__(self, parent)

    def body(self, master):
        sum_v = 0.0
        tk.Label(master, text="E-vec").grid(row=0, column=0, padx=3, pady=3)
        for index in range(self.data.shape[1]):
            indexs = "E" + str(index)
            label = tk.Label(master, text=indexs)
            label.grid(row=index+1, column=0)
        tk.Label(master, text="E-val").grid(row=0, column=1, padx=3, pady=3)
        for index in range(self.data.shape[1]):
            sum_v += self.eigenvalues[index]
            label = tk.Label(master, text="{0:.4f}".format(self.eigenvalues[index]))
            label.grid(row=index+1, column=1)
        tk.Label(master, text="Cumulative").grid(row=0, column=2, padx=3, pady=3)
        cul = 0.0
        for index in range(self.data.shape[1]):
            cul += self.eigenvalues[index]/sum_v
            label = tk.Label(master, text="{0:.4f}".format(cul))
            label.grid(row=index+1, column=2)
        for column in range(len(self.headers)):
            tk.Label(master, text=self.headers[column]).grid(row=0, column=3+column, padx=3, pady=3)
            for index in range(self.data.shape[1]):
                label = tk.Label(master, text="{0:.4f}".format(self.eigenvectors[index,column]))
                label.grid(row=index+1, column=column+3)
        
#This creates the dialog to choose the setting up of kmeans
class KmeansDialog(Dialog):
    def __init__(self, parent, headers):
        self.headers = headers
        self.metric = ["SSD", "Cosine", "correlation"]
        self.min = [1e-5, 1e-7, 1e-9]
        self.max = [100, 200, 300]
        Dialog.__init__(self, parent)

    def body(self, master):
        tk.Label(master, text="Choose the columns to implement K means").grid(row=0, column=0)
        self.var_headers = {}
        for index, i in enumerate(self.headers):
            self.var_headers[index] = tk.IntVar()
            self.liX = tk.Checkbutton(master, text=i, variable=self.var_headers[index])
            self.liX.grid(row=index/4+1, column=index % 4)
        self.e = tk.Entry(master)
        tk.Label(master, text="Type the number of clusters").grid(row=len(self.headers)+1, column=0)
        self.e.grid(row=len(self.headers)+1, column=1)
        tk.Label(master, text="choose the metric").grid(row=len(self.headers)+2, column=0)
        self.liM = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=3)
        self.liM.grid(row=len(self.headers)+2, column=1)
        for i in self.metric:
            self.liM.insert(tk.END, i)
        tk.Label(master, text="Choose the threshold").grid(row=len(self.headers)+3, column=0)
        self.liT = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=3)
        self.liT.grid(row=len(self.headers)+3, column=1)
        for i in self.min:
            self.liT.insert(tk.END, i)
        tk.Label(master, text="Choose the max iterations").grid(row=len(self.headers)+4, column=0)
        self.liI = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=3)
        self.liI.grid(row=len(self.headers)+4, column=1)
        for i in self.max:
            self.liI.insert(tk.END, i)

    def apply(self):
        self.kmeans_header = []
        for i in range(len(self.headers)):
            if self.var_headers[i].get() == 1:
                self.kmeans_header.append(self.headers[i])
        self.k_num = int(self.e.get())
        if self.k_num == '':
            tkMessageBox.showinfo("error", "Type the name of the analysis")
        else:
            self.k_num = int(self.e.get())
        item1 = self.liM.curselection()
        item2 = self.liT.curselection()
        item3 = self.liI.curselection()
        element1 = int(item1[0])
        element2 = int(item2[0])
        element3 = int(item3[0])
        self.datacoM = self.metric[element1]
        self.datacoI = int(self.min[element2])
        self.datacoT = float(self.max[element3])

#This creates the dialog to plot the result
class KmeansPlot(Dialog):
    def __init__(self, parent, headers):
        self.headers = headers
        Dialog.__init__(self, parent)

    def body(self, master):
        header_num = len(self.headers)
        tk.Label(master, text="The column of x axis").grid(row=0, column=0)
        tk.Label(master, text="The column of y axis").grid(row=header_num+1, column=0)
        tk.Label(master, text="The column of z axis").grid(row=header_num+2, column=0)
        tk.Label(master, text="The column of size axis").grid(row=header_num+3, column=0)
        self.liX = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liX.grid(row=0, column=1)
        for i in self.headers:
            self.liX.insert(tk.END, i)
        self.liY = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liY.grid(row=header_num+1, column=1)
        for i in self.headers:
            self.liY.insert(tk.END, i)
        self.headers.append("None")
        self.liZ = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liZ.grid(row=header_num+2, column=1)
        for i in self.headers:
            self.liZ.insert(tk.END, i)
        self.liSize = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=5)
        self.liSize.grid(row=header_num+3, column=1)
        for i in self.headers:
            self.liSize.insert(tk.END, i)

    def apply(self):
        item1 = self.liX.curselection()
        item2 = self.liY.curselection()
        item3 = self.liZ.curselection()
        item5 = self.liSize.curselection()
        
        element1 = int(item1[0])
        element2 = int(item2[0])
        element3 = int(item3[0])
        element5 = int(item5[0])
        
        if element1 == element2 or element1 == element3 or element2 == element3:
            tkMessageBox.showinfo("error", "you can't choose the same column for two axes")
            return
        self.datacoX = self.headers[element1]
        self.datacoY = self.headers[element2]
        self.datacoZ = self.headers[element3]
        self.datacoS = self.headers[element5]

#This creates the dialog to choose the colors of clusters
class KmeansPlotC(Dialog):
    def __init__(self, parent, K):
        self.K = K
        Dialog.__init__(self, parent)

    def body(self, master):
        print "colors.cnames", colors.cnames
        selected = []
        s = "Choose " + str(self.K) + " colors"
        tk.Label(master, text=s).grid(row=0, column=0)
        self.var = {}
        for index, i in enumerate(colors.cnames.keys()):
            self.var[index] = tk.IntVar()
            self.liX = tk.Checkbutton(master, text=i, variable=self.var[index])
            self.liX.grid(row=index/8+1, column=index%8)
    
    def apply(self):
        self.kmeans_color = []
        for i in range(len(colors.cnames)):
            if self.var[i].get() == 1:
                print "self.var[i]",self.var[i]
                self.kmeans_color.append(colors.cnames[colors.cnames.keys()[i]])
        if len(self.kmeans_color) != self.K:
            tkMessageBox.showinfo("error", "the number of color does not match")
            return
#this creates the windonw to select whether to plot classification or not
class PlotAdvanced(Dialog):
    def __init__(self, parent):
        Dialog.__init__(self,parent)

    def body(self, master):
        self.method = ["continuous", "discrete"]
        tk.Label(master, text="Choose the way to plot color").grid(row=0, column=0)
        self.liC = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0, height=2)
        self.liC.insert(tk.END, "Using continuous data as color value")
        self.liC.insert(tk.END, "Using discrete data as color value")
        self.liC.grid(row=0, column=1)

    def apply(self):
        item = self.liC.curselection()

        element = int(item[0])
        self.dataC = self.method[element]
# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()

        self.root.Trans = 1.0
        self.root.Scale = 1.0
        self.root.Rotate = 1.0
        # width and height of the window
        self.initDx = width
        self.initDy = height

        self.w = self.initDx
        self.h = self.initDy

        # set up the geometry for the window
        self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

        # set the title of the window
        self.root.title("Data Analytics")

        # set the maximum size of the window for resizing
        self.root.maxsize( 1600, 900 )

        # setup the menus
        self.buildMenus()

        # build the controls
        self.buildControls()

        # build the Canvas
        self.buildCanvas()

        self.buildDialog()

        # bring the window to the front
        self.root.lift()

        # - do idle events here to get actual canvas size
        self.root.update_idletasks()

        # now we can ask the size of the canvas
        print self.canvas.winfo_geometry()

        # set up the key bindings
        self.setBindings()

        self.view = view.View()
        self.axisPoints = np.matrix([[0,0,0,1],
                                    [1,0,0,1],
                                    [0,0,0,1],
                                    [0,1,0,1],
                                    [0,0,0,1],
                                    [0,0,1,1]])
        self.axes = []
        self.dataP = []
        self.PdataP = []
        self.RdataP = []
        self.KdataP = []
        self.root.dataFile = {}
        print "self.root.dataFile", self.root.dataFile
        self.dataColumn = {}

        self.dataColor = {}
        self.dataSize = {}
        self.dataHeaders = {}
        self.color_header = {}
        self.size_header = {}
        self.root.filenames = {}
        self.buildAxes()
        self.dataObjDic = {}
        self.handleButton1Holder = (0,0)
        # set up the application state
        self.objects = [] # list of data objects that will be drawn in the canvas
        self.data = None # will hold the raw data someday.
        self.baseClick = None # used to keep track of mouse movement
        self.baseClick = None
        self.baseClick3 = None
        self.originalExtent = []
        self.factor = 0.0

        self.regFile = []
        self.regdataHeaders = {}
        self.line = []
        self.regEndpoints = {}
        self.reg_text_info = {}
        self.reg_label = {}
        self.independent_var = {}
        self.linear_reg = {}
        self.recall_analy = {}

        self.PCAcounter = {}
        self.PCAresult = {}
        self.pcalist_s = []
        self.PCAplotlist = {}

        self.PCAdataColumn = {}
        self.PCAdataColor = {}
        self.PCAdataSize = {}

        self.KdataColumn = {}
        self.KdataColor = {}
        self.KdataSize = {}
        self.KdataHeaders = {}

        self.CdataColumns = {}
        self.CdataColor = {}
        self.CdataSize = {}
        self.CdataHeaders = {}

        self.plot_pendingFile = []
        
        
        
    #this handles opning files
    def handleOpen(self):
        fn = tkFileDialog.askopenfilename( parent=self.root,
      title='Choose a data file', initialdir='.' )
        if fn != None and fn != '':
            filename = os.path.split(fn)[1]
            filen = filename +"\n"
            if not filename in self.root.filenames.keys():
                print "keys are", filename
                self.root.filenames[filename] = len(self.root.filenames) + 1
            self.root.dataFile[filename] = data.Data(fn)
            self.PCAcounter[filename] = 0
            self.text.insert(tk.END, filen)
        print self.root.dataFile

    
    #This handles deleting files
    def handleDelete(self):
        self.buildFileDialog()
        filename = self.fileDialog.filenames
        for obj in self.dataP:
            self.canvas.delete(obj)
        self.dataP = []
        self.line = []
        self.root.filenames.pop(filename)
        self.dataColumn.pop(filename)
        self.dataColor.pop(filename)
        self.dataSize.pop(filename)
        self.dataHeaders.pop(filename)
        self.color_header.pop(filename)
        self.size_header.pop(filename)
        self.root.dataFile.pop(filename)
        self.text.delete('1.0', tk.END)
        for filen in self.root.filenames.keys():
            print filen
            self.text.insert(tk.END, filen)
        self.regFile.remove(fileselected)
        #print "self.regFile", self.regFile
        #print "self.reg_label", self.reg_label
        self.reg_label[fileselected].destroy()
        for obj in self.line:
            self.canvas.delete(obj)
        self.updateAxes()
        self.updateFits()

    #This function deletes the plot:
    def handlePlotDelete(self):
        for obj in self.dataP:
            self.canvas.delete(obj)
        for obj in self.PdataP:
            self.canvas.delete(obj)
        for obj in self.KdataP:
            self.canvas.delete(obj)
        self.KdataColumn = {}
        self.KdataColor = {}
        self.KdataSize = {}
        self.KdataHeaders = {}
        self.dataP = []
        self.PdataP = []
        self.KdataP = []
        self.RdataP = []
        self.updateAxes()
        self.updateFits()
        
    #This handles plotting data
    def handlePlotData(self):
        self.buildChooseData()
        fileselected = self.chooseDialog.filenames
        self.dataHeaders[fileselected] = []
        self.buildDataDialog(fileselected)
        self.dataHeaders[fileselected] = [self.dataDialog.datacoX, self.dataDialog.datacoY, self.dataDialog.datacoZ]
        self.color_header[fileselected] = self.dataDialog.datacoC
        self.size_header[fileselected] = self.dataDialog.datacoS
        self.plot_pendingFile.append(fileselected)

    #This handles linear regression dialog
    def handleLinearRegression(self):
        self.buildChooseData()
        fileselected = self.chooseDialog.filenames
        if fileselected != '' and self.chooseDialog.cancel_sig == 0:
            self.regFile.append(self.chooseDialog.filenames)
            self.dataHeaders[fileselected] = []
            self.buildLinearDialog(fileselected)
            if self.linearDialog.cancel_sig == 1:
                self.regFile.delete(self.chooseDialog.filenames)
            if self.linearDialog2.cancel_sig == 0:
                self.independent_var[fileselected] = self.linearDialog.linearInd[:-1]
                print "self.independent_var[fileselected]", self.independent_var[fileselected]
                if self.linearDialog2.linearcoZ == "None":
                    self.dataHeaders[fileselected] = [self.linearDialog2.linearcoX, self.linearDialog2.linearcoY]
                else:
                    self.dataHeaders[fileselected] = [self.linearDialog2.linearcoX, self.linearDialog2.linearcoY, self.linearDialog2.linearcoZ]
                self.color_header[fileselected] = self.linearDialog2.linearcoC
                self.size_header[fileselected] = self.linearDialog2.linearcoS
                for obj in self.dataP:
                    self.canvas.delete(obj)
                for obj in self.axes:
                    self.canvas.delete(obj)
                self.dataP = []
                self.axes = []
                self.text2.delete('1.0', tk.END)
                self.text3.delete('1.0', tk.END)
                row_num = self.root.dataFile[fileselected].get_raw_num_rows()
                self.dataColor[fileselected] = []
                self.dataSize[fileselected] = []
                
                #Below this, this function initializes or nomalizes color and size data
                if self.color_header[fileselected] != "None":
                    self.dataColor[fileselected] = self.root.dataFile[fileselected].get_data([self.color_header[fileselected]])
                    minC = np.min(self.dataColor[fileselected], axis=0)
                    maxC = np.max(self.dataColor[fileselected], axis=0)
                    rangeC = maxC - minC
                    rangeCli = rangeC[0].tolist()
                    for i in range(len(rangeCli[0])):
                        if rangeCli[0][i] == 0:
                            rangeCli[0][i] = 1.0
                    rangeC = np.asmatrix(rangeCli)
                    self.dataColor[fileselected] = 1- ((maxC - self.dataColor[fileselected])/rangeC)
                    self.dataColor[fileselected] = self.dataColor[fileselected].tolist() 
                else:
                    for i in range(row_num):
                        self.dataColor[fileselected].append([0.5])
                if self.size_header[fileselected] != "None":
                        self.dataSize[fileselected] = self.root.dataFile[fileselected].get_data([self.size_header[fileselected]])
                        minC = np.min(self.dataSize[fileselected], axis=0)
                        maxC = np.max(self.dataSize[fileselected], axis=0)
                        rangeC = maxC - minC
                        rangeCli = rangeC[0].tolist()
                        for i in range(len(rangeCli[0])):
                            if rangeCli[0][i] == 0:
                                rangeCli[0][i] = 1.0
                        rangeC = np.asmatrix(rangeCli)
                        self.dataSize[fileselected] = 1- ((maxC - self.dataSize[fileselected])/rangeC)
                        self.dataSize[fileselected] = self.dataSize[fileselected].tolist()
                        size = self.dataSize[fileselected]
                else:
                    for i in range(row_num):
                        self.dataSize[fileselected].append([0])
                self.buildLinearMulRegression()
                self.updateAxes()
                self.updatePoints()

    #This creates the dialog to delete linear regression
    def handleDeleteLinearRegression(self):
        self.buildChooseData()
        fileselected = self.chooseDialog.filenames
        self.regFile.remove(fileselected)
        self.reg_label[fileselected].destroy()
        for obj in self.line:
            self.canvas.delete(obj)
        self.line = []
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

    #This function handles PCA analysis
    def handlePCA(self):
        self.buildChooseData()
        fileselected = self.chooseDialog.filenames
        if fileselected != '' and self.chooseDialog.cancel_sig == 0:
            self.buildPCAdialog(fileselected)
            pca_header = self.PCADialog.pca_header
            print "pca_header is", pca_header
            savefile = self.PCADialog.savefile
            pca_data = analysis.pca(self.root.dataFile[fileselected], pca_header, True, fileselected, savefile)
            self.PCAcounter[fileselected] += 1
            s =  pca_data.get_save_file()
            self.PCAresult[s] = pca_data
            self.pcalist.insert(tk.END, s)
            self.pcalist_s.append(s)
            if len(self.pcalist_s) == 1:
                button = tk.Button( self.rightcntlframe, text="Plot", 
                               command=self.pcaOpen )
                button2 = tk.Button(self.rightcntlframe, text="Detail",
                                command=self.pcaDetail)
                button3 = tk.Button(self.rightcntlframe, text="Delete",
                             command=self.pcaDelete)
                button4 = tk.Button(self.rightcntlframe, text="Data joint",
                             command=self.pcaJoint)
                button5 = tk.Button(self.rightcntlframe, text='Save as CSV',
                             command=self.savefile)
                button.pack(side=tk.LEFT)
                button2.pack(side=tk.LEFT)
                button3.pack(side=tk.LEFT)
                button4.pack(side=tk.LEFT)
                button5.pack(side=tk.LEFT)
    
    #This function handles kmeans
    def handleKmeans(self):
        self.buildChooseData()
        fileselected = self.chooseDialog.filenames
        if fileselected != '' and self.chooseDialog.cancel_sig == 0:
            data = self.root.dataFile[fileselected]
            headers = self.root.dataFile[fileselected].get_headers()
            self.buildKmeansDialog(headers)
            headers_list = self.KmeansDialog.kmeans_header
            K = self.KmeansDialog.k_num
            metric = self.KmeansDialog.datacoM
            error = self.KmeansDialog.datacoT
            iteration = self.KmeansDialog.datacoI
            codebook, codes, errors = analysis.kmeans(data, headers_list, K, metric = metric, min_num = error, max_ite = iteration)
            data.increment_IDs_counter()
            s = "ID" + str(data.get_IDs_counter())
            data.adding_column(s, 'numeric', codes)
            self.buildKmeansPlot(headers_list)
            self.buildKmeansPlotC(K)
            headers_li = [self.KmeansPlot.datacoX, self.KmeansPlot.datacoY, self.KmeansPlot.datacoZ]
            self.KdataHeaders[fileselected] = headers_li
            size = self.KmeansPlot.datacoS
            color_header = self.KmeansPlotC.kmeans_color
            self.buildpointsK(fileselected,data,headers_li,size,color_header)


    #This function saved the data as CSV
    def savefile(self):
        result_name = self.pcalist_s[self.pcalist.curselection()[0]]
        if result_name != '':
            pca_data = self.PCAresult[result_name]
            headers = pca_data.get_headers()
            pdata = pca_data.get_data_r()
            eigenvalues = pca_data.get_eigenvalues()
            eigenvectors = pca_data.get_eigenvectors()
            mean = pca_data.get_data_means()
            print "headers", headers
            print "eigenvectors", eigenvectors.shape
            print "mean", mean
            self.buildChooseData()
            fileselected = self.chooseDialog.filenames
            if fileselected != '' and self.chooseDialog.cancel_sig == 0:
                name = result_name + ".csv"
                f = open(name, 'ab')
                csvWriter = csv.writer(f)
                headers_e = []
                for i in range(pdata.shape[1]):
                    s = "E" + str(i)
                    headers_e.append(s)
                csvWriter.writerow(headers_e)
                print "pdata.tolist()", pdata.tolist()
                for item in pdata.tolist():
                    csvWriter.writerow(item)
                headers_e = []
                for i in range(pdata.shape[1]):
                    s = "E" + str(i) +"_val"
                    headers_e.append(s)
                csvWriter.writerow(headers_e)
                csvWriter.writerow(eigenvalues.tolist())
                headers_e = []
                for i in range(pdata.shape[1]):
                    s = "E" + str(i) +"_vec"
                    headers_e.append(s)
                csvWriter.writerow(headers_e)
                for item in eigenvectors.tolist():
                    csvWriter.writerow(item)
                headers_e = []
                for i in range(pdata.shape[1]):
                    s = "E" + str(i) +"_mean"
                    headers_e.append(s)
                csvWriter.writerow(headers_e)
                csvWriter.writerow(mean.tolist()[0])
                f.close()

    #this function makes it possible to joint the result of PCA to the original data
    def pcaJoint(self):
        result_name = self.pcalist_s[self.pcalist.curselection()[0]]
        self.buildChooseData()
        fileselected = self.chooseDialog.filenames
        if fileselected != '' and self.chooseDialog.cancel_sig == 0:
            pca_data = self.PCAresult[result_name]
            self.PCAcounter[fileselected] += 1
            headers = []
            for index in range(pca_data.get_data_r().shape[1]):
                indexs = "E" + str(index)
                headers.append(indexs)
            for i in range(len(headers)):
                self.root.dataFile[fileselected].adding_column(headers[i], "numeric", pca_data.get_data_r()[:,i].flatten().tolist()[0])
            print "jointed data", self.root.dataFile[fileselected].get_headers()

    #This function plot the data rojected on eigen vectors
    def pcaOpen(self):
        result_name = self.pcalist_s[self.pcalist.curselection()[0]]
        if (result_name in self.PCAplotlist.keys()):
            self.PCAplotlist[result_name] += 1
            dnum = self.PCAplotlist[result_name]
        else:
            self.PCAplotlist[result_name] = 1
            dnum = self.PCAplotlist[result_name]
            self.PCAdataColumn[result_name] = {}
            self.PCAdataColor[result_name] = {}
            self.PCAdataSize[result_name] = {}
        presult = self.PCAresult[result_name]
        eigenvectors = presult.get_eigenvectors()
        eigenvalues = presult.get_eigenvalues()
        print "eienvalues", eigenvalues
        print "eigenvectors", eigenvectors
        presult_data = presult.get_data_r()
        headers = []
        for index in range(presult_data.shape[1]):
            indexs = "E" + str(index)
            headers.append(indexs)
        self.buildPCAplotDialog(headers)
        if self.PCAplotDialog.datacoZ != "None":
            headers = [self.PCAplotDialog.datacoX[1:], self.PCAplotDialog.datacoY[1:], self.PCAplotDialog.datacoZ[1:]]
        else:
            headers = [self.PCAplotDialog.datacoX[1:], self.PCAplotDialog.datacoY[1:], "None"]
        if self.PCAplotDialog.datacoC != "None":
            color_header = self.PCAplotDialog.datacoC[1:]
        else:
            color_header = self.PCAplotDialog.datacoC
        if self.PCAplotDialog.datacoS != "None":
            size_header = self.PCAplotDialog.datacoS[1:]
        else:
            size_header = self.PCAplotDialog.datacoS
        row_num = len(presult_data)
        self.PCAdataColor[result_name][dnum-1] = []
        self.PCAdataSize[result_name][dnum-1] = []
        for i in range(row_num):
            self.PCAdataColor[result_name][dnum-1].append([0.0])
            self.PCAdataSize[result_name][dnum-1].append([0.0])
        color = self.PCAdataColor[result_name][dnum-1]
        size = self.PCAdataSize[result_name][dnum-1]

        if headers[2] == "None":
            self.PCAdataColumn[result_name][dnum-1] = presult.get_data_s(headers[:2])
            zeros = np.zeros([row_num, 1])
            ones = np.ones([row_num, 1])
            dataM = np.column_stack((self.PCAdataColumn[result_name][dnum-1], zeros))
            dataM = np.column_stack((dataM, ones))
        else:
            self.PCAdataColumn[result_name][dnum-1] = presult.get_data_s(headers)
            ones = np.ones([row_num, 1])
            dataM = np.column_stack((self.PCAdataColumn[result_name][dnum-1], ones))
        minC = np.min(dataM, axis=0)
        maxC = np.max(dataM, axis=0)
        rangeC = maxC - minC
        rangeCli = rangeC[0].tolist()
        for i in range(len(rangeCli[0])):
            if rangeCli[0][i] == 0:
                rangeCli[0][i] = 1.0
        rangeC = np.asmatrix(rangeCli)
        self.PCAdataColumn[result_name][dnum-1] = 1- ((maxC - dataM)/rangeC)
        


        #create color matrix
        if color_header != "None":
            self.PCAdataColor[result_name][dnum-1] = presult.get_data_s([color_header])
            minC = np.min(self.PCAdataColor[result_name][dnum-1], axis=0)
            maxC = np.max(self.PCAdataColor[result_name][dnum-1], axis=0)
            rangeC = maxC - minC
            rangeCli = rangeC[0].tolist()
            for i in range(len(rangeCli[0])):
                if rangeCli[0][i] == 0:
                    rangeCli[0][i] = 1.0
            rangeC = np.asmatrix(rangeCli)
            self.PCAdataColor[result_name][dnum-1] = 1- ((maxC - self.PCAdataColor[result_name][dnum-1])/rangeC)
            self.PCAdataColor[result_name][dnum-1] = self.PCAdataColor[result_name][dnum-1].tolist()
            color = self.PCAdataColor[result_name][dnum-1]

        #create size matrix
        if size_header != "None":
            self.PCAdataSize[result_name][dnum-1] = presult.get_data_s([size_header])
            minC = np.min(self.PCAdataSize[result_name][dnum-1], axis=0)
            maxC = np.max(self.PCAdataSize[result_name][dnum-1], axis=0)
            rangeC = maxC - minC
            rangeCli = rangeC[0].tolist()
            for i in range(len(rangeCli[0])):
                if rangeCli[0][i] == 0:
                    rangeCli[0][i] = 1.0
            rangeC = np.asmatrix(rangeCli)
            self.PCAdataSize[result_name][dnum-1] = 1- ((maxC - self.PCAdataSize[result_name][dnum-1])/rangeC)
            self.PCAdataSize[result_name][dnum-1] = self.PCAdataSize[result_name][dnum-1].tolist()
            size = self.PCAdataSize[result_name][dnum-1]

        pts = (self.view.build() * self.PCAdataColumn[result_name][dnum-1].T).T.tolist()
            

        for index,item in enumerate(pts):
            print "color[index]", color[index]
            rgb = colorsys.hsv_to_rgb(0.5, 1, color[index][0])
            rgb = "#%02x%02x%02x" % (rgb[0]*255, rgb[1]*255, rgb[2]*255)
            coordination = [item[0]-(2+2*size[index][0]), item[1]-(2+2*size[index][0]), item[0]+(2+2*size[index][0]), item[1]+(2+2*size[index][0])] 
            obj = self.canvas.create_oval(coordination, fill=rgb)
            self.dataObjDic[obj] = presult.get_row(index)
            self.PdataP.append(obj)
            #print "length of dataP is", len(self.dataP)
        """
        for obj in self.PdataP:
            self.canvas.tag_bind(obj, "<Enter>", self.printInfo)
            self.canvas.tag_bind(obj, "<Leave>", self.deleteInfo)
        """
        print "presult", presult.get_data
        print "headers, color_header, size_header", headers, color_header, size_header
        #this create dialog to plot data 

        #data_matrix = presult.get_data()
        #data_h_matrix = presult.get_h_data()
        #print "data_matrix,  data_header, data_h_matrix", data_matrix, data_header, data_h_matrix

    #This function shows the detail  of the pca analysis
    def pcaDetail(self):
        print "self.pcaDetail"
        if self.pcalist.curselection() != '':
            result_name = self.pcalist_s[self.pcalist.curselection()[0]]
            presult = self.PCAresult[result_name]
            eigenvectors = presult.get_eigenvectors()
            eigenvalues = presult.get_eigenvalues().tolist()[0]
            presult_data = presult.get_data_r()
            self.buildDetailDialog(presult_data, eigenvalues, eigenvectors, presult.get_data_headers())

    #This fcuntion deleted the analysis result which  is selected
    def pcaDelete(self):
        result_name = self.pcalist_s[self.pcalist.curselection()[0]]
        if result_name != '':
            self.PCAresult.pop(result_name)
            self.pcalist.delete(0, tk.END)
            self.pcalist_s.remove(result_name)
            for item in self.pcalist_s:
                self.pcalist.insert(tk.END, item)
            


    #This calls plotting data function
    def plotData(self):
        self.root.update()
        self.methodDialog = PlotAdvanced(self.root)
        if not len(self.dataHeaders.keys()) == len(self.root.dataFile.keys()):
            tkMessageBox.showinfo("error", "No columns selected")
            #self.cancel()
        else :
            if (self.methodDialog.dataC == "continuous"):
                self.buildPoints(self.dataHeaders, self.color_header, self.size_header)
            else:
                filename = self.plot_pendingFile[0]
                unique, mapping = np.unique(np.array(self.root.dataFile[filename].get_data(["category"])), return_inverse=True)
                self.buildKmeansPlotC(len(unique))
                color_header = self.KmeansPlotC.kmeans_color
                print "headers_list", self.root.dataFile[filename].get_headers()
                print "data", self.root.dataFile[filename].get_data(self.root.dataFile[filename].get_headers())
                print "size header", self.size_header[self.plot_pendingFile[0]]
                print "color header", self.color_header[self.plot_pendingFile[0]]
                self.buildpointsK(filename, self.root.dataFile[filename], self.dataHeaders[self.plot_pendingFile[0]], self.size_header[self.plot_pendingFile[0]], color_header, False, mapping)

    #This function creates axes
    def buildAxes(self):
        self.cloneView = self.view.clone()
        vtm = self.view.build()
        pts = (vtm * self.axisPoints.T).T
        for i in range(2):
            pts2 = np.hstack((pts[i*2, [0,1]],pts[i*2+1, [0,1]]))
            pts2 = pts2.tolist()
            self.axes.append(self.canvas.create_line(pts2))
        pt3 = np.hstack((pts[4, [0,1]], pts[5, [0,1]]))
        pt3 = pt3.tolist()
        self.axes.append(self.canvas.create_line(pt3))

    #This function actually plots the data
    def buildPoints(self, headers_list, color_header, size_header):
        for obj in self.axes:
            self.canvas.delete(obj)
        self.axes = []
        for obj in self.dataP:
            self.canvas.delete(obj)
        self.dataP = []
        #print "self.root.dataFile.keys() is", self.root.dataFile.keys()
        for filename in self.root.dataFile.keys():
            self.dataColor[filename] = []
            self.dataSize[filename] = []
            color = []
            row_num = self.root.dataFile[filename].get_raw_num_rows()
            for i in range(row_num):
                self.dataColor[filename].append([0.0])
                self.dataSize[filename].append([0.0])
            color = self.dataColor[filename]
            size = self.dataSize[filename]

            #create the data matrix for XYZ
            if headers_list[filename][2] == "None":
                #print "headers_list, headers_list[:2]", headers_list
                headers_list[filename] = headers_list[filename][:2]
                self.dataColumn[filename] = self.root.dataFile[filename].get_data(headers_list[filename])
                zeros = np.zeros([row_num, 1])
                ones = np.ones([row_num, 1])
                dataM = np.column_stack((self.dataColumn[filename], zeros))
                dataM = np.column_stack((dataM, ones))
            else:
                self.dataColumn[filename] = self.root.dataFile[filename].get_data(headers_list[filename])
                ones = np.ones([row_num, 1])
                dataM = np.column_stack((self.dataColumn[filename], ones))
            minC = np.min(dataM, axis=0)
            maxC = np.max(dataM, axis=0)
            rangeC = maxC - minC
            rangeCli = rangeC[0].tolist()
            for i in range(len(rangeCli[0])):
                if rangeCli[0][i] == 0:
                    rangeCli[0][i] = 1.0
            rangeC = np.asmatrix(rangeCli)
            self.dataColumn[filename] = 1- ((maxC - dataM)/rangeC)

            #create color matrix
            if color_header[filename] != "None":
                self.dataColor[filename] = self.root.dataFile[filename].get_data([color_header[filename]])
                minC = np.min(self.dataColor[filename], axis=0)
                maxC = np.max(self.dataColor[filename], axis=0)
                rangeC = maxC - minC
                rangeCli = rangeC[0].tolist()
                for i in range(len(rangeCli[0])):
                    if rangeCli[0][i] == 0:
                        rangeCli[0][i] = 1.0
                rangeC = np.asmatrix(rangeCli)
                self.dataColor[filename] = 1- ((maxC - self.dataColor[filename])/rangeC)
                self.dataColor[filename] = self.dataColor[filename].tolist()
                color = self.dataColor[filename]

            #create size matrix
            if size_header[filename] != "None":
                self.dataSize[filename] = self.root.dataFile[filename].get_data([size_header[filename]])
                minC = np.min(self.dataSize[filename], axis=0)
                maxC = np.max(self.dataSize[filename], axis=0)
                rangeC = maxC - minC
                rangeCli = rangeC[0].tolist()
                for i in range(len(rangeCli[0])):
                    if rangeCli[0][i] == 0:
                        rangeCli[0][i] = 1.0
                rangeC = np.asmatrix(rangeCli)
                self.dataSize[filename] = 1- ((maxC - self.dataSize[filename])/rangeC)
                self.dataSize[filename] = self.dataSize[filename].tolist()
                size = self.dataSize[filename]

            pts = (self.view.build() * self.dataColumn[filename].T).T.tolist()
            

            for index,item in enumerate(pts):
                rgb = colorsys.hsv_to_rgb(0.5, 1, color[index][0])
                rgb = "#%02x%02x%02x" % (rgb[0]*255, rgb[1]*255, rgb[2]*255)
                coordination = [item[0]-(2+2*size[index][0]), item[1]-(2+2*size[index][0]), item[0]+(2+2*size[index][0]), item[1]+(2+2*size[index][0])] 
                obj = self.canvas.create_oval(coordination, fill=rgb)
                self.dataObjDic[obj] = self.root.dataFile[filename].get_row(index)
                self.dataP.append(obj)
            #print "length of dataP is", len(self.dataP)
        self.updateAxes()
        self.updatePoints()
        for obj in self.dataP:
            self.canvas.tag_bind(obj, "<Enter>", self.printInfo)
            self.canvas.tag_bind(obj, "<Leave>", self.deleteInfo)

    def buildpointsK(self, filename, data, headers_list, size_header, color_header, kmean = True, mapping= None):
        for obj in self.axes:
            self.canvas.delete(obj)
        self.axes = []
        for obj in self.KdataP:
            self.canvas.delete(obj)
        self.KdataP = []
        row_num = data.get_raw_num_rows()
        self.KdataSize[filename] = []
        self.KdataColor[filename] = []
        color = []
        row_num = data.get_raw_num_rows()
        s = "ID" + str(data.get_IDs_counter())
        for i in range(row_num):
            self.KdataSize[filename].append([0.0])
            if kmean == True:
                self.KdataColor[filename].append(color_header[int(data.get_data([s])[i][0])]) 
            else:
                print "mapping[i]", mapping[i]
                self.KdataColor[filename].append(color_header[int(mapping[i])])

        color = self.KdataColor[filename]
        size = self.KdataSize[filename]
        if headers_list[2] == "None":
            #print "headers_list, headers_list[:2]", headers_list
            headers_list = headers_list[:2]
            self.KdataColumn[filename] = data.get_data(headers_list)
            zeros = np.zeros([row_num, 1])
            ones = np.ones([row_num, 1])
            dataM = np.column_stack((self.KdataColumn[filename], zeros))
            dataM = np.column_stack((dataM, ones))
        else:
            self.KdataColumn[filename] = data.get_data(headers_list)
            ones = np.ones([row_num, 1])
            dataM = np.column_stack((self.KdataColumn[filename], ones))
        minC = np.min(dataM, axis=0)
        maxC = np.max(dataM, axis=0)
        rangeC = maxC - minC
        rangeCli = rangeC[0].tolist()
        for i in range(len(rangeCli[0])):
            if rangeCli[0][i] == 0:
                rangeCli[0][i] = 1.0
        rangeC = np.asmatrix(rangeCli)
        self.KdataColumn[filename] = 1- ((maxC - dataM)/rangeC)

        #create size matrix
        if size_header != "None":
            print "size", size
            self.KdataSize[filename] = data.get_data([size_header])
            minC = np.min(self.KdataSize[filename], axis=0)
            maxC = np.max(self.KdataSize[filename], axis=0)
            rangeC = maxC - minC
            rangeCli = rangeC[0].tolist()
            for i in range(len(rangeCli[0])):
                if rangeCli[0][i] == 0:
                    rangeCli[0][i] = 1.0
            rangeC = np.asmatrix(rangeCli)
            self.KdataSize[filename] = 1- ((maxC - self.KdataSize[filename])/rangeC)
            self.KdataSize[filename] = self.KdataSize[filename].tolist()
            size = self.KdataSize[filename]

        pts = (self.view.build() * self.KdataColumn[filename].T).T.tolist()
        for index,item in enumerate(pts):
            rgb = self.KdataColor[filename][index]
            coordination = [item[0]-(2+2*size[index][0]), item[1]-(2+2*size[index][0]), item[0]+(2+2*size[index][0]), item[1]+(2+2*size[index][0])] 
            obj = self.canvas.create_oval(coordination, fill=rgb)
            self.dataObjDic[obj] = self.root.dataFile[filename].get_row(index)
            self.KdataP.append(obj)

        self.updateAxes()
        #self.updatePoints()
        for obj in self.KdataP:
            self.canvas.tag_bind(obj, "<Enter>", self.printInfo)
            self.canvas.tag_bind(obj, "<Leave>", self.deleteInfo)

    

        #create the data matrix for XYZ
        if headers_list[filename][2] == "None":
            #print "headers_list, headers_list[:2]", headers_list
            headers_list[filename] = headers_list[filename][:2]
            self.dataColumn[filename] = self.root.dataFile[filename].get_data(headers_list[filename])
            zeros = np.zeros([row_num, 1])
            ones = np.ones([row_num, 1])
            dataM = np.column_stack((self.dataColumn[filename], zeros))
            dataM = np.column_stack((dataM, ones))
        else:
            self.dataColumn[filename] = self.root.dataFile[filename].get_data(headers_list[filename])
            ones = np.ones([row_num, 1])
            dataM = np.column_stack((self.dataColumn[filename], ones))
        minC = np.min(dataM, axis=0)
        maxC = np.max(dataM, axis=0)
        rangeC = maxC - minC
        rangeCli = rangeC[0].tolist()
        for i in range(len(rangeCli[0])):
            if rangeCli[0][i] == 0:
                rangeCli[0][i] = 1.0
        rangeC = np.asmatrix(rangeCli)
        self.dataColumn[filename] = 1- ((maxC - dataM)/rangeC)
    #This function updates axes and redraws them
    def updateAxes(self):
        for obj in self.axes:
            self.canvas.delete(obj)
        self.axes = []
        vtm = self.view.build()
        pts = (vtm * self.axisPoints.T).T
        for i in range(2):
            pts2 = np.hstack((pts[i*2, [0,1]],pts[i*2+1, [0,1]]))
            pts2 = pts2.tolist()
            obj = self.canvas.create_line(pts2)
            self.axes.append(obj)
            for index, filename in enumerate(self.root.dataFile.keys()):
                if (filename in self.dataHeaders.keys() and len(self.dataHeaders[filename]) != 0):
                    self.axes.append(self.canvas.create_text(pts2[0][2], pts2[0][3]+10*index, 
                        text=self.dataHeaders[filename][i]))
                if (filename in self.KdataHeaders.keys() and len(self.KdataHeaders) != 0):
                    self.axes.append(self.canvas.create_text(pts2[0][2], pts2[0][3]+10*index, 
                        text=self.KdataHeaders[filename][i]))
        pts3 = np.hstack((pts[4, [0,1]], pts[5, [0,1]]))
        pts3 = pts3.tolist()
        self.axes.append(self.canvas.create_line(pts3))
        for index, filename in enumerate(self.root.dataFile.keys()):
            if (filename in self.dataHeaders.keys() and len(self.dataHeaders[filename]) != 0):
                if len(self.dataHeaders[filename]) > 2:
                    self.axes.append(self.canvas.create_text(pts3[0][2], pts3[0][3]+10*index, 
                        text=self.dataHeaders[filename][2]))
                if (filename in self.KdataHeaders.keys() and len(self.KdataHeaders) > 2):
                    self.axes.append(self.canvas.create_text(pts2[0][2], pts2[0][3]+10*index, 
                        text=self.KdataHeaders[filename][i]))



    #this fucntion updates points by relocating them.
    def updatePoints(self):
        #print "self.dataP len", len(self.dataP)
        index_num = 0
        for i, filename in enumerate(self.root.dataFile.keys()):
            item_num = 0
            if (filename in self.dataColumn.keys() and len(self.dataColumn[filename]) != 0):

                pts = (self.view.build() * self.dataColumn[filename].T).T.tolist()
                #print "pts", pts
                color = self.dataColor[filename]
                size = self.dataSize[filename]
                for index, item in enumerate(pts):
                    rgb = colorsys.hsv_to_rgb(0.5, 1, color[index][0])
                    rgb = "#%02x%02x%02x" % (rgb[0]*255, rgb[1]*255, rgb[2]*255)
                    coordination = [item[0]-(2+2*size[index][0]), item[1]-(2+2*size[index][0]), 
                        item[0]+(2+2*size[index][0]), item[1]+(2+2*size[index][0])] 
                    self.canvas.coords(self.dataP[index+item_num], coordination[0], coordination[1], coordination[2], coordination[3])
                item_num = self.root.dataFile[filename].get_raw_num_rows() 

        if len(self.PCAplotlist.keys()) != 0:
            for i, result_name in enumerate(self.PCAplotlist.keys()):
                for i in range(self.PCAplotlist[result_name]):
                    pts = (self.view.build() * self.PCAdataColumn[result_name][i].T).T.tolist()
                    #print "pts", pts
                    color = self.PCAdataColor[result_name][i]
                    size = self.PCAdataSize[result_name][i]
                    for index, item in enumerate(pts):
                        rgb = colorsys.hsv_to_rgb(0.5, 1, color[index][0])
                        rgb = "#%02x%02x%02x" % (rgb[0]*255, rgb[1]*255, rgb[2]*255)
                        coordination = [item[0]-(2+2*size[index][0]), item[1]-(2+2*size[index][0]),
                            item[0]+(2+2*size[index][0]), item[1]+(2+2*size[index][0])] 
                        self.canvas.coords(self.PdataP[index+index_num], coordination[0], coordination[1], coordination[2], coordination[3])
                    index_num = len(pts)
        if len(self.KdataColumn.keys()) != 0 and len(self.KdataP) != 0:
            item_num = 0
            for filename in self.KdataColumn.keys():
                pts = (self.view.build() * self.KdataColumn[filename].T).T.tolist()
                for index,item in enumerate(pts):
                    size = self.KdataSize[filename]
                    rgb = self.KdataColor[filename][index]
                    coordination = [item[0]-(2+2*size[index][0]), item[1]-(2+2*size[index][0]), item[0]+(2+2*size[index][0]), item[1]+(2+2*size[index][0])] 
                    self.canvas.coords(self.KdataP[index+index_num], coordination[0], coordination[1], coordination[2], coordination[3])
                index_num = len(pts)

                
        for obj in self.dataP:
            self.canvas.tag_bind(obj, "<Enter>", self.printInfo)
            self.canvas.tag_bind(obj, "<Leave>", self.deleteInfo)
        for obj in self.PdataP:
            self.canvas.tag_bind(obj, "<Enter>", self.printInfo)
            self.canvas.tag_bind(obj, "<Leave>", self.deleteInfo)
        for obj in self.KdataP:
            self.canvas.tag_bind(obj, "<Enter>", self.printInfo)
            self.canvas.tag_bind(obj, "<Leave>", self.deleteInfo)

    #This function updates the fitted line
    def updateFits(self):
        for i, filename in enumerate(self.regFile):
            line = (self.view.build() * self.regEndpoints[filename].T).T.tolist()
            coordination = [line[2][0], line[2][1], line[3][0], line[3][1]]
            #print "line", line
            #print "coordination", coordination
            for obj in self.line:
                self.canvas.coords(obj,coordination[0], coordination[1], coordination[2], coordination[3])
            self.reg_label[filename].place(x=0, y=self.h-30-30*i)

    #this fcuntion implement simple linear regression by using linregress function
    def buildLinearRegression(self):
        for i, filename in enumerate(self.regFile):
            row_num = self.root.dataFile[filename].get_raw_num_rows()
            indeColumn = self.root.dataFile[filename].get_data([self.dataHeaders[filename][0]])
            depenColumn = self.root.dataFile[filename].get_data([self.dataHeaders[filename][1]])
            indeColumn_norm = analysis.normalize_columns_separately(self.root.dataFile[filename], [self.dataHeaders[filename][0]])
            depenColumn_norm = analysis.normalize_columns_separately(self.root.dataFile[filename], [self.dataHeaders[filename][1]])
            matrixA = np.column_stack((indeColumn_norm, depenColumn_norm))
            zeros = np.zeros([row_num, 1])
            ones = np.ones([row_num, 1])
            matrixA = np.column_stack((matrixA, zeros))
            matrixA = np.column_stack((matrixA, ones))
            self.dataColumn[filename] = matrixA
            #print "matrixA", matrixA
            pts = (self.view.build() * matrixA.T).T.tolist()
            for index, item in  enumerate(pts):
                coordination = [item[0]-2, item[1]-2, item[0]+2, item[1]+2]
                obj = self.canvas.create_oval(coordination, fill="black")
                self.RdataP.append(obj)
            slope, intercept, r_value, p_value, std_err = stats.linregress(indeColumn.flatten(), depenColumn.flatten())
            x_range = analysis.data_range(self.root.dataFile[filename], [self.dataHeaders[filename][0]])
            y_range = analysis.data_range(self.root.dataFile[filename], [self.dataHeaders[filename][1]])
            #print "x_range, y_range", x_range, y_range
            end_points1 = ((x_range[0][0] * slope + intercept) - y_range[0][0])/(y_range[0][1] - y_range[0][0])
            end_points2 = ((x_range[0][1] * slope + intercept) - y_range[0][0])/(y_range[0][1] - y_range[0][0])
            self.regEndpoints[filename] = np.matrix([[0,0,0,1],
                                        [1,0,0,1],
                                        [0,end_points1,0,1],
                                        [1,end_points2,0,1],
                                        [0,0,0,1],
                                        [0,0,1,1]])
            line = (self.view.build() * self.regEndpoints[filename].T).T.tolist()
            coordination = [line[2][0], line[2][1], line[3][0], line[3][1]]
            #print "coordination", coordination
            obj = self.canvas.create_line(coordination, fill="red")
            self.line.append(obj)

            self.reg_text_info[filename] = filename + " slope: %f, intercept: %f, r_value: %f" % (slope, intercept, r_value)
            self.reg_label[filename] = tk.Label(self.canvas, text=self.reg_text_info[filename], fg="black", anchor = tk.S)
            self.reg_label[filename].place(x=0, y=self.initDy-30-30*i)

    #this function implements linear regression by using linear regression funciton in analysis.py 
    def buildLinearMulRegression(self):
        for i, filename in enumerate(self.regFile):
            row_num = self.root.dataFile[filename].get_raw_num_rows()
            color = self.dataColor[filename]
            size = self.dataSize[filename]
            if len(self.dataHeaders[filename]) == 2:
                #print "self.dataHeaders[filename]", self.dataHeaders[filename]
                indeColumn = self.root.dataFile[filename].get_data([self.dataHeaders[filename][0]])
                depenColumn = self.root.dataFile[filename].get_data([self.dataHeaders[filename][1]])
                indeColumn_norm = analysis.normalize_columns_separately(self.root.dataFile[filename], [self.dataHeaders[filename][0]])
                depenColumn_norm = analysis.normalize_columns_separately(self.root.dataFile[filename], [self.dataHeaders[filename][1]])
                zeros = np.zeros([row_num, 1])
                ones = np.ones([row_num, 1])
                matrixA = np.column_stack((indeColumn_norm, depenColumn_norm))
                matrixA = np.column_stack((matrixA, zeros))
                matrixA = np.column_stack((matrixA, ones))
                self.dataColumn[filename] = matrixA
            elif len(self.dataHeaders[filename]) == 3:
                #print "self.dataHeaders[filename]", self.dataHeaders[filename]
                indeColumn = self.root.dataFile[filename].get_data([self.dataHeaders[filename][0]])
                depenColumn = self.root.dataFile[filename].get_data([self.dataHeaders[filename][1]])
                depenColumn2 = self.root.dataFile[filename].get_data([self.dataHeaders[filename][2]])
                indeColumn_norm = analysis.normalize_columns_separately(self.root.dataFile[filename], [self.dataHeaders[filename][0]])
                depenColumn_norm = analysis.normalize_columns_separately(self.root.dataFile[filename], [self.dataHeaders[filename][1]])
                depenColumn2_norm = analysis.normalize_columns_separately(self.root.dataFile[filename], [self.dataHeaders[filename][2]])
                ones = np.ones([row_num, 1])
                matrixA = np.column_stack((indeColumn_norm, depenColumn_norm))
                matrixA = np.column_stack((matrixA, depenColumn2_norm))
                matrixA = np.column_stack((matrixA, ones))
                self.dataColumn[filename] = matrixA
            pts = (self.view.build() *  self.dataColumn[filename].T).T.tolist()
            for index, item in  enumerate(pts):
                rgb = colorsys.hsv_to_rgb(0.5, 1, color[index][0])
                rgb = "#%02x%02x%02x" % (rgb[0]*255, rgb[1]*255, rgb[2]*255)
                coordination = [item[0]-(2+2*size[index][0]), item[1]-(2+2*size[index][0]), 
                        item[0]+(2+2*size[index][0]), item[1]+(2+2*size[index][0])]
                obj = self.canvas.create_oval(coordination, fill=rgb)
                self.dataObjDic[obj] = self.root.dataFile[filename].get_row(index)
                self.dataP.append(obj)
            print "dataP points number", len(self.dataP)
            coeff, sse, R2, t, p = analysis.linear_regression(self.root.dataFile[filename],self.independent_var[filename], [self.dataHeaders[filename][1]])
            self.linear_reg[filename] = [coeff, sse, R2, t, p]
            #print "self.root.dataFile[filename],self.independent_var[filename],[self.dataHeaders[filename][1]", self.root.dataFile[filename], self.independent_var[filename], self.dataHeaders[filename][1]
            #print "self.linear_reg[filename]", self.linear_reg[filename]
            self.writeLine(filename, coeff, R2, i)
    

    #this function actually draws line with the certain coeff
    def writeLine(self, filename, coeff, R2, index):
        if len(coeff) == 2:
            x_range = analysis.data_range(self.root.dataFile[filename], [self.dataHeaders[filename][0]])
            y_range = analysis.data_range(self.root.dataFile[filename], [self.dataHeaders[filename][1]])
            end_points1 = ((x_range[0][0] * coeff[0] + coeff[1]) - y_range[0][0])/(y_range[0][1] - y_range[0][0])
            end_points2 = ((x_range[0][1] * coeff[0] + coeff[1]) - y_range[0][0])/(y_range[0][1] - y_range[0][0])
            self.regEndpoints[filename] = np.matrix([[0,0,0,1],
                                    [1,0,0,1],
                                    [0,end_points1,0,1],
                                    [1,end_points2,0,1],
                                    [0,0,0,1],
                                    [0,0,1,1]])
            line = (self.view.build() * self.regEndpoints[filename].T).T.tolist()
            coordination = [line[2][0], line[2][1], line[3][0], line[3][1]] 
        elif len(coeff) >= 3:
            x_range = analysis.data_range(self.root.dataFile[filename], [self.dataHeaders[filename][0]])
            y_range = analysis.data_range(self.root.dataFile[filename], [self.dataHeaders[filename][1]])
            z_range = analysis.data_range(self.root.dataFile[filename], [self.dataHeaders[filename][2]])
            end_points1 = ((x_range[0][0] * coeff[0] + z_range[0][0] * coeff[1] + coeff[2]) - y_range[0][0])/(y_range[0][1] - y_range[0][0])
            end_points2 = ((x_range[0][1] * coeff[0] + z_range[0][1] *coeff[1] + coeff[2]) - y_range[0][0])/(y_range[0][1] - y_range[0][0])
            self.regEndpoints[filename] = np.matrix([[0,0,0,1],
                                    [1,0,0,1],
                                    [0,end_points1,0,1],
                                    [1,end_points2,1,1],
                                    [0,0,0,1],
                                    [0,0,1,1]])
            line = (self.view.build() * self.regEndpoints[filename].T).T.tolist()
            coordination = [line[2][0], line[2][1], line[3][0], line[3][1]] 

        obj = self.canvas.create_line(coordination, fill="red")
        self.line.append(obj)

        self.reg_text_info[filename] = filename + "coefficient: %s, intercept: %f, r_value: %f" % (coeff[:2], coeff[-1], R2)
        self.reg_label[filename] = tk.Label(self.canvas, text=self.reg_text_info[filename], fg="black", anchor = tk.S)
        self.reg_label[filename].place(x=0, y=self.initDy-30-30*index)
        print "coefficient", coeff
    #This makes it possible to resize the graph dynamically
    def resize(self, event):
        self.w,self.h = event.width, event.height
        
        self.view.screen = [(400.0/float(self.initDx))*self.w, (400.0/float(self.initDy))*self.h]
        print "self.view.screen changed", self.view.screen
        self.updateAxes()
        self.updatePoints()
        if self.regFile != None:
            self.updateFits()

    #creating the dialog        
    def buildDialog(self):
        self.root.update()
        self.dialog = MyDialog(self.root)
    
    #creating dialog to choose the columns to represent
    def buildDataDialog(self, filenames):
        self.root.update()
        self.dataDialog = DataDialog(self.root, filenames)

    #creating the dialog to delete datasets.
    def buildFileDialog(self):
        self.root.update()
        self.fileDialog = FileManagementDialog(self.root)

    #creating the dialog to choose variables for linear regression
    def buildLinearDialog(self, filenames):
        self.root.update()
        print "filename inside build is", filenames
        self.linearDialog = LinearDialog(self.root, filenames)
        ind = self.linearDialog.linearInd
        dep = self.linearDialog.linearcoY
        ind.append(dep)
        headers = ind
        self.linearDialog2 = LinearDialog2(self.root, headers)

    #this function is called when a user changes the setting of data points
    def updateDialog(self):
        self.dialog = MyDialog(self.root)

    #This creates the dialog to choose the data sets to change the setting
    def buildChooseData(self):
        self.root.update()
        self.chooseDialog = ChoosingData(self.root)

    #this crate the fialog to choose the file to compute linear regression
    def buildChooseFile(self):
        self.root.update()
        self.ChosenFile = ChoosingFile_forReg(self.root)

    def buildChooseVar(self):
        self.root.update()
        self.selectedVar = LinearDialog(self.root)

    #This fucntion creates PCA dialog
    def buildPCAdialog(self, filename):
        self.root.update()
        self.PCADialog = PCADialog(self.root, filename)

    #This cuntion creates PCA plot dialog
    def buildPCAplotDialog(self, headers_list):
        self.root.update()
        self.PCAplotDialog = PCAplotDialog(self.root, headers_list)

    #this creates the dialog to show the detail of PCA
    def buildDetailDialog(self, presult_data, eigenvalues, eigenvectors, headers):
        self.root.update()
        self.PCAdetailDialog = PCAresultWindow(self.root, presult_data, eigenvalues, eigenvectors, headers)

    #This creates the dialog to choose the detail of kmeans
    def buildKmeansDialog(self, headers):
        self.root.update()
        self.KmeansDialog = KmeansDialog(self.root, headers)

    #This creates the dialog to plot the result of kmeans
    def buildKmeansPlot(self, headers):
        self.root.update()
        self.KmeansPlot = KmeansPlot(self.root, headers)

    #This creates the dialog to choose the color of clusters
    def buildKmeansPlotC(self, K):
        self.root.update()
        self.KmeansPlotC = KmeansPlotC(self.root, K)

    #This fucntion creates the clone of view object
    def reset(self):
        self.view = self.cloneView.clone()
        self.updateAxes()
        self.updatePoints()
        self.text2.delete('1.0', tk.END)
        self.text3.delete('1.0', tk.END)

    #This function resets everything
    def resetAll(self):
        self.view = self.cloneView.clone()
        self.updateAxes()
        self.updatePoints()
        if self.regFile != None:
            self.updateFits()
        self.text2.delete('1.0', tk.END)
        self.text3.delete('1.0', tk.END)

    #this function creates the menu button
    def buildMenus(self):
        
        # create a new menu
        menu = tk.Menu(self.root)

        # set the root menu to our new menu
        self.root.config(menu = menu)

        # create a variable to hold the individual menus
        menulist = []

        # create a file menu
        filemenu = tk.Menu( menu )
        menu.add_cascade( label = "File", menu = filemenu )
        menulist.append(filemenu)

        # create another menu for kicks
        cmdmenu = tk.Menu( menu )
        menu.add_cascade( label = "Command", menu = cmdmenu )
        menulist.append(cmdmenu)

        viewmenu = tk.Menu(menu)
        menu.add_cascade(label ="Plot", menu = viewmenu)
        menulist.append(viewmenu)

        linearmenu = tk.Menu(menu)
        menu.add_cascade(label="Linear Regression", menu=linearmenu)
        menulist.append(linearmenu)
        # menu text for the elements
        # the first sublist is the set of items for the file menu
        # the second sublist is the set of items for the option menu
        menutext = [ [ 'File Open', 'Delete Data File', 'Quit  \xE2\x8C\x98-Q' ],
                     [ 'Linear Regression', 'Cancel Linear Regression', 'PCA Analysis', 'K-means classifier'],
                     [ 'Choose Column', 'Plot Data', 'Delete Ploted Data', 'Save Plot'], 
                     [ 'Save analysis result', 'Recall analysis']]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [ [self.handleOpen, self.handleDelete, self.handleQuit],
                    [self.handleLinearRegression, self.handleDeleteLinearRegression, self.handlePCA, self.handleKmeans],
                    [self.handlePlotData, self.plotData,self.handlePlotDelete, self.savePlot ], 
                    [self.saveAnalysis, self.recallAnalysis]]


        
        # build the menu elements and callbacks
        for i in range( len( menulist ) ):
            for j in range( len( menutext[i]) ):
                if menutext[i][j] != '-':
                    print "menutext[i][j] is", menutext[i][j]
                    menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
                else:
                    menulist[i].add_separator()

    # create the canvas object
    def buildCanvas(self):
        self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
        self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
        self.canvas.bind('<Configure>', self.resize)
        return

    # build a frame and put controls in it
    def buildControls(self):

        ### Control ###
        # make a control frame on the right
        self.rightcntlframe = tk.Frame(self.root)
        self.rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # make a separator frame
        sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
        sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label( self.rightcntlframe, text="Control Panel", width=45 )
        label.pack( side=tk.TOP, pady=10 )

        # make a menubutton
        #self.colorOption = tk.StringVar( self.root )
        #self.colorOption.set("black")
        #colorMenu = tk.OptionMenu( rightcntlframe, self.colorOption, 
                                        #"black", "blue", "red", "green" ) # can add a command to the menu
        #colorMenu.pack(side=tk.TOP)

        # make a button in the frame
        # and tell it to call the handleButton method when it is pressed.
        button = tk.Button( self.rightcntlframe, text="Reset", 
                               command=self.resetAll )
        button2 = tk.Button(self.rightcntlframe, text="Change Setting",
                             command=self.updateDialog)
        button7 = tk.Button(self.rightcntlframe, text="Save plot", command=self.savePlot)
        button8 = tk.Button(self.rightcntlframe, text="Save analysis result",
                            command=self.saveAnalysis)
        button9 = tk.Button(self.rightcntlframe, text="Recall analysis", command=self.recallAnalysis)


        button.pack(side=tk.TOP)  # default side is top
        button2.pack(side=tk.TOP)
        

        #resultframe = tk.Frame(rightcntlframe)
        #resultframe.pack(side=tk.TOP, padx=2, pady=2, fill=tk.X)

        sep2 = tk.Frame( self.rightcntlframe, height=2, bd=1, relief=tk.SUNKEN)
        sep2.pack( side=tk.TOP, padx = 2, pady = 2, fill=tk.X)

        self.text = tk.Text(self.rightcntlframe, width=30, height=5)
        self.text.insert(tk.END, "Uploaded file:")
        self.text.pack(side=tk.TOP)
        

        sep4 = tk.Frame( self.rightcntlframe, height=2, bd=1, relief=tk.SUNKEN)
        sep4.pack( side=tk.TOP, padx = 2, pady = 2, fill=tk.X)
        self.text5 = tk.Text(self.rightcntlframe, width=30, height=1)

        self.text5.insert(tk.END, "Graph info")
        self.text5.pack(side=tk.TOP)
        self.text2 = tk.Text(self.rightcntlframe, width=30, height=2)
        self.text2.pack(side=tk.TOP)
        self.text3 = tk.Text(self.rightcntlframe, width=30, height=2)
        self.text3.pack(side=tk.TOP)

        #self.linearlist = tk.Listbox(self.rightcntlframe, selectmode=tk.SINGLE, exportselection=0,height= 5)
        #self.linearlist.pack(side=tk.TOP)

        sep3 = tk.Frame( self.rightcntlframe, height=2, bd=1, relief=tk.SUNKEN)
        sep3.pack( side=tk.TOP, padx = 2, pady = 2, fill=tk.X)
        self.text4 = tk.Text(self.rightcntlframe, width=30, height=1)
        self.text4.insert(tk.END, "PCA Analysis:")
        self.text4.pack(side=tk.TOP)
        self.pcalist = tk.Listbox(self.rightcntlframe, selectmode=tk.SINGLE, exportselection=0,height= 5)
        self.pcalist.pack(side=tk.TOP)


        

        return

    #this function binds buttons to the specif functions
    def setBindings(self):
        # bind mouse motions to the canvas
        self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
        self.canvas.bind('<Button-2>', self.handleMouseButton2)
        self.canvas.bind('<Command-Button-1>', self.handleMouseButton2)
        self.canvas.bind( '<Shift-Button-1>', self.handleMouseButton3 )
        self.canvas.bind('<B1-Motion>', self.handleMouseButton1Motion)
        self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
        self.canvas.bind('<Command-B1-Motion>', self.handleMouseButton2Motion)
        self.canvas.bind( '<Shift-B1-Motion>', self.handleMouseButton3Motion )
        self.canvas.bind('Command-o>', self.handleOpen)

        

        # bind command sequences to the root window
        self.root.bind( '<Command-q>', self.handleQuit )

    #This function quits the qpplication
    def handleQuit(self, event=None):
        print 'Terminating'
        self.root.destroy()

    def handleButton1(self):
        print 'handling command button:', self.colorOption.get()

    def handleMenuCmd1(self):
        print 'handling menu command 1'

    #this function implements the first step of the transformation of the graph when
    #the button1 is pressed
    def handleMouseButton1(self, event):
        print 'handle mouse button 1: %d %d' % (event.x, event.y)
        self.baseClick = (event.x, event.y)
        
    #This function implements the first step of the rotation of the graph when the button
    #button2 is pressed
    def handleMouseButton2(self, event):
        self.baseClick2 = (event.x, event.y)
        self.clone = self.view.clone()
        print 'handle mouse button 2: %d %d' % (event.x, event.y)

    #This function implements the first step of the scaling of the graph when the button
    #3 is pressed 
    def handleMouseButton3(self, event):
        print 'inside hundle mouse mouse button'
        clone = self.view.clone()
        self.originalExtent = clone.extent
        self.baseClick3 = (event.x, event.y)

    #this is clalled when the first mouse is being moved
    def handleMouseButton1Motion(self, event):
        motion = (event.x, event.y)
        self.root.Trans = self.dialog.dataTrans
        dx = float(motion[0]) - float(self.baseClick[0]) 
        dy = float(motion[1]) - float(self.baseClick[1]) 
        motionX = float(dx) / float(self.view.screen[0])
        motionY = float(dy) / float(self.view.screen[1])
        delta0 = motionX * self.view.extent[0]
        delta1 = motionY * self.view.extent[1]
        self.view.vrp += self.root.Trans*  delta0 * self.view.u + self.root.Trans* delta1 * self.view.vup
        self.updateAxes()
        self.updatePoints()
        self.baseClick = (event.x, event.y)
        if self.regFile != None:
            self.updateFits()

    # This is called if the second mouse button is being moved
    def handleMouseButton2Motion(self, event):
        self.text2.delete('1.0', tk.END)
        self.root.Rotate = self.dialog.dataRotate
        diff = (self.baseClick2[0] - event.x , self.baseClick2[1] - event.y)
        delta0 = math.pi*(float(diff[0])/200.0)*180
        delta1 = math.pi*(float(diff[1])/200.0)*180
        self.view = self.clone.clone()
        self.view.rotateVRC(self.root.Rotate*delta0, self.root.Rotate*delta1)
        self.updateAxes()
        self.updatePoints()
        if self.regFile != None:
            self.updateFits()
        str2 = "The rotation around VUP is %.2f.\n" % delta0 
        str3 = "The rotation around U is %.2f.\n" % delta1
        self.text2.insert(tk.END, str2)
        self.text2.insert(tk.END, str3)


    # This is called if the third mouse button is being moved
    def handleMouseButton3Motion(self, event):
        self.text3.delete('1.0', tk.END)
        # calculate the difference
        self.root.Scale = self.dialog.dataScale
        
        diff = (self.baseClick3[0] - event.x , self.baseClick3[1] - event.y)
        self.factor = 1 - (float(diff[1]) / float(self.initDy))*3
        if (self.factor > 3):
            self.factor = 3
        elif(self.factor < 0.1):
            self.factor = 0.1

        for i in range(len(self.view.extent)):
            self.view.extent[i] = self.originalExtent[i] * self.factor * (1/self.root.Scale)
        self.updateAxes()
        self.updatePoints()
        if self.regFile != None:
            self.updateFits()
        #print self.factor
        str1 = "The scale is %.2f.\n" % self.factor 
        self.text3.insert(tk.END, str1)
        # update base click
        #print 'handle button1 motion %d %d' % (diff[0], diff[1])

    #This funtion prints out the position of the mouse while the mouse is above 
    #some objects
    def printInfo(self, event):
        mousepo = (event.x, event.y)
        x = mousepo[0] + 20
        y = mousepo[1] + 25
        info = self.detectpoint(mousepo)[0]
        if not info == None:
            self.tw = tk.Toplevel(self.root)
            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(self.tw, text=info, justify='left',
                           background='yellow', relief='solid', borderwidth=1,
                           font=("times", "12", "normal"))
            label.pack(ipadx=1)

    #Once the mouse leaves the object, the coordinate information disappears
    def deleteInfo(self, event):
        if self.tw:
            self.tw.destroy()

    #Once the mouse over the certain object, which determines which object is 
    #under the mouse
    def detectpoint(self, mousepo):
        for obj in self.dataP:
            coordinates = self.canvas.coords(obj)
            if (coordinates[0]-5 < mousepo[0] < coordinates[2]+5 ):
                if (coordinates[1]-5 < mousepo[1] < coordinates[3]+5):
                    matinfo = self.dataObjDic[obj]
                    return matinfo.tolist()
        return None

    #This function saves the canvas as postscript picture
    def savePlot(self):
        f = tkFileDialog.asksaveasfilename(defaultextension=".ps")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.canvas.postscript(file=f, colormode='color')
        #f.close()

    #This cuntion saves the analysis result as a text file:
    def saveAnalysis(self):
        f = tkFileDialog.asksaveasfilename(defaultextension=".txt")
        target = open(f, 'w')
        for i in self.regFile:
            self.recall_analy[f] = [self.dataHeaders.copy(), self.color_header.copy(), self.size_header.copy(), self.linear_reg[i][:]]
            print "self.recall_analy[f]", f, self.recall_analy[f]
            ind_num = len(self.independent_var[i])
            target.write("Here is the result of linear regression between %s\n" % ','.join(map(str, self.dataHeaders[i])))
            target.write("Independent variable(s): %s\n" % ','.join(map(str, self.independent_var[i])))
            target.write("Dependent variable: %s\n" % self.dataHeaders[i][1])
            print self.linear_reg[i]
            if ind_num == 1:
                target.write("The linear regression equation: (%s) = %f * (%s) + %f\n" % (self.dataHeaders[i][1], self.linear_reg[i][0][0],self.dataHeaders[i][0],self.linear_reg[i][0][1]))
            elif ind_num == 2:
                target.write("The linear regression equation: (%s) = %f * (%s) + %f * (%s) + %f\n" % (self.dataHeaders[i][1], self.linear_reg[i][0][0],self.dataHeaders[i][0], 
                            self.linear_reg[i][0][1],self.dataHeaders[i][2], self.linear_reg[i][0][2]))
            elif ind_num == 3:
                target.write("The linear regression equation: (%s) = %f * (%s) + %f * (%s) + %f * (%s)+ %f\n" % (self.dataHeaders[i][1], self.linear_reg[i][0][0],self.dataHeaders[i][0], 
                            self.linear_reg[i][0][1],self.dataHeaders[i][2],self.linear_reg[i][0][2], self.color_header[i], self.linear_reg[i][0][3]))
            elif ind_num == 4:
                print self.dataHeaders[i][1], self.linear_reg[i][0][0],self.dataHeaders[i][0], self.linear_reg[i][0][1],self.dataHeaders[i][2],self.linear_reg[i][0][2], self.color_header[i],self.linear_reg[i][0][3],self.size_header[i],  self.linear_reg[i][0][4]
                target.write("The linear regression equation: (%s) = %f * (%s) + %f * (%s) + %f * (%s)+ %f * (%s) + %f\n" % (self.dataHeaders[i][1], self.linear_reg[i][0][0],self.dataHeaders[i][0], 
                            self.linear_reg[i][0][1],self.dataHeaders[i][2],self.linear_reg[i][0][2], self.color_header[i],self.linear_reg[i][0][3],self.size_header[i],  self.linear_reg[i][0][4]))
            target.write("The sum squared error of this model is: %f\n" % self.linear_reg[i][1][0])
            target.write("The coefficient of determianation is: %f\n" % self.linear_reg[i][2])
            if ind_num == 1:
                target.write("The t statistic (coefficients/standar error): first one = %f, second one = %f\n" % (self.linear_reg[i][3][0], self.linear_reg[i][3][1]))
            elif ind_num == 2:
                target.write("The t statistic (coefficients/standar error): first one = %f, second one = %f, third one = %f\n" % (self.linear_reg[i][3][0], self.linear_reg[i][3][1], self.linear_reg[i][3][2]))
            elif ind_num == 3:
                target.write("The t statistic (coefficients/standar error): first one = %f, second one = %f, third one = %f, fourth one = %f\n" % (self.linear_reg[i][3][0], self.linear_reg[i][3][1], self.linear_reg[i][3][2], self.linear_reg[i][3][3]))
            elif ind_num == 4:
                target.write("The t statistic (coefficients/standar error): first one = %f, second one = %f, third one = %f, fourth one = %f, fifth one = %f\n" % (self.linear_reg[i][3][0], self.linear_reg[i][3][1], self.linear_reg[i][3][2], self.linear_reg[i][3][3], self.linear_reg[i][3][4]))
            if ind_num == 1:
                target.write("The P value: first one = %f, second one = %f\n" % (self.linear_reg[i][4][0], self.linear_reg[i][4][1]))
            elif ind_num == 2:
                target.write("The P value: first one = %f, second one = %f, third one = %f\n" % (self.linear_reg[i][4][0], self.linear_reg[i][4][1], self.linear_reg[i][4][2]))
            elif ind_num == 3:
                target.write("The P value: first one = %f, second one = %f, third one = %f, fourth one = %f\n" % (self.linear_reg[i][4][0], self.linear_reg[i][4][1], self.linear_reg[i][4][2], self.linear_reg[i][4][3]))
            elif ind_num == 4:
                target.write("The P value: first one = %f, second one = %f, third one = %f, fourth one = %f, fifth one = %f\n" % (self.linear_reg[i][4][0], self.linear_reg[i][4][1], self.linear_reg[i][4][2], self.linear_reg[i][4][3], self.linear_reg[i][4][4]))
    
    #This recalls the analysis result
    def recallAnalysis(self):
        for obj in self.line:
            self.canvas.delete(obj)
        for obj in self.dataP:
            self.canvas.delete(obj)
        self.line = []
        self.dataP = []
        f = tkFileDialog.askopenfilename()
        print "self.racall_analy in recall", f, self.recall_analy[f]
        data_h, color_h, size_h, reg_r =  self.recall_analy[f]
        filename = data_h.keys()[0]
        if not filename in self.regFile:
            self.regFile.append(filename)
        self.dataHeaders[filename] = data_h[filename]
        self.color_header[filename] = color_h[filename]
        self.size_header[filename] = size_h[filename]
        self.dataColor[filename] = []
        self.dataSize[filename] = []
        row_num = self.root.dataFile[filename].get_raw_num_rows()
        #print "self.color_header[fileselected], self.size_header[fileselected]",self.color_header[filename],  self.size_header[filename]
        if self.color_header[filename] != "None":
            self.dataColor[filename] = self.root.dataFile[filename].get_data([self.color_header[filename]])
            minC = np.min(self.dataColor[filename], axis=0)
            maxC = np.max(self.dataColor[filename], axis=0)
            rangeC = maxC - minC
            rangeCli = rangeC[0].tolist()
            for i in range(len(rangeCli[0])):
                if rangeCli[0][i] == 0:
                    rangeCli[0][i] = 1.0
            rangeC = np.asmatrix(rangeCli)
            self.dataColor[filename] = 1- ((maxC - self.dataColor[filename])/rangeC)
            self.dataColor[filename] = self.dataColor[filename].tolist() 
            #print "self.dataColor[fileselected]", self.dataColor[fileselected]
        else:
            for i in range(row_num):
                self.dataColor[filename].append([0.5])
        if self.size_header[filename] != "None":
                self.dataSize[filename] = self.root.dataFile[filename].get_data([self.size_header[filename]])
                minC = np.min(self.dataSize[filename], axis=0)
                maxC = np.max(self.dataSize[filename], axis=0)
                rangeC = maxC - minC
                rangeCli = rangeC[0].tolist()
                for i in range(len(rangeCli[0])):
                    if rangeCli[0][i] == 0:
                        rangeCli[0][i] = 1.0
                rangeC = np.asmatrix(rangeCli)
                self.dataSize[filename] = 1- ((maxC - self.dataSize[filename])/rangeC)
                self.dataSize[filename] = self.dataSize[filename].tolist()
                size = self.dataSize[filename]
        else:
            for i in range(row_num):
                self.dataSize[filename].append([0])
        self.independent_var[filename] = [data_h[filename][0]]
        #print "self.independent_var[filename]", self.independent_var[filename]
        self.buildLinearMulRegression()
                
    def main(self): 
        print 'Entering main loop'
        self.root.mainloop()

if __name__ == "__main__":
    dapp = DisplayApp(1200, 675)
    dapp.main()

