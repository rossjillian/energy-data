import torch
from core import get_loader
import os

DATA_ROOT = os.getenv('DATA_ROOT')


def main():
    # Load Torch model
    torch_model = torch.hub.load("pytorch/vision", "resnet50", weights="IMAGENET1K_V2")

    # Load dataset
    loader = get_loader(DATA_ROOT)

    # Export the PyTorch model to ONNX format
    example_input = next(iter(loader))[0]
    onnx_model_path = "resnet50.onnx"
    torch.onnx.export(torch_model, example_input, onnx_model_path)


if __name__ == '__main__':
    main()
