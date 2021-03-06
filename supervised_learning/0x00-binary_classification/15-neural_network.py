#!/usr/bin/env python3
""" neural network with one hidden layer """
import numpy as np
import matplotlib.pyplot as plt


class NeuralNetwork:
    """ NeuralNetwork - defines a neural network with one hidden layer
    """
    def __init__(self, nx, nodes):
        """
        Args:
            nx:  is the number of input features
            nodes:  is the number of nodes found
                    in the hidden layer.
            W1: The weights vector for the hidden layer.
            b1: The bias for the hidden layer.
            A1: The activated output for the hidden layer.
            b2: The bias for the output neuron.
            A2: The activated output for the output neuron (prediction).
        """
        if type(nx) is not int:
            raise TypeError("nx must be an integer")
        elif nx < 1:
            raise ValueError("nx must be a positive integer")
        else:
            self.nx = nx

        if type(nodes) is not int:
            raise TypeError("nodes must be an integer")
        elif nodes < 1:
            raise ValueError("nodes must be a positive integer")
        else:
            self.nodes = nodes

        self.__W1 = np.random.randn(self.nodes, self.nx)
        self.__b1 = np.zeros((self.nodes, 1))
        self.__A1 = 0

        self.__W2 = np.random.randn(1, self.nodes)
        self.__b2 = 0
        self.__A2 = 0

    @property
    def W1(self):
        """ W1
        Return:
            private W1
        """
        return self.__W1

    @property
    def b1(self):
        """ b1
        Return:
            private b1
        """
        return self.__b1

    @property
    def A1(self):
        """ A1
        Return:
            private A1
        """
        return self.__A1

    @property
    def W2(self):
        """ W2
        Return:
            private W2
        """
        return self.__W2

    @property
    def b2(self):
        """ b2
        Return:
            private b2
        """
        return self.__b2

    @property
    def A2(self):
        """ A2
        Return:
            private A2
        """
        return self.__A2

    def forward_prop(self, X):
        """ forward_prop - Calculates the forward propagation

        Args:
           X:   contains the input data
        Return:
            Returns the private attributes __A1 and __A2
        """
        Z1 = np.matmul(self.__W1, X) + self.__b1
        self.__A1 = 1 / (1 + np.exp(-Z1))
        Z2 = np.matmul(self.__W2, self.__A1) + self.__b2
        self.__A2 = 1 / (1 + np.exp(-Z2))

        return self.__A1, self.__A2

    def cost(self, Y, A):
        """ cost - Calculates the cost of the model
                   using logistic regression.

        Args:
            Y contains labels for the input data
            A containing the activated output

        Return:
            Returns the cost
        """
        m = Y.shape[1]
        logprobs1 = Y * np.log(A)
        logprobs2 = (np.log(1.0000001 - A) * (1 - Y))
        cost = -(1 / m) * np.sum(logprobs1 + logprobs2)
        return cost

    def evaluate(self, X, Y):
        """ evaluate - Evaluates the neuron’s predictions
        Args:
            X - (nx, m) that contains the input data.
            Y - (1, m) contains the correct labels for the input data.

        Return
            Returns the neuron’s prediction and the cost of the network.
        """
        self.forward_prop(X)
        cost = self.cost(Y, self.__A2)

        return np.where(self.__A2 >= 0.5, 1, 0), cost

    def gradient_descent(self, X, Y, A1, A2, alpha=0.05):
        """ gradient_descent - Calculates one pass of gradient
                               descent on the neural network

            X contains the input data.
            Y contains the correct labels for the input data.
            A1 is the output of the hidden layer
            A2 is the predicted output
            alpha is the learning rate
        """
        m = Y.shape[1]
        dZ2 = A2 - Y
        dW2 = (1 / m) * np.matmul(dZ2, A1.T)
        db2 = (1 / m) * np.sum(dZ2, axis=1, keepdims=True)
        dZ1 = np.matmul(self.__W2.T, dZ2) * (A1 * (1 - A1))
        dW1 = (1 / m) * np.matmul(dZ1, X.T)
        db1 = (1 / m) * np.sum(dZ1, axis=1, keepdims=True)

        self.__W1 = self.__W1 - alpha * dW1
        self.__b1 = self.__b1 - alpha * db1
        self.__W2 = self.__W2 - alpha * dW2
        self.__b2 = self.__b2 - alpha * db2

    def train(self, X, Y, iterations=5000, alpha=0.05,
              verbose=True, graph=True, step=100):
        """ train - Trains the neuron
        Args:
            X           contains the input data
            Y           that contains the correct labels for the input data
            iterations  is the number of iterations to train over
            alpha       is the learning rate

        Return
            Returns the evaluation of the training data
        """
        if type(iterations) is not int:
            raise TypeError("iterations must be an integer")
        elif iterations <= 0:
            raise ValueError("iterations must be a positive integer")
        elif type(alpha) is not float:
            raise TypeError("alpha must be a float")
        elif alpha <= 0:
            raise ValueError("alpha must be positive")
        elif verbose is True or graph is True:
            if type(step) is not int:
                raise TypeError("step must be an integer")
            elif step <= 0 or step > iterations:
                raise ValueError("step must be positive and <= iterations")

        xiterations = np.arange(0, iterations + 1)
        ycost = []

        for i in range(iterations + 1):
            self.forward_prop(X)
            self.gradient_descent(X, Y, self.__A1, self.__A2, alpha)
            cost = self.cost(Y, self.__A2)
            ycost.append(cost)
            print("Cost after {} iterations: {}".format(i, cost))

        plt.plot(xiterations, ycost)
        plt.xlabel("iteration")
        plt.ylabel("cost")
        plt.title("Training Cost")
        plt.show()

        return self.evaluate(X, Y)
