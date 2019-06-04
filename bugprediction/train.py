# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

from os import path

from numpy import genfromtxt
from torch import Tensor
from torch.autograd import Variable
from torch.nn import MSELoss
from torch.optim import SGD
from linear_regression_model import LinearRegressionModel


def train():
    # Load data
    data_set_path = path.join(path.abspath(path.dirname(__file__)), '../resources/eclipse-data-set.csv')
    data = genfromtxt(data_set_path, delimiter=';', skip_header=1, usecols=[1, 2, 3, 4, 5])
    y_truth = Variable(Tensor(data[:, 0].reshape((-1, 1))))  # first column is number of bugs
    x_input = Variable(Tensor(data[:, 2].reshape((-1, 1))))  # third column is weighted entropy
    # x_input = Variable(Tensor(data[:, 3].reshape((-1, 1))))  # third column is linear entropy
    # x_input = Variable(Tensor([[1.0], [2.0], [3.0]]))
    # y_truth = Variable(Tensor([[2.0], [4.0], [6.0]]))

    model = LinearRegressionModel(1, 1)
    criterion = MSELoss()
    optimizer = SGD(model.parameters(), lr=0.001)
    for epoch in range(500):

        # Forward pass: Compute predicted y by passing
        # x to the model
        y_predicted = model(x_input)

        # Compute and print loss
        loss = criterion(y_predicted, y_truth)

        # Zero
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print('epoch {0}, loss {1}'.format(epoch, loss.data))


if __name__ == '__main__':
    train()
