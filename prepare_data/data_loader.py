import json
import pandas as pd


def get_data(json_path):
    with open(json_path) as f:
        data = json.load(f)
        df_imgs = pd.DataFrame(data['images'])
        df_anns = pd.DataFrame(data['annotations'])
        return data, df_imgs, df_anns
