#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
import csv

# Create img directory if it doesn't exist
os.makedirs('img', exist_ok=True)

# Color scheme for different family roles/relationships
role_colors = {
    'Patriarch': ('#1a237e', 'white'),     # Dark blue
    'Matriarch': ('#c2185b', 'white'),     # Dark pink
    'Son': ('#0277bd', 'white'),           # Light blue
    'Daughter': ('#e91e63', 'white'),      # Pink
    'Granddaughter': ('#ff69b4', 'white'), # Light pink
    'Grandson': ('#4db8ff', 'white'),      # Lighter blue
}

# Load people from CSV
people = []
try:
    with open('data/people.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Name'] and row['Image_Filename']:
                # Generate initials from name
                name_parts = row['Name'].split()
                initials = ''.join([part[0].upper() for part in name_parts[:2]])
                
                # Get color based on role
                role = row.get('Role', 'Family')
                bg_color, text_color = role_colors.get(role, ('#999999', 'white'))
                
                # Convert jpg to png
                image_file = row['Image_Filename'].replace('.jpg', '.png').replace('.jpeg', '.png')
                
                people.append((image_file, initials, bg_color, text_color))
    
    # Add default avatar
    people.append(('default.png', 'User', '#cccccc', 'white'))
except Exception as e:
    print(f"Error reading CSV: {e}")
    people = [('default.png', 'User', '#cccccc', 'white')]

# Image specifications
SIZE = 200  # 200x200 pixels (1:1 aspect ratio)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    if hex_color == 'white':
        return (255, 255, 255)
    elif hex_color == 'black':
        return (0, 0, 0)
    else:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_avatar(filename, initials, bg_color, text_color):
    """Create a circular avatar image with transparent background"""
    # Create a transparent image (RGBA)
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a filled circle
    draw.ellipse([0, 0, SIZE, SIZE], fill=hex_to_rgb(bg_color) + (255,))
    
    # Try to use a system font, fallback to default
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 60)
    except:
        try:
            font = ImageFont.truetype('/usr/share/fonts/TTF/arial.ttf', 60)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
    
    # Calculate text position for centering
    if font:
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        # Fallback for default font
        text_width = len(initials) * 20
        text_height = 30
        font = ImageFont.load_default()
    
    x = (SIZE - text_width) // 2
    y = (SIZE - text_height) // 2
    
    # Draw the text
    draw.text((x, y), initials, fill=hex_to_rgb(text_color) + (255,), font=font)
    
    # Save the image as PNG to preserve transparency
    img.save(f'img/{filename}', 'PNG')
    print(f"Created: img/{filename}")

# Create all avatars
for filename, initials, bg_color, text_color in people:
    create_avatar(filename, initials, bg_color, text_color)

print("All avatar images created successfully!")
print("Images are 200x200 pixels with circular shape and transparent background")
