from dotenv import load_dotenv
load_dotenv()  

import streamlit as st
import os
import sqlite3

import google.generativeai as genai


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

  
    fixed_sql = sql.replace("[", "(").replace("]", ")") 

    try:
        cur.execute(fixed_sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.Error as e:
        st.error(f"Error executing fixed query: {e}")
        return None  # Indicate no results

prompt = [
    """
    You are an expert in understanding user preferences and converting their English questions into SQL queries to retrieve data from a recipe database. After fetching the data, you will suggest a recipe to the user based on their query.

    **Database Details:**  
    The SQL database is named `recipes` and contains the following columns:  
    - `Name`: The name of the recipe.  
    - `Taste`: The flavor profile of the recipe (e.g., Sweet, Spicy, Savory).  
    - `Cuisine_Type`: The cuisine type of the recipe (e.g., Italian, Indian, American).  
    - `Preparation_Time`: The time required to prepare the recipe (in minutes).  
    - `Ingredients`: A list of required ingredients.  
    - `Instructions`: Step-by-step instructions for preparing the recipe.  

    **Your Task:**  
    - Step 1: Understand the user query to identify their preferences (e.g., taste, cuisine type, preparation time, or available ingredients).  
    - Step 2: Convert the query into an SQL command to fetch matching recipes from the database.  
    - Step 3: Retrieve a recipe that best matches the user's preferences.  
    - Step 4: Provide the recipe in a user-friendly format.  

    **Example Query:**  
    - User: "I want a sweet dish from Italian cuisine that I can make quickly."  
    - SQL Query:  
      ```
      SELECT * FROM recipes 
      WHERE Taste = 'Sweet' AND Cuisine_Type = 'Italian' AND Preparation_Time <= 30;
      ```  
    - Output:  
      ```
      Name: Tiramisu  
      Taste: Sweet  
      Cuisine_Type: Italian  
      Preparation_Time: 20 minutes  
      Ingredients:  
        - 200g Mascarpone Cheese  
        - 100ml Coffee  
        - 100g Sugar  
        - Ladyfinger Biscuits  
        - Cocoa Powder  
      Instructions:  
        1. Dip the ladyfinger biscuits in coffee.  
        2. Layer them in a dish with mascarpone cheese and sugar mixture.  
        3. Repeat the layers and dust with cocoa powder.  
        4. Chill for 2 hours before serving.  
      ```  

    **Key Guidelines:**  
    - The SQL query must be clear, concise, and optimized.  
    - Suggest the recipe in a structured, easy-to-read format.  
    - Always prioritize recipes that closely match the user's preferences.
    """
]

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Gemini Generated SQL Query:")
    st.code(response)

    try:
        response = read_sql_query(response, "recipes.db")
        if response is not None:  # Check if query execution was successful
            st.subheader("Query Results:")
            for row in response:
                st.write(row)
    except Exception as e:
        st.error(f"Error: {e}")