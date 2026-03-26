import os
import json

def clean_data(data, image_folder, output_path):
    images = data['images']
    annotations = data['annotations']

    # Get valid image IDs (those with annotations)
    valid_image_ids = {ann['image_id'] for ann in annotations}

    # Keep only images that have annotations
    images = [img for img in images if img['id'] in valid_image_ids]

    # Keep only annotations linked to those images
    valid_ids = {img['id'] for img in images}
    annotations = [ann for ann in annotations if ann['image_id'] in valid_ids]

    # Delete images without annotations from disk
    valid_filenames = {img['file_name'] for img in images}
    for file in os.listdir(image_folder):
        if file.endswith(".jpg") and file not in valid_filenames:
            os.remove(os.path.join(image_folder, file))

    # Save cleaned JSON
    data['images'] = images
    data['annotations'] = annotations

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(" Cleaning done")