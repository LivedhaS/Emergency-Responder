import streamlit as st
import numpy as np
import tensorflow as tf
import pymongo
import gridfs
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

# Must be first Streamlit command
st.set_page_config(page_title="Burn Classifier", page_icon="🔥")

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["burn_classification_db"]
fs = gridfs.GridFS(db)

# Load the trained model
@st.cache_resource
def load_burn_model():
    return tf.keras.models.load_model("burn_classification.keras")

model = load_burn_model()
CLASS_NAMES = ["Mild Burn", "Moderate Burn", "Severe Burn"]

# Treatment info with local video paths
def get_treatment_recommendation(burn_degree):
    recommendations = {
        "Mild Burn": {
            "text": """- Cool the burn with cool water for 10-15 minutes.
- Apply aloe vera or moisturizing lotion.
- Use pain relievers like ibuprofen.
- Cover with a sterile bandage.""",
            "video": "videos/first.mp4"
        },
        "Moderate Burn": {
            "text": """- Cool with water for at least 10 minutes.
- Do not pop blisters.
- Apply antibiotic ointment & bandage.
- Take pain relievers.""",
            "video": "videos/second.mp4"
        },
        "Severe Burn": {
            "text": """- Call emergency services immediately.
- Do not remove clothing stuck to the burn.
- Cover with a clean cloth.
- Elevate burn if possible.""",
            "video": "https://www.youtube.com/embed/TzAziq6TxG8"
        }
    }
    return recommendations.get(burn_degree, {"text": "Please consult a doctor.", "video": None})

# Streamlit UI
st.title("🔥 Burn Classification AI Assistant")
st.write("Upload an image of a burn injury to classify its severity and get treatment advice.")

uploaded_file = st.file_uploader("📷 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Convert image to binary
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_binary = img_byte_arr.getvalue()

    if model:
        # Preprocess image
        img_resized = img.resize((224, 224))
        img_array = image.img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Prediction
        prediction = model.predict(img_array)
        predicted_class = CLASS_NAMES[np.argmax(prediction)]
        confidence = np.max(prediction) * 100

        # Display Results
        st.subheader(f"🩺 Prediction: {predicted_class}")
        st.write(f"🔍 Confidence: **{confidence:.2f}%**")

        treatment_info = get_treatment_recommendation(predicted_class)
        st.markdown("### 💊 Treatment Recommendation:")
        st.write(treatment_info["text"])
        
        if predicted_class == "Severe Burn":
            st.markdown(
                """
                <div style="
                    border: 2px solid red; 
                    border-radius: 10px; 
                    padding: 20px; 
                    background-color: #ffe6e6; 
                    color: red; 
                    text-align: center;
                ">
                    <h2>🚨 SEEK IMMEDIATE MEDICAL CARE 🚨</h2>
                </div>
                <div style="margin-bottom: 20px;"></div>
                """,
                unsafe_allow_html=True
            )
        # Display local video
        elif treatment_info["video"]:
            st.markdown("### 🎥 Watch Treatment Video:")
            with open(treatment_info["video"], "rb") as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)

        # Save to GridFS & MongoDB
        image_id = fs.put(img_binary, filename=uploaded_file.name)
        db.history.insert_one({
            "userId": None,  # Add actual user ID if authenticated
            "imageUrl": str(image_id),
            "confidence": float(confidence),
            "severity": predicted_class
        })

        st.success("✅ Image and prediction saved successfully!")
    else:
        st.error("❌ Model not loaded. Please check the model path.")
