import streamlit as st
import uuid
import firebase_admin
from firebase_admin import credentials, db
import openai
import json
import random
import requests
from base64 import b64encode

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# Load secrets from Streamlit secrets
secrets = st.secrets

# GitHub 토큰 및 레포지토리 정보
GITHUB_TOKEN = secrets["MY_GITHUB_TOKEN"]
GITHUB_REPO = "your-username/student-apps"

# API 키 리스트
api_keys = [
    secrets["api_key1"],
    secrets["api_key2"],
    secrets["api_key3"],
    secrets["api_key4"],
    secrets["api_key5"],
    secrets["api_key6"],
    secrets["api_key7"],
    secrets["api_key8"],
    secrets["api_key9"],
    secrets["api_key10"],
    secrets["api_key11"],
    secrets["api_key12"]
]

# 랜덤하게 API 키 선택
selected_api_key = random.choice(api_keys)
openai.api_key = selected_api_key

# Firebase 초기화
if not firebase_admin._apps:
    firebase_credentials_json = secrets["firebase_credentials_json"]
    cred_data = json.loads(firebase_credentials_json)
    cred = credentials.Certificate(cred_data)
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://metawebapp-10956-default-rtdb.firebaseio.com/'})

# Streamlit 페이지 설정
st.title("교사용 AI 수업 도구 생성기")

# 교사가 인공지능의 필요성을 입력
teacher_request = st.text_area("어떤 인공지능을 만들고 싶으신가요?")

# 앱 타입 선택
app_type = st.selectbox("앱 타입을 선택하세요:", ["텍스트 생성", "이미지 생성", "이미지 분석", "챗봇"])

def create_and_push_app(app_id, app_code):
    app_path = f"apps/{app_id}/app.py"

    # GitHub API를 사용하여 파일 추가 및 커밋
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{app_path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Add new app {app_id}",
        "content": b64encode(app_code.encode("utf-8")).decode("utf-8"),
        "branch": "main"
    }

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

# 앱 생성 및 배포
if st.button("앱 생성"):
    app_id = str(uuid.uuid4())
    system_prompt = f"""
### 기능 설명
- assistant는 주어진 "요청"을 바탕으로 GPT가 효율적으로 작동하기 위한 "시스템 프롬프트"로 수정한다.
- "시스템 프롬프트"는 학생을 위한 GPT-API 기반 챗봇의 시스템 프롬프트이다.
- 수정될 프롬프트는 구조별로 식별부호 ##를 사용한다.
- text로 표현이 어려운 개념이나 역사적 사건의 연대는 명확하게 설명하도록 한다.
- 시스템 프롬프트의 구조에는 대화 설정, 규칙, 대화 과정, 필요한 예시를 포함한다.

### 시스템 프롬프트의 예

## 대화 설정:
- assistant는 친절하고 명확한 설명을 제공하며, 사회과학 지식이 풍부해야 함.
- 대화의 목적은 user가 사회과학 개념과 역사적 사건을 숙달하는 것임.
- 출력에는 제시한 질문의 답변을 명확하게 포함한다.

## 규칙:
- 다양한 주제의 사회과학 질문을 학생에게 제시하도록 함.
- 질문을 제시할 때 답변을 HTML 주석 태그 (<!-- -->)를 사용하여 숨김 처리하도록 함.
- 중요한 개념이나 연대를 정확히 설명하도록 지시함.
- 답변의 정확성을 유지하도록 함.

## 대화 과정:
- user가 정답을 맞출 경우 칭찬하고 다음 질문으로 넘어감.
- user가 오답을 제시하면 힌트를 제공하고, 필요시 추가 설명을 제시함.
- user가 특정 개념을 이해하기 어려워하면, 추가 예시나 설명을 제공하도록 함.
- user가 대화를 종료하려 할 때, 학습한 내용을 요약하고 채점 결과와 통계를 제공하도록 함.
- user가 잘못된 정보를 고집할 경우, 단호하게 바로잡고, 대화 목적과 관련 없는 대화를 거절하도록 지시함.

## user가 정답을 입력한 경우 대화 예시:
- 프랑스 혁명은 언제 일어났을까요? <!-- 1789년 -->
- 1789년입니다.
- 잘했어요. 이제 다음 질문을 풀어볼까요?

## user가 오답을 입력한 경우 대화 예시:
- 산업 혁명이 시작된 나라는 어디일까요? <!-- 영국 -->
- 모르겠어요.
- 산업 혁명은 18세기 후반에 시작되었고, 이 나라는 세계 최초로 대규모 기계화가 이루어졌어요.
- 영국입니다.
- 맞아요. 이제 다음 질문을 풀어볼까요?

### 요청
{teacher_request}
"""

    app_code = f'''
import streamlit as st
import openai
import random
import os

st.set_page_config(layout="wide")

secrets = st.secrets

api_keys = [
    secrets["api_key1"],
    secrets["api_key2"],
    secrets["api_key3"],
    secrets["api_key4"],
    secrets["api_key5"],
    secrets["api_key6"],
    secrets["api_key7"],
    secrets["api_key8"],
    secrets["api_key9"],
    secrets["api_key10"],
    secrets["api_key11"],
    secrets["api_key12"]
]

selected_api_key = random.choice(api_keys)
openai.api_key = selected_api_key

st.title("학생용 AI 수업 도구")

system_prompt = """{system_prompt}"""

st.header("추가 프롬프트를 입력하세요:")
student_prompt = st.text_area("추가 프롬프트")

st.header("결과:")
if st.button("생성"):
    combined_prompt = system_prompt + " " + student_prompt
    if "{app_type}" == "텍스트 생성" or "{app_type}" == "챗봇":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {{"role": "system", "content": system_prompt}},
                {{"role": "user", "content": combined_prompt}}
            ]
        )
        st.write(response.choices[0].message['content'])
    
    elif "{app_type}" == "이미지 생성":
        response = openai.Image.create(
            prompt=combined_prompt,
            n=1,
            size="1024x1024"
        )
        st.image(response['data'][0]['url'])
    
    elif "{app_type}" == "이미지 분석":
        uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            response = openai.Image.create(
                prompt="Analyze this image: " + combined_prompt,
                n=1,
                size="1024x1024"
            )
            st.image(response['data'][0]['url'])
    '''

    create_and_push_app(app_id, app_code)
    st.success(f"앱이 생성되었습니다! 앱 ID: {app_id}")
    st.info(f"앱이 자동으로 배포되고 있습니다. 배포 완료 후 URL을 공유하겠습니다.")

# 예제 프롬프트와 앱 타입 제공
st.sidebar.header("예제 데이터")
if st.sidebar.button("예제 데이터 로드"):
    st.session_state['teacher_request'] = "교육에서 인공지능의 활용 가능성에 대해 설명하세요."
    st.session_state['app_type'] = "텍스트 생성"

if 'teacher_request' in st.session_state:
    st.text_area("요청", value=st.session_state['teacher_request'], key="teacher_request_example")
if 'app_type' in st.session_state:
    st.selectbox("앱 타입", ["텍스트 생성", "이미지 생성", "이미지 분석", "챗봇"], index=["텍스트 생성", "이미지 생성", "이미지 분석", "챗봇"].index(st.session_state['app_type']), key="app_type_example")
