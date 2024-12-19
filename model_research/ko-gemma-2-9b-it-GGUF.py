from llama_cpp import Llama
from datasets import load_dataset
from evaluate import load
from transformers import pipeline
from tqdm import tqdm
import pandas as pd

llm = Llama.from_pretrained(
    repo_id="tensorblock/ko-gemma-2-9b-it-GGUF",
    filename="ko-gemma-2-9b-it-Q4_K_M.gguf",
)

dataset = load_dataset("HAERAE-HUB/KMMLU-HARD", "accounting", split="test[:5%]")
print(dataset.column_names)
print("Sample data:", dataset[0])
print("Question:", dataset[0]['question'])
print("Answer:", dataset[0]['answer'])
metric = load("rouge")

def evaluate(model_name, dataset):
    print("Start evaluating QA")
    pipe = pipeline(
        task="text-generation",
        model=model_name,
        device_map="auto",
    )
    pipe.model.eval()

    references = []
    answers = []

    for data in tqdm(dataset, total=len(dataset)):
        question = data['question']
        answer_reference = data['answer']

        prompt =f"너는 주어진 question을 이용해서 사용자의 질문에 대답해주는 질의응답 어시스턴트야.\n"\
                f"You are a assistant that helps users by using given question.\n"\
                f"Question: {question}\nAnswer:"

        generated = pipe(
            prompt,
            max_new_tokens=2048,
            temperature=0.3,
            top_p=0.9,
            eos_token_id=pipe.tokenizer.eos_token_id
        )

        # prompt = pipe.tokenizer.apply_chat_template(
        #     message,
        #     tokenize=False,
        #     add_generation_prompt=True
        # )

        # terminators = [
        #     pipe.tokenizer.eos_token_id,
        #     pipe.tokenizer.convert_tokens_to_ids("<end_of_turn>")
        # ]

        # answer = pipe(
        #     prompt,
        #     max_new_tokens=2048,
        #     eos_token_id=terminators,
        #     temperature=0.3,
        #     top_p=0.9
        # )

        generated_text = generated[0]['generated_text'][len(prompt):].strip()
        print("Generated Answer:", generated_text)
        answers.append(generated_text)
        references.append(answer_reference)

        # print("answer:", answer[0]['generated_text'][len(prompt):])
        #
        # answers.append(answer[0]['generated_text'][len(prompt):])
        # references.append(data['answer'])

    df = pd.DataFrame(list(zip(answers, references)), columns=['Generated Answer', 'Reference Answer'])
    print("Processing to make dataframe to csv...")
    model_name_str = model_name.split("/")[-1]
    df.to_csv(f'./{model_name_str}.csv', index=False)
    print("Process completed")

    score = metric.compute(predictions=answers, references=references)

    return score

model_name_str = "ko-gemma-2-9b-it"
score = evaluate(model_name_str, dataset)
print("Model:", model_name_str)
print("Score:", score)
with open(f"{model_name_str}.txt", "w") as f:
    f.write(f"{score}")
print(f"Complete to save {model_name_str} rouge score in {model_name_str}.txt")

# response = llm.create_chat_completion(
#     messages = [
#         {
#             "role": "system",
#             "content": "You are a helpful assistant."
#         },
#         {
#             "role": "user",
#             "content": "What is the capital of France?"
#
#         }
#     ]
# )
#
# output = response['choices'][0]['message']['content']
# print(output)