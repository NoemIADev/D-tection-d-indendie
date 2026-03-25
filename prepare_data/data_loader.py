import json
import pandas as pd

def load_coco_json(json_path):
    """Reads the COCO JSON file and returns the raw dictionary."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def get_dataframes(coco_data):
    """Converts COCO data into two clean Pandas DataFrames."""
    df_images = pd.DataFrame(coco_data['images'])
    df_annotations = pd.DataFrame(coco_data['annotations'])
    
    return df_images, df_annotations