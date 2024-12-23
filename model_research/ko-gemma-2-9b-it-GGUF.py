import pandas as pd
from datasets import load_dataset
from llama_cpp import Llama
from evaluate import load
from tqdm import tqdm

# tokenizer = LlamaTokenizer.from_pretrained("tensorblock/ko-gemma-2-9b-it-GGUF")
# model = LlamaForCausalLM.from_pretrained(
#     repo_id="tensorblock/ko-gemma-2-9b-it-GGUF",
#     filename="ko-gemma-2-9b-it-Q4_K_M.gguf",
#     device_map="auto"
# )

llm = Llama.from_pretrained(
    repo_id="tensorblock/ko-gemma-2-9b-it-GGUF",
    filename="ko-gemma-2-9b-it-Q4_K_M.gguf",
    n_ctx=2048
)

dataset = load_dataset("HAERAE-HUB/KMMLU-HARD", "accounting", split="test[:5%]")
print(dataset.column_names)
print("Sample data:", dataset[0])
print("A:", dataset[0]['A'])
print("CoT:", dataset[0]['cot'])
print("Question:", dataset[0]['question'])
print("Answer", dataset[0]['answer'])

# metric = load("rouge")

def evaluate(model, dataset):
    print("Start evaluating QA")

    references = []
    predictions = []

    choice_to_number = {'A':1, 'B':2, 'C':3, 'D':4}

    for data in tqdm(dataset, total=len(dataset)):
        question = data['question']
        A = data['A']
        B = data['B']
        C = data['C']
        D = data['D']
        answer = data.get('answer', None)

        if answer is None:
            print("Missing answer in data.")
            continue
        else:
            answer = int(answer)

        system_message = f"""
            너는 회계 질문에 대한 답을 하는 어시스턴트야. 주어진 질문에 대해 A, B, C, D 중에서 정답을 선택하고, 오직 그 답만 한 글자로 답변해줘.
            
            다음은 예시야:
            Question: 수정 전 잔액시산표의 차변 합계액은 1,000,000원이다. 보혐료 미경과액 30,000원과 이자수의 미수액 20,000원을 계산한 후의 수정 후 잔액시산표 차변 합계액은 얼마인가?
            A: 970,000원
            B: 990,000원
            C: 1,020,000원
            D: 1,050,000원
            
            [모델은 내부적으로 생각합니다.]
            - 보험료 미경과액은 차변의 비용을 감소시키고 자산인 선급보험료를 증가시키므로 차변 합계에는 영향이 없음.
            - 이자수익 미수액은 차변에 자산으로 추가되므로 차변 합계액에 20,000원이 증가함.
            - 따라서 수정 후 차변 합계액은 1,000,000원 + 20,000원 = 1,020,000원.
            - 정답은 C.
            
            최종 답변: C
            
        """
        user_message = f"Question: {question}\nA: {A}\nB: {B}\nC: {C}\nD: {D}\nAnswer"

        try:
            response = model.create_chat_completion(
                max_tokens=128,
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_message
                    },
                ]
            )

            generated_answer = response['choices'][0]['message']['content'].strip().upper()
            print("generated Answer:", generated_answer)

        except Exception as e:
            print(f"Error during model generation: {e}")
            generated_answer = ''

        if generated_answer in ['A', 'B', 'C', 'D']:
            predicted_number = choice_to_number[generated_answer]
            predictions.append(predicted_number)
            references.append(answer)
        else:
            print(f"Unexpected model response: {generated_answer}")
            continue

    if not predictions or not references:
        print("유효한 예측과 참조가 없습니다.")
        return None

    print(f"Number of valid answers: {len(predictions)}")
    print(f"Number of valid references: {len(references)}")

    correct = sum([1 for pred, ref in zip(predictions, references) if pred == ref])
    total = len(predictions)
    accuracy = correct / total if total > 0 else 0
    print(f"Accuracy: {accuracy * 100: .2f}%")

    df = pd.DataFrame({'Generated Answer': predictions,
                        'Reference Answer': references})
    print("Processing to make dataframe to csv...")
    df.to_csv('./evaluation_results.csv', index=False)
    print("Process completed")

    return {'accuracy': accuracy}

score = evaluate(llm, dataset)
print("Model:", llm)
print("Score:", score)

with open("model_accuracy_score.txt", "w") as f:
    f.write(str(score))
print("Complete to save rouge score in model_rouge_score.txt")