from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "deeptrace_cnn.pth"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DeepTraceCNN(nn.Module):
    def __init__(self):
        super(DeepTraceCNN, self).__init__()

        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(128 * 4 * 4, 128)
        self.fc2 = nn.Linear(128, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))

        x = torch.flatten(x, 1)

        print("Flattened feature shape:", x.shape)
        print("Expected fc1 input:", self.fc1.in_features)

        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x


model = DeepTraceCNN().to(DEVICE)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True)
)

model.eval()

transform = transforms.ToTensor()


def predict_image(image_path):
    image = Image.open(image_path).convert("RGB").resize((32, 32))
    image_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)

    predicted_index = probabilities.argmax(dim=1).item()

    class_names = ["FAKE", "REAL"]
    prediction = class_names[predicted_index]
    confidence = probabilities[0, predicted_index].item() * 100

    return prediction, confidence


if __name__ == "__main__":
    from gradcam import generate_gradcam

    image_path = input("Enter the image path: ").strip().strip('"')

    prediction, confidence = predict_image(image_path)

    print("\n--- Hybrid DeepTrace Results ---")
    print("Prediction:", prediction)
    print(f"Confidence: {confidence:.2f}%")

    explanation_prediction, explanation_confidence, output_path = (
        generate_gradcam(image_path)
    )

    print("\n--- Explainable AI Results ---")
    print("Grad-CAM prediction:", explanation_prediction)
    print(f"Grad-CAM confidence: {explanation_confidence:.2f}%")
    print("Visualization saved to:", output_path)