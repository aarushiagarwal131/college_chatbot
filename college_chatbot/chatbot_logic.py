import re

# Define a dictionary mapping keywords to URLs
FAQ_LINKS = {
    "placements": "https://ctp.nitj.ac.in/index_placements",
    "courses": "https://yourinstitute.edu/courses",
    "exam dates": "https://yourinstitute.edu/exam-dates",
    # Add more mappings as needed
}


def get_relevant_links(query):
    print(f"User query: {query}")  # Debugging line
    for keyword, link in FAQ_LINKS.items():
        print(f"Checking if {keyword} is in query")  # Debugging line
        if re.search(keyword, query, re.IGNORECASE):
            print(f"Found relevant link for {keyword}")  # Debugging line
            return f"For {keyword}, please refer to: {link}"
    return "I'm sorry, I couldn't find information on that topic. Please try rephrasing or visit the institute website."
