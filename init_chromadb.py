import chromadb
from batch_parser import batch_parse

def init_chromadb(input_dir='html', output_file='courses/courses.json', db_path='chromadb'):
    # Load courses using batch_parser
    courses = batch_parse(input_dir, output_file)

    if not courses:
        print("No courses to add.")
        return

    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    # Delete existing collection if it exists
    try:
        client.delete_collection("courses")
    except:
        pass

    # Create collection
    collection = client.create_collection(
        name="courses",
        metadata={"description": "Course catalog"}
    )

    # Prepare data for ChromaDB
    ids = []
    documents = []
    metadatas = []

    for course in courses:
        course_id = course.get('course_number')
        description = course.get('course_description', '')

        if course_id and description:
            ids.append(course_id)
            documents.append(description)
            metadatas.append({"course_number": course_id})

    # Add to collection
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"ChromaDB initialized with {len(ids)} courses at '{db_path}'")

if __name__ == "__main__":
    init_chromadb()
