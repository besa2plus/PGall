# 예제 유틸리티 라이브러리

PGall에서 라이브러리가 어떻게 작동하는지 보여주기 위한 예제 라이브러리입니다.

## 주요 기능

- `say_hello(name)`: 간단한 인사 메시지를 출력합니다.

## 사용법

플러그인의 `main.py`에서 다음과 같이 사용할 수 있습니다.

```python
import sys
import os

# `libs` 디렉토리 경로 추가
libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'py'))
sys.path.insert(0, libs_path)

# 라이브러리 import
from example import say_hello

# 함수 호출
say_hello("developer")
```
