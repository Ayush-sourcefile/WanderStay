import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Load intents from the JSON file
file_path = os.path.abspath("./patterns.json")
with open(file_path, "r") as file:
    intents = json.load(file)

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer(ngram_range=(1, 4))
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response
        
counter = 0

def main():
    global counter
    st.title("WanderStay, a premium hotel finder of INDIA")

    # Create a sidebar menu with options
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Menu
    if choice == "Home":
        st.write("Welcome to WanderStay, your one stop solution for finding famous hotels in INDIA. Please kindly search for hotels in state wise or UT wise format like:- 'Recommend some best-rated hotels to rent in Goa', and then press Enter to start the conversation.")

        # Check if the chat_log.csv file exists, and if not, create it with column names
        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:

            # Convert the user input to a string
            user_input_str = str(user_input)

            response = chatbot(user_input)
            st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{counter}")

            # Get the current timestamp
            timestamp = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

            # Save the user input and chatbot response to the chat_log.csv file
            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting with me. Have a great JORNEY ahead!")
                st.stop()

    # Conversation History Menu
    elif choice == "Conversation History":
        # Display the conversation history in a collapsible expander
        st.header("Conversation History")
        # with st.beta_expander("Click to see Conversation History"):
        with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"Chatbot: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("---")

    elif choice == "About":
        st.write("The main goal of making WanderStay is to assist people in India by serving as a personalized, intelligent travel assistant for finding hotels across states and union territories")

        st.subheader("Overview of WanderStay:")

        st.write("""
        Wanderstay is divided into various parts:
        \n1. It allows users to search for hotels in a specific state, city, or union territory by simply entering their destination.
                 \n2. It categorizes hotels based on region, making it easier for users to navigate their options.
                 \n3. For each state or union territory, WanderStay can provide curated lists of iconic hotels with cultural or historical value (e.g., palaces in Rajasthan),eco-friendly stays or rural homestay,modern business hotels in metro cities like Mumbai, Delhi, or Bengaluru.
                 \n4. It also promotes sustainable and eco-friendly accommodations for environmentally conscious travelers.
        """)

        st.subheader("Dataset of WanderStay")

        st.write("""
        The dataset used in WanderStay is a collection of labelled patterns and entities. The data is stored in a list.
        - Patterns: The intent of the user input (e.g. "greeting", "Hotels", "JOURNEY")
        - Entities: The entities extracted from user input (e.g. "Hi", "Show some hotels to stay in for vacations in Goa", "Famous hotels to stay in Gujarat")
        - Text: The user input text.
        """)

        st.subheader("Streamlit WanderStay's Interface:")

        st.write("WanderStay's interface is built using Streamlit. The interface includes a text input box for users to input their text and a chat window to display the chatbot's responses. The interface uses the trained model to generate responses to user input.")

        st.subheader("Conclusion:")

        st.write("By offering tailored services and an easy-to-use interface, WanderStay ensures travelers across India find the best accommodation options, saving time, money, and effort. It serves as a one-stop solution for planning stays during vacations, work trips, or even pilgrimages.\n\nDEAR customers, please be ensured that WanderStay will be opreational soon across the GLOBLE")

if __name__ == '__main__':
    main()
