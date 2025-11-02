# 📚 Libraries

PGall 공통 라이브러리 디렉토리입니다. 여러 플러그인에서 재사용할 수 있는 공통 코드들이 언어별로 정리되어 있습니다.

## 개요

라이브러리는 플러그인 개발자들이 자주 사용하는 기능들을 미리 구현해둔 코드 모음입니다. 플러그인에서 이 라이브러리들을 사용하면 개발 시간을 단축하고 코드 품질을 높일 수 있습니다.

## 언어별 라이브러리

### 📁 `js/` - JavaScript/TypeScript 라이브러리

Node.js 및 브라우저 환경에서 사용할 수 있는 JavaScript/TypeScript 라이브러리들이 위치할 예정입니다.

**현재 상태:** 빈 디렉토리 (기여를 기다리고 있습니다!)

**기여 가능한 라이브러리 예시:**
- 파일 처리 유틸리티
- 재사용 가능한 웹 컴포넌트  
- REST API 클라이언트 헬퍼
- 데이터 검증 라이브러리

### 📁 `py/` - Python 라이브러리

Python 프로젝트에서 사용할 수 있는 라이브러리들이 위치할 예정입니다.

**현재 상태:** 빈 디렉토리 (기여를 기다리고 있습니다!)

**기여 가능한 라이브러리 예시:**
- 파일 처리 및 변환
- 웹 스크래핑 도구
- 데이터 분석 유틸리티
- 이미지/영상 처리 도구

### 📁 `rust/` - Rust 라이브러리

성능이 중요한 작업을 위한 Rust 라이브러리들이 위치할 예정입니다.

**현재 상태:** 빈 디렉토리 (기여를 기다리고 있습니다!)

**기여 가능한 라이브러리 예시:**
- 고성능 파일 처리
- 암호화/해시 유틸리티
- 네트워크 프로그래밍 도구
- 시스템 리소스 모니터링

## 라이브러리 사용하기

### 1. 플러그인에서 라이브러리 사용

`plugin.json`의 `dependencies.libs` 필드에 사용할 라이브러리를 명시합니다:

```json
{
  "name": "My Plugin",
  "dependencies": {
    "libs": ["py/file-processor", "js/web-components"],
    "external": ["requests", "express"]
  }
}
```

### 2. 라이브러리 import 방법

#### Python
```python
# 상대경로로 라이브러리 import
import sys
sys.path.append('../../libs/py/file-processor')
from file_processor import convert_image

# 또는 PYTHONPATH 설정 후
from libs.py.file_processor import convert_image
```

#### JavaScript/TypeScript
```javascript
// 상대경로로 라이브러리 import
import { FileUploader } from '../../libs/js/web-components/FileUploader';
import { ApiClient } from '../../libs/js/api-client/client';
```

#### Rust
```rust
// Cargo.toml에서 경로 의존성 설정
[dependencies]
file-ops = { path = "../../libs/rust/file-ops" }

// 코드에서 사용
use file_ops::process_file;
```

## 라이브러리 명세 (`library.json`)

모든 라이브러리는 루트 디렉토리에 `library.json` 파일을 포함해야 합니다. 이 파일을 통해 PGall 시스템이 라이브러리를 인식하고, 기여자를 명시하며, 플러그인과의 의존성을 관리합니다.

**필수 필드:**
- `name` (string): 라이브러리 이름 (고유 식별자, 예: "file-processor")
- `description` (string): 라이브러리에 대한 간략한 설명
- `authors` (string[]): 제작자 목록
- `version` (string): 라이브러리 버전
- `language` (string): 주 사용 언어 ("python", "javascript", "rust")

**선택 필드:**
- `tags` (string[]): 검색 및 분류를 위한 태그
- `repository` (string): 원본 소스 코드 저장소 URL

**예시 `library.json`:**
```json
{
  "name": "vision-utils",
  "description": "OpenCV와 TensorFlow를 활용한 이미지 및 영상 처리 유틸리티",
  "authors": ["besa", "hardl"],
  "version": "0.1.0",
  "language": "python",
  "tags": ["vision", "ai", "image-processing", "opencv"],
  "repository": "https://github.com/PGall/libs/tree/main/py/vision-utils"
}
```

## 라이브러리 개발하기

### 1. 새 라이브러리 생성

```bash
# 언어별 디렉토리에 새 라이브러리 생성
cd libs/py/
mkdir my-new-lib
cd my-new-lib/
```

### 2. `library.json` 파일 생성
새 라이브러리 디렉토리의 루트에 `library.json` 파일을 생성하고 위 `라이브러리 명세` 섹션을 참고하여 내용을 작성합니다.

### 3. 라이브러리 구조

#### Python 라이브러리
```
my-python-lib/
├── library.json        # 👈 라이브러리 명세 파일
├── README.md           # 라이브러리 설명 및 사용법
├── __init__.py         # 패키지 초기화
├── setup.py           # 설치 스크립트 (선택사항)
├── requirements.txt   # 의존성
├── src/
│   └── main_module.py
├── tests/
│   └── test_main.py
└── examples/
    └── usage_example.py
```

#### JavaScript 라이브러리
```
my-js-lib/
├── library.json        # 👈 라이브러리 명세 파일
├── README.md
├── package.json       # NPM 패키지 설정
├── tsconfig.json      # TypeScript 설정
├── src/
│   └── index.ts
├── dist/              # 빌드 결과물
├── tests/
└── examples/
```

#### Rust 라이브러리
```
my-rust-lib/
├── library.json        # 👈 라이브러리 명세 파일
├── README.md
├── Cargo.toml         # Rust 패키지 설정
├── src/
│   └── lib.rs
├── tests/
└── examples/
```

### 4. 라이브러리 요구사항

✅ **모든 라이브러리는 다음을 포함해야 합니다:**

- `library.json` 파일
- `README.md` - 라이브러리 목적, API 문서, 사용 예시
- 사용 예시 코드
- 명확한 API 인터페이스
- 의존성 명시

### 4. API 설계 가이드라인

#### 일관성 있는 네이밍
```python
# 좋은 예
def convert_image_to_pdf(image_path: str, output_path: str) -> bool:
def process_file_batch(file_paths: List[str]) -> List[ProcessResult]:

# 나쁜 예
def img2pdf(img, out):
def proc_files(files):
```

#### 명확한 에러 처리
```python
class FileProcessorError(Exception):
    """파일 처리 중 발생하는 에러"""
    pass

def convert_image(input_path: str) -> str:
    if not os.path.exists(input_path):
        raise FileProcessorError(f"파일을 찾을 수 없습니다: {input_path}")
```

#### 타입 힌트 사용 (Python/TypeScript)
```python
from typing import List, Optional, Dict

def analyze_data(
    data: List[Dict[str, Any]], 
    config: Optional[Dict[str, str]] = None
) -> AnalysisResult:
    pass
```

## 라이브러리 목록

### Python (`py/`)
📂 *빈 디렉토리* - 첫 번째 Python 라이브러리 기여자를 기다리고 있습니다!

### JavaScript (`js/`)
📂 *빈 디렉토리* - 첫 번째 JavaScript 라이브러리 기여자를 기다리고 있습니다!

### Rust (`rust/`)
📂 *빈 디렉토리* - 첫 번째 Rust 라이브러리 기여자를 기다리고 있습니다!

## 기여하기

라이브러리 생태계 확장에 기여하려면:

1. **새 라이브러리 개발**: 자주 사용되는 기능을 재사용 가능한 라이브러리로 분리
2. **기존 라이브러리 개선**: 성능 최적화, 기능 추가, 버그 수정
3. **문서 개선**: 사용법 예시, API 문서 보완
4. **테스트 추가**: 신뢰성 향상을 위한 테스트 케이스 작성

모든 기여는 Signed-off-by 커밋과 함께 PR로 제출해주세요!
