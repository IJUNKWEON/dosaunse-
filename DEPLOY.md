# 🚀 도사운세 Render.com 배포 가이드

## 📋 사전 준비

### 1. GitHub 저장소 생성
1. GitHub에 로그인
2. New Repository 클릭
3. 저장소 이름: `dosaunse` (또는 원하는 이름)
4. Public 또는 Private 선택
5. Create Repository

### 2. 코드 업로드
```bash
# Git 초기화
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit - 도사운세 프로젝트"

# GitHub 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/dosaunse.git

# 푸시
git branch -M main
git push -u origin main
```

---

## 🌐 Render.com 배포

### 1단계: Render 회원가입
1. https://render.com 접속
2. Sign Up (GitHub 계정으로 가입 추천)
3. 이메일 인증 완료

### 2단계: 새 Web Service 생성
1. Dashboard에서 **"New +"** 클릭
2. **"Web Service"** 선택
3. **"Build and deploy from a Git repository"** 선택
4. GitHub 저장소 연결 허용
5. 생성한 저장소(`dosaunse`) 선택

### 3단계: 설정
다음 정보 입력:

- **Name**: `dosaunse` (또는 원하는 이름)
- **Region**: `Singapore` (가장 가까운 서버)
- **Branch**: `main`
- **Root Directory**: (비워두기)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
- **Instance Type**: `Free` 선택

### 4단계: 환경 변수 설정
**Environment Variables** 섹션에서:

1. **Add Environment Variable** 클릭
2. 다음 변수 추가:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `sk-proj-2xr9...` (실제 OpenAI API 키) |
| `PYTHON_VERSION` | `3.12.0` |
| `SECRET_KEY` | `your-secret-key-here` (랜덤 문자열) |

### 5단계: 배포 시작
1. **"Create Web Service"** 클릭
2. 자동으로 배포 시작 (5-10분 소요)
3. 로그에서 진행 상황 확인

---

## ✅ 배포 완료 후

### 접속 URL
배포 완료 후 URL이 생성됩니다:
```
https://dosaunse.onrender.com
```

### 관리자 페이지
```
https://dosaunse.onrender.com/admin

기본 계정:
- ID: admin
- PW: admin1234
```

**⚠️ 첫 로그인 후 반드시 비밀번호를 변경하세요!**

---

## 🔧 문제 해결

### 배포 실패시
1. Render 대시보드에서 **"Logs"** 탭 확인
2. 에러 메시지 확인
3. 환경 변수 설정 재확인

### 슬립 모드 (15분 미접속)
무료 플랜은 15분 동안 접속이 없으면 슬립 모드:
- 첫 접속시 30초~1분 소요
- 해결: 유료 플랜 ($7/월) 또는 Uptime Robot으로 자동 핑

---

## 🌐 커스텀 도메인 연결 (선택사항)

### 도메인 구매 후
1. Render 대시보드 → Settings → Custom Domain
2. 도메인 입력 (예: dosaunse.com)
3. DNS 설정:
   ```
   Type: CNAME
   Name: @
   Value: dosaunse.onrender.com
   ```
4. SSL 자동 발급 (무료)

---

## 📊 업데이트 방법

코드 수정 후:
```bash
git add .
git commit -m "업데이트 내용"
git push origin main
```

Render가 자동으로 감지하여 재배포합니다!

---

## 💡 주의사항

1. **.env 파일은 업로드하지 마세요** (이미 .gitignore에 설정됨)
2. **OpenAI API 키**는 Render 환경 변수로만 설정
3. **관리자 비밀번호** 반드시 변경
4. **무료 플랜 제한**: 월 750시간 (충분함)

---

## 🆘 도움이 필요하면

- Render 문서: https://render.com/docs
- Render 커뮤니티: https://community.render.com

배포 성공을 기원합니다! 🎉

