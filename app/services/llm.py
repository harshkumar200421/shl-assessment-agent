import google.generativeai as genai

from app.core.config import GEMINI_API_KEY


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please set it in your environment variables."
    )


genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)


def generate(prompt: str) -> str:
    """
    Generate a response from Gemini.
    """

    try:

        response = model.generate_content(
            prompt
        )

        if response.text:
            return response.text

        return '{"reply":"No response generated.","recommendations":[]}'

    except Exception as e:

        print("Gemini Error:", str(e))

        return f"""{{
    "reply":"Unable to generate recommendation at this moment.",
    "needs_clarification":false,
    "clarification_question":"",
    "recommendations":[],
    "end_of_conversation":false
}}"""