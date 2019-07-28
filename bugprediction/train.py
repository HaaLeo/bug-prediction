# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

from os import path
import json

import numpy as np
import matplotlib.pyplot as plt
from torch import Tensor, save, load
from torch.autograd import Variable
from torch.nn import MSELoss
from torch.optim import SGD
from linear_regression_model import LinearRegressionModel

# pylint: disable=too-many-statements,too-many-locals

def train():
    # Load data
    data_set_path = path.join(path.abspath(path.dirname(__file__)), '../resources/eclipse-data-set.csv')
    data = np.genfromtxt(data_set_path, delimiter=';', skip_header=1, usecols=[1, 2, 3, 4, 5, 6])
    np.random.shuffle(data)

    n_rows = data.shape[0]
    train_rows = int(n_rows*0.8)
    test_rows = int((n_rows - train_rows)/2)

    # x_input = Variable(Tensor(data[:, 3].reshape((-1, 1))))  # third column is linear entropy
    # x_input = Variable(Tensor([[1.0], [2.0], [3.0]]))
    # y_truth = Variable(Tensor([[2.0], [4.0], [6.0]]))

    epochs = 2001
    criterion = MSELoss()

    entropy_map = {
        1: 'full_not_decayed',
        2: 'weighted_not_decayed',
        3: 'full_linear_decayed',
        4: 'full_log_decayed',
        5: 'full_exp_decayed'
    }

    learing_rate_map = {
        1: (0.0000005, 0.000001),
        2: (0.0001, 0.005),
        3: (0.0001, 0.005),
        4: (0.0001, 0.005),
        5: (0.0001, 0.005)
    }
    for entropy_col, entropy_type in entropy_map.items():
        y_train = Variable(Tensor(data[:train_rows, 0].reshape((-1, 1))))  # first column is number of bugs
        x_train = Variable(Tensor(data[:train_rows, entropy_col].reshape((-1, 1))))  # third column is weighted entropy
        y_val = Variable(Tensor(data[train_rows+1:train_rows+test_rows, 0].reshape((-1, 1))))  # first column is number of bugs
        x_val = Variable(Tensor(data[train_rows+1:train_rows+test_rows, entropy_col].reshape((-1, 1))))  # third column is weighted entropy
        y_test = Variable(Tensor(data[train_rows+test_rows+1:, 0].reshape((-1, 1))))  # first column is number of bugs
        x_test = Variable(Tensor(data[train_rows+test_rows+1:, entropy_col].reshape((-1, 1))))  # third column is weighted entropy

        model_file_name = entropy_type + '_hcm'
        model_dir = path.normpath(path.join(path.abspath(path.dirname(__file__)), '../resources/models'))
        model_file_path = path.join(model_dir, model_file_name + '.pt')

        learing_rates = np.linspace(*learing_rate_map[entropy_col])

        # Try to load model
        old_model = LinearRegressionModel(1, 1)
        try:
            old_model.load_state_dict(load(model_file_path))
        except FileNotFoundError:
            print('File="{}" was not found. Create new model.'.format(model_file_path))
        y_test_pred_old = old_model(x_test)
        y_test_loss_old = criterion(y_test_pred_old, y_test)

        for learing_rate in learing_rates:
            train_loss_list = []
            val_loss_list = []
            test_loss_list = []

            print('Train for entropy type="{0}" and learning rate="{1}"'.format(entropy_type, learing_rate))
            model = LinearRegressionModel(1, 1)

            optimizer = SGD(model.parameters(), lr=learing_rate)
            for epoch in range(epochs):

                # Forward pass: Compute predicted y by passing
                # x to the model
                y_predicted = model(x_train)

                # Compute and print loss
                train_loss = criterion(y_predicted, y_train)
                train_loss_list.append(float(train_loss.data))

                # Val loss
                y_val_pred = model(x_val)
                val_loss = criterion(y_val_pred, y_val)
                val_loss_list.append(float(val_loss.data))

                # Zero
                optimizer.zero_grad()
                train_loss.backward()
                optimizer.step()

                y_test_pred = model(x_test)
                test_loss = criterion(y_test_pred, y_test)
                test_loss_list.append(float(test_loss.data))

                if epoch % 50 == 0:
                    print('epoch {0}, loss {1}'.format(epoch, train_loss.data))
                    if test_loss.data < y_test_loss_old.data:
                        print('Save model with prediction error {}.'.format(test_loss))
                        save(model.state_dict(), model_file_path)
                        meta_data = {
                            'history_complexity_metric': entropy_type,
                            'learning_rate': learing_rate,
                            'val_loss': val_loss_list,
                            'train_loss': train_loss_list,
                            'test_loss': test_loss_list
                        }

                        with open(path.join(model_dir, model_file_name + '_meta.json'), 'w') as write_file:
                            json.dump(meta_data, write_file, indent=4)

                        y_test_loss_old = test_loss

    # Compute and print loss
    test_loss = criterion(y_test_pred, y_test)
    print('Test loss {0}'.format(test_loss.data))

    train_plt, = plt.plot(range(epochs), train_loss_list, label='Train Loss')
    val_plt, = plt.plot(range(epochs), val_loss_list, label='Validation Loss')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Loss')
    plt.legend(handles=[train_plt, val_plt])
    plt.show()


if __name__ == '__main__':
    train()
