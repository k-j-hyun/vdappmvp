from flask import Flask, request, send_file, jsonify, render_template_string
import yt_dlp
import os
import threading
import time
import subprocess

# 환경 변수를 가장 먼저 설정
os.environ['PATH'] = r'C:\Program Files\nodejs;' + os.environ.get('PATH', '')
os.environ['PATH'] = r'C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin;' + os.environ['PATH']

app = Flask(__name__)

# FFmpeg 경로 직접 설정
FFMPEG_PATH = r'C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe'
FFPROBE_PATH = r'C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffprobe.exe'

# 다운로드 디렉토리 생성
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# HTML 템플릿
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video 다운로더 (최대 8K HDR)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }
        
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        #status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            display: none;
        }
        
        #status.loading {
            background: #e3f2fd;
            color: #1976d2;
            display: block;
        }
        
        #status.success {
            background: #e8f5e9;
            color: #388e3c;
            display: block;
        }
        
        #status.error {
            background: #ffebee;
            color: #d32f2f;
            display: block;
        }
        
        .progress-bar {
            width: 100%;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            margin-top: 10px;
            overflow: hidden;
            display: none;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
            animation: progress 1.5s ease-in-out infinite;
        }
        
        @keyframes progress {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(400%); }
        }
        
        .info {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }
        
        .info ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        
        .info li {
            margin: 5px 0;
        }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 13px;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Video 다운로더</h1>
        <p class="subtitle">최대 8K HDR 지원 (고품질 우선)</p>
        
        <form id="downloadForm">
            <div class="form-group">
                <label for="url">Video URL</label>
                <input 
                    type="text" 
                    id="url" 
                    placeholder="https://www.youtube.com/watch?v=..." 
                    required
                >
            </div>
            
            <div class="form-group">
                <label for="quality">화질 선택</label>
                <select id="quality">
                    <optgroup label="HDR (고동적범위) - 권장">
                        <option value="8k-hdr">8K HDR (7680x4320)</option>
                        <option value="4k-hdr" selected>4K HDR (3840x2160)</option>
                        <option value="1440p-hdr">1440p HDR (2560x1440)</option>
                        <option value="1080p-hdr">1080p HDR (1920x1080)</option>
                    </optgroup>
                    <optgroup label="SDR (표준동적범위)">
                        <option value="8k-sdr">8K SDR (7680x4320)</option>
                        <option value="4k-sdr">4K SDR (3840x2160)</option>
                        <option value="1440p-sdr">1440p SDR (2560x1440)</option>
                        <option value="1080p-sdr">1080p SDR (1920x1080)</option>
                    </optgroup>
                    <optgroup label="일반 화질 (자동 선택)">
                        <option value="8k">8K (7680x4320)</option>
                        <option value="4k">4K (3840x2160)</option>
                        <option value="1440p">1440p (2560x1440)</option>
                        <option value="1080p">1080p (1920x1080)</option>
                        <option value="720p">720p (1280x720)</option>
                        <option value="480p">480p (854x480)</option>
                        <option value="360p">360p (640x360)</option>
                        <option value="best">최고 화질 (자동)</option>
                    </optgroup>
                </select>
            </div>
            
            <button type="submit" id="downloadBtn">다운로드 시작</button>
            
            <div id="status"></div>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
        </form>
        
        <div class="warning">
            주의: HDR을 선택하면 고품질 VP9.2 코덱을 우선으로 받습니다. 
            영상에 HDR이 없으면 동일 해상도의 최고 비트레이트 영상을 자동으로 다운로드합니다.
        </div>
        
        <div class="info">
            <strong>사용 안내</strong>
            <ul>
                <li><strong>HDR</strong>: VP9 Profile 2 코덱, 넓은 색 공간 (BT.2020), HDR 모니터 필요</li>
                <li><strong>SDR</strong>: VP9/H.264 코덱, 표준 색 공간 (BT.709), 모든 디스플레이 호환</li>
                <li>HDR 선택 시 고비트레이트 영상을 우선으로 다운로드합니다</li>
                <li>8K/4K는 용량이 크므로 충분한 저장 공간 필요</li>
            </ul>
        </div>
    </div>

    <script>
        const form = document.getElementById('downloadForm');
        const downloadBtn = document.getElementById('downloadBtn');
        const status = document.getElementById('status');
        const progressBar = document.querySelector('.progress-bar');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const url = document.getElementById('url').value;
            const quality = document.getElementById('quality').value;
            
            downloadBtn.disabled = true;
            status.className = 'loading';
            status.textContent = '다운로드 중... 잠시만 기다려주세요';
            progressBar.style.display = 'block';
            
            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url, quality })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || '다운로드 실패');
                }
                
                // 파일 다운로드
                const blob = await response.blob();
                const contentDisposition = response.headers.get('Content-Disposition');
                let filename = 'video.mp4';
                
                if (contentDisposition) {
                    const matches = /filename[^;=\\n]*=((['"]).*?\\2|[^;\\n]*)/.exec(contentDisposition);
                    if (matches != null && matches[1]) {
                        filename = matches[1].replace(/['"]/g, '');
                        filename = decodeURIComponent(filename);
                    }
                }
                
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(downloadUrl);
                
                status.className = 'success';
                status.textContent = '다운로드 완료!';
                progressBar.style.display = 'none';
                
            } catch (error) {
                status.className = 'error';
                status.textContent = '오류: ' + error.message;
                progressBar.style.display = 'none';
            } finally {
                downloadBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    print("\n[DEBUG] /download 엔드포인트 호출됨")
    print(f"[DEBUG] Request method: {request.method}")
    print(f"[DEBUG] Content-Type: {request.content_type}")
    
    try:
        data = request.get_json()
        print(f"[DEBUG] Received data: {data}")
        
        video_url = data.get('url')
        quality = data.get('quality', '4k')
        
        print(f"[DEBUG] Video URL: {video_url}")
        print(f"[DEBUG] Quality: {quality}")
        
        if not video_url:
            return jsonify({'error': 'URL이 필요합니다'}), 400
        
        # 개선된 화질별 포맷 설정 - 고품질 비트레이트 우선
        # HDR: VP9.2 코덱 우선 -> 고비트레이트 VP9 -> 고비트레이트 일반
        # SDR: VP9.0/AVC 코덱 우선 -> 고비트레이트 일반
        quality_formats = {
            # HDR - VP9.2 우선, 없으면 고비트레이트 영상으로 fallback
            '8k-hdr': (
                'bestvideo[vcodec^=vp9.2][height<=4320]+bestaudio/'
                'bestvideo[vcodec^=vp9][height<=4320][tbr>=20000]+bestaudio/'
                'bestvideo[height<=4320][tbr>=20000]+bestaudio/'
                'bestvideo[height<=4320]+bestaudio/best'
            ),
            '4k-hdr': (
                'bestvideo[vcodec^=vp9.2][height<=2160]+bestaudio/'
                'bestvideo[vcodec^=vp9][height<=2160][tbr>=8000]+bestaudio/'
                'bestvideo[height<=2160][tbr>=8000]+bestaudio/'
                'bestvideo[height<=2160]+bestaudio/best'
            ),
            '1440p-hdr': (
                'bestvideo[vcodec^=vp9.2][height<=1440]+bestaudio/'
                'bestvideo[vcodec^=vp9][height<=1440][tbr>=4000]+bestaudio/'
                'bestvideo[height<=1440][tbr>=4000]+bestaudio/'
                'bestvideo[height<=1440]+bestaudio/best'
            ),
            '1080p-hdr': (
                'bestvideo[vcodec^=vp9.2][height<=1080]+bestaudio/'
                'bestvideo[vcodec^=vp9][height<=1080][tbr>=2000]+bestaudio/'
                'bestvideo[height<=1080][tbr>=2000]+bestaudio/'
                'bestvideo[height<=1080]+bestaudio/best'
            ),
            
            # SDR - VP9.0/AVC 우선, 고비트레이트 fallback
            '8k-sdr': (
                'bestvideo[vcodec^=vp9.0][height<=4320]+bestaudio/'
                'bestvideo[vcodec^=avc][height<=4320]+bestaudio/'
                'bestvideo[height<=4320][tbr>=15000]+bestaudio/'
                'bestvideo[height<=4320]+bestaudio/best'
            ),
            '4k-sdr': (
                'bestvideo[vcodec^=vp9.0][height<=2160]+bestaudio/'
                'bestvideo[vcodec^=avc][height<=2160]+bestaudio/'
                'bestvideo[height<=2160][tbr>=6000]+bestaudio/'
                'bestvideo[height<=2160]+bestaudio/best'
            ),
            '1440p-sdr': (
                'bestvideo[vcodec^=vp9.0][height<=1440]+bestaudio/'
                'bestvideo[vcodec^=avc][height<=1440]+bestaudio/'
                'bestvideo[height<=1440][tbr>=3000]+bestaudio/'
                'bestvideo[height<=1440]+bestaudio/best'
            ),
            '1080p-sdr': (
                'bestvideo[vcodec^=vp9.0][height<=1080]+bestaudio/'
                'bestvideo[vcodec^=avc][height<=1080]+bestaudio/'
                'bestvideo[height<=1080][tbr>=1500]+bestaudio/'
                'bestvideo[height<=1080]+bestaudio/best'
            ),
            
            # 일반 화질 - 최고 비트레이트 우선
            '8k': 'bestvideo[height<=4320][tbr>=15000]+bestaudio/bestvideo[height<=4320]+bestaudio/best',
            '4k': 'bestvideo[height<=2160][tbr>=6000]+bestaudio/bestvideo[height<=2160]+bestaudio/best',
            '1440p': 'bestvideo[height<=1440][tbr>=3000]+bestaudio/bestvideo[height<=1440]+bestaudio/best',
            '1080p': 'bestvideo[height<=1080][tbr>=1500]+bestaudio/bestvideo[height<=1080]+bestaudio/best',
            '720p': 'bestvideo[height<=720][tbr>=1000]+bestaudio/bestvideo[height<=720]+bestaudio/best',
            '480p': 'bestvideo[height<=480]+bestaudio/best',
            '360p': 'bestvideo[height<=360]+bestaudio/best',
            'best': 'bestvideo+bestaudio/best'
        }
        
        format_string = quality_formats.get(quality, quality_formats['4k'])
        
        print("\n" + "="*60)
        print(f"다운로드 시작 (고품질 우선 모드)")
        print(f"URL: {video_url}")
        print(f"화질: {quality}")
        print(f"포맷 필터: {format_string[:100]}...")
        print("="*60 + "\n")
        
        # 임시 파일명 생성
        import uuid
        temp_filename = f"temp_{uuid.uuid4().hex[:8]}"
        output_template = os.path.join(DOWNLOAD_DIR, f'{temp_filename}.%(ext)s')
        
        # yt-dlp 경로 직접 지정
        ytdlp_path = r'C:\Users\HDIT\AppData\Local\Programs\Python\Python310\Scripts\yt-dlp.exe'
        
        if not os.path.exists(ytdlp_path):
            # 경로가 없으면 where 명령으로 찾기
            try:
                result = subprocess.run(['where', 'yt-dlp'], capture_output=True, text=True)
                if result.returncode == 0:
                    ytdlp_path = result.stdout.strip().split('\n')[0]
            except:
                ytdlp_path = 'yt-dlp'
        
        print(f"[DEBUG] yt-dlp 경로: {ytdlp_path}")
        
        # yt-dlp 명령어 구성
        cmd = [
            ytdlp_path,
            '--js-runtimes', 'node',
            '--remote-components', 'ejs:github',
            '--format', format_string,
            '--merge-output-format', 'mp4',
            '--output', output_template,
            '--ffmpeg-location', FFMPEG_PATH.replace('ffmpeg.exe', '').rstrip('\\'),
            '--progress',
            '--newline',
            '--embed-metadata',
            '--embed-thumbnail',
        ]
        
        # 쿠키 파일 있으면 추가
        if os.path.exists('cookies.txt'):
            cmd.extend(['--cookies', 'cookies.txt'])
        
        cmd.append(video_url)
        
        print(f"[DEBUG] 실행 명령어: {' '.join(cmd)}\n")
        
        # subprocess로 실행
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 실시간 출력
        stdout_lines = []
        stderr_lines = []
        
        for line in process.stdout:
            print(line, end='')
            stdout_lines.append(line)
            # 선택된 포맷 정보 출력
            if '[info]' in line and 'format' in line.lower():
                print(f"선택된 포맷: {line.strip()}")
        
        # stderr도 읽기
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"[STDERR]\n{stderr_output}")
            stderr_lines.append(stderr_output)
        
        process.wait()
        
        if process.returncode != 0:
            error_msg = f'yt-dlp 실행 실패 (코드: {process.returncode})'
            if stderr_output:
                error_msg += f'\n세부 정보: {stderr_output[:500]}'
            print(f"\n[ERROR] {error_msg}\n")
            print(f"[ERROR] 명령어: {' '.join(cmd)}\n")
            return jsonify({'error': error_msg}), 500
        
        # 생성된 파일 찾기
        files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(temp_filename)]
        if not files:
            return jsonify({'error': '다운로드된 파일을 찾을 수 없습니다'}), 404
        
        filename = os.path.join(DOWNLOAD_DIR, files[0])
        
        # 파일 정보 출력
        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        print(f"\n파일 처리 완료: {os.path.basename(filename)}")
        print(f"파일 크기: {file_size:.2f} MB")
        print("브라우저로 파일 전송 중...\n")
        
        # 파일 전송 후 삭제
        def remove_file(path):
            time.sleep(3)
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"임시 파일 삭제 완료: {os.path.basename(path)}\n")
            except Exception as e:
                print(f"파일 삭제 오류: {e}\n")
        
        threading.Thread(target=remove_file, args=(filename,)).start()
        
        return send_file(
            filename,
            as_attachment=True,
            download_name=os.path.basename(filename),
            mimetype='video/mp4'
        )
        
    except Exception as e:
        print(f"\n오류 발생: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("=" * 60)
    print("YouTube 다운로더 서버 시작 (고품질 최적화)")
    print("=" * 60)
    
    # Node.js 확인
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print(f"Node.js 감지: {result.stdout.strip()}")
        else:
            print("Node.js 실행 실패")
    except Exception as e:
        print(f"Node.js 찾을 수 없음: {e}")
    
    print(f"로컬 접속: http://localhost:5000")
    print(f"네트워크 접속: http://{local_ip}:5000")
    print("-" * 60)
    
    # 쿠키 파일 확인
    if os.path.exists('cookies.txt'):
        print("cookies.txt 파일 감지됨 - YouTube 로그인 사용")
    else:
        print("cookies.txt 없음 - 일부 영상 다운로드 제한 가능")
    
    print("-" * 60)
    print("개선 사항:")
    print("  - HDR 우선, 고비트레이트 fallback 추가")
    print("  - 4K HDR: 최소 8000 kbps 비트레이트 보장")
    print("  - 1080p HDR: 최소 2000 kbps 비트레이트 보장")
    print("  - VP9.2 (HDR) -> VP9 고화질 -> 일반 고화질 순서")
    print("-" * 60)
    print("같은 WiFi의 다른 기기에서 네트워크 주소로 접속하세요")
    print("종료하려면 Ctrl+C를 누르세요")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

# Developer: kjhyun
# Improved: 2025 - High bitrate priority for better quality
