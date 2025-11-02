import sys
import os

def main():
    """
    예제 플러그인의 메인 함수입니다.
    `libs` 디렉토리의 로컬 라이브러리를 어떻게 import하고 사용하는지 보여줍니다.
    또한 외부 의존성(colorama)이 제대로 설치되는지도 테스트합니다.
    """
    # 1. 외부 의존성 테스트
    print("=" * 60)
    print("🔍 외부 의존성 테스트: colorama 라이브러리")
    print("=" * 60)
    
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)  # Windows 호환성
        
        print(f"{Fore.GREEN}✅ colorama 라이브러리가 성공적으로 import 되었습니다!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📦 외부 의존성 설치가 제대로 작동합니다.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎨 이제 터미널에 색상을 출력할 수 있습니다!{Style.RESET_ALL}")
        print(f"{Fore.RED}❤️  {Fore.GREEN}💚 {Fore.BLUE}💙 {Fore.MAGENTA}💜{Style.RESET_ALL}")
        
    except ImportError as e:
        print(f"❌ colorama를 import 할 수 없습니다.")
        print(f"의존성 설치가 실패했을 수 있습니다: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🔍 로컬 라이브러리 테스트: libs/py/example")
    print("=" * 60)
    
    # 2. 로컬 라이브러리 테스트
    try:
        # `libs` 디렉토리의 경로를 올바르게 추적합니다.
        # 이 파일의 위치: plugins/example/main.py
        # 상대 경로: ../../libs/py
        libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'py'))
        if libs_path not in sys.path:
            sys.path.insert(0, libs_path)
        
        # 이제 라이브러리를 import 할 수 있습니다.
        from example import say_hello
        
        print(f"{Fore.GREEN}✅ lib/py/example 라이브러리로부터 `say_hello` 함수를 성공적으로 import 했습니다.{Style.RESET_ALL}")
        say_hello("PGall 사용자")

    except ImportError as e:
        print(f"{Fore.RED}\n❌ `example` 라이브러리를 import 할 수 없습니다.{Style.RESET_ALL}")
        print("`libs/py/example` 디렉토리가 올바른 구조로 존재하는지 확인해주세요.")
        print(f"에러 상세 정보: {e}")
    except Exception as e:
        print(f"{Fore.RED}\n❌ 예상치 못한 에러가 발생했습니다: {e}{Style.RESET_ALL}")
    
    print("\n" + "=" * 60)
    print(f"{Fore.GREEN}🎉 Example_Plugin 실행 완료!{Style.RESET_ALL}")
    print("=" * 60)

if __name__ == "__main__":
    main()
