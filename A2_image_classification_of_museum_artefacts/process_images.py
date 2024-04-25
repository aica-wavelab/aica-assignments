# Import MobileNetV1
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
from keras.models import Model
from keras.layers import GlobalAveragePooling2D
from keras.preprocessing import image
from keras.applications.mobilenet import decode_predictions
import numpy as np

import pandas as pd

# Metadata data path
df = pd.read_csv("./MAMe_metadata/MAMe_dataset.csv")

# Image data path
data_path = "./data_256"

model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3), alpha=1.0, pooling="max", classes=1000)

# Extract features in the most efficient way possible (i.e. without using a for loop but batching the images)
def extract_features(df, model, batch_size=1024*(2**3)):
    features = []
    for i in range(0, len(df), batch_size):
        images = []
        for j in range(i, min(i + batch_size, len(df))):
            img = image.load_img(data_path + "/" + df["Image file"][j], target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)
            images.append(img)
        images = np.vstack(images)
        features.append(model.predict(images))
    return np.vstack(features)

features = extract_features(df, model)


df["MobileNetV1 features"] = features.tolist()
df.to_parquet("./data/MAMe_dataset_extended.parquet", index=False, compression="gzip", engine="pyarrow")