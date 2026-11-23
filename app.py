import streamlit as st
import pandas as pd

# 1. 시작: 페이지 기본 설정
st.set_page_config(page_title="영화 관람 등급 및 주의 요소 가이드", page_icon="🎬")
st.title("🎬 영화 관람 등급 판별 및 콘텐츠 주의 요소 가이드")
st.write("관람할 영화와 나이를 선택하면 개인 맞춤형 위험도 점수와 주의 요소를 분석합니다.")

# 2. 데이터 구조(리스트): 영화별 등급 정보와 주의 요소 데이터를 리스트로 구성
movie_list = [
    ["명량", 15, 75, "중", "폭력성 및 잔인함"],
    ["곤지암", 15, 75, "중", "무서움"],
    ["범죄도시", 19, 85, "상", "과도한 폭력성 및 유혈 묘사"],
    ["부산행", 15, 70, "중", "공포감 및 긴장감"],
    ["기생충", 15, 65, "중", "선정성 및 폭력성"],
    ["파묘", 15, 75, "중", "공포 및 오컬트적 기괴함"],
    ["인사이드 아웃 2", 0, 15, "하", "특이사항 없음 (전체관람가)"]
]

# 4. 함수(def): 영화 이름과 나이를 매개변수로 받아 위험도 점수와 경고문 리턴
def check_risk(mov_name, age):
    score = 0
    warning_msg = ""
    movie_grade = 0
    reason = ""

    for movie in movie_list:
        if movie[0] == mov_name:
            movie_grade = movie[1]
            score = movie[2]
            reason = movie[4]
            break

    if reason == "특이사항 없음 (전체관람가)":
        warning_msg = f"'{mov_name}'은(는) 모든 연령이 안심하고 관람할 수 있는 영화입니다."
    else:
        warning_msg = f"영화 관람 시 {reason}에 주의가 필요합니다."

    # 조건문(if-elif-else): 나이에 따라 점수를 폭넓게 조절
    if age <= 7:
        score += 15  # 7세 이하: +15점 가산
        warning_msg += " [어린이 시청 경고: 보호자의 각별한 지도가 필요합니다.]"
        if mov_name == "곤지암":
            warning_msg += " 특히 '곤지암'은 공포 수위가 매우 높아 7세 이하 어린이 시청을 강력히 제한합니다!"
    elif age < movie_grade:
        score += 10  # 관람 등급 미만: +10점 가산
        warning_msg += f" [관람 등급 제한: 만 {movie_grade}세 이상 관람가 영화입니다.]"
    else:
        score -= 15  # 관람 등급 충족(성인 등): 위험도 -15점 감산
        if score < 0:
            score = 0
        warning_msg += " [연령 기준 충족: 관람 가능한 연령입니다.]"

    if score > 100:
        score = 100

    return score, warning_msg

# 3. 입력 받기
st.subheader("1. 영화 및 연령 정보 입력")
movie_titles = [movie[0] for movie in movie_list]
selected_movie = st.selectbox("영화를 선택하세요:", movie_titles)
user_age = st.slider("관람자의 만 나이를 입력하세요:", min_value=1, max_value=100, value=15)

# 4 & 5. 버튼 클릭 시 결과 출력
if st.button("위험도 분석하기", type="primary"):
    st.divider()
    st.subheader("2. 개인 맞춤 분석 결과")

    risk_score, alert_message = check_risk(selected_movie, user_age)
    st.metric(label="심약자 위험도 점수", value=f"{risk_score}점")

    if user_age <= 7 or risk_score >= 70:
        st.error(f"🚨 {alert_message}")
    elif risk_score >= 40:
        st.warning(f"⚠️ {alert_message}")
    else:
        st.success(f"✅ {alert_message}")

    # 6. 반복 출력
    st.subheader("3. 주의해야 할 영화 목록")
    table_data = []
    for movie in movie_list:
        if movie[3] in ["상", "중"]:
            table_data.append({
                "영화명": movie[0],
                "위험도": movie[3],
