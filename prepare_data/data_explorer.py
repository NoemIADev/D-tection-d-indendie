import pandas as pd

# 1. Nombre total d’images
def count_images(df_images):
    return len(df_images)


# 2. Nombre total d’annotations
def count_annotations(df_annotations):
    return len(df_annotations)


# 3. Liste des catégories
def get_categories(data):
    # on récupère les catégories dans le JSON
    categories = data["categories"]
    return [cat["name"] for cat in categories]


# 4. Nombre d’annotations par image
def annotations_per_image(df_annotations):
    # groupby = regrouper par image_id
    return df_annotations.groupby("image_id").size()


# 5. Stats sur les annotations par image
def annotation_stats(df_annotations):
    counts = df_annotations.groupby("image_id").size()
    
    return {
        "min": counts.min(),
        "max": counts.max(),
        "mean": counts.mean()
    }

# 6. Nombre d’images par catégorie
def images_per_category(df_annotations):
    return df_annotations.groupby("category_id")["image_id"].nunique()