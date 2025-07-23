import plotly.graph_objects as go
import os

def create_chart(result, columns, question):
    try:
        os.makedirs("charts", exist_ok=True)
        normalized_question = question.lower().strip()
        if "total sales" in normalized_question:
            total = sum(row[0] for row in result) if result else 0
            fig = go.Figure(data=[
                go.Bar(x=["Total Sales"], y=[total], marker_color="#1f77b4")
            ])
            fig.update_layout(title="Total Sales", xaxis_title="Metric", yaxis_title="Amount")
        elif "highest cpc" in normalized_question:
            product, cpc = result[0] if result else ("Unknown", 0)
            fig = go.Figure(data=[
                go.Bar(x=[product], y=[cpc], marker_color="#1f77b4")
            ])
            fig.update_layout(title="Highest CPC", xaxis_title="Product", yaxis_title="CPC")
        else:
            return None
        output_path = "charts/output.html"
        fig.write_html(output_path)
        return output_path
    except Exception as e:
        return f"Error creating chart: {e}"