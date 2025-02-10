from googlesearch import search  # 구글 검색 결과 가져오기
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 검색어 입력
query = "CS 면접 질문 site:github.com OR site:tistory.com OR site:velog.io"

# 구글 검색 결과에서 URL 가져오기
search_results = search(query, num_results=30)  # 최대 n개 사이트 가져오기

# 크롤링할 URL 리스트
urls = list(search_results)

print(f"총 {len(urls)}개의 URL을 찾았습니다.")

# 크롤링한 데이터를 저장할 리스트
data = []

# 각 사이트 크롤링
for idx, url in enumerate(urls, 1):
    print(f"\n[{idx}] 크롤링 중: {url}")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # 질문이 포함될 가능성이 높은 태그 찾기 (예제: <h2>, <p>, <li> 태그)
            questions = soup.find_all(["h2", "h3"])

            for q in questions: # 상위 10개 말고 전부 크롤링
                # question[:10] 상위 10개만 저장
                # print(f"- {q.text.strip()}") # 상위 10개문서 출력
                question_text = q.text.strip()

                # 답변 담을 변수 <p> <li> 태그
                answer_text = ""
                # 질문 (h2, h3태그) 다음에 올 태그를 답변으로 설정 <p> <li> 태그
                # 그냥 answer_text로하면 bs4 객체 상태라 null값으로 저장됨,
                # 여기서 text를 따로 추출하기 위해 answer_text.text로 해야 answer에 답변이 저장
                answer_text = q.find_next_sibling()
                answer_text = answer_text.text.strip()
                print(f"answer_text : {answer_text}")
                #if next_element and next_element.name in ["p", "li"]:
                # if next_element:
                #     answer_text = next_element.strip()

                # 빈 문자열 제외하고 저장
                if question_text and answer_text:
                    data.append({"question" : question_text, "answer" : answer_text})

            time.sleep(2)  # 너무 빠른 요청 방지
        else:
            print(f"Failed to fetch {url}, Status Code:", response.status_code)

    except Exception as e:
        print(f"크롤링 실패: {e}")

print("\n✅ 모든 검색 결과에서 크롤링 완료!")

# Dataframe으로 바꾼 후 json으로 저장
df = pd.DataFrame(data)

# Json 파일로 저장
df.to_json("cs_interview_question.json", orient="records", force_ascii=False, indent=4)
print("\n Json 파일로 저장 완료")

# 이후 쓸데없는 q/a 경우 생성형 ai에 보내 1차적으로 걸러내고 -> 이땐 rule-based로 했음 cs 단어들을 지정해서
# 하지만 이는 맥락을 이해못할 수 있으므로 요청할 때 LLM을 활용한 의미론적으로 판단해달라고 해야할 듯
# 한 번 검수한 파일을 추가적으로 내가 검수해서 2차적으로 걸러내는 과정을 거침
# 이렇게 얻은 cleaned_cs_interview_question.json