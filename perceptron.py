import numpy as np
class Perceptron:
    def __init__(self,weights,bias):
        '''
        Weights is expected to be an array of real numbers representing the weights
        Bias is expected to be a real number quantifying how easy it is to return 1
        '''
        self.weights = weights
        self.bias = bias
    def evaluate(self, inputs): 
        if sum(self.weights*inputs) + self.bias > 0:
            return 1
        else:
            return 0
    def train(self, inputs, output,l_rate):
        '''
        As above the inputs are an array of the real inputs
        The output is the known output of that array of inputs
        l_rate is the learning rate
        '''
        w_error =l_rate*( output - self.evaluate(inputs) )  
        for i in range(len(inputs)):
            self.weights[i] += w_error*inputs[i]
    


