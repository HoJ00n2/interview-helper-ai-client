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
    당신은 기업의 면접관입니다. 답변자의 {user_input}과 관련하여 꼬리 질문을 해야합니다.
    만약 답변자의 입력값이 카테고리라면 그와 관련한 질문으로 면접을 시작합니다.
    만약 답변자의 입력값이 질문에 대한 답이라면 입력값과 관련한 꼬리 질문을 생성해도 되고, 처음 카테고리와 관련한 새로운 질문을 해도 됩니다.
    
    다음은 예시입니다:
    <usr>
    성격
    <bot>
    당신의 성격의 장점이 무엇인가요?
    
    <usr>
    저는 시간을 잘 지킨다는 장점이 있습니다.
    <bot>
    시간을 잘 지키는 것이 업무를 하는데 있어서 어떤 긍정적인 영향을 미치나요?
    
    <usr>
    시간을 지킴으로 사람들과 원할한 커뮤니케이션이 가능하고 이것이 업무적 성과에 긍정적 영향을 미친다고 생각합니다.
    <bot>
    당신의 성격의 단점이 무엇인가요?
    
    
    이런식으로 꼬리질문 혹은 답변자가 선택한 카테고리에 맞는 질문을 하면 됩니다.
    답변: {user_input}
    """

    try:
        output = llm(
            prompt=prompt,
            max_tokens=256,
            echo=False
        )
        response= output['choices'][0]['text']
        return response
    except Exception as e:
        return f"Error generating question: {e}"

def main():
    print("모의 면접 서비스에 오신 것을 환영합니다!")
    print("원하는 질문 카테고리 또는 답변을 입력하세요. 종료하려면 '끝'을 입력하세요.")

    while True:
        user_input = input("입력 : ")

        if user_input in ["끝", "종료"]:
            print("모의 면접을 종료합니다. 수고하셨습니다!")
            break

        if user_input:
            question = generate_interview_question(user_input)
            print(f"면접 질문: {question}")
        else:
            print("입력이 비어 있습니다. 다시 입력해주세요.")

if __name__=="__main__":
    main()

