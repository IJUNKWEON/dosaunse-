# -*- coding: utf-8 -*-
"""
도사운세 관리자 페이지 확장 HTML 템플릿
"""

ADMIN_API_USAGE_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API 사용량 - 도사운세 관리자</title>
    <style>
        :root {
            --paper-bg: #f5efe6;
            --ink-black: #1a1a1a;
            --seal-red: #c41e3a;
            --gold: #d4af37;
            --border-dark: #4a3f35;
            --paper-white: #fdfbf7;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Malgun Gothic', 'Noto Serif KR', serif;
            background: var(--paper-bg);
            background-image: 
                repeating-linear-gradient(90deg, rgba(74, 63, 53, 0.02) 0px, transparent 1px, transparent 50px, rgba(74, 63, 53, 0.02) 51px),
                repeating-linear-gradient(0deg, rgba(74, 63, 53, 0.02) 0px, transparent 1px, transparent 50px, rgba(74, 63, 53, 0.02) 51px);
        }
        .header {
            background: linear-gradient(135deg, #4a3f35 0%, #2d2520 100%);
            color: var(--paper-white);
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-bottom: 3px solid var(--seal-red);
        }
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { font-size: 24px; font-weight: 700; letter-spacing: 2px; }
        .nav {
            display: flex;
            gap: 10px;
        }
        .nav a {
            color: var(--paper-white);
            text-decoration: none;
            padding: 8px 16px;
            border: 2px solid transparent;
            transition: all 0.3s;
            font-weight: 600;
        }
        .nav a:hover {
            border-color: var(--seal-red);
            background: rgba(196, 30, 58, 0.1);
        }
        .container {
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: var(--paper-white);
            padding: 25px;
            border: 3px solid var(--border-dark);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            color: var(--ink-black);
            font-size: 14px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .stat-card .number {
            font-size: 36px;
            font-weight: bold;
            color: var(--seal-red);
        }
        .stat-card .sub {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }
        .chart-container {
            background: var(--paper-white);
            padding: 25px;
            border: 3px solid var(--border-dark);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            background: var(--paper-white);
            border: 3px solid var(--border-dark);
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e0d5c7;
        }
        th {
            background: #e8dcc4;
            font-weight: 700;
            color: var(--ink-black);
        }
        tr:hover {
            background: #faf8f4;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🔮 도사운세 관리자</h1>
            <div class="nav">
                <a href="{{ url_for('admin.dashboard') }}">대시보드</a>
                <a href="{{ url_for('admin.logs') }}">접속 로그</a>
                <a href="{{ url_for('admin.system_status') }}">플랫폼 통계</a>
                <a href="{{ url_for('admin.notices') }}">공지사항</a>
                <a href="{{ url_for('admin.settings') }}">사이트 설정</a>
                <a href="{{ url_for('admin.account') }}">계정 관리</a>
                <a href="{{ url_for('admin.admin_logout') }}">로그아웃</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        <h2 style="margin-bottom: 20px;">💰 API 사용량 모니터링</h2>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>오늘 사용량</h3>
                <div class="number">{{ "${:,.0f}".format(stats.today.cost or 0) }}</div>
                <div class="sub">{{ "{:,}".format(stats.today.tokens or 0) }} tokens</div>
            </div>
            <div class="stat-card">
                <h3>이번 주 사용량</h3>
                <div class="number">{{ "${:,.0f}".format(stats.week.cost or 0) }}</div>
                <div class="sub">{{ "{:,}".format(stats.week.tokens or 0) }} tokens</div>
            </div>
            <div class="stat-card">
                <h3>이번 달 사용량</h3>
                <div class="number">{{ "${:,.0f}".format(stats.month.cost or 0) }}</div>
                <div class="sub">{{ "{:,}".format(stats.month.tokens or 0) }} tokens</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3 style="margin-bottom: 15px;">📊 카테고리별 사용량</h3>
            <table>
                <thead>
                    <tr>
                        <th>운세 종류</th>
                        <th>호출 횟수</th>
                        <th>총 토큰</th>
                        <th>예상 비용</th>
                    </tr>
                </thead>
                <tbody>
                    {% for cat, count, tokens, cost in stats.category_usage %}
                    <tr>
                        <td>{{ cat }}</td>
                        <td>{{ count }}회</td>
                        <td>{{ "{:,}".format(tokens or 0) }}</td>
                        <td><strong>${{ "{:,.2f}".format(cost or 0) }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
'''

ADMIN_SYSTEM_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>시스템 상태 - 도사운세 관리자</title>
    <style>
        :root {
            --paper-bg: #f5efe6;
            --ink-black: #1a1a1a;
            --seal-red: #c41e3a;
            --gold: #d4af37;
            --border-dark: #4a3f35;
            --paper-white: #fdfbf7;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Malgun Gothic', 'Noto Serif KR', serif;
            background: var(--paper-bg);
            background-image: 
                repeating-linear-gradient(90deg, rgba(74, 63, 53, 0.02) 0px, transparent 1px, transparent 50px, rgba(74, 63, 53, 0.02) 51px),
                repeating-linear-gradient(0deg, rgba(74, 63, 53, 0.02) 0px, transparent 1px, transparent 50px, rgba(74, 63, 53, 0.02) 51px);
        }
        .header {
            background: linear-gradient(135deg, #4a3f35 0%, #2d2520 100%);
            color: var(--paper-white);
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-bottom: 3px solid var(--seal-red);
        }
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { font-size: 24px; font-weight: 700; letter-spacing: 2px; }
        .nav {
            display: flex;
            gap: 10px;
        }
        .nav a {
            color: var(--paper-white);
            text-decoration: none;
            padding: 8px 16px;
            border: 2px solid transparent;
            transition: all 0.3s;
            font-weight: 600;
        }
        .nav a:hover {
            border-color: var(--seal-red);
            background: rgba(196, 30, 58, 0.1);
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .system-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .system-card {
            background: var(--paper-white);
            padding: 25px;
            border: 3px solid var(--border-dark);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .system-card h3 {
            color: var(--ink-black);
            font-size: 18px;
            margin-bottom: 20px;
            font-weight: 700;
        }
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e0d5c7;
            border: 2px solid var(--border-dark);
            margin: 10px 0;
            position: relative;
        }
        .progress-fill {
            height: 100%;
            background: var(--seal-red);
            transition: width 0.3s;
        }
        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: 700;
            color: var(--ink-black);
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px;
            background: #faf8f4;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🔮 도사운세 관리자</h1>
            <div class="nav">
                <a href="{{ url_for('admin.dashboard') }}">대시보드</a>
                <a href="{{ url_for('admin.logs') }}">접속 로그</a>
                <a href="{{ url_for('admin.system_status') }}">플랫폼 통계</a>
                <a href="{{ url_for('admin.notices') }}">공지사항</a>
                <a href="{{ url_for('admin.settings') }}">사이트 설정</a>
                <a href="{{ url_for('admin.account') }}">계정 관리</a>
                <a href="{{ url_for('admin.admin_logout') }}">로그아웃</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        <h2 style="margin-bottom: 20px;">📊 도사운세 통계</h2>
        
        <div class="system-grid">
            <div class="system-card">
                <h3>💾 데이터베이스</h3>
                <div class="info-row">
                    <span>DB 크기</span>
                    <span><strong>{{ system_info.db_size }} MB</strong></span>
                </div>
                <div class="info-row">
                    <span>총 접속 로그</span>
                    <span>{{ "{:,}".format(system_info.total_logs) }}건</span>
                </div>
                <div class="info-row">
                    <span>총 API 호출</span>
                    <span>{{ "{:,}".format(system_info.total_api_calls) }}회</span>
                </div>
                <div class="info-row">
                    <span>관리자 수</span>
                    <span>{{ system_info.total_admins }}명</span>
                </div>
                <div class="info-row">
                    <span>공지사항 수</span>
                    <span>{{ system_info.total_notices }}개</span>
                </div>
            </div>
            
            <div class="system-card">
                <h3>👥 성별 통계</h3>
                {% for gender, count in system_info.gender_stats %}
                <div class="info-row">
                    <span>{{ '남성' if gender == 'male' else ('여성' if gender == 'female' else '미상') }}</span>
                    <span><strong>{{ "{:,}".format(count) }}명</strong></span>
                </div>
                {% endfor %}
            </div>
            
            <div class="system-card">
                <h3>🔮 인기 운세 TOP 10</h3>
                {% for fortune_type, count in system_info.category_stats %}
                <div class="info-row">
                    <span>{{ fortune_type or '미분류' }}</span>
                    <span><strong>{{ "{:,}".format(count) }}회</strong></span>
                </div>
                {% endfor %}
            </div>
            
            <div class="system-card">
                <h3>📅 최근 7일 접속 추이</h3>
                {% if system_info.daily_stats %}
                    {% for date, count in system_info.daily_stats %}
                    <div class="info-row">
                        <span>{{ date if date else '-' }}</span>
                        <span><strong>{{ "{:,}".format(count) }}건</strong></span>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="info-row">
                        <span>데이터 없음</span>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
'''

ADMIN_NOTICES_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>공지사항 - 도사운세 관리자</title>
    <style>
        :root {
            --paper-bg: #f5efe6;
            --ink-black: #1a1a1a;
            --seal-red: #c41e3a;
            --gold: #d4af37;
            --border-dark: #4a3f35;
            --paper-white: #fdfbf7;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Malgun Gothic', 'Noto Serif KR', serif;
            background: var(--paper-bg);
            background-image: 
                repeating-linear-gradient(90deg, rgba(74, 63, 53, 0.02) 0px, transparent 1px, transparent 50px, rgba(74, 63, 53, 0.02) 51px),
                repeating-linear-gradient(0deg, rgba(74, 63, 53, 0.02) 0px, transparent 1px, transparent 50px, rgba(74, 63, 53, 0.02) 51px);
        }
        .header {
            background: linear-gradient(135deg, #4a3f35 0%, #2d2520 100%);
            color: var(--paper-white);
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-bottom: 3px solid var(--seal-red);
        }
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { font-size: 24px; font-weight: 700; letter-spacing: 2px; }
        .nav {
            display: flex;
            gap: 10px;
        }
        .nav a {
            color: var(--paper-white);
            text-decoration: none;
            padding: 8px 16px;
            border: 2px solid transparent;
            transition: all 0.3s;
            font-weight: 600;
        }
        .nav a:hover {
            border-color: var(--seal-red);
            background: rgba(196, 30, 58, 0.1);
        }
        .container {
            max-width: 1000px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .box {
            background: var(--paper-white);
            padding: 30px;
            border: 3px solid var(--border-dark);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .box h3 {
            margin-bottom: 20px;
            color: var(--ink-black);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 700;
            color: var(--ink-black);
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid var(--border-dark);
            background: var(--paper-white);
            font-family: inherit;
        }
        textarea {
            min-height: 100px;
        }
        button {
            padding: 10px 20px;
            background: var(--seal-red);
            color: white;
            border: 2px solid var(--border-dark);
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            letter-spacing: 1px;
        }
        button:hover {
            background: #a01828;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(196, 30, 58, 0.3);
        }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 12px;
            border: 2px solid #155724;
            margin-bottom: 20px;
            font-weight: 600;
        }
        table {
            width: 100%;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0d5c7;
        }
        th {
            background: #e8dcc4;
            font-weight: 700;
        }
        .badge-active { 
            background: #d4edda; 
            color: #155724; 
            padding: 4px 12px;
            border: 2px solid #155724;
            font-weight: 600;
        }
        .badge-inactive { 
            background: #f8d7da; 
            color: #721c24; 
            padding: 4px 12px;
            border: 2px solid #721c24;
            font-weight: 600;
        }
        .delete-btn {
            padding: 5px 12px;
            background: #dc3545;
            color: white;
            border: 2px solid var(--border-dark);
            cursor: pointer;
            font-size: 12px;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🔮 도사운세 관리자</h1>
            <div class="nav">
                <a href="{{ url_for('admin.dashboard') }}">대시보드</a>
                <a href="{{ url_for('admin.logs') }}">접속 로그</a>
                <a href="{{ url_for('admin.system_status') }}">플랫폼 통계</a>
                <a href="{{ url_for('admin.notices') }}">공지사항</a>
                <a href="{{ url_for('admin.settings') }}">사이트 설정</a>
                <a href="{{ url_for('admin.account') }}">계정 관리</a>
                <a href="{{ url_for('admin.admin_logout') }}">로그아웃</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        <h2 style="margin-bottom: 20px;">📢 공지사항 관리</h2>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="success">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="box">
            <h3>➕ 새 공지사항 추가</h3>
            <form method="POST">
                <input type="hidden" name="action" value="add">
                <div class="form-group">
                    <label>제목</label>
                    <input type="text" name="title" required>
                </div>
                <div class="form-group">
                    <label>내용</label>
                    <textarea name="content" required></textarea>
                </div>
                <div class="form-group">
                    <label>우선순위 (높을수록 우선)</label>
                    <input type="number" name="priority" value="0">
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="is_active" checked> 활성화
                    </label>
                </div>
                <button type="submit">추가</button>
            </form>
        </div>
        
        <div class="box">
            <h3>📋 공지사항 목록</h3>
            <table>
                <thead>
                    <tr>
                        <th>제목</th>
                        <th>우선순위</th>
                        <th>상태</th>
                        <th>작성일</th>
                        <th>관리</th>
                    </tr>
                </thead>
                <tbody>
                    {% for notice in notices %}
                    <tr>
                        <td>{{ notice.title }}</td>
                        <td>{{ notice.priority }}</td>
                        <td>
                            {% if notice.is_active %}
                                <span class="badge-active">활성</span>
                            {% else %}
                                <span class="badge-inactive">비활성</span>
                            {% endif %}
                        </td>
                        <td>{{ notice.created_at.strftime('%Y-%m-%d') }}</td>
                        <td>
                            <form method="POST" style="display: inline;" onsubmit="return confirm('삭제하시겠습니까?');">
                                <input type="hidden" name="action" value="delete">
                                <input type="hidden" name="notice_id" value="{{ notice.id }}">
                                <button type="submit" class="delete-btn">삭제</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
'''

