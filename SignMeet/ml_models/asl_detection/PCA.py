import os
import cv2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Configuration
image_size = (32, 32)
patch_size = (7, 7)
num_filters = 4
block_size = (8, 8)
max_classes = 5
images_per_class = 10
max_patches_for_pca = 10000  # limit to avoid memory issues

def load_images(dataset_path):
    images = []
    labels = []
    label_names = sorted(os.listdir(dataset_path))[:max_classes]
    for label_idx, label_name in enumerate(label_names):
        label_path = os.path.join(dataset_path, label_name)
        if os.path.isdir(label_path):
            count = 0
            for file in os.listdir(label_path):
                if count >= images_per_class:
                    break
                img_path = os.path.join(label_path, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    img = cv2.resize(img, image_size)
                    images.append(img)
                    labels.append(label_idx)
                    count += 1
    return np.array(images), np.array(labels), label_names

def extract_patches(images, patch_size):
    patches = []
    for img in images:
        for i in range(0, img.shape[0] - patch_size[0] + 1, 4):
            for j in range(0, img.shape[1] - patch_size[1] + 1, 4):
                patch = img[i:i+patch_size[0], j:j+patch_size[1]]
                patches.append(patch.flatten())
    return np.array(patches)

def learn_pca_filters(patches, num_filters):
    if len(patches) > max_patches_for_pca:
        print(f"[INFO] Sampling {max_patches_for_pca} patches from {len(patches)} for PCA...")
        indices = np.random.choice(len(patches), max_patches_for_pca, replace=False)
        patches = patches[indices]
    pca = PCA(n_components=num_filters)
    pca.fit(patches)
    filters = pca.components_.reshape((num_filters, patch_size[0], patch_size[1]))
    return filters

def convolve_images(images, filters):
    feature_maps = []
    for img in images:
        maps = []
        for filt in filters:
            response = cv2.filter2D(img, -1, filt)
            maps.append(response)
        feature_maps.append(np.stack(maps, axis=0))
    return np.array(feature_maps)

def compute_histograms(feature_maps, block_size):
    histograms = []
    for maps in feature_maps:
        binary_maps = (maps > 0).astype(np.uint8)
        combined = np.zeros_like(binary_maps[0], dtype=np.uint8)
        for i, bm in enumerate(binary_maps):
            combined += bm << i
        h_blocks = combined.shape[0] // block_size[0]
        w_blocks = combined.shape[1] // block_size[1]
        hist = []
        for i in range(h_blocks):
            for j in range(w_blocks):
                block = combined[i*block_size[0]:(i+1)*block_size[0],
                                 j*block_size[1]:(j+1)*block_size[1]]
                h, _ = np.histogram(block, bins=2*num_filters, range=(0, 2*num_filters))
                hist.extend(h)
        histograms.append(hist)
    return np.array(histograms)

def main():
    dataset_path = 'C:\\DISHA\\sign\\archive (6)\\ASL_Alphabet_Dataset\\asl_alphabet_train'  # <-- Change this path if needed
    print("[INFO] Loading images...")
    images, labels, label_names = load_images(dataset_path)
    print(f"[INFO] Loaded {len(images)} images across {len(label_names)} classes.")

    print("[INFO] Extracting patches...")
    patches = extract_patches(images, patch_size)
    print(f"[INFO] Extracted {patches.shape[0]} patches.")

    print("[INFO] Learning PCA filters...")
    filters = learn_pca_filters(patches, num_filters)
    print("[INFO] Filters learned.")

    print("[INFO] Convolving images...")
    feature_maps = convolve_images(images, filters)
    print("[INFO] Convolution complete.")

    print("[INFO] Computing histograms...")
    histograms = compute_histograms(feature_maps, block_size)
    print("[INFO] Histogram encoding complete.")

    print("[INFO] Training classifier...")
    X_train, X_test, y_train, y_test = train_test_split(histograms, labels, test_size=0.2, random_state=42)
    clf = SVC()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("[INFO] Classification Results:")
    labels_all = list(range(len(label_names)))
    print(classification_report(y_test, y_pred, labels=labels_all, target_names=label_names, zero_division=0))

if __name__ == "__main__":
    main()