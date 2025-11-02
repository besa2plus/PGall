import sys
import os

def main():
    """
    예제 플러그인의 메인 함수입니다.
    `libs` 디렉토리의 로컬 라이브러리를 어떻게 import하고 사용하는지 보여줍니다.
    """
    print("예제 플러그인이 실행되었습니다...")
    
    try:
        # `libs` 디렉토리의 경로를 올바르게 추적합니다.
        # 이 파일의 위치: plugins/example/main.py
        # 상대 경로: ../../libs/py
        libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'py'))
        if libs_path not in sys.path:
            sys.path.insert(0, libs_path)
        
        # 이제 라이브러리를 import 할 수 있습니다.
        from example import say_hello
        
        print("lib/py/example 라이브러리로부터 `say_hello` 함수를 성공적으로 import 했습니다.")
        say_hello("PGall 사용자")

    except ImportError as e:
        print("\n`example` 라이브러리를 import 할 수 없습니다.")
        print("`libs/py/example` 디렉토리가 올바른 구조로 존재하는지 확인해주세요.")
        print(f"에러 상세 정보: {e}")
    except Exception as e:
        print(f"\n예상치 못한 에러가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
