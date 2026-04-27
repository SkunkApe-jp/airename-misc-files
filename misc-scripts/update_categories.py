import json
import os
import shutil
from pathlib import Path

# Define category mappings based on image analysis
CATEGORY_MAPPINGS = {
    # Art & Still Life
    "deer-wireframe-wallpaper.jpg": "Art_Still_Life/3D_Art",
    "wilted-rose.jpg": "Art_Still_Life/Still_Life",
    "window-with-branches-and-books.jpg": "Indoors_Personal/Interior_Views",
    
    # Urban/Cityscapes - Cityscapes at Dusk
    "cityscape-at-dusk.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "cityscape-at-dusk-1.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "cityscape-at-dusk-2.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "cityscape-at-dusk-3.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "cityscape-at-dusk-4.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "cityscape-at-dusk-5.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "city-industry-sunset.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "city-dining-scene-at-dusk.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    "city-sunset-view.jpg": "Urban_Cityscapes/Cityscapes_at_Dusk",
    
    # Urban/Cityscapes - Nighttime City
    "noir-city-street-at-night.jpg": "Urban_Cityscapes/Nighttime_City",
    "city-nighttime-billboard.jpg": "Urban_Cityscapes/Nighttime_City",
    "city-night-billboard-eyes.jpg": "Urban_Cityscapes/Nighttime_City",
    "city-nighttime-traffic-scene.jpg": "Urban_Cityscapes/Nighttime_City",
    "urban-night-scene.jpg": "Urban_Cityscapes/Nighttime_City",
    "urban-night-scene-1.jpg": "Urban_Cityscapes/Nighttime_City",
    "nighttime-parking-lot-scene.jpg": "Urban_Cityscapes/Nighttime_City",
    "nighttime-city-beach-scene.jpg": "Urban_Cityscapes/Nighttime_City",
    "neon-lit-storefront-at-night.jpg": "Urban_Cityscapes/Nighttime_City",
    
    # Urban/Cityscapes - Street Scenes
    "city-street-scene.jpg": "Urban_Cityscapes/Street_Scenes",
    "city-street-at-dusk.jpg": "Urban_Cityscapes/Street_Scenes",
    "city-street-at-night.jpg": "Urban_Cityscapes/Street_Scenes",
    "urban-street-scene.jpg": "Urban_Cityscapes/Street_Scenes",
    "urban-street-scene-at-dusk.jpg": "Urban_Cityscapes/Street_Scenes",
    "urban-street-scene-at-dusk-1.jpg": "Urban_Cityscapes/Street_Scenes",
    "city-street-scene-at-dusk.jpg": "Urban_Cityscapes/Street_Scenes",
    "urban-bike-lane-scene.jpg": "Urban_Cityscapes/Street_Scenes",
    "sidewalk-scene-with-hedge.jpg": "Urban_Cityscapes/Street_Scenes",
    
    # Urban/Cityscapes - Rainy City
    "city-street-rainy-day.jpg": "Urban_Cityscapes/Rainy_City",
    "city-street-rainy-day-1.jpg": "Urban_Cityscapes/Rainy_City",
    "city-street-rainy-day-2.jpg": "Urban_Cityscapes/Rainy_City",
    
    # Urban/Cityscapes - Urban Architecture
    "urban-rooftop-scene.jpg": "Urban_Cityscapes/Urban_Architecture",
    "city-view-from-apartment.jpg": "Urban_Cityscapes/Urban_Architecture",
    "city-view-from-room.png": "Urban_Cityscapes/Urban_Architecture",
    "urban-landscape-at-dusk.jpg": "Urban_Cityscapes/Urban_Architecture",
    "urban-scene-at-dusk.jpg": "Urban_Cityscapes/Urban_Architecture",
    "urban-scene-with-buildings-and-wires.jpg": "Urban_Cityscapes/Urban_Architecture",
    "urban-river-scene.jpg": "Urban_Cityscapes/Urban_Architecture",
    "urban-canal-scene.jpg": "Urban_Cityscapes/Urban_Architecture",
    "urban-park-scene.jpg": "Urban_Cityscapes/Urban_Architecture",
    
    # Japanese Scenes - Japanese Streets
    "japanese-street-scene-at-dusk.jpg": "Japanese_Scenes/Japanese_Streets",
    "urban-street-scene-at-dusk.jpg": "Japanese_Scenes/Japanese_Streets",
    "traditional-japanese-street-scene.jpg": "Japanese_Scenes/Japanese_Streets",
    "urban-dusk-scene.jpg": "Japanese_Scenes/Japanese_Streets",
    "urban-tram-scene-at-dusk.jpg": "Japanese_Scenes/Japanese_Streets",
    "city-street-at-dusk.jpg": "Japanese_Scenes/Japanese_Streets",
    
    # Japanese Scenes - Japanese Gardens
    "japanese-garden-scene.jpg": "Japanese_Scenes/Japanese_Gardens",
    "traditional-japanese-scene-at-dusk.jpg": "Japanese_Scenes/Japanese_Gardens",
    
    # Japanese Scenes - Japanese Storefronts
    "japanese-storefront-at-dusk.jpg": "Japanese_Scenes/Japanese_Storefronts",
    "nighttime-storefront-scene.jpg": "Japanese_Scenes/Japanese_Storefronts",
    "nighttime-store-scene.jpg": "Japanese_Scenes/Japanese_Storefronts",
    "japanese-cafe-at-night.jpg": "Japanese_Scenes/Japanese_Storefronts",
    "japanese-vending-machines-night.jpg": "Japanese_Scenes/Japanese_Storefronts",
    
    # Japanese Scenes - Japanese Landscapes
    "rural-japanese-landscape.jpg": "Japanese_Scenes/Japanese_Landscapes",
    "mountain-town-at-dusk.jpg": "Japanese_Scenes/Japanese_Landscapes",
    "asian-alleyway-scene.jpg": "Japanese_Scenes/Japanese_Landscapes",
    "japanese-alleyway-scene.jpg": "Japanese_Scenes/Japanese_Landscapes",
    
    # Nature & Landscapes - Beaches & Coastal
    "lonely-beach-scene-at-sunset.jpg": "Nature_Landscapes/Beaches_Coastal",
    "nighttime-city-beach-scene.jpg": "Nature_Landscapes/Beaches_Coastal",
    
    # Nature & Landscapes - Tropical
    "stormy-tropical-landscape.jpg": "Nature_Landscapes/Tropical",
    
    # Nature & Landscapes - Gardens & Parks
    "urban-park-scene.jpg": "Nature_Landscapes/Gardens_Parks",
    "japanese-garden-scene.jpg": "Nature_Landscapes/Gardens_Parks",
    
    # Indoors & Personal
    "classroom-at-sunset.jpg": "Indoors_Personal/Classroom_Workplace",
    "coffee-by-window.jpg": "Indoors_Personal/Interior_Views",
    "window-with-branches-and-books.jpg": "Indoors_Personal/Interior_Views",
    "city-view-from-apartment.jpg": "Indoors_Personal/Interior_Views",
    "city-view-from-room.png": "Indoors_Personal/Interior_Views",
    
    # Transportation & Infrastructure - Trains & Stations
    "train-arriving-at-station.jpg": "Transportation_Infrastructure/Trains_Stations",
    "train-station-platform.jpg": "Transportation_Infrastructure/Trains_Stations",
    "train-car-interior-with-red-bow.jpg": "Transportation_Infrastructure/Trains_Stations",
    
    # Transportation & Infrastructure - Bridges
    "bridge-at-dusk.jpg": "Transportation_Infrastructure/Bridges",
    "rainbow-bridge-tokyo-night.jpg": "Transportation_Infrastructure/Bridges",
    "nighttime-city-beach-scene.jpg": "Transportation_Infrastructure/Bridges",
    
    # Transportation & Infrastructure - Roads & Traffic
    "city-nighttime-traffic-scene.jpg": "Transportation_Infrastructure/Roads_Traffic",
    "nighttime-parking-lot-scene.jpg": "Transportation_Infrastructure/Roads_Traffic",
    "urban-tram-scene-at-dusk.jpg": "Transportation_Infrastructure/Roads_Traffic",
    
    # Atmospheric & Moody - Foggy Scenes
    "foggy-street-scene.jpg": "Atmospheric_Moody/Foggy_Scenes",
    "foggy-street-scene-1.jpg": "Atmospheric_Moody/Foggy_Scenes",
    "foggy-street-scene-2.jpg": "Atmospheric_Moody/Foggy_Scenes",
    
    # Atmospheric & Moody - Nighttime Mood
    "noir-city-street-at-night.jpg": "Atmospheric_Moody/Nighttime_Mood",
    "nighttime-storefront-scene.jpg": "Atmospheric_Moody/Nighttime_Mood",
    "urban-night-scene-1.jpg": "Atmospheric_Moody/Nighttime_Mood",
    "blue-lit-alleyway-scene.jpg": "Atmospheric_Moody/Nighttime_Mood",
    "city-night-billboard-eyes.jpg": "Atmospheric_Moody/Nighttime_Mood",
}

def update_descriptions_json(json_path):
    """Update categories in descriptions.json file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for key in data:
        # Extract filename from path
        filename = os.path.basename(key)
        if filename in CATEGORY_MAPPINGS:
            data[key]["category"] = CATEGORY_MAPPINGS[filename]
            updated_count += 1
            print(f"Updated: {filename} -> {CATEGORY_MAPPINGS[filename]}")
    
    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\nTotal updated: {updated_count} images")
    return data

def move_images_to_folders(data, source_dir, target_base_dir):
    """Move images to their assigned folders"""
    source_path = Path(source_dir)
    target_path = Path(target_base_dir)
    
    moved_count = 0
    not_found = []
    
    for key in data:
        # Extract filename from path
        filename = os.path.basename(key)
        category = data[key].get("category", "Unsorted")
        
        # Skip if category is Unsorted or the deer-wireframe image (already in different location)
        if category == "Unsorted" or "deer-wireframe" in filename.lower():
            continue
        
        # Source file path
        source_file = source_path / filename
        
        # Target folder path
        target_folder = target_path / category
        target_file = target_folder / filename
        
        # Create target folder if it doesn't exist
        target_folder.mkdir(parents=True, exist_ok=True)
        
        # Move file if it exists
        if source_file.exists():
            shutil.move(str(source_file), str(target_file))
            moved_count += 1
            print(f"Moved: {filename} -> {category}")
        else:
            not_found.append(filename)
    
    print(f"\nTotal moved: {moved_count} images")
    if not_found:
        print(f"\nNot found ({len(not_found)}):")
        for f in not_found:
            print(f"  - {f}")

if __name__ == "__main__":
    # Paths
    json_path = r"c:\Users\lllllIIlll\AppData\Roaming\image_organizer\descriptions.json"
    source_dir = r"C:\Users\lllllIIlll\Pictures\classA\Calm\Unsorted"
    target_base_dir = r"C:\Users\lllllIIlll\Pictures\classA\Calm"
    
    print("Step 1: Updating descriptions.json...")
    data = update_descriptions_json(json_path)
    
    print("\nStep 2: Moving images to folders...")
    move_images_to_folders(data, source_dir, target_base_dir)
    
    print("\nDone!")
