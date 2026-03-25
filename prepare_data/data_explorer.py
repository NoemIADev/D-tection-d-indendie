import pandas as pd

def count_categories(df_annotations):
    """Prints the number of annotations per category."""
    # In COCO, category_id links to the name of the object (e.g., fire)
    print("--- Categories Distribution ---")
    print(df_annotations['category_id'].value_counts())

def get_image_stats(df_images):
    """Prints basic info about image resolutions."""
    print("--- Image Statistics ---")
    print(f"Total Images: {len(df_images)}")
    print(f"Average Width: {df_images['width'].mean()}")
    print(f"Average Height: {df_images['height'].mean()}")

def get_basic_stats(df_imgs, df_anns):
    """Prints total counts for images and annotations."""
    print(f"Total Images: {len(df_imgs)}")
    print(f"Total Annotations: {len(df_anns)}")

def show_categories(coco_data):
    """Prints the names of the categories available."""
    # Categories are usually in the raw JSON dictionary, not just the DF
    categories = coco_data.get('categories', [])
    print("Categories found:", [cat['name'] for cat in categories])

def count_annotations_per_image(df_anns):
    """Shows how many annotations exist per image (min, max, mean)."""
    stats = df_anns.groupby('image_id').size()
    print("--- Annotations per Image ---")
    print(f"Average: {stats.mean():.2f}")
    print(f"Max in one image: {stats.max()}")
    print(f"Min in one image: {stats.min()}")

def get_image_resolutions(df_imgs):
    """Checks if all images are the same size."""
    resolutions = df_imgs.groupby(['width', 'height']).size()
    print("--- Image Resolutions ---")
    print(resolutions)

def count_annotations_per_category(df_anns, coco_data):
    """Counts how many times each category appears in the annotations."""
    # Create a dictionary to map ID to Name: {0: 'wildfire', 1: 'fire'}
    categories = {cat['id']: cat['name'] for cat in coco_data['categories']}
    
    # Map the IDs in the dataframe to names
    df_anns['category_name'] = df_anns['category_id'].map(categories)
    
    print("--- Distribution per Category ---")
    print(df_anns['category_name'].value_counts())