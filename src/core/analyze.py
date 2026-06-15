import json
from os import getenv

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=getenv("GROQ")
)


def generate_local_insights(report):

    insights = []

    vendors = report.get("vendors", [])

    if vendors:

        top_vendor = vendors[0]

        insights.append({
            "source": "local",
            "text": (
                f"Highest spending vendor is "
                f"{top_vendor['vendor']}"
            )
        })

    summary = report["summary"]

    invoice_count = summary["invoice_count"]
    total_spend = summary["total_spend"]
    total_vat = summary["total_vat"]

    status = report["approval_status"]

    pending = status["pending"]
    rejected = status["rejected"]

    if pending > 0 and invoice_count > 0:

        percent = round(
            (pending / invoice_count) * 100,
            1
        )

        insights.append({
            "source": "local",
            "text": (
                f"{percent}% of invoices are "
                f"still pending approval"
            )
        })

    if rejected > 0:

        insights.append({
            "source": "local",
            "text": (
                f"{rejected} invoices have "
                f"been rejected"
            )
        })

    insights.append({
        "source": "local",
        "text": (
            f"Total recorded spend is "
            f"{total_spend:.2f}"
        )
    })

    insights.append({
        "source": "local",
        "text": (
            f"Total VAT recorded is "
            f"{total_vat:.2f}"
        )
    })

    return insights


def generate_ai_insights(report):

    prompt = f"""
You are a financial analyst.

Review the following invoice report and provide exactly 3 concise business insights.

Focus on:
- spending trends
- approval bottlenecks
- vendor concentration
- unusual observations

Return only plain text bullet points.

Report:

{json.dumps(report, indent=2)}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        lines = [
            line.strip("-• ").strip()
            for line in content.splitlines()
            if line.strip()
        ]

        return [
            {
                "source": "ai",
                "text": line
            }
            for line in lines[:5]
        ]

    except Exception as err:

        return [{
            "source": "ai",
            "text": (
                f"AI analysis unavailable: "
                f"{str(err)}"
            )
        }]