"""
VisionModule: Модуль компьютерного зрения для AI-бейбика.
Позволяет распознавать объекты и эмоции на изображениях.
"""
import cv2
import torch
import torchvision.transforms as T
from torchvision.models import resnet18
from typing import List, Tuple

class VisionModule:
    def __init__(self, device: str = 'cpu'):
        self.device = device
        self.model = resnet18(pretrained=True).to(device)
        self.model.eval()
        self.transform = T.Compose([
            T.ToPILImage(),
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        # Классы ImageNet (1000 классов)
        with open('imagenet_classes.txt', 'r', encoding='utf-8') as f:
            self.class_names = [line.strip() for line in f.readlines()]

    def predict(self, image_bgr) -> Tuple[str, float]:
        """
        Получить топ-1 предсказание для изображения (BGR, как из cv2.imread).
        """
        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            logits = self.model(input_tensor)
            probs = torch.nn.functional.softmax(logits, dim=1)
            conf, idx = torch.max(probs, 1)
        return self.class_names[idx.item()], conf.item()

    def extract_features(self, image_bgr) -> torch.Tensor:
        """
        Получить эмбеддинги (признаки) изображения для дальнейшей интеграции с мозгом.
        """
        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            features = self.model.avgpool(self.model.layer4(self.model.layer3(self.model.layer2(self.model.layer1(self.model.relu(self.model.bn1(self.model.conv1(input_tensor))))))))
        return features.squeeze()
