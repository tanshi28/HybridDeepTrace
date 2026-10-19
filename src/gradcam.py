from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from torchvision import transforms

try:
    from .predict import model, DEVICE
except ImportError:
    from predict import model, DEVICE


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def generate_gradcam(image_path):
    # The CNN was trained on 32x32 RGB images, so use the same input size here.
    image = Image.open(image_path).convert("RGB").resize((32, 32))
    image_tensor = transforms.ToTensor()(image).unsqueeze(0).to(DEVICE)

    activations = None
    gradients = None

    def forward_hook(module, inputs, output):
        nonlocal activations
        activations = output

    def backward_hook(module, grad_input, grad_output):
        nonlocal gradients
        gradients = grad_output[0]

    forward_handle = model.conv3.register_forward_hook(forward_hook)
    backward_handle = model.conv3.register_full_backward_hook(backward_hook)

    try:
        model.eval()
        model.zero_grad(set_to_none=True)

        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_index = output.argmax(dim=1).item()
        output[0, predicted_index].backward()

        if activations is None or gradients is None:
            raise RuntimeError("Grad-CAM could not capture CNN activations or gradients.")

        weights = gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * activations).sum(dim=1, keepdim=True)
        cam = F.relu(cam)
        cam = F.interpolate(
            cam,
            size=(image.height, image.width),
            mode="bilinear",
            align_corners=False,
        )

        cam = cam.squeeze().detach().cpu().numpy()
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)

        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = RESULTS_DIR / "gradcam_prediction.png"

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        axes[0].imshow(image)
        axes[0].set_title("Original Image")
        axes[0].axis("off")

        axes[1].imshow(cam, cmap="jet")
        axes[1].set_title("Grad-CAM Heatmap")
        axes[1].axis("off")

        axes[2].imshow(image)
        axes[2].imshow(cam, cmap="jet", alpha=0.4)
        axes[2].set_title("Explanation Overlay")
        axes[2].axis("off")

        fig.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        class_names = ["FAKE", "REAL"]
        prediction = class_names[predicted_index]
        confidence = probabilities[0, predicted_index].item() * 100

        return prediction, confidence, output_path

    finally:
        forward_handle.remove()
        backward_handle.remove()
        model.zero_grad(set_to_none=True)
