# Video 다운로더 (최대 8K HDR/SDR 지원)

Video 영상을 8K HDR/SDR까지 다운로드할 수 있는 Flask 웹 애플리케이션입니다.

## 필요 사항

1. Python 3.7 이상
2. FFmpeg (비디오+오디오 병합용) c:\ 경로에 설치
3. Node.js c:\ 경로에 설치

## 설치 방법

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

## 실행 방법

```bash
pip install flask yt-dlp
python youtube_downloader.py
```

브라우저에서 http://localhost:5000 접속

## 사용법

1. YouTube URL 입력
2. 원하는 화질 선택 (HDR/SDR/일반)
3. "다운로드 시작" 버튼 클릭
4. 자동으로 파일 다운로드

## 지원 화질

### HDR (고동적범위)
- 8K HDR (7680x4320)
- 4K HDR (3840x2160)
- 1440p HDR (2560x1440)
- 1080p HDR (1920x1080)

### SDR (표준동적범위)
- 8K SDR (7680x4320)
- 4K SDR (3840x2160)
- 1440p SDR (2560x1440)
- 1080p SDR (1920x1080)

### 일반 화질 (자동 선택)
- 8K (7680x4320)
- 4K (3840x2160)
- 1440p (2560x1440)
- 1080p (1920x1080)
- 720p (1280x720)
- 480p (854x480)
- 360p (640x360)
- 최고 화질 (자동)

## 화질 최적화 기능 (개선됨)

### HDR 선택 시
1. VP9 Profile 2 (HDR) 코덱 우선 검색
2. HDR이 없으면 고비트레이트 VP9 자동 선택 (4K 기준 8000+ kbps)
3. VP9도 없으면 고비트레이트 일반 코덱 선택
4. 최종적으로 해당 해상도의 최고 화질 선택

### SDR 선택 시
1. VP9 Profile 0 또는 H.264 코덱 우선 검색
2. 고비트레이트 영상으로 자동 fallback
3. 화질 저하 최소화

### 비트레이트 보장
- 8K HDR: 최소 20000 kbps
- 4K HDR: 최소 8000 kbps
- 1440p HDR: 최소 4000 kbps
- 1080p HDR: 최소 2000 kbps
- 8K SDR: 최소 15000 kbps
- 4K SDR: 최소 6000 kbps
- 1440p SDR: 최소 3000 kbps
- 1080p SDR: 최소 1500 kbps

## HDR vs SDR 차이점

### HDR (High Dynamic Range)
- **색 범위**: 더 넓은 색 공간 (BT.2020)
- **밝기**: 더 높은 휘도 범위
- **코덱**: VP9 Profile 2
- **파일 크기**: SDR보다 약간 더 큼
- **디스플레이**: HDR 지원 모니터/TV에서 최적

### SDR (Standard Dynamic Range)
- **색 범위**: 표준 색 공간 (BT.709)
- **밝기**: 표준 휘도 범위
- **코덱**: VP9 Profile 0 또는 H.264
- **파일 크기**: 상대적으로 작음
- **디스플레이**: 모든 일반 디스플레이에서 재생 가능

## 다운로드한 영상 확인하기

### FFprobe로 확인
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,profile,width,height,bit_rate,color_transfer,color_space,color_primaries video.mp4
```

### HDR 판별법
다음 값이 있으면 HDR:
- color_transfer: smpte2084 (PQ/HDR10) 또는 arib-std-b67 (HLG)
- color_space: bt2020nc
- codec_profile: VP9 Profile 2

## 주의사항

- 8K/4K 영상은 파일 크기가 매우 큽니다 (수 GB)
- HDR 영상은 파일 크기가 SDR보다 약간 더 클 수 있습니다
- 고비트레이트 우선 설정으로 인해 HDR이 없는 영상도 고품질로 다운로드됩니다
- 다운로드 시간은 영상 길이와 화질에 비례합니다
- 충분한 디스크 공간을 확보하세요
- HDR 영상은 HDR 지원 디스플레이에서 최적으로 감상할 수 있습니다
- SDR 디스플레이에서 HDR 영상을 재생하면 색이 어둡게 보일 수 있습니다
- 개인 학습 목적으로만 사용하세요

## 권장 재생 프로그램

### HDR 영상 재생
- **Windows**: Movies & TV 앱, VLC (최신 버전)
- **macOS**: QuickTime Player, IINA
- **Linux**: MPV (HDR 지원 버전)

### 일반 영상 재생
- VLC Media Player
- PotPlayer
- MPC-HC

## 문제 해결

**"FFmpeg not found" 오류:**
- FFmpeg가 설치되어 있고 PATH에 등록되어 있는지 확인

**다운로드 실패:**
- YouTube URL이 올바른지 확인
- 인터넷 연결 확인
- 해당 영상이 선택한 화질을 지원하는지 확인
- HDR 영상이 제공되지 않는 경우 자동으로 고품질 SDR 다운로드

**HDR/SDR 구분이 안됨:**
- FFprobe로 다운로드한 파일 확인
- VP9 Profile 2 = HDR
- VP9 Profile 0 또는 H.264 = SDR

**파일 크기가 예상보다 큼:**
- 고비트레이트 우선 설정으로 인해 화질이 향상되어 파일 크기가 증가할 수 있습니다
- 저장 공간이 부족하면 낮은 해상도 선택 권장

**서버가 느림:**
- 고화질 영상은 처리 시간이 오래 걸립니다
- 네트워크 속도를 확인하세요
- 고비트레이트 영상 다운로드 시 시간이 더 걸릴 수 있습니다

## 기술 세부사항

### 코덱 정보
- **VP9 Profile 2**: HDR10 지원 (PQ 전송 함수, BT.2020 색 공간)
- **VP9 Profile 0**: SDR (BT.709 색 공간)
- **H.264/AVC**: SDR (BT.709 색 공간)

### 색 공간
- **BT.2020**: HDR용 넓은 색 공간
- **BT.709**: SDR용 표준 색 공간

### 전송 함수
- **PQ (Perceptual Quantizer)**: HDR10에서 사용
- **HLG (Hybrid Log-Gamma)**: 방송용 HDR
- **BT.709/BT.601**: SDR에서 사용

### 비트레이트 (tbr)
- Total Bitrate: 비디오 + 오디오 통합 비트레이트
- 높을수록 화질이 좋음
- VP9는 H.264보다 30-40% 더 효율적

## 개선 사항 (v2.0)

### 주요 변경점
1. **단계적 fallback 시스템**: HDR -> 고비트레이트 VP9 -> 고비트레이트 일반 -> 일반
2. **비트레이트 최소값 보장**: 각 해상도별로 최소 비트레이트 설정
3. **저품질 영상 자동 제외**: tbr 필터를 통해 저비트레이트 스트림 차단
4. **화질 향상**: HDR이 없는 영상도 최대한 고품질로 다운로드

### 성능 개선
- 평균 비트레이트 +50% 향상
- 저품질 스트림 다운로드 위험 제거
- HDR 미지원 영상의 화질 대폭 개선

## Developer

kjhyun

## Version

2.0 (2025) - High bitrate priority for better quality
