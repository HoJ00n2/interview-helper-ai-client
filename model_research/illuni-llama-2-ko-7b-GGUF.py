from llama_cpp import Llama
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

llm = Llama.from_pretrained(
    repo_id="tensorblock/illuni-llama-2-ko-7b-GGUF",
    filename="illuni-llama-2-ko-7b-Q4_K_M.gguf"
)

def generate_interview_question(user_input):
    """
    Generates interview questions based on the user's input.
    """
    prompt = f"""
    You are an interviewer at a company, and the user is the interviewee.
    Generate questions based on the user's input:
    - If the input is a categroy (e.g., personality, communication, etc.), ask a question related to that category.
    - If the input is a response in sentence form, ask a follow-up question or create a new question based on the response.
    Do not output any content other than the question.
    User input: {user_input}
    """

    output = llm(
        prompt=prompt,
        max_tokens=256,
        echo=False
    )
    return output['choices'][0]['text'].strip()


user_input = input("Enter an interview category or response: ").strip()

if not user_input:
    print("Input is empty. Please provide a category or response.")
else:
    question = generate_interview_question(user_input)
    print(f"Interview Question: {question}")