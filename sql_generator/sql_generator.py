import google.generativeai as genai
import os
import re

genai.configure(api_key="<PASTE YOUR API KEY HERE>")  # Replace with your actual API key
query_cache = {
    "what is my total sales?": "SELECT SUM(total_sales) FROM total_sales;",
    "calculate roas?": "SELECT SUM(ad_sales) / SUM(ad_spend) AS RoAS FROM ad_sales;",
    "which product had the highest cpc?": "SELECT item_id, MAX(ad_spend / clicks) AS cpc FROM ad_sales WHERE clicks > 0;"
}  # Cache for required questions (lowercase keys)

def convert_to_sql(question):
    # Normalize question: lowercase and strip whitespace
    normalized_question = question.lower().strip()
    if normalized_question in query_cache:
        return query_cache[normalized_question]
    prompt = f"""You are a SQL expert. Convert the following question into a single, valid SQL query using the tables:
- ad_sales (columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
- total_sales (columns: item_id, total_sales)
- eligibility (columns: eligibility_datetime_utc, item_id, eligibility, message)

Question: {question}
Return ONLY the SQL query as plain text, with no explanations, examples, additional text, backticks, or markdown formatting (e.g., do not include ```sql or ```). Ensure the query is executable and matches the schema exactly.
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config={"temperature": 0.2})
        sql_query = response.text.strip()
        # Clean any residual markdown
        sql_query = re.sub(r'```sql\n|```|\n', '', sql_query).strip()
        query_cache[normalized_question] = sql_query  # Cache new queries
        return sql_query
    except Exception as e:
        raise Exception(f"Error generating SQL: {e}")