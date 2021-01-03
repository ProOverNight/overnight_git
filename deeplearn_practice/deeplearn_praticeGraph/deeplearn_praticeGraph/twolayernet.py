import sys, os
sys.path.append(os.pardir)
import numpy as np
from layer_native import *
from collections import OrderedDict
from gradient import numerical_gradient

class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std = 0.01):
        #가중치 초기화
        #params: 신경망의 매개변수 저장
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

        #layers: 순서 있는 딕셔너리 변수, 신경망 계층 보관
        self.layers = OrderedDict()
        self.layers['Affine1'] = Affine(self.params['W1'], self.params['b1'])
        self.layers['Relu1'] = Relu()
        self.layers['Affine2'] = Affine(self.params['W2'], self.params['b2'])

        #lastLAyer: 신경망 마지막 계층
        self.lastLayer = SoftmaxWithLoss()

    def predict(self, x):
        #예측함수 / x: 이미지 데이터
        for layer in self.layers.values():
            x = layer.forward(x)

        return x

    def loss(self, x, t):
        #손실함수 값 구하기
        #x: 이미지 데이터 / t: 정답레이블
        y = self.predict(x)
        return self.lastLayer.forward(y, t)

    def accuracy(self, x, t):
        #정확도 구하기
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        if t.ndim != 1 : t = np.argmax(t, axis=1)

        accuracy = np_sum(y == t) / float(x.shape[0])

        return accuracy

    def numerical_gradient(self, x, t):
        #가중치 매개변수(w) 기울기 구하기(수치미분)
        # W = self.loss(x, t)
        loss_W = lambda W: self.loss(x, t)

        grads = {}
        grads['W1'] = numerical_gradient(loss_W, self.params['W1'])
        grads['b1'] = numerical_gradient(loss_W, self.params['b1'])
        grads['W2'] = numerical_gradient(loss_W, self.params['W2'])
        grads['b2'] = numerical_gradient(loss_W, self.params['b2'])

        return grads

    def gradient(self, x, t):
        #가중치 매개변수(w) 기울기 구하기(오차역전파법)
        #순전파
        self.loss(x, t)

        #역전파
        dout = 1
        dout = self.lastLayer.backward(dout)

        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        #결과저장
        grads['W1']  = self.layers['Affine1'].dW
        grads['b1']  = self.layers['Affine1'].db
        grads['W2']  = self.layers['Affine2'].dW
        grads['b2']  = self.layers['Affine2'].db

        return grads