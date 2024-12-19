from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("illuni/illuni-llama-2-ko-7b")
model = AutoModelForCausalLM.from_pretrained("illuni/illuni-llama-2-ko-7b")

pipe = pipeline("text-generation",
                model=model,
                tokenizer=tokenizer,
                device_map="auto")

context = input("면접 질문의 카테고리나 답변을 입력하세요: ").strip()
if not context:
    print("입력값이 비어 있습니다. 카테고리나 대답을 입력해주세요.")
    exit()

prompt = f"""
당신은 기업의 면접관입니다. 사용자의 입력에 따라 질문하세요:
1. 입력값이 카테고리라면, 해당 카테고리에 맞는 질문을 합니다.
2. 입력값이 대답이라면, 그 대답에 맞는 꼬리 질문을 하거나 새 질문을 합니다.
다른 내용은 출력하지 마세요.
입력값: {context}
"""

sequences = pipe(
    prompt,
    max_new_tokens=50,
    do_sample=True,
    top_k=50,
    top_p=0.9,
    return_full_text=False,
)

for i, seq in enumerate(sequences, start=1):
    print(f"[질문 {i}]: {seq['generated_text'].strip()}")