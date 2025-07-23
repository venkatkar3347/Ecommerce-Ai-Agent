def interpret_response(question, result):
    normalized_question = question.lower().strip()
    if "total sales" in normalized_question:
        total = sum(row[0] for row in result) if result else 0
        return f"Your total sales amount is {total:.2f}."
    elif "roas" in normalized_question:
        roas = result[0][0] if result else 0
        return f"Your Return on Ad Spend (RoAS) is {roas:.2f}."
    elif "highest cpc" in normalized_question:
        product, cpc = result[0] if result else ("Unknown", 0)
        return f"The product with the highest CPC is {product} with a CPC of {cpc}."
    elif "eligible products" in normalized_question:
        products = [row[0] for row in result] if result else []
        return f"Eligible products: {', '.join(products) if products else 'None'}."
    else:
        return f"Result for '{question}': {result}"