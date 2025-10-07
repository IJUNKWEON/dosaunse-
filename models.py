# -*- coding: utf-8 -*-
"""
도사운세 데이터베이스 모델
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    """관리자 계정"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """비밀번호 해시화"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """비밀번호 확인"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'


class AccessLog(db.Model):
    """접속 로그"""
    __tablename__ = 'access_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))  # IPv6 지원
    user_agent = db.Column(db.String(255))
    birth_date = db.Column(db.String(10))  # YYYY-MM-DD
    birth_time = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    calendar_type = db.Column(db.String(10))  # solar/lunar
    fortune_type = db.Column(db.String(50))  # 운세 종류
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(100))  # 접속 위치 (선택)
    
    def __repr__(self):
        return f'<AccessLog {self.ip_address} - {self.fortune_type}>'


class SiteSettings(db.Model):
    """사이트 설정"""
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SiteSettings {self.key}>'


class FortuneCategory(db.Model):
    """운세 카테고리"""
    __tablename__ = 'fortune_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(10))
    color = db.Column(db.String(20))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FortuneCategory {self.name}>'


class Notice(db.Model):
    """공지사항"""
    __tablename__ = 'notices'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=0)  # 높을수록 우선순위
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notice {self.title}>'


class APIUsage(db.Model):
    """API 사용량 추적"""
    __tablename__ = 'api_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    tokens_used = db.Column(db.Integer, default=0)
    estimated_cost = db.Column(db.Float, default=0.0)
    response_time = db.Column(db.Float)  # 초 단위
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<APIUsage {self.category} - {self.tokens_used} tokens>'

