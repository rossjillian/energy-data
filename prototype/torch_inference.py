import torch
import os

from core import get_loader

DATA_ROOT = os.getenv('DATA_ROOT')


def main():
    # Load Torch model
    torch_model = torch.hub.load("pytorch/vision", "resnet50", weights="IMAGENET1K_V2")
    torch_model.eval()

    # Load dataset
    loader = get_loader(DATA_ROOT)

    # Run inference on Torch model
    torch_total, torch_correct = 0, 0
    with torch.no_grad():
        for idx, (inputs, targets) in enumerate(loader):
            inputs = inputs.cuda()
            targets = targets.cuda()

            outputs = torch_model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            torch_total += targets.size(0)
            torch_correct += (predicted == targets).sum()

    print("Torch model accuracy: %f" % (torch_correct / torch_total))


if __name__ == '__main__':
    main()
