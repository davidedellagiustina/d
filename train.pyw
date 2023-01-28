import numpy as np
import pickle
from bin.modules.mnist import Mnist
from bin.modules.ann import Ann
from bin.neural_network.network import NeuralNetwork

# Settings

layers = [784, 120, 50, 10]
epochs = 50
learning_rate = 1.0

# Training script

if __name__ == "__main__":
	layers_string = ""
	i = 0
	for layer in layers[1:-1]:
		i += 1
		layers_string += str(layer)
	layers_string = str(i) + "h" + layers_string
	ann = NeuralNetwork(layers)
	training_set, test_set = Mnist.unpickle("res/mnist/mnist_complete_set.pkl")
	print("Training started")
	ann.sgd(training_set, epochs, 15, learning_rate, test_set)
	print("Training completed. Efficiency on mnist test set: " + str(ann.evaluate(test_set) * 100 / len(test_set)) + "%")
	Ann.pickle(ann, "res/neural_network/ann_%s_%s.pkl" % (layers_string, ann.evaluate(test_set)))