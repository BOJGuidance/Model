# 베이스 이미지 설정
FROM python:3.11.7

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 파일 복사
COPY ./requirements.txt /app/requirements.txt

# 필요한 패키지 설치
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Chrome 드라이버 다운로드 및 설치
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O /tmp/chrome_version && \
    wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chrome_version /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Chrome 다운로드 및 설치
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chrome-linux64.zip -O /tmp/chrome-linux64.zip \
    && unzip /tmp/chrome-linux64.zip -d /opt/google \
    && rm /tmp/chrome-linux64.zip \
    && ln -s /opt/google/chrome-linux64/chrome /usr/local/bin/chrome

# 소스 코드 복사
COPY . /app

# Django 애플리케이션 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
