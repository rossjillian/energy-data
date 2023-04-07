from torchvision import datasets, transforms
import os
import torch


def get_loader(data_root):
    # Load dataset
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    transform = transforms.Compose([
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize
    ])
    dataset = datasets.ImageFolder(os.path.join(data_root, 'test'), transform=transform)
    loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=1,
        shuffle=False
    )
    return loader

