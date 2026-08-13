import os
import gradio as gr
from google import genai

# Get Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("IQG")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash"


SYSTEM_PROMPT = """
You are an Interactive Study Assistant.

Your job is to help students learn concepts clearly.

You can:
- Explain difficult concepts
- Generate MCQ questions
- Generate short-answer questions
- Create quizzes
- Give answers and explanations
- Create study notes
- Summarize topics
- Give examples
- Help students revise

Always:
- Use simple English
- Explain step by step
- Be friendly and encouraging
- Give examples when useful
"""


def ask_gemini(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=SYSTEM_PROMPT + "\n\nStudent request:\n" + prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error: {str(e)}"


def study_assistant(topic, action):

    if not topic.strip():
        return "⚠️ Please enter a topic."

    prompt = f"""
Topic:
{topic}

Student wants:
{action}

Give a clear and useful response.
"""

    return ask_gemini(prompt)


with gr.Blocks(
    title="Interactive Study Assistant",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # 🎓 Interactive Study Assistant

        ### Learn • Practice • Revise

        Your AI-powered study assistant using Google Gemini.
        """
    )

    topic = gr.Textbox(
        label="📚 Enter Your Topic",
        placeholder="Example: Probability, Python, DBMS, Data Structures..."
    )

    action = gr.Dropdown(
        choices=[
            "Explain the topic",
            "Generate MCQ quiz",
            "Generate short-answer questions",
            "Create study notes",
            "Summarize the topic",
            "Give examples",
            "Help me revise"
        ],
        value="Explain the topic",
        label="🎯 What do you want to do?"
    )

    button = gr.Button(
        "🚀 Start Learning",
        variant="primary"
    )

    output = gr.Markdown(
        "Your answer will appear here."
    )

    button.click(
        fn=study_assistant,
        inputs=[topic, action],
        outputs=output
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
