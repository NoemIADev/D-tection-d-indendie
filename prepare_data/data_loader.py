import json
import pandas as pd

def load_coco_json():
    with open("Data/raw/_annotations.coco.json", "r") as f:
        data = json.load(f)
    return data

def get_dataframes(data):
    df_images = pd.DataFrame(data["images"])
    df_annotations = pd.DataFrame(data["annotations"])
    df_categories = pd.DataFrame(data["categories"])
    return df_images, df_annotations, df_categories
