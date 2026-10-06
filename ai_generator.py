import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def generate_ai_notes(text, topic, level):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing in the .env file."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert educational notes generator.

Create clear and easy-to-understand study notes from the
following material.

Topic:
{topic}

Student level:
{level}

Source material:
{text}

Generate the notes using this structure:

# {topic}

## 1. Overview
Give a simple introduction.

## 2. Important Concepts
Explain the main concepts clearly.

## 3. Key Points
Give important points in bullet form.

## 4. Detailed Explanation
Explain the topic in simple language.

## 5. Important Terms
List important terms and their meanings.

## 6. Examples
Give useful examples where appropriate.

## 7. Quick Revision
Give a short revision section.

## 8. Possible Exam Questions
Give 5 useful questions.

Keep the language simple and suitable for students.
Do not invent facts that are not supported by the source material.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text