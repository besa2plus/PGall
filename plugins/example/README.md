# 예제 플러그인

PGall에서 플러그인이 어떻게 작동하고, 어떻게 라이브러리를 사용하는지 보여주기 위한 예제입니다.

## 기능

이 플러그인은 `libs/py/example` 라이브러리의 `say_hello` 함수를 호출하여 그 결과를 터미널에 출력합니다.

## 실행 방법

1.  `libs/py/example` 라이브러리가 존재하는지 확인하세요.
2.  PGall 런처를 사용하여 이 플러그인을 실행하세요.

### CLI 런처 사용 예시

```bash
# launchers/pgall-cli 디렉토리로 이동
cd ../../launchers/pgall-cli

# "Example Plugin" 실행
python main.py run "Example Plugin"
```

### 예상 출력 결과

```
예제 플러그인이 실행되었습니다...
`example` 라이브러리에서 `say_hello` 함수를 성공적으로 import 했습니다.
Hello, PGall 사용자! 이 메시지는 'example' 라이브러리에서 보냈습니다.
```
