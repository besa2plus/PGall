# 🔌 Plugins

PGall 플러그인 디렉토리입니다. 여기에 여러분이 만든 프로젝트를 기여할 수 있습니다.

## 플러그인 기여하기

### 1. 새 플러그인 디렉토리 생성

```bash
cd plugins/
mkdir my-awesome-plugin
cd my-awesome-plugin/
```

### 2. 플러그인 규약: 표준 스크립트

PGall은 **표준 스크립트 파일**을 사용하여 플러그인을 실행합니다. 이를 통해 개발자는 완전한 자율성을 가지며, 런처는 단순하고 예측 가능하게 동작합니다.

**필수 파일:**
- `plugin.json`: 플러그인 메타데이터
- `run.sh` (또는 `run.bat`): 플러그인 실행 스크립트

**선택 파일:**
- `install.sh` (또는 `install.bat`): 의존성 설치 스크립트

**권장 구조:**
```
my-plugin/
├── plugin.json       # (아래 예시 참고)
├── install.sh       # (선택) 의존성 설치
├── run.sh           # (필수) 플러그인 실행
├── README.md
└── ... (소스 코드, 의존성 파일 등)
```

#### `plugin.json` 명세
`plugin.json`에는 순수한 메타데이터만 담습니다.

- `name` (string): 플러그인 이름
- `description` (string): 플러그인 설명
- `authors` (string[]): 제작자 목록
- `version` (string): 플러그인 버전
- `level` (string): 프로젝트 복잡도 (`function`, `service`, `production`)
- `language` (string): 주 사용 언어
- `tags` (string[]): 카테고리/검색용 태그
- `platforms` (object): 지원하는 OS 정보
  - `windows` (string): "supported" | "unsupported"
  - `macos` (string): "supported" | "unsupported"
  - `linux` (string): "supported" | "unsupported"

**예시 `plugin.json`:**
```json
{
  "name": "이미지 리사이저",
  "description": "여러 이미지를 일괄로 리사이즈하는 도구",
  "authors": ["your-github-username"],
  "version": "1.0.0",
  "level": "function",
  "language": "python",
  "tags": ["image", "resize", "batch"],
  "platforms": {
    "windows": "supported",
    "macos": "supported",
    "linux": "supported"
  }
}
```

### 3. 스크립트 작성 가이드

#### `install.sh` (의존성 설치)
- 이 스크립트는 런처가 플러그인을 실행하기 전에 **한 번** 호출합니다.
- 예시 (`requirements.txt` 사용):
  ```bash
  #!/bin/bash
  set -e
  
  # 가상환경 생성 및 의존성 설치
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
  ```

#### `run.sh` (플러그인 실행)
- 이 스크립트는 플러그인을 실제로 실행하는 로직을 담습니다.
- 예시 (Python 가상환경):
  ```bash
  #!/bin/bash
  set -e

  # 가상환경 활성화 및 메인 스크립트 실행
  source .venv/bin/activate
  python main.py
  ```
- 예시 (Docker):
  ```bash
  #!/bin/bash
  docker-compose up
  ```

> **Windows 사용자**: `.sh` 파일 대신 `.bat` 파일을 생성할 수 있습니다. 런처는 OS에 맞는 파일을 우선적으로 실행합니다. (예: `run.bat` > `run.sh`)

### 4. 필수 요구사항

✅ **모든 플러그인은 다음을 포함해야 합니다:**

- `plugin.json` 파일
- `README.md` (문제 → 해결 → 실행 방법 + 구조 설명)
- 실행 결과 증빙 (영상/GIF/스크린샷)
- 의존성 파일 (`requirements.txt`, `package.json`, `Cargo.toml` 등)

### 5. 테스트

플러그인을 PGall에서 제대로 실행되는지 테스트해보세요:

```bash
# PGall 런처 실행
cd ../../launchers/pgall-cli/
python main.py

# 또는 웹 UI
cd ../pgall-web/
npm start
```

### 6. PR 제출

- **Signed-off-by 커밋** 필수: `git commit -sm "플러그인 추가: 이미지 리사이저"`
- 플러그인이 정상 동작하는지 확인 후 PR 생성

---

## 기존 플러그인 목록

- [`smart-cctv/`](./smart-cctv/) - 얼굴/차량 감지 및 이벤트 기록을 통한 스마트 관제 시스템 (Production)

---

궁금한 점이 있으시면 [이슈](../../issues)를 생성해주세요!
