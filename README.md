# Video 다운로더 (최대 8K 지원)

Video 영상을 8K까지 다운로드할 수 있는 Flask 웹 애플리케이션입니다.

##  필요 사항

1. Python 3.7 이상
2. FFmpeg (비디오+오디오 병합용) c:\ 경로에 설치
3. Node.js c:\ 경로에 설치

##  설치 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. FFmpeg 설치

**Windows:**
- https://ffmpeg.org/download.html 에서 다운로드
- 환경 변수 PATH에 추가

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## ▶ 실행 방법

```bash
pip install flask yt-dlp
python youtube_downloader.py
```

브라우저에서 http://localhost:5000 접속

##  사용법

1. YouTube URL 입력
2. 원하는 화질 선택 (360p ~ 8K)
3. "다운로드 시작" 버튼 클릭
4. 자동으로 파일 다운로드

##  지원 화질

- 8K (7680x4320)
- 4K (3840x2160)
- 1440p (2560x1440)
- 1080p (1920x1080)
- 720p (1280x720)
- 480p (854x480)
- 360p (640x360)
- 최고 화질 (자동)

##  주의사항

- 8K/4K 영상은 파일 크기가 매우 큽니다 (수 GB)
- 다운로드 시간은 영상 길이와 화질에 비례합니다
- 충분한 디스크 공간을 확보하세요
- 개인 학습 목적으로만 사용하세요

##  문제 해결

**"FFmpeg not found" 오류:**
- FFmpeg가 설치되어 있고 PATH에 등록되어 있는지 확인

**다운로드 실패:**
- YouTube URL이 올바른지 확인
- 인터넷 연결 확인
- 해당 영상이 선택한 화질을 지원하는지 확인

**서버가 느림:**
- 고화질 영상은 처리 시간이 오래 걸립니다
- 네트워크 속도를 확인하세요
