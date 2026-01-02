import json
import os
from parser import parse_courses

def batch_parse(input_dir = 'html', output_file = 'courses/courses.json'):
    # Get all HTML files in the input directory
    html_files = [f for f in os.listdir(input_dir) if f.endswith('.html')]

    if not html_files:
        print(f"No HTML files found in '{input_dir}' directory.")
        return

    print(f"Found {len(html_files)} HTML file(s) to process...")

    # Use dict to deduplicate by course_number
    courses_dict = {}

    for filename in html_files:
        input_path = os.path.join(input_dir, filename)

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            data = parse_courses(html_content)

            for course in data:
                course_id = course.get('course_number')
                if course_id and course_id not in courses_dict:
                    courses_dict[course_id] = course

            print(f"  {filename} ({len(data)} courses)")

        except Exception as e:
            print(f"  Error processing {filename}: {e}")

    # Convert dict values to list
    all_courses = list(courses_dict.values())

    # Create output directory if needed
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_courses, f, indent=4)

    print(f"\nDone! {len(all_courses)} unique courses saved to '{output_file}'.")

    return all_courses

if __name__ == "__main__":
    batch_parse()
