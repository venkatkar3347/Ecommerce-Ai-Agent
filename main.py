from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from sql_generator.sql_generator import convert_to_sql
from utils.interpreter import interpret_response
from utils.visualizer import create_chart

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_agent(query: Query):
    try:
        # Convert question to SQL using Gemini
        sql = convert_to_sql(query.question)
        
        # Execute SQL query
        conn = sqlite3.connect("db/ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Get column names
        conn.close()
        
        # Interpret result into human-readable response
        response = interpret_response(query.question, result)
        
        # Generate chart for specific queries
        chart_path = None
        if "total sales" in query.question.lower() or "highest cpc" in query.question.lower():
            chart_path = create_chart(result, columns, query.question)
        
        return {"answer": response, "sql_query": sql, "raw_result": result, "chart": chart_path}
    except Exception as e:
        return {"error": f"Failed to process query: {e}"}