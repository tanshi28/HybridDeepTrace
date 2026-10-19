import streamlit as st

st.set_page_config(
    page_title="Hybrid DeepTrace",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 12% 18%, rgba(0, 210, 255, 0.13), transparent 38%),
        radial-gradient(ellipse at 88% 68%, rgba(125, 75, 255, 0.15), transparent 42%),
        radial-gradient(ellipse at 50% 110%, rgba(35, 77, 140, 0.12), transparent 45%),
        #070a12;
    color: #f2f5ff;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}

/* Subtle animated digital grid */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(91, 205, 255, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(91, 205, 255, 0.035) 1px, transparent 1px);
    background-size: 42px 42px;
    mask-image: linear-gradient(to bottom, black 0%, rgba(0,0,0,0.55) 55%, transparent 95%);
    animation: gridDrift 24s linear infinite;
}

/* Ambient scan line; kept faint so content remains readable */
.stApp::after {
    content: "";
    position: fixed;
    left: 0;
    right: 0;
    top: -20%;
    height: 22%;
    pointer-events: none;
    z-index: 0;
    background: linear-gradient(to bottom, transparent, rgba(74, 220, 255, 0.035), transparent);
    animation: ambientScan 12s linear infinite;
}

[data-testid="stAppViewContainer"] > .main,
[data-testid="stHeader"],
[data-testid="stBottom"] {
    position: relative;
    z-index: 1;
}

@keyframes gridDrift {
    from { background-position: 0 0, 0 0; }
    to { background-position: 0 42px, 42px 0; }
}

@keyframes ambientScan {
    from { transform: translateY(0); }
    to { transform: translateY(600%); }
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after,
    .status,
    .hero-title span {
        animation: none !important;
    }
}

.brand {
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 4px;
    color: #e8edff;
}

.brand span {
    color: #69e6ff;
    text-shadow: 0 0 18px rgba(105, 230, 255, 0.30);
}

.status {
    display: inline-block;
    margin-top: 70px;
    padding: 9px 16px;
    border: 1px solid rgba(105, 230, 255, 0.3);
    border-radius: 30px;
    background: rgba(105, 230, 255, 0.06);
    box-shadow: 0 0 24px rgba(0, 210, 255, 0.055), inset 0 0 16px rgba(0, 210, 255, 0.025);
    color: #69e6ff;
    font-size: 12px;
    letter-spacing: 2px;
    backdrop-filter: blur(10px);
    animation: badgeAppear 0.8s ease both;
}

@keyframes badgeAppear {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-title {
    margin-top: 25px;
    font-size: clamp(48px, 7vw, 82px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -4px;
    color: #f5f7ff;
}

.hero-title span {
    background: linear-gradient(90deg, #72e7ff, #a9a0ff, #72e7ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 6s ease infinite;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 100% center; }
}

.subtitle {
    margin-top: 22px;
    color: #a4adc4;
    font-size: 18px;
    line-height: 1.8;
}

.divider {
    height: 1px;
    margin-top: 48px;
    background: linear-gradient(90deg, transparent, #27344c, transparent);
}

.footer-note {
    margin-top: 35px;
    color: #65718b;
    font-size: 11px;
    letter-spacing: 1.5px;
}

/* Animated encryption ribbon: visible visual identity without covering controls. */
.encryption-ribbon {
    position: relative;
    height: 64px;
    margin: 24px 0 2px;
    overflow: hidden;
    border: 1px solid rgba(105, 230, 255, .18);
    border-radius: 12px;
    background: linear-gradient(90deg, rgba(8,17,32,.94), rgba(18,15,43,.82), rgba(8,17,32,.94));
    box-shadow: inset 0 0 28px rgba(105,230,255,.045), 0 8px 28px rgba(0,0,0,.12);
}
.encryption-ribbon:before, .encryption-ribbon:after {
    content: "0101  A7F3  //  0xDE  110010  CIPHER  01AF  //  10110  0x7C  ENCRYPT  1101  0xA9  //  HASH  010101";
    position: absolute; left: 0; white-space: nowrap; width: max-content;
    color: rgba(105,230,255,.62); font: 12px/1.2 monospace; letter-spacing: 5px;
    text-shadow: 0 0 9px rgba(105,230,255,.32);
    animation: cipherFlow 22s linear infinite;
}
.encryption-ribbon:before { top: 14px; }
.encryption-ribbon:after {
    top: 37px; color: rgba(169,160,255,.58); letter-spacing: 7px;
    animation: cipherFlowReverse 28s linear infinite;
}
.encryption-caption {
    position: absolute; right: 12px; bottom: 5px; z-index: 2;
    color: #7785a3; font: 8px/1.2 monospace; letter-spacing: 2px;
    background: rgba(7,10,18,.75); padding: 2px 5px; border-radius: 3px;
}
@keyframes cipherFlow { from { transform: translateX(0); } to { transform: translateX(-35%); } }
@keyframes cipherFlowReverse { from { transform: translateX(-22%); } to { transform: translateX(0); } }

/* Consistent glass panels and responsive layout. */
[data-testid="stMetric"], [data-testid="stAlert"] { border-radius: 14px; }
[data-testid="stImage"] img { border: 1px solid rgba(105,230,255,.12); }
[data-testid="stFileUploaderDropzone"] { background: rgba(9,15,28,.55); }
.stCaption, [data-testid="stCaptionContainer"] { color: #8d9ab4; }
@media (max-width: 700px) {
    .block-container { padding-top: 1rem; }
    .status { margin-top: 38px; font-size: 10px; letter-spacing: 1px; }
    .hero-title { letter-spacing: -2px; }
    .subtitle { font-size: 15px; }
    .encryption-ribbon { height: 54px; }
}
@media (prefers-reduced-motion: reduce) {
    .encryption-ribbon:before, .encryption-ribbon:after { animation: none !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="brand">HYBRID <span>DEEPTRACE</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="encryption-ribbon" aria-hidden="true"><div class="encryption-caption">SIGNAL STREAM // LIVE VISUAL</div></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status">● &nbsp; AI-POWERED IMAGE AUTHENTICITY ANALYSIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">Let\'s <span>detect.</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Is it real, or is it artificially generated?<br>
        Explore image authenticity with machine learning and explainable AI.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">IMAGE ANALYSIS &nbsp; · &nbsp; CNN CLASSIFICATION &nbsp; · &nbsp; GRAD-CAM EXPLANATIONS</div>',
    unsafe_allow_html=True
)
st.markdown("""
<style>
.upload-heading {
    margin-top: 55px;
    margin-bottom: 8px;
    color: #edf1ff;
    font-size: 25px;
    font-weight: 700;
}

.upload-description {
    margin-bottom: 25px;
    color: #8995b0;
    font-size: 14px;
}

div[data-testid="stFileUploader"] {
    padding: 22px;
    border: 1px solid rgba(105, 230, 255, 0.25);
    border-radius: 18px;
    background: rgba(15, 22, 39, 0.75);
    backdrop-filter: blur(12px);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.16), inset 0 0 24px rgba(105, 230, 255, 0.018);
    transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
}

div[data-testid="stFileUploader"]:hover {
    border-color: rgba(105, 230, 255, 0.75);
    box-shadow: 0 0 26px rgba(105, 230, 255, 0.08), 0 12px 35px rgba(0, 0, 0, 0.16);
    transform: translateY(-1px);
}

div[data-testid="stFileUploader"] section {
    background: transparent;
}

div[data-testid="stFileUploader"] button {
    border: 1px solid #69e6ff;
    border-radius: 9px;
    color: #69e6ff;
    background: rgba(105, 230, 255, 0.07);
}

div[data-testid="stFileUploader"] button:hover {
    border-color: #a9a0ff;
    color: #a9a0ff;
}

div.stButton > button {
    width: 100%;
    height: 52px;
    margin-top: 15px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(90deg, #69dff7, #a49aff);
    color: #080b14;
    font-size: 15px;
    font-weight: 800;
    transition: 0.3s ease;
}

div.stButton > button:hover {
    box-shadow: 0 0 25px rgba(105, 230, 255, 0.25);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="upload-heading">Begin your analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="upload-description">'
    'Upload an image to examine its authenticity using Hybrid DeepTrace.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Drop an image here or browse your files",
    type=["png", "jpg", "jpeg"],
    help="Supported formats: PNG, JPG and JPEG"
)

if uploaded_file is not None:
    from PIL import Image

    try:
        image = Image.open(uploaded_file).convert("RGB")
    except Exception:
        st.error("This file could not be opened as an image. Please upload a valid PNG or JPG file.")
        st.stop()

    preview_col, details_col = st.columns([1, 1.4], gap="large")
    with preview_col:
        st.image(image, caption="Image selected for analysis", use_container_width=True)
    with details_col:
        st.markdown("### Input details")
        st.markdown(f"**Filename:** `{uploaded_file.name}`")
        st.markdown(f"**Dimensions:** `{image.width} × {image.height}` pixels")
        st.markdown(f"**Format:** `{uploaded_file.type or 'Image'}`")
        st.markdown("**Processing:** RGB conversion → 32 × 32 CNN input")
        st.caption("The model uses a resized copy for inference; the original upload is not modified.")

    if st.button("🔍  Analyze Image", use_container_width=True):
        import tempfile
        import time
        from pathlib import Path
        from src.predict import predict_image
        from src.gradcam import generate_gradcam
        from src.model_comparison import compare_models

        temp_path = None
        try:
            # Save uploaded bytes to a temporary file for the model functions.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            progress_text = st.empty()
            progress_bar = st.progress(0)
            scan_animation = st.empty()

            scan_animation.markdown("""
            <style>
            .scan-container {
                position: relative; width: 100%; height: 180px; margin: 20px 0;
                overflow: hidden; border: 1px solid rgba(105,230,255,.35);
                border-radius: 16px;
                background: radial-gradient(circle at center, rgba(40,100,170,.20), transparent 65%), #0b1020;
            }
            .scan-grid {
                position: absolute; inset: 0;
                background-image: linear-gradient(rgba(105,230,255,.06) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(105,230,255,.06) 1px, transparent 1px);
                background-size: 24px 24px;
            }
            .scan-line {
                position: absolute; width: 100%; height: 2px; background: #69e6ff;
                box-shadow: 0 0 12px #69e6ff, 0 0 30px #69e6ff;
                animation: deeptrace-scan 2s linear infinite;
            }
            .scan-label {
                position: absolute; bottom: 16px; left: 18px; color: #69e6ff;
                font-family: monospace; font-size: 12px; letter-spacing: 2px;
            }
            @keyframes deeptrace-scan { 0% { top: 0; } 100% { top: 100%; } }
            </style>
            <div class="scan-container">
                <div class="scan-grid"></div><div class="scan-line"></div>
                <div class="scan-label">DEEPTRACE // IMAGE ANALYSIS IN PROGRESS</div>
            </div>
            """, unsafe_allow_html=True)

            progress_text.markdown("🔄 Preparing image...")
            progress_bar.progress(15)

            prediction, confidence = predict_image(temp_path)

            progress_text.markdown("🧠 CNN classification complete...")
            progress_bar.progress(45)

            explanation_prediction, explanation_confidence, output_path = generate_gradcam(temp_path)
            output_path = Path(output_path).resolve()

            progress_text.markdown("🔬 Generating visual explanation...")
            progress_bar.progress(75)

            with st.spinner("Comparing traditional machine-learning models..."):
                traditional_results = compare_models(temp_path)

            progress_bar.progress(100)
            time.sleep(0.35)
            scan_animation.empty()
            progress_text.empty()
            progress_bar.empty()

            st.markdown("---")
            st.markdown("## Analysis Report")
            if prediction == "FAKE":
                st.error("⚠️ AI-GENERATED IMAGE DETECTED")
            else:
                st.success("✅ IMAGE CLASSIFIED AS REAL")

            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Prediction", prediction)
            with metric_col2:
                st.metric("Model Confidence", f"{confidence:.2f}%")

            st.caption("Model: Hybrid DeepTrace CNN | Input resized to 32 × 32 pixels")
            st.info("Interpret this result as a model prediction, not a definitive authenticity verdict. Compression, resizing, image style and data-domain differences can affect performance.")

            st.markdown("""
            <style>
            .visual-heading { font-size: 24px; font-weight: 750; color: #eef2ff; margin-top: 38px; margin-bottom: 8px; }
            .visual-description { color: #929db5; font-size: 13px; margin-bottom: 20px; }
            .visual-card { padding: 15px; border: 1px solid rgba(105,230,255,.20); border-radius: 14px; background: rgba(17,25,43,.75); margin-bottom: 12px; }
            .visual-card-title { color: #69e6ff; font-size: 14px; font-weight: 700; letter-spacing: 1px; margin-bottom: 6px; }
            .visual-card-description { color: #929db5; font-size: 12px; line-height: 1.6; }
            div[data-testid="stImage"] img { border-radius: 12px; }
            div[data-testid="stMetric"] { background: rgba(19,29,49,.75); border: 1px solid rgba(105,230,255,.18); padding: 20px; border-radius: 14px; }
            </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="visual-heading">Visual Intelligence</div>', unsafe_allow_html=True)
            st.markdown('<div class="visual-description">Explore the image regions that influenced the model prediction.</div>', unsafe_allow_html=True)

            if output_path.is_file():
                from PIL import Image as PILImage
                with PILImage.open(output_path) as saved_figure:
                    figure = saved_figure.convert("RGB")
                    width, height = figure.size
                    # Grad-CAM creates a horizontal three-panel matplotlib figure.
                    panel_width = width // 3
                    original_panel = figure.crop((0, 0, panel_width, height))
                    heatmap_panel = figure.crop((panel_width, 0, panel_width * 2, height))
                    overlay_panel = figure.crop((panel_width * 2, 0, width, height))

                panel_columns = st.columns(3)
                panel_info = [
                    ("01 / ORIGINAL", "The uploaded image used for analysis.", original_panel),
                    ("02 / HEATMAP", "Highlights regions contributing to the CNN prediction.", heatmap_panel),
                    ("03 / OVERLAY", "Combines the original image with the attention heatmap.", overlay_panel),
                ]
                for column, (title, description, panel) in zip(panel_columns, panel_info):
                    with column:
                        st.markdown(
                            f'<div class="visual-card"><div class="visual-card-title">{title}</div>'
                            f'<div class="visual-card-description">{description}</div></div>',
                            unsafe_allow_html=True,
                        )
                        st.image(panel, use_container_width=True)
            else:
                st.warning(f"Grad-CAM visualization was not created at: {output_path}")
                st.caption("Check the results folder and the path returned by generate_gradcam().")

            st.caption("Grad-CAM highlights image regions that influenced the CNN prediction. It does not independently prove that an image is real or AI-generated.")

            st.markdown("---")
            st.markdown("## Multi-Model Analysis")
            st.caption("Compare the CNN with three traditional machine-learning models.")
            comparison_results = {"CNN": prediction, **traditional_results}

            model_columns = st.columns(4)
            for column, (model_name, model_prediction) in zip(model_columns, comparison_results.items()):
                with column:
                    st.markdown(f"### {model_name}")
                    if model_prediction == "FAKE":
                        st.error("🤖 AI-GENERATED")
                    else:
                        st.success("✅ REAL")

            real_votes = sum(value == "REAL" for value in comparison_results.values())
            fake_votes = sum(value == "FAKE" for value in comparison_results.values())
            st.markdown("### Prediction Consensus")
            vote_col1, vote_col2 = st.columns(2)
            with vote_col1:
                st.metric("REAL predictions", f"{real_votes}/4")
            with vote_col2:
                st.metric("FAKE predictions", f"{fake_votes}/4")

            if real_votes > fake_votes:
                st.success(f"{real_votes} out of 4 models classified this image as REAL. This does not guarantee authenticity.")
            elif fake_votes > real_votes:
                st.warning(f"{fake_votes} out of 4 models classified this image as FAKE. This does not guarantee the image is AI-generated.")
            else:
                st.warning("The models are evenly split. Their predictions disagree.")

            # Export a compact, reproducible summary of this inference session.
            import json
            from datetime import datetime, timezone
            report = {
                "project": "Hybrid DeepTrace",
                "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "input": {
                    "filename": uploaded_file.name,
                    "format": uploaded_file.type,
                    "width_pixels": image.width,
                    "height_pixels": image.height,
                    "model_input_size": "32x32 RGB"
                },
                "cnn_prediction": prediction,
                "cnn_confidence_percent": round(float(confidence), 2),
                "model_predictions": comparison_results,
                "consensus": {"REAL_votes": real_votes, "FAKE_votes": fake_votes},
                "interpretation_note": "Predictions are model outputs, not proof of authenticity. CNN confidence is not a calibrated probability.",
                "explainability_note": "Grad-CAM highlights regions that influenced the CNN prediction; it does not prove authenticity."
            }
            st.download_button(
                "⬇️ Download Analysis Report (JSON)",
                data=json.dumps(report, indent=2),
                file_name="hybrid_deeptrace_analysis.json",
                mime="application/json",
                use_container_width=True
            )

            with st.expander("How to read this report"):
                st.markdown(
                    "- **CNN prediction:** output of the trained convolutional neural network.\n"
                    "- **Confidence:** the model's reported score; it may not be calibrated.\n"
                    "- **Model comparison:** independent predictions from the CNN, SVM, Random Forest and XGBoost.\n"
                    "- **Consensus:** a simple vote count, not a separately validated ensemble model.\n"
                    "- **Grad-CAM:** a visual explanation of regions influencing the CNN, not a manipulation detector by itself."
                )

            st.markdown("---")
            st.caption("HYBRID DEEPTRACE · IMAGE AUTHENTICITY ANALYSIS · RESEARCH PROTOTYPE")

        except Exception as error:
            st.error("Analysis could not be completed.")
            st.code(f"{type(error).__name__}: {error}", language="text")
            st.info("Verify that the trained model files exist, dependencies are installed, and the project is launched from the HybridDeepTrace root folder.")
        finally:
            if temp_path and Path(temp_path).exists():
                Path(temp_path).unlink(missing_ok=True)
