import os
import chromadb
from init_chromadb import init_chromadb

DB_PATH = 'chromadb'

def get_collection():
    """Get the courses collection, initializing if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        print("ChromaDB not found. Initializing...")
        init_chromadb()

    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection("courses")

def search(collection, query, n_results=5):
    """Search for courses matching the query."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def main():
    collection = get_collection()
    print(f"\nCourse search ready. Type 'quit' to exit.\n")

    while True:
        query = input("Search: ").strip()

        if query.lower() == 'quit':
            break

        if not query:
            continue

        results = search(collection, query)

        if not results['ids'][0]:
            print("No results found.\n")
            continue

        print()
        for i, (course_id, doc, distance) in enumerate(zip(
            results['ids'][0],
            results['documents'][0],
            results['distances'][0]
        )):
            print(f"{i+1}. {course_id} (score: {1 - distance:.3f})")
            print(f"   {doc[:400]}{'...' if len(doc) > 400 else ''}")
            print()

if __name__ == "__main__":
    main()
