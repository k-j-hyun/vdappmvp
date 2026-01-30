import subprocess
import json
import sys
import os

def check_video_info(video_path):
    """영상 파일의 HDR/SDR 정보를 확인"""
    
    if not os.path.exists(video_path):
        print(f"[오류] 파일을 찾을 수 없습니다: {video_path}")
        return
    
    # FFprobe 경로 (Windows 기준)
    ffprobe_path = r'C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffprobe.exe'
    
    # 시스템에 설치된 ffprobe 사용 시도
    if not os.path.exists(ffprobe_path):
        ffprobe_path = 'ffprobe'
    
    cmd = [
        ffprobe_path,
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-show_format',
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print(f"[오류] FFprobe 실행 실패: {result.stderr}")
            return
        
        data = json.loads(result.stdout)
        
        print("=" * 70)
        print(f"영상 정보: {os.path.basename(video_path)}")
        print("=" * 70)
        
        # 비디오 스트림 찾기
        video_stream = None
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                video_stream = stream
                break
        
        if not video_stream:
            print("[오류] 비디오 스트림을 찾을 수 없습니다.")
            return
        
        # 기본 정보
        print(f"\n[기본 정보]")
        print(f"  - 코덱: {video_stream.get('codec_name', 'N/A')}")
        print(f"  - 해상도: {video_stream.get('width', 'N/A')}x{video_stream.get('height', 'N/A')}")
        print(f"  - 프레임레이트: {video_stream.get('r_frame_rate', 'N/A')}")
        if video_stream.get('bit_rate'):
            print(f"  - 비트레이트: {int(video_stream.get('bit_rate', 0)) // 1000} kbps")
        else:
            print(f"  - 비트레이트: N/A")
        
        # 색 공간 정보
        color_space = video_stream.get('color_space', 'unknown')
        color_transfer = video_stream.get('color_transfer', 'unknown')
        color_primaries = video_stream.get('color_primaries', 'unknown')
        color_range = video_stream.get('color_range', 'unknown')
        
        print(f"\n[색 공간 정보]")
        print(f"  - Color Space: {color_space}")
        print(f"  - Color Transfer: {color_transfer}")
        print(f"  - Color Primaries: {color_primaries}")
        print(f"  - Color Range: {color_range}")
        
        # HDR 판별
        is_hdr = False
        hdr_type = "SDR"
        
        if color_transfer in ['smpte2084', 'arib-std-b67']:
            is_hdr = True
            if color_transfer == 'smpte2084':
                hdr_type = "HDR10 (PQ)"
            elif color_transfer == 'arib-std-b67':
                hdr_type = "HLG (Hybrid Log-Gamma)"
        
        if color_primaries == 'bt2020' and not is_hdr:
            hdr_type = "Wide Color Gamut (WCG)"
        
        print(f"\n[동적 범위]")
        if is_hdr:
            print(f"  >>> {hdr_type} 영상입니다!")
            print(f"  >>> HDR 지원 디스플레이에서 최적의 화질로 감상하세요")
        else:
            print(f"  >>> {hdr_type} 영상입니다")
        
        # 코덱 프로필 정보
        codec_name = video_stream.get('codec_name', '')
        profile = video_stream.get('profile', 'N/A')
        
        print(f"\n[코덱 상세]")
        print(f"  - 프로필: {profile}")
        
        if codec_name == 'vp9':
            if 'Profile 2' in profile or 'profile 2' in profile.lower():
                print(f"  >>> VP9 Profile 2 (HDR 지원 코덱)")
            elif 'Profile 0' in profile or 'profile 0' in profile.lower():
                print(f"  >>> VP9 Profile 0 (SDR 코덱)")
            else:
                print(f"  >>> VP9 코덱")
        elif codec_name == 'h264' or codec_name == 'avc':
            print(f"  >>> H.264/AVC 코덱 (일반적으로 SDR)")
        elif codec_name == 'hevc' or codec_name == 'h265':
            print(f"  >>> H.265/HEVC 코덱")
        
        # 파일 크기
        file_size = os.path.getsize(video_path)
        file_size_mb = file_size / (1024 * 1024)
        file_size_gb = file_size / (1024 * 1024 * 1024)
        
        print(f"\n[파일 정보]")
        if file_size_gb >= 1:
            print(f"  - 크기: {file_size_gb:.2f} GB")
        else:
            print(f"  - 크기: {file_size_mb:.2f} MB")
        
        print("\n" + "=" * 70)
        
        # 권장 사항
        if is_hdr and color_transfer == 'smpte2084':
            print("\n[재생 권장 사항]")
            print("  - Windows: 'Movies & TV' 앱, VLC (최신 버전)")
            print("  - macOS: QuickTime Player, IINA")
            print("  - HDR 지원 모니터/TV에서 최상의 화질을 경험할 수 있습니다")
            print("  - SDR 디스플레이에서는 색이 어둡게 보일 수 있습니다")
        
    except subprocess.TimeoutExpired:
        print("[오류] FFprobe 실행 시간 초과")
    except json.JSONDecodeError:
        print("[오류] FFprobe 출력 파싱 실패")
    except Exception as e:
        print(f"[오류] {e}")

def main():
    if len(sys.argv) < 2:
        print("사용법: python check_video_hdr.py <비디오_파일_경로>")
        print("\n예시:")
        print("  python check_video_hdr.py video.mp4")
        print("  python check_video_hdr.py C:\\Downloads\\my_video.mp4")
        return
    
    video_path = sys.argv[1]
    check_video_info(video_path)

if __name__ == '__main__':
    main()
