# -*- coding: utf-8 -*-
"""
도사운세 관리자 페이지 HTML 템플릿
"""

ADMIN_LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>도사운세 관리자 로그인</title>
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
            background: linear-gradient(135deg, #e8dcc4 0%, #d4c5a9 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                repeating-linear-gradient(90deg, rgba(74, 63, 53, 0.03) 0px, transparent 1px, transparent 40px, rgba(74, 63, 53, 0.03) 41px),
                repeating-linear-gradient(0deg, rgba(74, 63, 53, 0.03) 0px, transparent 1px, transparent 40px, rgba(74, 63, 53, 0.03) 41px);
            pointer-events: none;
        }
        .login-container {
            background: var(--paper-white);
            padding: 50px 40px;
            border: 4px solid var(--border-dark);
            box-shadow: 0 10px 40px rgba(0,0,0,0.3), inset 0 0 0 1px rgba(212, 175, 55, 0.3);
            width: 100%;
            max-width: 420px;
            position: relative;
            z-index: 1;
        }
        .login-container::before {
            content: '吉';
            position: absolute;
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 50px;
            background: var(--seal-red);
            color: white;
            font-size: 32px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4);
        }
        h1 {
            text-align: center;
            color: var(--ink-black);
            margin-bottom: 35px;
            font-size: 26px;
            font-weight: 700;
            letter-spacing: 3px;
        }
        .form-group {
            margin-bottom: 22px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            color: var(--ink-black);
            font-weight: 600;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid var(--border-dark);
            background: var(--paper-white);
            font-size: 14px;
            transition: all 0.3s;
            font-family: inherit;
        }
        input:focus {
            outline: none;
            border-color: var(--seal-red);
            box-shadow: 0 0 0 3px rgba(196, 30, 58, 0.1);
        }
        button {
            width: 100%;
            padding: 14px;
            background: var(--seal-red);
            color: white;
            border: 2px solid var(--border-dark);
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            letter-spacing: 2px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }
        button:hover {
            background: #a01828;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .error {
            background: #fff0f0;
            color: var(--seal-red);
            padding: 12px;
            border: 2px solid var(--seal-red);
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🔮 도사운세 관리자</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="error">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <div class="form-group">
                <label>아이디</label>
                <input type="text" name="username" required autofocus>
            </div>
            <div class="form-group">
                <label>비밀번호</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">로그인</button>
        </form>
    </div>
</body>
</html>
'''

ADMIN_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>도사운세 관리자 대시보드</title>
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
        h1 { 
            font-size: 24px; 
            font-weight: 700;
            letter-spacing: 2px;
        }
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
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: var(--paper-white);
            padding: 25px;
            border: 3px solid var(--border-dark);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            position: relative;
        }
        .stat-card::before {
            content: '';
            position: absolute;
            top: 10px;
            right: 10px;
            width: 30px;
            height: 30px;
            background: var(--seal-red);
            opacity: 0.1;
            border-radius: 50%;
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
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border: 2px solid;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-male { 
            background: #e3f2fd; 
            color: #1976d2; 
            border-color: #1976d2;
        }
        .badge-female { 
            background: #fce4ec; 
            color: #c2185b; 
            border-color: #c2185b;
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
        <h2 style="margin-bottom: 20px;">📊 통계 현황</h2>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>전체 접속 수</h3>
                <div class="number">{{ stats.total_access }}</div>
            </div>
            <div class="stat-card">
                <h3>오늘 접속</h3>
                <div class="number">{{ stats.today_access }}</div>
            </div>
            <div class="stat-card">
                <h3>주간 접속</h3>
                <div class="number">{{ stats.week_access }}</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3 style="margin-bottom: 15px;">🔥 인기 운세 TOP 10</h3>
            <table>
                <thead>
                    <tr>
                        <th>순위</th>
                        <th>운세 종류</th>
                        <th>조회 수</th>
                    </tr>
                </thead>
                <tbody>
                    {% for fortune, count in stats.fortune_stats %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ fortune or '메인페이지' }}</td>
                        <td><strong>{{ count }}</strong>회</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="chart-container">
            <h3 style="margin-bottom: 15px;">👥 성별 통계</h3>
            <table>
                <thead>
                    <tr>
                        <th>성별</th>
                        <th>접속 수</th>
                        <th>비율</th>
                    </tr>
                </thead>
                <tbody>
                    {% for gender, count in stats.gender_stats %}
                    <tr>
                        <td>
                            {% if gender == 'male' %}
                                <span class="badge badge-male">남성</span>
                            {% elif gender == 'female' %}
                                <span class="badge badge-female">여성</span>
                            {% else %}
                                <span class="badge">미지정</span>
                            {% endif %}
                        </td>
                        <td><strong>{{ count }}</strong>명</td>
                        <td>{{ "%.1f"|format(count * 100.0 / stats.total_access) }}%</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="chart-container">
            <h3 style="margin-bottom: 15px;">⏰ 최근 접속 로그</h3>
            <table>
                <thead>
                    <tr>
                        <th>시간</th>
                        <th>IP</th>
                        <th>운세</th>
                        <th>성별</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in stats.recent_logs[:10] %}
                    <tr>
                        <td>{{ log.timestamp.strftime('%Y-%m-%d %H:%M') }}</td>
                        <td>{{ log.ip_address }}</td>
                        <td>{{ log.fortune_type or '-' }}</td>
                        <td>
                            {% if log.gender == 'male' %}
                                <span class="badge badge-male">남성</span>
                            {% elif log.gender == 'female' %}
                                <span class="badge badge-female">여성</span>
                            {% else %}
                                -
                            {% endif %}
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

ADMIN_LOGS_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>접속 로그 - 도사운세 관리자</title>
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
        h1 { font-size: 24px; }
        .nav {
            display: flex;
            gap: 20px;
        }
        .nav a {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav a:hover {
            background: rgba(255,255,255,0.2);
        }
        .container {
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .filter-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .filter-row {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .filter-row input, .filter-row select {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .filter-row button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
        }
        table {
            width: 100%;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        th, td {
            padding: 15px;
            text-align: left;
            font-size: 14px;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        .pagination a {
            padding: 8px 12px;
            background: white;
            border-radius: 5px;
            text-decoration: none;
            color: #667eea;
        }
        .pagination a:hover {
            background: #667eea;
            color: white;
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
        <h2 style="margin-bottom: 20px;">📋 접속 로그 (총 {{ pagination.total }}건)</h2>
        
        <div class="filter-box">
            <form method="GET" class="filter-row">
                <input type="date" name="date_from" value="{{ date_from or '' }}" placeholder="시작일">
                <input type="date" name="date_to" value="{{ date_to or '' }}" placeholder="종료일">
                <select name="gender">
                    <option value="">전체 성별</option>
                    <option value="male" {% if gender == 'male' %}selected{% endif %}>남성</option>
                    <option value="female" {% if gender == 'female' %}selected{% endif %}>여성</option>
                </select>
                <button type="submit">검색</button>
                <a href="{{ url_for('admin.export_logs', date_from=date_from or '', date_to=date_to or '', gender=gender or '', fortune_type=fortune_type or '') }}" 
                   style="padding: 10px 20px; background: var(--gold); color: var(--ink-black); border: 2px solid var(--border-dark); text-decoration: none; font-weight: 700; display: inline-block; letter-spacing: 1px; transition: all 0.3s;">
                    📥 엑셀 다운로드
                </a>
            </form>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>시간</th>
                    <th>IP 주소</th>
                    <th>운세 종류</th>
                    <th>생년월일</th>
                    <th>출생시간</th>
                    <th>성별</th>
                    <th>양/음력</th>
                </tr>
            </thead>
            <tbody>
                {% for log in pagination.items %}
                <tr>
                    <td>{{ log.timestamp.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                    <td>{{ log.ip_address }}</td>
                    <td>{{ log.fortune_type or '-' }}</td>
                    <td>{{ log.birth_date or '-' }}</td>
                    <td>{{ log.birth_time or '-' }}</td>
                    <td>{{ log.gender or '-' }}</td>
                    <td>{{ log.calendar_type or '-' }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <div class="pagination">
            {% if pagination.has_prev %}
                <a href="{{ url_for('admin.logs', page=pagination.prev_num) }}">이전</a>
            {% endif %}
            <span style="padding: 8px 12px;">{{ pagination.page }} / {{ pagination.pages }}</span>
            {% if pagination.has_next %}
                <a href="{{ url_for('admin.logs', page=pagination.next_num) }}">다음</a>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

ADMIN_SETTINGS_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>사이트 설정 - 도사운세 관리자</title>
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
        h1 { font-size: 24px; }
        .nav {
            display: flex;
            gap: 20px;
        }
        .nav a {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav a:hover {
            background: rgba(255,255,255,0.2);
        }
        .container {
            max-width: 1000px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .settings-box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .setting-item {
            margin-bottom: 25px;
            padding-bottom: 25px;
            border-bottom: 1px solid #eee;
        }
        .setting-item:last-child {
            border-bottom: none;
        }
        label {
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            font-family: inherit;
        }
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        button {
            padding: 12px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        button:hover {
            background: #5568d3;
        }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 20px;
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
        <h2 style="margin-bottom: 20px;">⚙️ 사이트 설정</h2>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="success">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="settings-box">
            <form method="POST">
                <div class="setting-item">
                    <label>사이트 제목</label>
                    <input type="text" name="setting_site_title" value="{{ settings | selectattr('key', 'equalto', 'site_title') | map(attribute='value') | first or '도사운세' }}">
                </div>
                
                <div class="setting-item">
                    <label>헤더 로고 텍스트</label>
                    <input type="text" name="setting_header_logo" value="{{ settings | selectattr('key', 'equalto', 'header_logo') | map(attribute='value') | first or '도사운세' }}">
                </div>
                
                <div class="setting-item">
                    <label>헤더 서브타이틀</label>
                    <input type="text" name="setting_header_subtitle" value="{{ settings | selectattr('key', 'equalto', 'header_subtitle') | map(attribute='value') | first or '전통 사주로 보는 당신의 운명' }}">
                </div>
                
                <div class="setting-item">
                    <label>푸터 회사명</label>
                    <input type="text" name="setting_footer_company" value="{{ settings | selectattr('key', 'equalto', 'footer_company') | map(attribute='value') | first or '주식회사 대게' }}">
                </div>
                
                <div class="setting-item">
                    <label>푸터 이메일</label>
                    <input type="text" name="setting_footer_email" value="{{ settings | selectattr('key', 'equalto', 'footer_email') | map(attribute='value') | first or 'daegye54@gmail.com' }}">
                </div>
                
                <div class="setting-item">
                    <label>유튜브 채널 URL</label>
                    <input type="text" name="setting_youtube_url" value="{{ settings | selectattr('key', 'equalto', 'youtube_url') | map(attribute='value') | first or 'https://www.youtube.com/@dosaunse' }}">
                </div>
                
                <button type="submit">저장</button>
            </form>
        </div>
    </div>
</body>
</html>
'''

ADMIN_ACCOUNT_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>계정 관리 - 도사운세 관리자</title>
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
        h1 { font-size: 24px; }
        .nav {
            display: flex;
            gap: 20px;
        }
        .nav a {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav a:hover {
            background: rgba(255,255,255,0.2);
        }
        .container {
            max-width: 1000px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .box h3 {
            margin-bottom: 20px;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #333;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
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
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
        }
        .delete-btn {
            padding: 5px 12px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
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
        <h2 style="margin-bottom: 20px;">👤 계정 관리</h2>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="box">
            <h3>🔐 비밀번호 변경</h3>
            <form method="POST">
                <input type="hidden" name="action" value="change_password">
                <div class="form-group">
                    <label>현재 비밀번호</label>
                    <input type="password" name="current_password" required>
                </div>
                <div class="form-group">
                    <label>새 비밀번호</label>
                    <input type="password" name="new_password" required>
                </div>
                <div class="form-group">
                    <label>새 비밀번호 확인</label>
                    <input type="password" name="confirm_password" required>
                </div>
                <button type="submit">비밀번호 변경</button>
            </form>
        </div>
        
        <div class="box">
            <h3>➕ 관리자 추가</h3>
            <form method="POST">
                <input type="hidden" name="action" value="add_admin">
                <div class="form-group">
                    <label>아이디</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>이메일</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>비밀번호</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">관리자 추가</button>
            </form>
        </div>
        
        <div class="box">
            <h3>📋 관리자 목록</h3>
            <table>
                <thead>
                    <tr>
                        <th>아이디</th>
                        <th>이메일</th>
                        <th>가입일</th>
                        <th>최근 로그인</th>
                        <th>관리</th>
                    </tr>
                </thead>
                <tbody>
                    {% for adm in admins %}
                    <tr>
                        <td>{{ adm.username }}</td>
                        <td>{{ adm.email }}</td>
                        <td>{{ adm.created_at.strftime('%Y-%m-%d') }}</td>
                        <td>{{ adm.last_login.strftime('%Y-%m-%d %H:%M') if adm.last_login else '-' }}</td>
                        <td>
                            {% if adm.id != admin.id %}
                            <form method="POST" style="display: inline;" onsubmit="return confirm('정말 삭제하시겠습니까?');">
                                <input type="hidden" name="action" value="delete_admin">
                                <input type="hidden" name="admin_id" value="{{ adm.id }}">
                                <button type="submit" class="delete-btn">삭제</button>
                            </form>
                            {% else %}
                            <span style="color: #999;">현재 계정</span>
                            {% endif %}
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

ADMIN_CATEGORIES_HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>카테고리 관리 - 도사운세 관리자</title>
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
        h1 { font-size: 24px; }
        .nav {
            display: flex;
            gap: 20px;
        }
        .nav a {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav a:hover {
            background: rgba(255,255,255,0.2);
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        table {
            width: 100%;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        th, td {
            padding: 15px;
            text-align: left;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-active { background: #d4edda; color: #155724; }
        .badge-inactive { background: #f8d7da; color: #721c24; }
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
        <h2 style="margin-bottom: 20px;">📁 운세 카테고리 관리</h2>
        
        <table>
            <thead>
                <tr>
                    <th>아이콘</th>
                    <th>이름</th>
                    <th>키</th>
                    <th>정렬순서</th>
                    <th>상태</th>
                    <th>생성일</th>
                </tr>
            </thead>
            <tbody>
                {% for category in categories %}
                <tr>
                    <td>{{ category.icon }}</td>
                    <td>{{ category.name }}</td>
                    <td><code>{{ category.key }}</code></td>
                    <td>{{ category.sort_order }}</td>
                    <td>
                        {% if category.is_active %}
                            <span class="badge badge-active">활성</span>
                        {% else %}
                            <span class="badge badge-inactive">비활성</span>
                        {% endif %}
                    </td>
                    <td>{{ category.created_at.strftime('%Y-%m-%d') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''

