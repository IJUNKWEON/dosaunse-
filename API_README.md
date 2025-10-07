# 도사운세 Flask API 서버

OpenAI GPT-4o를 사용한 사주 운세 생성 API 서버입니다.

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정
```bash
# env_example.txt를 .env로 복사
cp env_example.txt .env

# .env 파일을 열어서 실제 OpenAI API 키로 수정
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 3. 서버 실행
```bash
python app.py
```

서버는 `http://localhost:5000`에서 실행됩니다.

## 📡 API 엔드포인트

### POST /saju
사주 운세 생성 API

**요청 예시:**
```json
{
  "birthDate": "1991-01-08",
  "birthTime": "오전 10시", 
  "gender": "male",
  "calendarType": "solar",
  "category": "오늘의 운세"
}
```

**응답 예시:**
```json
{
  "success": true,
  "fortune": {
    "title": "오늘의 운세 - 새로운 시작",
    "content": "오늘은 당신에게 좋은 기운이 도는 날입니다...",
    "advice": "과감하게 시작하세요.",
    "example": "오랜만에 연락 온 친구가 기회를 줄 수 있습니다."
  }
}
```

### GET /health
서버 상태 확인

**응답 예시:**
```json
{
  "status": "healthy",
  "message": "도사운세 API 서버가 정상 동작 중입니다.",
  "timestamp": "2024-07-24T03:15:30.123456"
}
```

## 🔧 프론트엔드 연동

웹사이트에서는 자동으로 API를 호출하며, API 호출이 실패하면 기존 시뮬레이션 로직으로 대체됩니다.

### 동시 실행 방법:
```bash
# 터미널 1: 프론트엔드 서버
python -m http.server 8000

# 터미널 2: Flask API 서버  
python app.py
```

- 프론트엔드: http://localhost:8000
- API 서버: http://localhost:5000

## ⚠️ 주의사항

1. **OpenAI API 키 필수**: OPENAI_API_KEY 환경변수가 설정되어야 합니다.
2. **CORS 설정**: 프론트엔드와 다른 포트에서 실행되므로 CORS가 활성화되어 있습니다.
3. **API 요금**: GPT-4o 사용 시 OpenAI API 요금이 발생합니다.
4. **개발 모드**: 현재는 개발 모드로 설정되어 있습니다.

## 🧪 테스트

### API 직접 테스트:
```bash
curl -X POST http://localhost:5000/saju \
  -H "Content-Type: application/json" \
  -d '{
    "birthDate": "1991-01-08",
    "birthTime": "오전 10시",
    "gender": "male", 
    "calendarType": "solar",
    "category": "오늘의 운세"
  }'
```

### 서버 상태 확인:
```bash
curl http://localhost:5000/health
```

## 📋 지원하는 운세 카테고리

- 오늘의 운세
- 내일의 운세  
- 이달의 운세
- 올해의 운세
- 평생 운세
- 애정운
- 재물운
- 사업운
- 학업운
- 띠별 운세
- 궁합
- 소원 성취 운세
- 별자리 운세
- 전생 운세
- 토정비결 