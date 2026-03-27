import json
from prepare_data.data_loader import load_coco_json
from prepare_data.data_cleaner import (
    get_extensions,
    find_images_without_annotations,
    find_annotations_without_images,
    clean_data,
)
print("import")

def run_pipeline():
    image_folder = "Data/raw"
    coco_path = "Data/raw/_annotations.coco.json"
    output_path = "Data/cleaned/_annotations.cleaned.coco.json"
    print("path ok")
    # charger le json
    data = load_coco_json()

    print("json charger")

    images = data["images"]
    annotations = data["annotations"]

    # explorer / vérifier
    extensions = get_extensions(image_folder)
    images_without_annotations = find_images_without_annotations(images, annotations)
    annotations_without_images = find_annotations_without_images(images, annotations)

    print("Extensions trouvées :", extensions)
    print("Nombre total d'images :", len(images))
    print("Nombre total d'annotations :", len(annotations))
    print("Images sans annotation :", len(images_without_annotations))
    print("Annotations sans image :", len(annotations_without_images))

    # nettoyage
    cleaned_data = clean_data(data, image_folder, output_path)

    print("Nettoyage terminé")

    return cleaned_data


run_pipeline()