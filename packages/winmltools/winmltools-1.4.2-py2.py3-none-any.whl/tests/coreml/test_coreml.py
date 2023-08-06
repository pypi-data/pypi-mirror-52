import unittest
import coremltools
import onnx
import os
from winmltools.config import cfg

from .._utils import *

models_dir = os.path.dirname(os.path.abspath(__file__)) + '/../models'

class TestKeras(unittest.TestCase):
    def test_LSTM(self):
        model = coremltools.models.MLModel(os.path.join(models_dir, 'coreml', 'LSTM.mlmodel'))
        for op_set in cfg.TO_TEST_OPSETS:
            result, _ = convert_model(model, 'coreml-lstm', opset=op_set)
            result_path = os.path.join(temp_model_path, 'coreml-lstm_opset' + str(op_set) + '.onnx')
            onnx.save_model(result, result_path)
            self.assertEqual(run_model(result_path), 0)

    def test_mnist(self):
        model = coremltools.models.MLModel(os.path.join(models_dir, 'coreml', 'mnist.mlmodel'))
        for op_set in cfg.TO_TEST_OPSETS:
            result, _ = convert_model(model, 'coreml-mnist', opset=op_set)
            result_path = os.path.join(temp_model_path, 'coreml-mnist' + str(op_set) + '.onnx')
            onnx.save_model(result, result_path)
            # TODO: Bug (7819) Failed to run this model with WinMLRunner
            self.assertEqual(run_model(result_path), 0)

    def test_simple_RNN(self):
        model = coremltools.models.MLModel(os.path.join(models_dir, 'coreml', 'SimpleRNN.mlmodel'))
        for op_set in cfg.TO_TEST_OPSETS:
            result, _ = convert_model(model, 'coreml-rnn', opset=op_set)
            result_path = os.path.join(temp_model_path, 'coreml-rnn_opset' + str(op_set) + '.onnx')
            onnx.save_model(result, result_path)
            # TODO: Bug (7820) Failed to run this model with WinMLRunner
            self.assertEqual(run_model(result_path), 0)