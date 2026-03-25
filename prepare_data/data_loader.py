import json
import pandas as pd

def load_coco_json():
    with open("Data/raw/_annotations.coco.json", "r") as f:
        data = json.load(f)
    return data

def get_dataframes(data):
    df_images = pd.DataFrame(data["images"])
    df_annotations = pd.DataFrame(data["annotations"])
    return df_images, df_annotations


# TEST (important sinon ton fichier sert à rien)
data = load_coco_json()
df_images, df_annotations = get_dataframes(data)

print(df_images.head())
print(df_annotations.head())