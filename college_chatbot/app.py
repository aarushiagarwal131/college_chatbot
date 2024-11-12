from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS  # Import CORS
from chatbot_logic import get_relevant_links  # Import logic to fetch relevant URLs
from dotenv import load_dotenv

# Load environment variables from .env file (optional)
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Use environment variable

# Initialize the model (Gemini 1.5)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Function to generate content based on the user query and links from chatbot_logic.py
def get_content_from_gemini(query, links):
    try:
        combined_input = f"""
            Query: {query}

            Link: {links} 

            Instructions: 

            1. Extract Information:  Use the provided link to find information related to the user's query.
            2. Focus on Freshers:  Tailor your response to the needs of first-year students (freshers). Provide information that would be most relevant to them. 
            3. Provide Concise Answers:  Keep the response brief and easy to understand. 
            4. Avoid Ambiguity: If the information is not available on the link, say "I'm sorry, I don't have information on that. I can only access information from the provided link."
            5. Format:
                * Start with: "The NIT Jalandhar chatbot welcomes you!" 
                * Use **bold** for important keywords.
                * Use *italics* for emphasis.
                * Separate information points with line breaks.
                * Respond in a conversational tone, using a plain text format without any markdown.
                
        """
        response = model.generate_content(combined_input)
        print(f"Gemini response: {response}")  # Debugging line

        # Ensure the response maintains formatting
        if response and hasattr(response, "text"):
            return response.text  # Returning the raw response without modification
        else:
            return "Sorry, I couldn't generate a valid response from the model."
    except Exception as e:
        return f"Error occurred while generating content: {str(e)}"


# Route to handle chat interactions
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Step 1: Get user query from the request
        user_query = request.json.get("query")
        if not user_query:
            return jsonify({"response": "No query provided."})

        # Step 2: Retrieve relevant links based on the user query
        relevant_links = get_relevant_links(user_query)

        if not relevant_links:
            return jsonify(
                {"response": "Sorry, I couldn't find relevant links for your query."}
            )

        # Step 3: Get the content from Gemini using the query and the relevant links
        generated_content = get_content_from_gemini(user_query, relevant_links)

        # Step 4: Return the generated content, maintaining the formatting
        return jsonify({"response": generated_content})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
