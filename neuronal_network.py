import numpy as np
import matplotlib.pyplot as plt
import os

class Neural_Network(object):
  def __init__(self):
  #parameters
    self.inputSize = 3
    self.outputSize = 2
    self.hiddenSize = 4

  #weights
    self.W1 = np.random.randn(self.inputSize, self.hiddenSize) # (3x2) weight matrix from input to hidden layer
    self.W2 = np.random.randn(self.hiddenSize, self.outputSize) # (3x1) weight matrix from hidden to output layer

  def forward(self, X):
    #forward propagation through our network
    self.z = np.dot(X, self.W1)
    self.z2 = self.sigmoid(self.z) # activation function

    self.z3 = np.dot(self.z2, self.W2)
    o = self.sigmoid(self.z3) # final activation function
    return o

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))

  def sigmoidPrime(self, s):
    #derivative of sigmoid
    return s * (1 - s)

  def backward(self, X, y, o):
    # backward propagate through the network
    self.o_error = y - o # error in output
    self.o_delta = self.o_error*self.sigmoidPrime(o) # applying derivative of sigmoid to error

    self.z2_error = self.o_delta.dot(self.W2.T) # z2 error: how much our hidden layer weights contributed to output error
    self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2) # applying derivative of sigmoid to z2 error

    self.W1 += X.T.dot(self.z2_delta) # adjusting first set (input --> hidden) weights
    self.W2 += self.z2.T.dot(self.o_delta) # adjusting second set (hidden --> output) weights

  def train(self, X, y):
    o = self.forward(X)
    self.backward(X, y, o)

  def saveWeights(self):
    print("Ecriture des fichiers")
    includes = "const int InputNodes = 3;\nconst int HiddenNodes = 4;\nconst int OutputNodes = 2;\n\n"
    HiddenWeights = "//Poids de la couche cachée\nconst float HiddenWeights[InputNodes][HiddenNodes] = {\n"
    i = 1
    for w in self.W1:

      HiddenWeights += '  {'
      for v in w:
        HiddenWeights += str(v)
        if i%4==0:
          HiddenWeights += '}'
          if i<12:
            HiddenWeights += ','
          HiddenWeights += '\n'
        else:
          HiddenWeights += ', '
        i+= 1
    HiddenWeights += '};'
    #print(HiddenWeights)
    #file = open("HiddenWeights.txt", 'w')
    file_path = os.path.join(os.path.dirname(__file__), "Weights.h")
    file = open(file_path, 'w')
    file.write(includes)
    file.write(HiddenWeights)
    #file.close()

    OutputWeights = '\n\n// Poids de la couche de sortie\nconst float OutputWeights[HiddenNodes][OutputNodes] ={\n'
    i = 1
    for w in self.W2:

      OutputWeights += '  {'
      for v in w:
        OutputWeights += str(v)
        if i%2==0:
          OutputWeights += '}'
          if i<8:
            OutputWeights += ','
          OutputWeights += '\n'
        else:
          OutputWeights += ', '
        i+= 1
    OutputWeights += '};'
    #print(OutputWeights)
    #file = open("OutputWeights.txt", 'w')
    file.write(OutputWeights)
    file.close()


  def predict(self, xPredicted):
    print("Predicted data based on trained weights: ")
    print("Input (scaled): \n" + str(xPredicted))
    print("Output: \n" + str(self.forward(xPredicted)))