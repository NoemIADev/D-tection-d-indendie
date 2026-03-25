import os
import pandas as pd

def get_file_extensions(folder_path):
    files = os.listdir(folder_path)
    extensions = {os.path.splitext(f)[1] for f in files if "." in f}
    return list(extensions)

def find_images_without_annotations(df_imgs, df_anns):
    annotated_ids = df_anns['image_id'].unique()
    empty_images = df_imgs[~df_imgs['id'].isin(annotated_ids)]
    return empty_images

def find_aberrant_boxes(df_anns):
    invalid = df_anns[df_anns['bbox'].apply(lambda x: x[2] <= 0 or x[3] <= 0)]
    return invalid

def check_folder_vs_json(df_imgs, folder_path):
    files_in_folder = set(os.listdir(folder_path))
    files_in_json = set(df_imgs['file_name'])
    
    orphans = files_in_folder - files_in_json
    return orphans