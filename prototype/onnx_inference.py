import onnxruntime
import os
import torch
from core import get_loader

DATA_ROOT = os.getenv('DATA_ROOT')


def main():
    onnx_model_path = "resnet50.onnx"

    # Load the ONNX model into ONNX Runtime
    ort_session = onnxruntime.InferenceSession(onnx_model_path)

    # Load dataset
    loader = get_loader(DATA_ROOT)

    # Run inference on ONNX model
    onnx_total, onnx_correct = 0, 0
    for idx, (inputs, targets) in enumerate(loader):
        ort_inputs = {ort_session.get_inputs()[0].name: inputs.numpy()}
        ort_outputs = ort_session.run(None, ort_inputs)

        _, predicted = torch.max(ort_outputs.data, 1)
        onnx_total += targets.size(0)
        onnx_correct += (predicted == targets).sum()

    print("ONNX model accuracy: %f" % (onnx_correct / onnx_total))


if __name__ == '__main__':
    main()
