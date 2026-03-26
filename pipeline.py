from pathlib import Path
import json

from prepare_data.data_loader import load_coco_json, coco_to_dataframes
from prepare_data.data_cleaner import (
    get_file_extensions,
    check_images_annotations_coherence,
    get_images_without_annotations,
    get_annotations_without_images,
    get_abnormal_annotations,
)


def run_pipeline(data_dir="data", save_cleaned_json=False):
    """
    Lance le pipeline de vérification/nettoyage sur le dataset COCO.
    """

    data_dir = Path(data_dir)
    coco_path = data_dir / "_annotations.coco.json"

    # 1) Chargement du json
    coco_data = load_coco_json(coco_path)

    # 2) Conversion en DataFrames
    images_df, annotations_df, categories_df = coco_to_dataframes(coco_data)

    # 3) Vérifications
    extensions = get_file_extensions(data_dir)
    missing_annotations = get_images_without_annotations(images_df, annotations_df)
    orphan_annotations = get_annotations_without_images(images_df, annotations_df)
    abnormal_annotations = get_abnormal_annotations(annotations_df)
    coherence_ok = check_images_annotations_coherence(images_df, annotations_df)

    # 4) Affichage résumé
    print("=== PIPELINE DATA ===")
    print(f"Extensions trouvées : {extensions}")
    print(f"Nombre d'images : {len(images_df)}")
    print(f"Nombre d'annotations : {len(annotations_df)}")
    print(f"Nombre de catégories : {len(categories_df)}")
    print(f"Images sans annotation : {len(missing_annotations)}")
    print(f"Annotations sans image : {len(orphan_annotations)}")
    print(f"Annotations aberrantes : {len(abnormal_annotations)}")
    print(f"Cohérence images/annotations : {coherence_ok}")

    # 5) Nettoyage simple
    # On garde seulement :
    # - les images qui ont au moins une annotation
    # - les annotations qui pointent vers une image existante
    valid_image_ids = set(annotations_df["image_id"].unique())
    cleaned_images_df = images_df[images_df["id"].isin(valid_image_ids)].copy()

    valid_ids_after_images = set(cleaned_images_df["id"].unique())
    cleaned_annotations_df = annotations_df[
        annotations_df["image_id"].isin(valid_ids_after_images)
    ].copy()

    # Suppression des annotations aberrantes
    if len(abnormal_annotations) > 0:
        abnormal_ids = set(abnormal_annotations["id"].unique())
        cleaned_annotations_df = cleaned_annotations_df[
            ~cleaned_annotations_df["id"].isin(abnormal_ids)
        ].copy()

    # 6) Reconstruction du json nettoyé
    cleaned_coco = {
        "images": cleaned_images_df.to_dict(orient="records"),
        "annotations": cleaned_annotations_df.to_dict(orient="records"),
        "categories": categories_df.to_dict(orient="records"),
    }

    # 7) Sauvegarde optionnelle
    if save_cleaned_json:
        output_path = data_dir / "_annotations.cleaned.coco.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_coco, f, ensure_ascii=False, indent=4)
        print(f"Fichier nettoyé sauvegardé : {output_path}")

    return {
        "extensions": extensions,
        "images_df": images_df,
        "annotations_df": annotations_df,
        "categories_df": categories_df,
        "missing_annotations": missing_annotations,
        "orphan_annotations": orphan_annotations,
        "abnormal_annotations": abnormal_annotations,
        "coherence_ok": coherence_ok,
        "cleaned_coco": cleaned_coco,
    }


if __name__ == "__main__":
    run_pipeline(data_dir="data", save_cleaned_json=True)