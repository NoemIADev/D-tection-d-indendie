import os
import json
import shutil

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

    # garder uniquement les annotations liées à une image existante
    image_ids = {img["id"] for img in images}
    annotations = [ann for ann in annotations if ann["image_id"] in image_ids]

    # garder uniquement les images avec au moins une annotation
    annotated_ids = {ann["image_id"] for ann in annotations}
    images = [img for img in images if img["id"] in annotated_ids]

    # créer le dossier de sortie si besoin
    output_folder = os.path.dirname(output_path)
    os.makedirs(output_folder, exist_ok=True)

    # copier seulement les images valides
    valid_filenames = {img["file_name"] for img in images}

    for file_name in valid_filenames:
        src = os.path.join(image_folder, file_name)
        dst = os.path.join(output_folder, file_name)

        if os.path.exists(src):
            shutil.copy(src, dst)

    # remettre les données nettoyées
    data["images"] = images
    data["annotations"] = annotations

    # sauvegarder le nouveau json clean
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data