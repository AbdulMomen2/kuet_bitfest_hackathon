import sqlite3
import random


conn = sqlite3.connect('recipes.db')


cursor = conn.cursor()

# Creating the recipe table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS recipe (
    Name VARCHAR(255),
    Taste VARCHAR(255),
    Cuisine_Type VARCHAR(255),
    Preparation_Time INT,  -- in minutes
    Reviews TEXT
);
""")

# Sample data for diversity
names = ["Pasta", "Burger", "Pizza", "Soup", "Salad", "Curry", "Cake", "Sandwich", "Stew", "Sushi"]
tastes = ["Sweet", "Savory", "Spicy", "Tangy", "Mild"]
cuisines = ["Italian", "Indian", "American", "Mexican", "Chinese", "Japanese", "French", "Thai", "Greek", "Mediterranean"]
reviews = [
    "Delicious and flavorful.",
    "Quick and easy to prepare.",
    "Perfect for special occasions.",
    "Healthy and refreshing.",
    "A bit too spicy for me.",
    "Rich and hearty.",
    "Loved by everyone in the family.",
    "Authentic taste, highly recommended.",
    "Light and fresh.",
    "Comfort food at its best."
]

# Generate 300 recipes
for i in range(300):
    name = f"{random.choice(names)} Recipe {i+1}"
    taste = random.choice(tastes)
    cuisine = random.choice(cuisines)
    prep_time = random.randint(10, 120)  # Random preparation time between 10 and 120 minutes
    review = random.choice(reviews)
    cursor.execute("INSERT INTO recipe VALUES (?, ?, ?, ?, ?)", (name, taste, cuisine, prep_time, review))

# Commit the changes
conn.commit()

# Display first 10 recipes to confirm insertion
data = cursor.execute("SELECT * FROM recipe LIMIT 10")
print("Sample Data Inserted in the Table:")
for row in data:
    print(row)

# Close the connection
conn.close()


