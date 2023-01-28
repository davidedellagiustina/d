import numpy as np
import pickle

# Mnist class

class Mnist(object):

	# Function that loads the mnist training and test data from csv files and prepares two arrays to be pickled

	@staticmethod
	def _load_(source_tr, source_te, destination):
		mnist_training_data = []
		mnist_test_data = []
		# Training set array
		with open(source_tr, "r") as f_tr:
			lines_tr = f_tr.readlines()
		for line_tr in lines_tr:
			line_tr = line_tr.replace("\n", "")
			bits_tr = line_tr.split(",")
			result_tr = np.array([[float(0 if i != int(bits_tr[0]) else 1)] for i in range(10)])
			mnist_training_data.append((np.array([[float(bit_tr) / 255] for bit_tr in bits_tr[1:]], dtype = "float32"), result_tr))
		# Test set array
		with open(source_te, "r") as f_te:
			lines_te = f_te.readlines()
		for line_te in lines_te:
			line_te = line_te.replace("\n", "")
			bits_te = line_te.split(",")
			mnist_test_data.append((np.array([[float(bit_te) / 255] for bit_te in bits_te[1:]], dtype = "float32"), int(bits_te[0])))
		return (mnist_training_data, mnist_test_data)

	# Function that pickles the arrays into a binary file

	@staticmethod
	def pickle(source_tr, source_te, destination):
		mnist_training_data, mnist_test_data = Mnist._load_(source_tr, source_te, destination)
		with open(destination, "wb") as f:
			pickle.dump((mnist_training_data, mnist_test_data), f, pickle.HIGHEST_PROTOCOL)

	# Function that pickles the arrays into a binary file

	@staticmethod
	def unpickle(source):
		with open(source, "rb") as f:
			mnist_training_data, mnist_test_data = pickle.load(f)
		return (mnist_training_data, mnist_test_data)