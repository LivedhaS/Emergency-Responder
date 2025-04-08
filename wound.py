import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load the model
MODEL_PATH = "C:/Users/slive/OneDrive/Desktop/burn/wound_classification_mobilenetv2.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Class labels
class_labels = ["Abrasions", "Bruises", "Burns", "Cut", "Ingrown nails", "Laceration", "Stab wound"]
IMG_SIZE = (224, 224)

# Treatment recommendations dictionary
treatment_guidelines = {
    "Abrasions": """
    - Clean the wound gently with water.
    - Apply antiseptic ointment.
    - Cover with a clean, non-stick bandage.
    - Monitor for signs of infection (redness, swelling, pus).
    """,

    "Bruises": """
    - Apply a cold compress or ice pack for 10–20 minutes.
    - Elevate the bruised area if possible.
    - Rest the area and avoid further trauma.
    - Pain relievers like paracetamol can help.
    """,

    "Burns": """
    - Cool the burn under running water for at least 10 minutes.
    - Do not apply ice or toothpaste.
    - Cover with a sterile, non-stick dressing.
    - Seek medical help for large, blistered, or deep burns.
    """,

    "Cut": """
    - Stop the bleeding by applying gentle pressure with a clean cloth.
    - Clean the cut with water.
    - Apply an antiseptic and cover with a sterile bandage.
    - Watch for signs of infection.
    """,

    "Ingrown nails": """
    - Soak the foot or hand in warm water for 15–20 minutes.
    - Gently lift the edge of the nail and place clean cotton underneath.
    - Avoid tight shoes or trauma.
    - Seek medical help if it becomes infected or doesn't improve.
    """,

    "Laceration": """
    - Apply direct pressure to stop bleeding.
    - Rinse the wound gently with clean water.
    - Apply an antibiotic ointment.
    - Use sterile bandage or dressing.
    - For deep lacerations, seek medical attention (may need stitches).
    """,

    "Stab wound": """
    - Do NOT remove the object if still embedded.
    - Apply pressure around the wound to stop bleeding.
    - Call emergency services immediately.
    - Keep the person still and calm.
    - Cover the wound with a sterile dressing or clean cloth.
    """
}

# Preprocessing function
def preprocess_image(image):
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Streamlit UI
st.set_page_config(page_title="Wound Classification", page_icon="🩹", layout="centered")
st.title("🩺 Wound Classification Model")

st.markdown(
    """
    Upload an image of a wound and the model will classify it into one of the following categories:
    **Abrasions, Bruises, Burns, Cut, Ingrown nails, Laceration, Stab wound**.
    """
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Predict
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        predicted_class = class_labels[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        # Display result
        st.success(f"✅ **Prediction:** {predicted_class}")
        st.info(f"🧠 **Confidence:** {confidence * 100:.2f}%")

        # Display treatment recommendation
        st.subheader("🩹 First Aid / Treatment Recommendation:")
        st.markdown(treatment_guidelines.get(predicted_class, "No recommendation available."))

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
