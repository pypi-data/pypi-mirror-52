import unittest
import keras
import onnx
import os

from .._utils import *
from winmltools.config import cfg
models_dir = os.path.dirname(os.path.abspath(__file__)) + '/../models'

class TestKeras(unittest.TestCase):
    def test_LSTM(self):
        model = keras.models.load_model(os.path.join(models_dir, 'keras', 'LSTM.keras'))
        for op_set in cfg.TO_TEST_OPSETS:
            result, _ = convert_model(model, 'keras-lstm', opset=op_set)
            result_path = os.path.join(temp_model_path, 'keras-lstm_opset' + str(op_set) + '.onnx')
            onnx.save_model(result, result_path)
            # TODO: Bug (7819) Failed to run this model with WinMLRunner
            # self.assertEqual(run_model(result_path), 0)

    def test_Conv2D(self):
        model = keras.models.load_model(os.path.join(models_dir, 'keras', 'Conv2D.keras'))
        for op_set in cfg.TO_TEST_OPSETS:
            result, _ = convert_model(model, 'keras-conv2d', opset=op_set)
            result_path = os.path.join(temp_model_path, 'keras-conv2d_opset' + str(op_set) + '.onnx')
            onnx.save_model(result, result_path)
            # TODO: Bug (7819) Failed to run this model with WinMLRunner
            # self.assertEqual(run_model(result_path), 0)

    def test_tanh(self):
        model = keras.models.load_model(os.path.join(models_dir, 'keras', 'tanh.keras'))
        for op_set in cfg.TO_TEST_OPSETS:
            result, _ = convert_model(model, 'keras-tanh', opset=op_set)
            result_path = os.path.join(temp_model_path, 'keras-tanh_opset' + str(op_set) + '.onnx')
            onnx.save_model(result, result_path)
            # TODO: Bug (7820) Failed to run this model with WinMLRunner
            # self.assertEqual(run_model(result_path), 0)
