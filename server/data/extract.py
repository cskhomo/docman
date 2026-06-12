import pdfplumber

def pdf_to_markdown(pdf_path, output_path="temp/output.md"):
    markdown = "# Extracted Invoice\n\n"

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):

            text = page.extract_text()

            markdown += f"## Page {i}\n\n"

            if text:
                markdown += text + "\n\n"
            else:
                markdown += "_No extractable text_\n\n"

            # Extract tables if present
            tables = page.extract_tables()

            if tables:
                for table in tables:
                    markdown += table_to_markdown(table)
                    markdown += "\n\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    return markdown


def table_to_markdown(table):
    if not table or len(table) == 0:
        return ""

    # Clean rows
    cleaned = [[cell if cell is not None else "" for cell in row] for row in table]

    header = cleaned[0]
    body = cleaned[1:]

    md = "| " + " | ".join(header) + " |\n"
    md += "| " + " | ".join(["---"] * len(header)) + " |\n"

    for row in body:
        md += "| " + " | ".join(row) + " |\n"

    return md


if __name__ == "__main__":
    result = pdf_to_markdown("temp/invoice.pdf")
    print(result)