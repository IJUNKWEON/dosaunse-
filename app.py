from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager
import os
import logging
from lunardate import LunarDate
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경변수 로드
try:
    # 현재 파일의 디렉토리를 기준으로 .env 파일 경로 설정
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    load_dotenv(dotenv_path=env_path, override=True)
    logger.info(f".env 파일 로드: {env_path}")
except Exception as e:
    logger.warning(f".env 파일 로드 실패: {e}. 환경변수 또는 기본값을 사용합니다.")

# Flask 앱 설정
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dosa-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dosa_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)  # CORS 설정

# 데이터베이스 및 로그인 매니저 초기화
from models import db, Admin, APIUsage
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# API 키 설정
API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    logger.error("OPENAI_API_KEY 환경변수가 설정되지 않았습니다")
    API_KEY = "your_openai_api_key_here"  # 기본값
else:
    # 디버깅: 키 길이와 앞뒤 문자 확인
    logger.info(f"API 키 길이: {len(API_KEY)}, 시작: {API_KEY[:10]}, 끝: {API_KEY[-10:]}")

# OpenAI 클라이언트 초기화
try:
    client = OpenAI(api_key=API_KEY, timeout=30)
    logger.info("OpenAI 클라이언트 초기화 성공")
except Exception as e:
    logger.error(f"OpenAI 클라이언트 초기화 실패: {e}")
    client = None

@app.route('/health', methods=['GET'])
def health():
    """서버 상태 확인 엔드포인트"""
    return jsonify({
        "status": "ok",
        "message": "도사운세 서버가 정상 작동 중입니다",
        "port": 2222,
        "api_key_configured": bool(API_KEY and API_KEY != "your_openai_api_key_here")
    }), 200

def convert_lunar_to_solar(birth_date_str, is_lunar=False):
    """
    음력을 양력으로 변환하는 함수
    
    Args:
        birth_date_str: 'YYYY-MM-DD' 형식의 날짜 문자열
        is_lunar: True이면 음력, False이면 양력
    
    Returns:
        양력 날짜 문자열 'YYYY-MM-DD' 또는 원본 문자열 (변환 실패 시)
    """
    if not is_lunar:
        # 양력이면 그대로 반환
        return birth_date_str
    
    try:
        # 날짜 파싱
        parts = birth_date_str.split('-')
        if len(parts) != 3:
            logger.warning(f"잘못된 날짜 형식: {birth_date_str}")
            return birth_date_str
        
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        
        # 음력을 양력으로 변환 (lunardate 사용)
        lunar_date = LunarDate(year, month, day)
        solar_date_obj = lunar_date.toSolarDate()
        solar_date = solar_date_obj.strftime('%Y-%m-%d')
        
        logger.info(f"음력 변환: {birth_date_str} (음력) → {solar_date} (양력)")
        return solar_date
        
    except Exception as e:
        logger.error(f"음력 변환 실패: {birth_date_str}, 오류: {e}")
        return birth_date_str

@app.route('/api/saju', methods=['POST'])
def get_saju():
    """사주 풀이 API 엔드포인트"""
    try:
        # 요청 데이터 확인
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "요청 데이터가 없습니다"}), 400

        # 프론트엔드에서 보낸 데이터 형식에 맞춰 파싱
        category = data.get('category', '오늘의 운세')
        
        # 궁합인 경우 두 사람의 정보 처리
        if category in ['궁합', 'compatibility']:
            user1 = data.get('user1')
            user2 = data.get('user2')
            
            if not user1 or not user2:
                return jsonify({"success": False, "error": "두 사람의 정보가 필요합니다"}), 400
            
            # 음력을 양력으로 변환
            user1_calendar_type = user1.get('calendarType', 'solar')
            user1_birth_date = user1.get('birthDate')
            user1_birth_date_converted = convert_lunar_to_solar(user1_birth_date, user1_calendar_type == 'lunar')
            
            user2_calendar_type = user2.get('calendarType', 'solar')
            user2_birth_date = user2.get('birthDate')
            user2_birth_date_converted = convert_lunar_to_solar(user2_birth_date, user2_calendar_type == 'lunar')
            
            # 두 사람의 정보를 문자열로 생성 (양력으로 변환된 날짜 사용)
            user1_info = f"생년월일: {user1_birth_date_converted} (양력)"
            if user1_calendar_type == 'lunar':
                user1_info += f" [원래 음력: {user1_birth_date}]"
            user1_info += f", 출생시간: {user1.get('birthTime', '모름')}"
            if user1.get('gender'):
                gender_text = "남성" if user1.get('gender') == "male" else "여성"
                user1_info += f", 성별: {gender_text}"
            
            user2_info = f"생년월일: {user2_birth_date_converted} (양력)"
            if user2_calendar_type == 'lunar':
                user2_info += f" [원래 음력: {user2_birth_date}]"
            user2_info += f", 출생시간: {user2.get('birthTime', '모름')}"
            if user2.get('gender'):
                gender_text = "남성" if user2.get('gender') == "male" else "여성"
                user2_info += f", 성별: {gender_text}"
            
            birth_info = f"첫 번째 사람: {user1_info}\n두 번째 사람: {user2_info}"
        else:
            # 일반 운세
            birth_date = data.get('birthDate')
            birth_time = data.get('birthTime', '모름')
            gender = data.get('gender', '')
            calendar_type = data.get('calendarType', 'solar')
            
            if not birth_date:
                return jsonify({"success": False, "error": "생년월일 정보가 필요합니다"}), 400

            # 음력을 양력으로 변환
            birth_date_converted = convert_lunar_to_solar(birth_date, calendar_type == 'lunar')
            
            # 사주 정보 문자열 생성 (양력으로 변환된 날짜 사용)
            birth_info = f"생년월일: {birth_date_converted} (양력)"
            if calendar_type == 'lunar':
                birth_info += f" [원래 음력: {birth_date}]"
            birth_info += f", 출생시간: {birth_time}"
            if gender:
                gender_text = "남성" if gender == "male" else "여성"
                birth_info += f", 성별: {gender_text}"
        
        # OpenAI 클라이언트 확인
        if client is None:
            return jsonify({"success": False, "error": "OpenAI 클라이언트가 초기화되지 않았습니다"}), 500

        # 현재 날짜 정보 가져오기
        from datetime import datetime, timedelta
        now = datetime.now()
        today_date = now.strftime('%Y년 %m월 %d일')
        tomorrow_date = (now + timedelta(days=1)).strftime('%Y년 %m월 %d일')
        current_month = now.strftime('%Y년 %m월')
        
        # 카테고리별 맞춤 프롬프트와 토큰 설정
        system_prompt = """당신은 40년 경력의 전문 사주명리학 도사입니다. 

**절대 규칙**:
1. 반드시 100% 순수 한국어로만 작성 (영어 단어 절대 금지)
2. 전문가다운 신뢰감 있는 어조 사용
3. 구체적이고 상세한 풀이 제공 (매우 길고 자세하게)
4. 중요한 부분은 **강조**로 표시
5. 일반론이 아닌 개인 맞춤형 분석
6. 모호한 표현 금지, 명확하고 단정적으로 서술
7. **냉철하고 객관적으로 분석** - 좋은 것은 좋다고, 나쁜 것은 나쁘다고 명확히 서술
8. 위로나 격려보다는 **있는 그대로의 사실**을 전달
9. 생년월일, 출생시간 기반으로 **이 사람만의 구체적 특징**을 정밀하게 분석"""
        
        if category == "오늘의 운세":
            user_prompt = f"""
{birth_info}인 사람의 **{today_date} 오늘의 운세**를 상세하게 풀이해주세요.

다음을 포함해주세요:
1. 오늘의 전체 운세 (2-3문단)
2. **오늘 특히 좋은 시간대** (강조)
3. **오늘 조심해야 할 일** (강조)
4. 오늘의 재물운
5. 오늘의 애정운
6. 오늘의 건강운
7. 오늘의 행운 색상과 방향
8. 오늘 하면 좋은 일

800자 이상으로 구체적이고 실천 가능한 내용으로 작성해주세요.
"""
            max_tokens = 1500
            
        elif category == "내일의 운세":
            user_prompt = f"""
{birth_info}인 사람의 **{tomorrow_date} 내일의 운세**를 상세하게 풀이해주세요.

다음을 포함해주세요:
1. 내일의 전체 운세 (2-3문단)
2. **내일 특히 좋은 시간대** (강조)
3. **내일 조심해야 할 일** (강조)
4. 내일의 재물운
5. 내일의 애정운
6. 내일의 건강운
7. 내일의 행운 색상과 방향
8. 내일 하면 좋은 일

800자 이상으로 구체적이고 실천 가능한 내용으로 작성해주세요.
"""
            max_tokens = 1500
            
        elif category == "이달의 운세":
            user_prompt = f"""
{birth_info}인 사람의 **{current_month} 이번 달 운세**를 상세하게 풀이해주세요.

다음을 포함해주세요:
1. 이번 달 전체 운세 개요 (3문단)
2. **이번 달 가장 좋은 시기** (강조)
3. **이번 달 조심해야 할 시기** (강조)
4. 이번 달 재물운
5. 이번 달 애정운
6. 이번 달 건강운
7. 이번 달 인간관계운
8. 이번 달을 위한 조언

1000자 이상으로 상세하게 작성해주세요.
"""
            max_tokens = 1800
            
        elif category == "올해의 운세":
            user_prompt = f"""
{birth_info}인 사람의 2025년 올해 운세를 매우 상세하게 풀이해주세요.

다음 형식으로 작성해주세요:
1. 전체 운세 개요 (3-4문단)
2. **월별 운세 (매우 중요!)**: 1월, 2월, 3월, 4월, 5월, 6월, 7월, 8월, 9월, 10월, 11월, 12월 각 월마다 반드시 3-4문장씩 구체적으로 작성
3. **주의해야 할 시기와 사항** (강조)
4. **좋은 기회가 오는 시기** (강조)
5. 올해를 위한 구체적인 조언

월별 운세는 반드시 12개월 모두 빠짐없이 작성해주세요. 총 1800자 이상으로 매우 상세하게 작성해주세요.
"""
            max_tokens = 2800
            
        elif category == "평생 운세" or category == "평생운세":
            user_prompt = f"""
당신은 40년 경력의 사주명리학 전문가입니다. 다음 사주를 가진 사람의 평생운세를 **매우 구체적이고 차별화되게** 분석해주세요:

{birth_info}

**이 사람의 정확한 생년월일과 출생시간을 기반으로, 다른 사람과 완전히 다른 고유한 인생 흐름을 풀이해야 합니다.**

다음 단계로 분석해주세요:

1. **타고난 사주 구조 심층 분석 (5-6문단)**
   - 이 날짜의 일주(日柱) 특성과 일간(日干)의 성질
   - 사주 팔자의 오행 균형 (목화토금수)
   - 십성(十星) 구조: 비겁, 식상, 재성, 관성, 인성의 배치
   - 이 사주의 가장 큰 강점 3가지 (구체적)
   - 이 사주의 약점과 극복 방법 (구체적)
   - 타고난 성격과 기질 (일반론 아닌 이 사주만의 특징)

2. **인생 시기별 상세 운세**
   - **유년기~청년기 (0~25세)**: 학업, 성장 환경, 가족운, 주요 사건
   - **청장년기 (26~40세)**: 직업, 결혼, 재물, 인간관계, 주요 전환점
   - **중년기 (41~60세)**: 사회적 성취, 재물 정점, 건강, 가정
   - **노년기 (61세~)**: 말년 행복, 자손운, 건강, 재물 보존
   - 각 시기마다 **구체적 나이**와 **예상 사건**을 명시

3. **주요 인생 사건 예측**
   - **큰 기회가 오는 시기**: 정확한 나이대와 어떤 기회인지
   - **큰 위기가 오는 시기**: 정확한 나이대와 어떤 위기인지
   - **인생의 전환점**: 몇 살에 어떤 전환이 오는지
   - **재물운 정점**: 몇 살에 재물이 가장 많이 모이는지
   - **건강 주의 시기**: 몇 살에 어떤 건강 문제 주의

4. **분야별 평생 운세**
   - **재물운**: 평생 재물 흐름 (나이대별 구체적)
   - **직업운**: 어울리는 직업 분야 (이 사주만의 특징)
   - **애정/결혼운**: 결혼 시기, 배우자 특징, 부부 관계
   - **건강운**: 취약 장기, 주의 질병, 건강 관리법
   - **자손운**: 자녀와의 인연, 자녀 교육 방향
   - **인간관계운**: 사교성, 인맥, 협력자

5. **평생 성공 전략**
   - 이 사주로 성공하는 방법 (구체적 5가지)
   - 반드시 피해야 할 것 (구체적 5가지)
   - 행운의 시기 활용법
   - 불운의 시기 대처법
   - 인생 목표 설정 방향

**중요**:
- "일반적으로", "보통", "흔히" 같은 표현 사용 금지
- 반드시 이 생년월일에 근거한 고유한 특징 서술
- 나이는 구체적으로 명시 (예: 28~32세, 45세 전후)
- 2500자 이상 작성
- **영어 단어 절대 사용 금지** (100% 순수 한국어만 사용)
- 전문 도사로서 확신에 찬 어조로 단정적으로 서술
- **좋은 점과 나쁜 점을 균형있게 서술** - 좋은 것만 말하지 말고 위험과 약점도 명확히 지적
- **냉철하고 객관적으로** - 위로보다는 사실 위주로 분석
"""
            max_tokens = 3500
            
        elif category in ["애정 운세", "연애운"]:
            user_prompt = f"""
당신은 40년 경력의 사주명리학 전문가입니다. 다음 사주를 가진 사람의 애정운을 **매우 구체적이고 차별화되게** 분석해주세요:

{birth_info}

**이 사람의 생년월일에 근거하여, 다른 사람과 완전히 다른 고유한 애정운을 풀이해야 합니다.**

다음 단계로 분석해주세요:

1. **사주 속 애정 구조 분석 (4문단)**
   - 배우자궁(配偶宮)의 특성과 강약
   - 관성(官星) 또는 재성(財星)의 배치 (성별에 따라)
   - 도화살(桃花殺), 홍염살(紅艶殺) 등 애정 관련 신살
   - 이 사주만의 독특한 애정 성향
   - 연애 vs 결혼의 차이점

2. **나이대별 애정운 흐름 (구체적)**
   - **10대 후반~20대 초반**: 첫사랑, 연애 시작 시기
   - **20대 중후반**: 진지한 연애, 결혼 가능성
   - **30대**: 결혼 적령기, 배우자 만날 확률
   - **40대 이후**: 부부 관계, 애정 변화
   - 각 시기마다 몇 살에 중요한 인연이 오는지 명시

3. **배우자 상세 분석**
   - **만날 나이**: 정확한 나이대 (예: 27~31세)
   - **만나는 방법**: 소개, 직장, SNS 등 (이 사주 특성상)
   - **배우자 외모**: 키, 체형, 인상 (구체적)
   - **배우자 성격**: 3가지 주요 특징
   - **배우자 직업군**: 어떤 계열 직업
   - **배우자 나이차**: 동갑, 연상, 연하 (몇 살 차이)
   - **궁합 점수**: 전반적 궁합도

4. **연애/결혼 패턴**
   - **사랑에 빠지는 타입** (이 사주만의 특징)
   - **연애할 때 모습** (장점 3가지, 단점 3가지)
   - **결혼 후 모습** (배우자에게 어떤 사람인지)
   - **이별/이혼 위험**: 몇 살 때 주의해야 하는지
   - **재혼 가능성**: 있다면 몇 살 때인지

5. **애정운 극대화 전략**
   - 좋은 인연 만나는 구체적 방법 5가지
   - 피해야 할 이성 타입 (구체적)
   - 애정운 높이는 색깔, 방향, 물건
   - 연애/결혼 성공을 위한 조언
   - 배우자와 행복하게 사는 비결

**중요**:
- "일반적으로", "보통" 같은 표현 금지
- 이 생년월일만의 고유한 애정 특성 서술
- 나이는 반드시 구체적으로 (예: 28~32세)
- 1600자 이상 작성
- **특정 날짜(오늘, 내일, 이번 달) 언급 금지**
- **영어 단어 절대 사용 금지** (순수 한국어만)
- 전문가로서 확신 있고 구체적으로 서술
- **좋은 점과 위험한 점을 모두 명확히 지적** - 이별/이혼 가능성도 솔직하게
- **냉철하고 현실적으로** - 이상화하지 말고 있는 그대로 분석
"""
            max_tokens = 2500
            
        elif category in ["재물 운세", "재물운", "금전 운세"]:
            user_prompt = f"""
당신은 40년 경력의 사주명리학 전문가입니다. 다음 사주를 가진 사람의 재물운을 **매우 구체적이고 차별화되게** 분석해주세요:

{birth_info}

**반드시 이 사람의 생년월일과 출생시간을 기반으로 한 고유한 사주 구조를 분석하여, 다른 사람과 완전히 다른 구체적인 재물운을 풀이해야 합니다.**

다음 단계로 분석해주세요:

1. **사주 구조 분석 (4-5문단)**
   - 이 생년월일의 일주(日柱)와 월주(月柱) 특성
   - 오행(목화토금수)의 균형과 부족
   - 재성(財星)의 위치와 강약
   - 비겁(比劫), 식상(食傷)의 상태
   - 이 사주만의 독특한 재물 구조

2. **재물 획득 방식 (3-4문단)**
   - 정재(正財) vs 편재(偏財) 성향
   - 근로소득형 vs 투자소득형 vs 사업소득형
   - 돈을 버는 타이밍과 패턴
   - 재물 증식 방법

3. **생애 재물운 흐름 (나이대별 상세 분석)**
   - 20대: 구체적 재물 상황과 조언
   - 30대: 구체적 재물 상황과 조언
   - 40대: 구체적 재물 상황과 조언
   - 50대 이후: 구체적 재물 상황과 조언
   - **각 나이대마다 이 사주만의 특징적인 재물 흐름 명시**

4. **재물운 극대화 전략**
   - **이 사주에 맞는 투자 방식** (부동산/주식/예금/사업 등)
   - **돈이 새는 구멍** (이 사주의 재물 손실 패턴)
   - **재물 들어오는 방향과 색깔**
   - 함께하면 재물운 좋아지는 사람의 특징

5. **구체적 주의사항과 해결책**
   - 재물 손실 시기 (구체적 나이와 이유)
   - 큰 돈 들어오는 시기 (구체적 나이와 방법)
   - 피해야 할 사업/투자 종류
   - 성공 가능성 높은 사업/투자 종류

**중요**: 
- "일반적으로", "보통", "대부분" 같은 표현 절대 금지
- 반드시 이 사주의 생년월일에 근거한 구체적 특징 서술
- 다른 사람이 읽으면 "이건 내 이야기가 아니네"라고 느낄 정도로 개인화된 내용
- 1800자 이상 작성
- **영어 단어 절대 사용 금지** (순수 한국어만)
- 전문 도사로서 단정적이고 확신 있게 서술
- **특정 날짜(오늘, 내일, 이번 달)는 언급하지 말 것**
- **재물운이 나쁜 부분도 명확히 지적** - 재물 손실 위험, 파산 가능성 등 솔직하게
- **냉철하게 현실을 직시** - 부자가 되기 어렵다면 그렇게 말하고, 쉽다면 그렇게 말하기
"""
            max_tokens = 2800
            
        elif category in ["사업운", "사업 운세"]:
            user_prompt = f"""
{birth_info}인 사람의 사업운을 평생 관점에서 상세하게 풀이해주세요.

**중요: 특정 날짜(오늘, 내일, 이번 달 등)를 언급하지 말고, 평생의 사업운 흐름으로 작성해주세요.**

다음을 포함해주세요:
1. 타고난 사업 재능과 성향 (3문단)
2. **사업 성공 가능성이 높은 분야** (강조)
3. **사업 시작하기 좋은 나이대와 시기** (강조)
4. **사업에서 조심해야 할 점** (강조)
5. 파트너십과 인맥 활용법
6. 사업 자금 운용 조언
7. 사업 성공을 위한 구체적 전략

1000자 이상으로 상세하게 작성해주세요.
"""
            max_tokens = 1800
            
        elif category in ["학업운", "학업 운세"]:
            user_prompt = f"""
{birth_info}인 사람의 학업운을 평생 관점에서 상세하게 풀이해주세요.

**중요: 특정 날짜(오늘, 내일, 이번 달 등)를 언급하지 말고, 평생의 학업운 흐름으로 작성해주세요.**

다음을 포함해주세요:
1. 타고난 학습 능력과 성향 (2-3문단)
2. **가장 잘 맞는 학습 분야** (강조)
3. **공부하기 좋은 나이대와 시기** (강조)
4. **학업에서 조심해야 할 점** (강조)
5. 효과적인 학습 방법
6. 시험운과 합격운
7. 학업 성취를 위한 조언

900자 이상으로 상세하게 작성해주세요.
"""
            max_tokens = 1600
            
        elif category in ["전생 운세", "전생운세", "past-life"]:
            user_prompt = f"""
{birth_info}인 사람의 전생 운세를 신비롭고 상세하게 풀이해주세요.

**중요: 전생의 삶과 현생과의 연결을 중심으로 작성해주세요.**

다음을 포함해주세요:
1. **전생에서의 신분과 삶** (3문단) - 어떤 시대, 어떤 사람이었는지
2. **전생에서 했던 일** (강조) - 직업, 역할, 특별한 경험
3. **전생의 업보와 인연** - 어떤 업을 지었고, 누구와 인연이 있었는지
4. **현생에 미치는 영향** (강조) - 전생의 업보가 현생에 어떻게 나타나는지
5. **풀어야 할 과제** - 이번 생에서 해결해야 할 전생의 업
6. **타고난 능력** - 전생에서 가져온 재능과 능력
7. **만날 인연** - 전생의 인연이 현생에서 다시 만날 가능성
8. **전생의 교훈** - 현생을 위한 전생의 가르침

1200자 이상으로 신비롭고 구체적으로 작성해주세요. 마치 도사가 보는 것처럼 생생하게 묘사해주세요.
"""
            max_tokens = 2200
            
        elif category in ["궁합", "compatibility"]:
            user_prompt = f"""
{birth_info}인 두 사람의 궁합을 매우 상세하게 풀이해주세요.

**중요: 사주 기반으로 두 사람의 궁합을 전문적으로 분석해주세요.**

다음을 포함해주세요:
1. **전체 궁합 분석** (3문단) - 두 사람의 사주 구성과 조화
2. **성격 궁합** (강조) - 성격적 특징과 어울림
3. **애정 궁합** (강조) - 사랑과 감정적 교류
4. **재물 궁합** - 경제적 가치관과 금전 운
5. **장수 궁합** - 서로의 건강과 장수에 미치는 영향
6. **자손 궁합** - 자녀 운과 가족 운
7. **조심해야 할 점** (강조) - 갈등 가능성과 주의사항
8. **좋은 점** (강조) - 서로를 보완하는 장점
9. **관계 발전 조언** - 두 사람이 더 행복하기 위한 구체적 조언

1300자 이상으로 매우 상세하게 작성해주세요. 점수나 등급은 언급하지 말고, 깊이 있는 분석에 집중해주세요.
"""
            max_tokens = 2500
            
        else:
            # 기타 모든 카테고리 (토정비결, 궁합, 띠별운세, 소원성취운세, 별자리운세 등)
            user_prompt = f"""
{birth_info}인 사람의 '{category}'를 매우 상세하고 구체적으로 풀이해주세요.

**중요: 특정 날짜(오늘, 내일, 이번 달 등)를 언급하지 말고, 장기적 관점에서 작성해주세요.**

다음을 포함해주세요:
1. 전체적인 운세 개요 (3-4문단)
2. **특히 좋은 점** (강조)
3. **주의해야 할 점** (강조)
4. 시기별 흐름 (나이대 또는 연도별)
5. 구체적이고 실천 가능한 조언

1000자 이상으로 상세하게 작성해주세요. 일반적인 이야기가 아닌 구체적인 내용으로 작성해주세요.
"""
            max_tokens = 2000

        # 사주 풀이 요청
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )

        result = response.choices[0].message.content
        
        # API 사용량 기록
        try:
            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
            # GPT-4 가격 기준 (입력: $0.03/1K, 출력: $0.06/1K tokens)
            estimated_cost = (tokens_used / 1000) * 0.045  # 평균 가격
            
            api_usage = APIUsage(
                category=category,
                tokens_used=tokens_used,
                estimated_cost=estimated_cost,
                response_time=0  # 필요시 추가
            )
            db.session.add(api_usage)
            db.session.commit()
        except Exception as api_log_error:
            logger.warning(f"API 사용량 기록 실패: {api_log_error}")
            db.session.rollback()
        
        # 접속 로그 기록
        try:
            if category in ['궁합', 'compatibility']:
                log_access(category, user1)
            else:
                log_access(category, data)
        except Exception as log_error:
            logger.warning(f"로그 기록 실패: {log_error}")

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        logger.exception(f"사주 풀이 중 오류 발생: {e}")
        return jsonify({
            "success": False,
            "error": f"사주 풀이 중 오류가 발생했습니다: {str(e)[:100]}"
        }), 500

@app.route('/debug/env', methods=['GET'])
def debug_env():
    """API 키 상태 확인 엔드포인트"""
    has_key = bool(API_KEY and API_KEY != "your_openai_api_key_here")
    key_status = "설정됨" if has_key else "설정되지 않음"

    return jsonify({
        "api_key_status": key_status,
        "client_initialized": client is not None,
        "server_port": 2222
    })

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """사이트 설정 조회 API"""
    from models import SiteSettings
    try:
        settings = {}
        all_settings = SiteSettings.query.all()
        for setting in all_settings:
            settings[setting.key] = setting.value
        
        # 기본값 설정
        defaults = {
            'site_title': '도사운세',
            'header_logo': '도사운세',
            'header_subtitle': '전통 사주로 보는 당신의 운명',
            'footer_company': '주식회사 대게',
            'footer_email': 'daegye54@gmail.com',
            'youtube_url': 'https://www.youtube.com/@dosaunse'
        }
        
        # 설정이 없으면 기본값 사용
        for key, default_value in defaults.items():
            if key not in settings:
                settings[key] = default_value
        
        return jsonify({
            "success": True,
            "settings": settings
        })
    except Exception as e:
        logger.error(f"설정 조회 실패: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """메인 페이지"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "index.html 파일을 찾을 수 없습니다", 404

@app.route('/styles.css', methods=['GET'])
def styles():
    """CSS 파일"""
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            response = app.make_response(f.read())
            response.headers['Content-Type'] = 'text/css'
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
    except FileNotFoundError:
        return "styles.css 파일을 찾을 수 없습니다", 404

@app.route('/script.js', methods=['GET'])
def script():
    """JavaScript 파일"""
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            response = app.make_response(f.read())
            response.headers['Content-Type'] = 'application/javascript'
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
    except FileNotFoundError:
        return "script.js 파일을 찾을 수 없습니다", 404

# 관리자 라우트 등록
from admin_routes import admin_bp, log_access
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    # 데이터베이스 초기화
    with app.app_context():
        db.create_all()
        logger.info("데이터베이스 테이블 초기화 완료")
        
        # 기본 관리자 계정 생성 (없을 경우에만)
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@dosa.com')
            admin.set_password('admin1234')  # 초기 비밀번호
            db.session.add(admin)
            db.session.commit()
            logger.info("기본 관리자 계정 생성됨 (admin / admin1234)")
    
    try:
        # 포트 설정 (환경 변수 또는 기본값)
        port = int(os.environ.get('PORT', 2222))
        
        logger.info("도사운세 서버를 시작합니다...")
        logger.info(f"포트: {port}")
        logger.info("API 키 상태: {}".format("설정됨" if API_KEY != "your_openai_api_key_here" else "설정되지 않음"))
        logger.info(f"관리자 페이지: http://localhost:{port}/admin")

        app.run(
            debug=True,
            host='0.0.0.0',
            port=port,
            use_reloader=True
        )
    except Exception as e:
        logger.error(f"서버 시작 실패: {e}")
        print(f"오류: {e}")
        print("서버를 시작할 수 없습니다. API 키를 확인해주세요.")

