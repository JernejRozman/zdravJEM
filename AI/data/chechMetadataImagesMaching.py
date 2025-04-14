import os
import csv

def check_images_in_metadata():
    # Directly refer to files in the same folder
    metadata_file = "./metadata.csv"
    images_folder = "./images"

    # Open the CSV file
    with open(metadata_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header (e.g. ["imageName", "zdravo", ...])
        metadata_names = set(row[0] for row in reader if row)

    # List all JPG/JPEG files in the images folder
    image_files = [
        f for f in os.listdir(images_folder)
        if f.lower().endswith((".jpg", ".jpeg"))
    ]

    # Check each image against metadata.csv names
    missing_in_metadata = []
    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        if base_name not in metadata_names:
            missing_in_metadata.append(image_file)

    # Print results
    if missing_in_metadata:
        print("These image files do NOT have corresponding entries in metadata.csv:")
        for img in missing_in_metadata:
            print("   -", img)
    else:
        print("All image files have corresponding entries in metadata.csv!")

if __name__ == "__main__":
    check_images_in_metadata()
