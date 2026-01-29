import os
import subprocess

# 경로 확인
ffmpeg_path = r'C:\ffmpeg-8.0.1\ffmpeg-8.0.1\bin'
print(f"경로 존재 여부: {os.path.exists(ffmpeg_path)}")
print(f"경로 내용:")

if os.path.exists(ffmpeg_path):
    files = os.listdir(ffmpeg_path)
    for f in files:
        print(f"  - {f}")
else:
    print("경로가 존재하지 않습니다!")
    print("\n가능한 경로 확인:")
    
    # 상위 디렉토리 확인
    base = r'C:\ffmpeg-8.0.1'
    if os.path.exists(base):
        print(f"\n{base} 내용:")
        for item in os.listdir(base):
            print(f"  - {item}")
            full_path = os.path.join(base, item)
            if os.path.isdir(full_path):
                print(f"    {full_path} 내용:")
                try:
                    for subitem in os.listdir(full_path):
                        print(f"      - {subitem}")
                except:
                    pass

# ffmpeg 명령어 직접 실행 테스트
print("\n\nffmpeg 명령어 테스트:")
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    print("성공! ffmpeg가 PATH에 있습니다.")
    print(result.stdout[:200])
except:
    print("실패! ffmpeg를 찾을 수 없습니다.")
