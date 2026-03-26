import os
import json

def get_extensions(image_folder):
    return {os.path.splitext(f)[1] for f in os.listdir(image_folder)}

def find_images_without_annotations(images, annotations):
    annotated_ids = {ann["image_id"] for ann in annotations}
    return [img for img in images if img["id"] not in annotated_ids]

def find_annotations_without_images(images, annotations):
    image_ids = {img["id"] for img in images}
    return [ann for ann in annotations if ann["image_id"] not in image_ids]

def clean_data(data, image_folder, output_path):
    images = data["images"]
    annotations = data["annotations"]

    image_ids = {img["id"] for img in images}

    # keep only annotations linked to real images
    annotations = [ann for ann in annotations if ann["image_id"] in image_ids]

    # keep only images that have at least one annotation
    annotated_ids = {ann["image_id"] for ann in annotations}
    images = [img for img in images if img["id"] in annotated_ids]

    # delete files on disk that are no longer in JSON
    valid_filenames = {img["file_name"] for img in images}
    deleted_count = 0

    for file in os.listdir(image_folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")) and file not in valid_filenames:
            os.remove(os.path.join(image_folder, file))
            deleted_count += 1

    data["images"] = images
    data["annotations"] = annotations

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print("Cleaning done.")
    print("Deleted files:", deleted_count)
    print("Clean JSON saved to:", output_path)