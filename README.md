# Hybrid DeepTrace
### Explainable AI-Generated Image Detection

Hybrid DeepTrace is an educational machine-learning project that estimates whether an image is **real** or **AI-generated**. It combines a Convolutional Neural Network (CNN), traditional machine-learning classifiers, and Grad-CAM visual explanations in a Streamlit web application.

> **Important:** Predictions are estimates from trained models, not definitive proof of an image's origin.

## Features

- Dark, cyber-forensics-inspired Streamlit interface.
- PNG, JPG, and JPEG image upload and preview.
- CNN prediction (`REAL` or `FAKE`) with a confidence score.
- Grad-CAM visual explanation: original image, heatmap, and overlay.
- Comparison of CNN, Support Vector Machine (SVM), Random Forest, and XGBoost predictions.
- Consensus summary showing how many models predict each class.
- Temporary upload-file cleanup after analysis.

If JSON report export is present in your local `app.py`, that option can also be used to save analysis details.

## How it works

1. **Upload:** The user selects an image in the Streamlit interface.
2. **Preprocessing:** The image is loaded as RGB and resized to 32 × 32 pixels for the current CNN.
3. **CNN inference:** The trained CNN predicts `REAL` or `FAKE` and returns a confidence score.
4. **Explainability:** Grad-CAM produces a heatmap and overlay to show regions that influenced the CNN prediction.
5. **Traditional-model inference:** Handcrafted features are passed to the SVM, Random Forest, and XGBoost models. The SVM uses its saved scaler.
6. **Comparison:** The app presents the four predictions and their agreement or disagreement.

### Handcrafted features

The traditional-model pipeline uses 24 features:
- **Texture:** 10 Local Binary Pattern (LBP) histogram features
- **Frequency:** 2 Discrete Cosine Transform (DCT)-based features
- **Color:** 12 RGB-channel statistics

## Project structure

The application expects a structure similar to the following. Keep filenames consistent with your local source code.

```text
HybridDeepTrace/
├── app.py
├── README.md
├── requirements.txt
├── src/
│   ├── preprocessing.py
│   ├── feature_extraction.py
│   ├── predict.py
│   ├── gradcam.py
│   └── model_comparison.py
├── models/
│   ├── deeptrace_cnn.pth
│   ├── svm_model.pkl
│   ├── scaler.pkl
│   ├── random_forest_model.pkl
│   └── xgboost_model.pkl
├── dataset/
│   └── raw/CIFAKE/
├── notebooks/
└── results/
```

The dataset is needed to reproduce training or evaluation; inference requires the application source and compatible trained model files. Avoid committing large datasets or model files to a public repository without checking their size and redistribution terms.

## Dataset

The project uses **CIFAKE**, containing real and AI-generated images. Images in the current pipeline are handled as 32 × 32 RGB inputs.

The recorded evaluation used a balanced test set of 20,000 images: 10,000 `REAL` and 10,000 `FAKE`. Traditional models were trained using a balanced 2,000-image training subset, split into 1,600 training and 400 validation examples. The CNN was evaluated in the project's separate training workflow.

Obtain the dataset from an authorized source and follow its license and usage terms.

## Evaluation results

These are the results recorded for this experiment, not a guarantee of performance on unseen or real-world images.

| Model | Accuracy | Precision (FAKE) | Recall (FAKE) | F1-score (FAKE) |
|---|---:|---:|---:|---:|
| CNN | 88.78% | 88.06% | 89.73% | 88.89% |
| SVM | 85.88% | 87.59% | 83.61% | 85.55% |
| XGBoost | 84.86% | 85.72% | 83.65% | 84.67% |
| Random Forest | 83.70% | 84.15% | 83.03% | 83.59% |

`FAKE` is the positive class for precision, recall, and F1-score. Results depend on the dataset, preprocessing, and test distribution. External evaluation is needed before drawing broader conclusions.

## Requirements

- Python 3.10 or 3.11 recommended
- pip
- The trained model files expected by the source code
- Packages listed in [`requirements.txt`](requirements.txt)

The project can run on CPU. GPU acceleration is optional and requires a compatible PyTorch/CUDA installation.

## Setup and run

### 1. Open the project directory

If the project is hosted on GitHub:

```bash
git clone <your-repository-url>
cd HybridDeepTrace
```

Or open a terminal in your existing project folder.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Check required files

- `app.py` is in the project root.
- `src/` contains the modules imported by the application.
- `models/` contains the trained models and SVM scaler.
- `results/` exists or can be created by the Grad-CAM code.

Saved models must match the architecture and feature-extraction pipeline used by the source code.

### 5. Start the app

```bash
streamlit run app.py
```

Open the local URL printed in the terminal (usually `http://localhost:8501`).

## Using the application

1. Upload a PNG, JPG, or JPEG image.
2. Review the image preview.
3. Click **Analyze Image**.
4. Review the CNN prediction and confidence.
5. Inspect the original image, Grad-CAM heatmap, and overlay.
6. Compare CNN, SVM, Random Forest, and XGBoost predictions.
7. Read the consensus carefully when models disagree.

## Interpreting results responsibly

- `FAKE` means the model classified the image as AI-generated; it does not prove that it was generated by AI.
- `REAL` does not guarantee that an image is authentic or unedited.
- Confidence is not necessarily a calibrated probability of authenticity.
- Grad-CAM highlights regions that influenced the CNN prediction; it does not independently verify an image's origin.
- Model agreement is useful context, not a guarantee of correctness.
- Performance may differ on images from unfamiliar generators, compressed or edited images, or distributions unlike CIFAKE.

## Troubleshooting

**`ModuleNotFoundError`:** Activate the correct virtual environment and run `python -m pip install -r requirements.txt`.

**Model file not found:** Check the filenames and paths expected by your code under `models/`.

**Grad-CAM image missing:** Confirm that `src/gradcam.py` is compatible with the CNN architecture and that the `results/` directory is writable. Check the output path returned by the Grad-CAM function.

**Model-loading/version errors:** Pickled scikit-learn and XGBoost models may depend on package versions. Install compatible versions or retrain and save the models in the current environment.

## Technology stack

Python · Streamlit · PyTorch · Torchvision · NumPy · Pillow · Matplotlib · scikit-learn · scikit-image · SciPy · XGBoost · Joblib

## Limitations and future work

- Evaluate on external datasets and images from multiple generators.
- Add ROC-AUC, precision-recall curves, and per-class metrics.
- Calibrate confidence scores and document decision thresholds.
- Test robustness to compression, resizing, and common image edits.
- Record reproducible training settings and random seeds.
- Add automated tests for preprocessing, inference, and report generation.

## Disclaimer

Hybrid DeepTrace is an educational project. Do not use it as the sole basis for decisions involving identity, reputation, legal matters, journalism, or other high-impact contexts. Corroborate predictions with independent evidence.

## Project information

**Project:** Hybrid DeepTrace  
**Focus:** Image authenticity classification and explainable AI
