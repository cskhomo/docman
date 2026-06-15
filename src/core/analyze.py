import json
from os import getenv
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=getenv("GROQ"))


def generate_local_insights(report):

    insights = []

    vendors = report["vendors"]

    if vendors:

        biggest_vendor = max(vendors.items(), key=lambda x: x[1])

        insights.append({
            "source": "local",
            "text": f"Highest spending vendor is {biggest_vendor[0]}"
        })

    pending = report["approval_status"]["pending"]
    if pending > 0:
        insights.append({
            "source": "local",
            "text": f"{pending} invoices still require approval"
        })

    rejected = report["approval_status"]["rejected"]
    if rejected > 0:
        insights.append({
            "source": "local",
            "text": f"{rejected} invoices have been rejected"
        })

    total_spend = report["summary"]["total_spend"]

    insights.append({
        "source": "local",
        "text": f"Total recorded spend is {total_spend:.2f}"
    })

    return insights


def generate_ai_insights(report):

    prompt = f"""
You are a financial analyst.

Analyze this report:

{json.dumps(report, indent=4)}

Return ONLY valid JSON:

{{
    "insights": [
        "Insight 1",
        "Insight 2",
        "Insight 3"
    ]
}}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        return [
            {"source": "ai", "text": i}
            for i in parsed.get("insights", [])
        ]

    except Exception as err:

        return [{
            "source": "ai",
            "text": f"AI analysis unavailable: {str(err)}"
        }]