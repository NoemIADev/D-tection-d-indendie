import pandas as pd

def show_stats(df_imgs, df_anns, coco_data):
    print(f"Total Images: {len(df_imgs)}")
    print(f"Total Annotations: {len(df_anns)}")
    
    # Simple Category mapping
    cats = {c['id']: c['name'] for c in coco_data.get('categories', [])}
    df_anns['name'] = df_anns['category_id'].map(cats)
    
    print("\n--- Categories Found ---")
    print(df_anns['name'].value_counts())
    
    # Simple Density math
    stats = df_anns.groupby('image_id').size()
    print("\n--- Annotations per Image ---")
    print(f"Avg: {stats.mean():.2f} | Max: {stats.max()} | Min: {stats.min()}")
