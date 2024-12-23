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
            Answer: C
            답이 C가 되는 근거: 차근 차근 생각해봅시다. 회계학 관련 정보를 위해 위키피디아를 참조하겠습니다. 주어진 문제는 수정 후 시산표의 합계에 영향을 주는 요소와 주지 않는 요소를 구분하고 이해하는 문제입니다.
            이 경우, 보험료 미경과액과 이자수익 미수액이 추가되었습니다. 보험료 미경과액은 차변에 계상되어 있는 보험료(비용)을 감소하면서 자산계정인 선급보험료가 동일금액이 차변에 증가하므로 영향을 주지 않습니다.
            다음으로 이자수익 미수액 20,000원은 아직 받지 않은 이자를 의미합니다. 이자미수액은 잔액시산표에서 차변이 기록됩니다.
            원래의 차변 합계액 1,000,000원에 이자 수익 미수액 20,000원을 더하면, 수정 후의 차변 합계액은 1,020,000원이 됩니다. 따라서, 정답은 C입니다.
            
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