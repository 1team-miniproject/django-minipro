from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",  # 1-2에서 생성한 데이터베이스 이름
        "USER": "daeun",  # 1-1에서 생성한 사용자 이름
        "PASSWORD": "",  # 1-1에서 설정한 비밀번호
        "HOST": "localhost",  # 내 컴퓨터에서 실행 중이므로 'localhost'
        "PORT": "5432",  # PostgreSQL 기본 포트
    }
}

# ...
