import json
import os

def fix_slashes(json_path):
    """Fix inconsistent slashes in JSON keys to use forward slashes consistently"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create new dict with fixed keys
    new_data = {}
    fixed_count = 0
    
    for key in data:
        # Replace backslashes with forward slashes
        new_key = key.replace("\\", "/")
        new_data[new_key] = data[key]
        
        if key != new_key:
            fixed_count += 1
            print(f"Fixed: {key} -> {new_key}")
    
    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nTotal keys fixed: {fixed_count}")
    return new_data

if __name__ == "__main__":
    json_path = r"c:\Users\lllllIIlll\AppData\Roaming\image_organizer\descriptions.json"
    
    print("Fixing inconsistent slashes in JSON keys...")
    fix_slashes(json_path)
    print("\nDone!")
