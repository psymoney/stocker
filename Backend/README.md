# Stocker Backend

### 개발환경 구동 가이드
#### 1. 환경설정
#### A. python virtual environment 설정
1) 가상환경 생성 
```
python3 -m venv .venv
```
    
2) 가상환경 실행  
- Mac
```
source .venv/bin/activate
```
- Windows
```
source .venv/script/activate
```

#### B. 라이브러리 설치
```
pip install -r requirements.txt
```

#### 2. 개발환경 실행
~~~
python manage.py runserver --settings=config.local
~~~
