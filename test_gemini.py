import google.generativeai as genai
genai.configure(api_key="AIzaSyCvoF_3SE0lSLdGnMiLXTxkhGhvV6TYwUA")  # Replace with your actual key
model = genai.GenerativeModel("gemini-1.5-flash")
prompt = """You are a SQL expert. Convert the following question into a single, valid SQL query using the tables:
- ad_sales (columns: product_name, revenue, spend, cpc)
- total_sales (columns: product_name, sales_amount)
- eligibility (columns: product_name, is_eligible)

Question: What is my total sales?
Return ONLY the SQL query as plain text, with no explanations, examples, or additional text. Do not include backticks, "sql", or any markdown formatting.
"""
response = model.generate_content(prompt, generation_config={"temperature": 0.2})
print(response.text)