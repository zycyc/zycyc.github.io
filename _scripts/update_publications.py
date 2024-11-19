import scholarly
import os
from datetime import datetime
import re

PUBLICATIONS_DIR = "_publications"
SCHOLAR_ID = "kkZVq8YAAAAJ"


def clean_filename(title):
    # Convert title to valid filename
    clean = re.sub(r"[^a-zA-Z0-9]", "", title)
    return clean[:20]  # Limit length


def create_md_file(title, venue, year):
    # Create filename first to check if it exists
    filename = f"{clean_filename(title)}.md"
    filepath = os.path.join(PUBLICATIONS_DIR, filename)

    # Skip if file already exists
    if os.path.exists(filepath):
        print(f"Skipping existing publication: {filename}")
        return

    # Search for the publication by title to get full details
    pub = scholarly.scholarly.search_single_pub(title)
    try:
        # Create markdown content
        content = f"""---
title: "{title}"
collection: publications
permalink: /publication/{os.path.splitext(filename)[0]}
date: {year}-01-01
venue: '{venue}'
paperurl: ''
link: '{pub.get('eprint_url', '')}'
---"""

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Created/updated: {filename}")

    except Exception as e:
        print(f"Error processing publication {pub['title']}: {e}")


def main():
    # Create publications directory if it doesn't exist
    os.makedirs(PUBLICATIONS_DIR, exist_ok=True)

    try:
        # Retrieve author by Scholar ID and fill details
        author = scholarly.scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.scholarly.fill(author)

        # Get all publication titles and sort by year (newest first)
        publications = author.get("publications", [])
        # pub_titles = [pub["bib"]["title"] for pub in publications]

        print(f"Found {len(publications)} publications")
        # Process each publication
        for pub in publications:
            title, venue, year = (
                pub["bib"].get("title", ""),
                pub["bib"].get("citation", "").split(",")[0],
                pub["bib"].get("pub_year", ""),
            )
            create_md_file(title, venue, year)

    except Exception as e:
        print(f"Error fetching author data: {e}")


if __name__ == "__main__":
    main()
