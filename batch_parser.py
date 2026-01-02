import json
import os
from parser import parse_courses

def batch_parse(input_dir, output_dir):

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all HTML files in the input directory
    html_files = [f for f in os.listdir(input_dir) if f.endswith('.html')]

    if not html_files:
        print(f"No HTML files found in '{input_dir}' directory.")
        return

    print(f"Found {len(html_files)} HTML file(s) to process...")

    total_courses = 0
    for filename in html_files:
        input_path = os.path.join(input_dir, filename)
        output_filename = os.path.splitext(filename)[0] + '.json'
        output_path = os.path.join(output_dir, output_filename)

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            data = parse_courses(html_content)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            print(f"  {filename} -> {output_filename} ({len(data)} courses)")
            total_courses += len(data)

        except Exception as e:
            print(f"  Error processing {filename}: {e}")

    print(f"\nDone! Processed {len(html_files)} file(s), {total_courses} total courses.")

if __name__ == "__main__":
    batch_parse('html', 'courses')
