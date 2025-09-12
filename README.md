# E-Shop
E-Commerce Product Recommendation Web Application – Project Report
1. Choice of Technology
Programming Language: Python

Python was selected due to its readability, large community support, and mature ecosystem for web development and database interaction. It enables quick prototyping and ease of maintenance.

Web Framework: Flask

Flask was chosen as the web framework because of:

Its lightweight and minimalist design, which makes it ideal for small to medium-scale applications.

Easy integration with templating (Jinja2), routing, and form handling.

Flexibility to structure the application in a simple yet extendable manner.

Database: SQLite

SQLite was used for simplicity and minimal setup requirements. It is file-based and ideal for prototyping or smaller-scale projects where concurrency is not a major concern.

Templating Engine: Jinja2

Jinja2 (built into Flask) was used to dynamically render HTML templates with embedded Python variables and control structures.

Frontend Tools:

Bootstrap 5.3: For responsive and consistent UI styling.

HTML5/CSS3: For standard layout and markup structure.

Supporting Libraries:

sqlite3: Built-in Python library for interacting with the SQLite database.

Flask: Core web framework used for routing and rendering.

2. Design Decisions
Product Model

Products were modeled in a products table with fields:

id: Auto-increment primary key.

name: Name of the product.

price: Floating point price.

category: Product category (used in recommendations).

tags: Comma-separated keywords.

description: Detailed product description.

This schema was designed for simplicity and flexibility. Tags as comma-separated strings simplify input, although they can be normalized into a separate table in a more scalable design.

Recommendation System Logic

A rule-based approach was implemented with the following scoring system:

+2 points if the product has the same category.

+1 point if the price difference is ≤ 10.

+1 point for shared tags (based on intersection of tag sets).

This scoring logic strikes a balance between relevance and simplicity. It avoids the need for ML models while still providing meaningful suggestions. The top 3 highest-scoring products are shown as recommendations.

Trade-offs & Simplifications:

No external libraries (like scikit-learn or pandas) were used to keep dependencies minimal.

Tag intersection was computed using set logic, assuming tags are entered correctly and consistently.

Simplified scoring system instead of cosine similarity, collaborative filtering, or embeddings.

3. Implementation Details
Key Modules
app.py

Main application file containing:

Route definitions (/, /product/<id>, /add, /edit/<id>, /delete/<id>, /recent)

Product CRUD logic

Recommendation logic

Session handling for recently viewed products

models.py

Database initialization script:

Defines schema for the products table.

Ensures the table exists on application startup.

Templates

layout.html: Base template with shared navigation and Bootstrap integration.

index.html: Lists products dynamically.

product_detail.html: Shows detailed view of a product and recommended items.

product_form.html: Used for both adding and editing products.

Workflow

Adding a Product:

Navigate to /add

Submit the form with product details

Stored in SQLite database via POST request

Viewing a Product:

Navigate to /product/<id>

Shows full details

Displays up to 3 recommended products

Recently Viewed Products:

Stored in session as a list of IDs

Viewable at /recent

4. Concerns & Challenges Faced
a. Session Storage for Recent Views

Storing recently viewed products using Flask.session required care to maintain order and limit size. The list is truncated to the last 5 items.

Workaround: Used list.insert(0, product_id) to maintain reverse chronological order.

b. Tag Matching Logic

Tags were stored as a string, which could lead to inconsistencies in matching (e.g., extra spaces, case differences).

Workaround: Basic split(',') and set() intersection was used, assuming clean input. Could be improved by trimming and lowercasing tags on both input and comparison.

c. SQL Query for Recently Viewed

Dynamically building a query with variable placeholders (?) was tricky.

Solution: Used ','.join('?' for _ in ids) to construct the IN clause safely.

d. Recommendations Based on Similarity

While the rule-based method works, it does not scale or learn from user behavior.

Improvement: With more time, we could:

Use TF-IDF or vector-based similarity on descriptions/tags.

Add user behavior tracking and collaborative filtering.

Normalize tags into a separate table for proper relational modeling.

5. References

Flask Documentation

Jinja2 Templating

SQLite in Python

Bootstrap 5

Stack Overflow (various threads on Flask forms, session handling, and SQLite queries)




Project Setup Instructions 

 1. Clone or Download the Project 

git clone URL - https://github.com/RM654/E-Shop.git  
 

If you're creating it from scratch, just ensure all the following files exist: 

app.py 

models.py 

templates (with all the .html files) 

database.db (or let it generate on first run) 

 

2. Create a Virtual Environment (Recommended) 

python -m venv venv 
source venv/bin/activate  # On Windows: venv\Scripts\activate 
 

 

3. Install Dependencies 

Create a requirements.txt file with: 

Flask==2.3.2 
 

Then install: 

pip install -r requirements.txt 
 

If requirements.txt doesn't exist: 

pip install Flask 
 

 

4. Initialize the SQLite Database 

The app auto-initializes the database on first run using: 

init_db() 
 

But to initialize it manually: 

python 
>>> from models import init_db 
>>> init_db() 
>>> exit() 
 

This will create database.db with a products table. 

 

5. Set Up the Project Structure 

Ensure your project folder is structured like this: 

E-Shop 
  app.py 
  models.py 
  database.db (optional, will be created if not present) 
  templates 
     layout.html 
     index.html 
     product_detail.html 
     product_form.html 
 

 

6. Run the Flask App 

In your terminal: 

export FLASK_APP=app.py          # On Windows: set FLASK_APP=app.py 
export FLASK_ENV=development     # Optional: enables debug mode 
flask run 
 

Or directly with Python: 

python app.py 
 

The app will be accessible at: 

http://127.0.0.1:5000/ 
 
