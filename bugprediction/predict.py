# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

from os import path
import logging

from torch import Tensor, load
from torch.autograd import Variable
import numpy as np

from .linear_regression_model import LinearRegressionModel

LOGGER = logging.getLogger(__name__)

def predict(hcm_map, **kwargs):
    try:
        model = _load_model(**kwargs)
    except FileNotFoundError:
        LOGGER.warn('No model is available for parameter="%s"', kwargs)
    np_list = np.array(list(hcm_map.values())).reshape((-1, 1))
    x_input = Variable(Tensor(np_list))

    predigtion = model.forward(x_input)

    return dict(zip(hcm_map.keys(), predigtion.flatten().tolist()))

def _load_model(**kwargs):
    model = LinearRegressionModel(1, 1)
    model_dir = path.normpath(path.join(path.abspath(path.dirname(__file__)), '../resources/models'))
    model_name = ''
    if kwargs['contribution'] == 'full':
        model_name += 'full'
    elif kwargs['contribution'] == 'percentage':
        model_name += 'weighted'
    else:
        pass

    # Currently only exp decay possible
    if kwargs['decay']:
        model_name += '_exp_decayed_hcm.pt'
    else:
        model_name += '_not_decayed_hcm.pt'

    model_path = path.join(model_dir, model_name)
    model.load_state_dict(load(model_path))

    return model
