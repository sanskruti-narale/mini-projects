import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, ConfusionMatrixDisplay

DATASET_DIR = "dataset"
IMG_SIZE = (128, 128)  

def crop_and_preprocess_signature(img_path):
    """
    Loads an image, strips excess white borders dynamically using bounding box 
    extraction, converts to binary inverted matrix, and flattens it for the ML model.
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    
    _, thresh_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    pixel_coordinates = np.argwhere(thresh_img > 0)
    
    if len(pixel_coordinates) == 0:
        resized_img = cv2.resize(thresh_img, IMG_SIZE)
    else:
        y_min, x_min = pixel_coordinates.min(axis=0)
        y_max, x_max = pixel_coordinates.max(axis=0)
        
        padding = 10
        h, w = img.shape
        y_min = max(0, y_min - padding)
        x_min = max(0, x_min - padding)
        y_max = min(h, y_max + padding)
        x_max = min(w, x_max + padding)
        
        cropped_img = thresh_img[y_min:y_max, x_min:x_max]
        resized_img = cv2.resize(cropped_img, IMG_SIZE)
    
    feature_vector = resized_img.flatten() / 255.0
    return feature_vector


# ==========================================
# STEP 1: DATASET GENERATION & LOADING
# ==========================================
print("[*] Accessing custom student dataset and preprocessing images...")
X = []  
y = []  

if not os.path.exists(DATASET_DIR):
    print(f"[!] Error: System folder '{DATASET_DIR}' not found. Please populate your dataset directories.")
    exit()

for student_name in os.listdir(DATASET_DIR):
    student_folder = os.path.join(DATASET_DIR, student_name)
    
    if os.path.isdir(student_folder):
        for img_name in os.listdir(student_folder):
            img_path = os.path.join(student_folder, img_name)
            
            features = crop_and_preprocess_signature(img_path)
            
            if features is not None:
                X.append(features)
                y.append(student_name)

X = np.array(X)
y = np.array(y)

unique_classes = sorted(list(np.unique(y)))
print(f"[+] Successfully loaded {len(X)} samples representing {len(unique_classes)} distinct students.")


# ==========================================
# STEP 2: TRAIN-TEST SPLIT
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# ==========================================
# STEP 3: CLASSIFIER MODEL TRAINING
# ==========================================
print("[*] Bootstrapping Support Vector Machine (SVM) Classifier Pipeline...")
# Utilizing a linear kernel for computational speed on structured flat pixel spaces
model = SVC(kernel='linear', C=1.0, probability=True, random_state=42)
model.fit(X_train, y_train)
print("[+] Model optimization routines complete!")


# ==========================================
# STEP 4: METRICS EVALUATION & PLOTTING
# ==========================================
y_pred = model.predict(X_test)

print("\n" + "="*30)
print("       EVALUATION SUMMARY       ")
print("="*30)
print(f"Global Classification Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print("Detailed Analytical Breakdown:\n", classification_report(y_test, y_pred))

print("[*] Rendering performance visualization charts...")
cm = confusion_matrix(y_test, y_pred, labels=unique_classes)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=unique_classes)

fig, ax = plt.subplots(figsize=(8, 6))
disp.plot(cmap=plt.cm.Blues, ax=ax, xticks_rotation=45)
plt.title("Signature Identification Confusion Matrix")
plt.tight_layout()
plt.show()


# ==========================================
# STEP 5: PREDICTION UTILITY (INFERENCE ENGINE)
# ==========================================
def identify_unknown_signature(test_image_path):
    """
    Accepts a single raw image file path, processes it, and predicts the 
    matching student name with classification confidence scores.
    """
    print(f"\n[*] Evaluating query signature input: {test_image_path}")
    features = crop_and_preprocess_signature(test_image_path)
    
    if features is None:
        print("[!] Execution Failure: Unable to locate or decode target file path.")
        return
    
    features = features.reshape(1, -1)
    
    predicted_label = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    class_index = list(model.classes_).index(predicted_label)
    confidence_score = probabilities[class_index] * 100
    
    print(f"➡ RESULT: Signature identified as belonging to **{predicted_label}**")
    print(f"➡ CONFIDENCE LEVEL: {confidence_score:.2f}%")

identify_unknown_signature("unseen_student_signature.jpeg")
