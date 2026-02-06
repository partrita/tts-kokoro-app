# tts-kokoro-app

Kokoro TTS용 로컬 애플리케이션입니다.

## Kokoro TTS란?

[Kokoro](https://huggingface.co/hexgrad/Kokoro-82M)는 8,200만 개의 파라미터를 가진 오픈 웨이트 TTS 모델입니다. 가벼운 아키텍처임에도 불구하고 대형 모델에 필적하는 품질을 제공하며, 훨씬 빠르고 비용 효율적입니다. Apache 라이선스가 적용된 가중치를 통해 프로덕션 환경부터 개인 프로젝트까지 어디에서나 배포할 수 있습니다.

## 웹 애플리케이션 주요 기능

이 프로젝트는 Kokoro 모델을 활용한 텍스트 음성 변환(TTS) 인터페이스를 제공합니다. 브라우저에서 직접 텍스트를 음성으로 변환하고 즉시 들어볼 수 있습니다.

- **인터랙티브 UI**: 텍스트를 직접 입력하거나 붙여넣어 음성을 생성할 수 있습니다.
- **음성 선택**: 다양한 Kokoro 목소리(여성, 남성, 미국/영국 발음 등)를 선택할 수 있습니다.
- **속도 조절**: 생성되는 음성의 속도를 0.5x에서 2.0x까지 조절할 수 있습니다.
- **모델 캐싱**: 효율적인 모델 관리를 통해 첫 실행 이후 매우 빠른 생성 속도를 제공합니다.

## 설치 안내

1.  **사전 준비 요구 사항**:
    *   `uv`: 빠르고 현대적인 Python 패키지 매니저. [uv 설치하기](https://github.com/astral-sh/uv).
    *   `ffmpeg`: 오디오 처리(MP3 내보내기)를 위해 시스템에 설치되어 있어야 합니다.
        *   macOS: `brew install ffmpeg`
        *   Debian/Ubuntu: `sudo apt-get install ffmpeg`
        *   기타 시스템: 각 환경의 패키지 관리자를 사용하세요.

2.  **저장소 클론**:
    ```bash
    gh repo clone partrita/tts-kokoro-app
    cd tts-kokoro-app
    ```

3.  **의존성 동기화 (가상 환경 자동 생성)**:
    ```bash
    uv sync
    ```

**주의 사항**: `kokoro` 라이브러리와 PyTorch 등의 의존성은 용량이 매우 큽니다. 설치 시 충분한 디스크 공간(수 GB 이상)이 있는지 확인하세요.

## 애플리케이션 실행

1.  **uv를 사용하여 Flask 웹 서버 시작**:
    ```bash
    uv run python -m app.main
    ```
2.  브라우저에서 `http://127.0.0.1:5001/`로 접속합니다.

## 사용 방법

1.  브라우저 화면의 텍스트 영역에 변환하고자 하는 텍스트를 입력합니다.
2.  원하는 목소리(Voice)와 재생 속도(Speed)를 선택합니다.
3.  **Generate Audio** 버튼을 클릭합니다.
4.  생성이 완료되면 하단에 나타나는 오디오 플레이어를 통해 결과를 확인할 수 있습니다.

## 레거시 명령줄 사용법 (CLI)

웹 인터페이스 외에도 명령줄에서 직접 음성을 생성할 수 있습니다.

```bash
python -m app.run --input data/welcome.txt --filename welcome --voice af_heart
```
- `--input (-i)`: 입력 텍스트 파일 경로
- `--filename (-n)`: 저장될 파일 이름 (확장자 제외)
- `--voice (-v)`: 목소리 이름 (기본값: af_heart)
