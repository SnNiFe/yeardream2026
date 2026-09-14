import json
import os
import re

from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage, messages_from_dict, messages_to_dict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

DIARY_FILE = 'diary_history.json'
HISTORY_FILE = 'chat_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return messages_from_dict(data)
        except Exception as e:
            print(f'기록 로드 실패, 새로 기록합니다: {e}')
            return []
    return []
def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages_to_dict(history), f, ensure_ascii=False, indent=2)

def load_diaries():
    if os.path.exists(DIARY_FILE):
        try:
            with open(DIARY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"일기 로드 실패: {e}")
            return []
    return []

def save_all_diaries(diaries):
    with open(DIARY_FILE, "w", encoding="utf-8") as f:
        json.dump(diaries, f, ensure_ascii=False, indent=2)

def get_saved_diaries_str():
    diaries = load_diaries()
    if not diaries:
        return "(현재 등록된 일정이 없습니다)"
    lines = []
    for d in diaries:
        d_id = d.get('id', '-')
        lines.append(f"{d_id}번: {d.get('time', '')} | {d.get('place', '')} | {d.get('action', '')}")
    return "\n".join(lines)

# ADD, UPDATE, DELETE 분기 처리 함수
def extract_and_save_diary(text: str):
    diaries = load_diaries()
    changed = False

    # 1. 다중 삭제 (DELETE) 처리
    # re.findall은 매칭되는 모든 ID 문자열 리스트를 가져옵니다: ['1', '2']
    delete_ids = re.findall(r"\[DIARY_DELETE:\s*(\d+)\s*\]", text)
    if delete_ids:
        del_ids_set = {int(i) for i in delete_ids}
        diaries = [d for d in diaries if d.get('id') not in del_ids_set]
        changed = True
        print(f"일정 다중 삭제 완료 (IDs: {del_ids_set})")

    # 2. 다중 수정 (UPDATE) 처리
    # (ID, 시간, 장소, 내용) 튜플 리스트를 가져옵니다
    updates = re.findall(r"\[DIARY_UPDATE:\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\]", text)
    for u in updates:
        target_id = int(u[0].strip())
        for d in diaries:
            if d.get('id') == target_id:
                d['time'] = u[1].strip()
                d['place'] = u[2].strip()
                d['action'] = u[3].strip()
                d['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                changed = True
                print(f"일정 수정 완료 (ID: {target_id})")

    # 3. 다중 추가 (ADD) 처리
    adds = re.findall(r"\[DIARY_ADD:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\]", text)
    for a in adds:
        next_id = max([d.get('id', 0) for d in diaries], default=0) + 1
        new_entry = {
            "id": next_id,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time": a[0].strip(),
            "place": a[1].strip(),
            "action": a[2].strip(),
        }
        diaries.append(new_entry)
        changed = True
        print(f"일정 추가 완료 (ID: {next_id})")

    # 변경사항이 하나라도 있으면 파일에 일괄 저장
    if changed:
        save_all_diaries(diaries)

conversation_history = load_history()
print(f'기록 {len(conversation_history)}개 로드 완료.')

model =ChatOllama(model="exaone3.5:2.4b", temperature=0) # qwen3:1.7b # exaone3.5:2.4b

WEEKDAYS = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
now = datetime.now()
today_str = f"{now.strftime('%Y년 %m월 %d일')} {WEEKDAYS[now.weekday()]}"

bot_prompt = f"""
    당신은 일정 정리 비서 AI입니다.
    오늘 날짜: {today_str}

    [현재 등록된 일정 목록]
    {{saved_diaries}}

    [기본 규칙]
    1. 오늘 날짜를 기준으로 일정을 계산하며, 요일 계산이 모호하면 사용자에게 날짜(YYYY-MM-DD)를 직접 물어보세요.
    2. 현재 등록된 일정을 물어볼 때는 태그 없이 일반 텍스트로만 친절하게 알려주세요.
    3. 일정을 새로 '추가', '수정', '삭제'할 때만 답변 맨 마지막 줄에 아래 태그를 정확히 한 줄 출력하세요.
    4. '답변:', 'AI:' 같은 접두어 라벨은 붙이지 마세요.
    5. 물어보지 않은 부분은 답변하지 마세요.

    [작업 태그 형식]
    - 추가: [DIARY_ADD: YYYY-MM-DD HH:MM | 장소 | 행동]
    - 수정: [DIARY_UPDATE: ID | YYYY-MM-DD HH:MM | 장소 | 행동]
    - 삭제: [DIARY_DELETE: ID]

    [대화 예시]
    사용자: 오늘 무슨 일정 있어?
    오늘 12시에 당산역에서 점심 약속이 등록되어 있어요!

    사용자: 내일 2시에 강남역에서 약속 있어.
    내일 강남역 약속을 등록해 둘게요.
    [DIARY_ADD: 2026-09-15 14:00 | 강남역 | 약속]

    사용자: 1번 일정 장소 사당역으로 바꿔줘.
    1번 일정의 장소를 사당역으로 변경했습니다.
    [DIARY_UPDATE: 1 | 2026-09-15 14:00 | 사당역 | 약속]

    사용자: 2번 일정 취소됐으니 지워줘.
    2번 일정을 삭제했습니다.
    [DIARY_DELETE: 2]
""".strip()

prompt = ChatPromptTemplate.from_messages([
    ("system",bot_prompt),
    MessagesPlaceholder(variable_name="history"), 
    ("user","{query}")
])

chain = prompt|model

def chat_answer(q:str):
    answer = ''
    current_diaries = get_saved_diaries_str()
    inputs = {
        'query': q,
        'history': conversation_history,
        'saved_diaries': current_diaries
    }
    for chunk in chain.stream(inputs):
        answer += chunk.content
        yield chunk.content

    clean_answer = re.sub(r'\[DIARY_(ADD|UPDATE|DELETE):.*?\]', '', answer).strip()

    conversation_history.append(HumanMessage(content=q))
    conversation_history.append(AIMessage(content=clean_answer))
    save_history(conversation_history)

    extract_and_save_diary(answer)
    print(f'history length : {len(conversation_history)}')