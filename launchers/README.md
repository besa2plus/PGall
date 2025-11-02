# 🚀 Launchers

PGall 플러그인 런처 애플리케이션들이 위치하는 디렉토리입니다.

## 개요

런처는 PGall의 핵심 구성 요소로, `plugins/` 디렉토리에 있는 모든 플러그인을 자동으로 스캔하고 사용자가 쉽게 설치/실행할 수 있는 인터페이스를 제공합니다.

## 런처 애플리케이션 (미구현)

### 1. `pgall-web/` - 웹 기반 UI 런처

브라우저에서 실행되는 웹 애플리케이션으로, 직관적인 UI를 통해 플러그인을 관리할 수 있습니다.

**특징:**
- 플러그인 카드 형태의 시각적 인터페이스
- 원클릭으로 플러그인 설치/실행
- 플러그인 상태 실시간 모니터링
- 태그 기반 플러그인 필터링/검색
- 복잡도별 플러그인 분류 뷰

**실행 방법:**
```bash
cd pgall-web/
npm install
npm start
# http://localhost:3000에서 접속
```

### 2. `pgall-cli/` - 커맨드라인 런처

터미널에서 실행되는 CLI 애플리케이션으로, 스크립트나 자동화에 적합합니다.

**특징:**
- 빠른 플러그인 목록 조회
- 배치 설치/실행 지원
- JSON 출력으로 파이프라인 연동 가능
- 로그 및 상태 추적

**실행 방법:**
```bash
cd pgall-cli/
python -m pip install -r requirements.txt
python main.py --help
```

**사용 예시:**
```bash
# 모든 플러그인 목록 조회
python main.py list

# 특정 플러그인 실행
python main.py run "Example_Plugin"

# 복잡도별 플러그인 조회
python main.py list --level production

# 플러그인 설치
python main.py install smart-cctv
```

## 런처의 작동 원리

### 1. 플러그인 스캔
런처 시작 시 `plugins/` 디렉토리를 재귀적으로 탐색하여 `plugin.json` 파일이 있는 모든 디렉토리를 플러그인으로 인식합니다.

### 2. 메타데이터 파싱
각 `plugin.json` 파일을 읽어서 플러그인의 메타데이터(이름, 설명, 복잡도, 의존성 등)를 파싱하고 인메모리 데이터베이스에 저장합니다.

### 3. 의존성 해결
플러그인 실행 전에 `plugin.json`의 `scripts.install` 명령어를 실행하여 필요한 의존성을 설치합니다.

### 4. 플러그인 실행
`scripts.start` 명령어를 실행하여 플러그인을 시작하고, 프로세스를 모니터링합니다.

### 5. 상태 관리
실행 중인 플러그인의 상태(실행 중, 중지됨, 오류)를 추적하고 UI에 반영합니다.

## 런처 개발하기

새로운 런처를 개발하려면 다음 기능을 구현해야 합니다:

### 필수 기능
- [ ] 플러그인 스캔 및 `plugin.json` 파싱
- [ ] 플러그인 목록 표시
- [ ] 플러그인 설치 (`scripts.install` 실행)
- [ ] 플러그인 실행 (`scripts.start` 실행)
- [ ] 플러그인 상태 모니터링

### 권장 기능
- [ ] 태그 기반 필터링
- [ ] 복잡도별 분류
- [ ] 검색 기능
- [ ] 의존성 관리
- [ ] 로그 수집 및 표시

### 예시 구현

```python
# 플러그인 스캔 예시 (Python)
import json
import os
from pathlib import Path

def scan_plugins():
    plugins = []
    plugins_dir = Path("../../plugins")
    
    for plugin_dir in plugins_dir.iterdir():
        if plugin_dir.is_dir():
            plugin_json = plugin_dir / "plugin.json"
            if plugin_json.exists():
                with open(plugin_json) as f:
                    plugin_data = json.load(f)
                    plugin_data['path'] = str(plugin_dir)
                    plugins.append(plugin_data)
    
    return plugins
```

## 기여하기

런처 개선에 기여하고 싶으시면:

1. 기존 런처의 기능 개선
2. 새로운 플랫폼용 런처 개발 (GUI, 모바일 앱 등)
3. 플러그인 생태계 확장을 위한 도구 개발

모든 기여는 환영합니다!
