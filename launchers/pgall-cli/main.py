import argparse
import json
import os
import subprocess
from pathlib import Path

# 프로젝트의 루트 디렉토리를 찾습니다. (launchers/pgall-cli/main.py 기준)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = PROJECT_ROOT / "plugins"

def scan_plugins():
    """`plugins` 디렉토리를 스캔하여 유효한 플러그인 목록을 반환합니다."""
    plugins = {}
    if not PLUGINS_DIR.exists():
        print(f"에러: 플러그인 디렉토리를 '{PLUGINS_DIR}'에서 찾을 수 없습니다.")
        return plugins

    for plugin_dir in PLUGINS_DIR.iterdir():
        if plugin_dir.is_dir():
            manifest_path = plugin_dir / "plugin.json"
            if manifest_path.exists():
                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                        plugin_name = manifest.get("name")
                        if plugin_name:
                            manifest["path"] = str(plugin_dir)
                            plugins[plugin_name] = manifest
                        else:
                            print(f"경고: '{manifest_path}'의 플러그인 명세에 'name' 속성이 없습니다.")
                except json.JSONDecodeError:
                    print(f"경고: '{manifest_path}'를 파싱할 수 없습니다. 유효하지 않은 JSON입니다.")
                except Exception as e:
                    print(f"경고: '{manifest_path}'를 읽는 중 예상치 못한 오류가 발생했습니다: {e}")
    return plugins

def list_plugins(plugins):
    """플러그인 목록을 보기 좋게 출력합니다."""
    if not plugins:
        print("설치된 플러그인이 없습니다.")
        return

    print(f"{'플러그인 이름':<25} {'버전':<10} {'레벨':<12} {'설명'}")
    print("-" * 80)
    for name, data in plugins.items():
        version = data.get('version', 'N/A')
        level = data.get('level', 'N/A')
        description = data.get('description', '')
        print(f"{name:<25} {version:<10} {level:<12} {description}")

def run_plugin(plugins, plugin_name):
    """특정 플러그인을 실행합니다."""
    plugin = plugins.get(plugin_name)
    if not plugin:
        print(f"에러: '{plugin_name}' 플러그인을 찾을 수 없습니다.")
        print("사용 가능한 플러그인:")
        list_plugins(plugins)
        return

    print(f"--- 플러그인 실행: {plugin_name} ---")

    plugin_path = plugin.get("path")
    scripts = plugin.get("scripts", {})
    
    # 1. 의존성 설치 (install 스크립트)
    install_script = scripts.get("install")
    if install_script:
        print(f"설치 스크립트 실행: '{install_script}'...")
        try:
            # shell=True를 사용하여 복잡한 명령어(예: pip install -r ...) 처리
            subprocess.run(install_script, cwd=plugin_path, check=True, shell=True)
            print("설치 스크립트가 성공적으로 완료되었습니다.")
        except subprocess.CalledProcessError as e:
            print(f"설치 스크립트 실행 중 오류 발생: {e}")
            return
        except FileNotFoundError:
            print(f"에러: 명령어를 찾을 수 없습니다. '{install_script.split()[0]}' 명령어가 PATH에 있는지 확인해주세요.")
            return

    # 2. 플러그인 실행 (start 스크립트)
    start_script = scripts.get("start")
    if not start_script:
        print("에러: 'plugin.json'에 'start' 스크립트가 정의되지 않았습니다.")
        return
        
    print(f"시작 스크립트 실행: '{start_script}'...")
    try:
        subprocess.run(start_script, cwd=plugin_path, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"시작 스크립트 실행 중 오류 발생: {e}")
    except FileNotFoundError:
        print(f"에러: 명령어를 찾을 수 없습니다. '{start_script.split()[0]}' 명령어가 PATH에 있는지 확인해주세요.")
        return
    
    print(f"--- 플러그인 종료: {plugin_name} ---")


def main():
    """CLI 애플리케이션의 메인 로직입니다."""
    parser = argparse.ArgumentParser(description="PGall - 플러그인 갤러리 런처")
    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어", required=True)

    # `list` 명령어
    parser_list = subparsers.add_parser("list", help="사용 가능한 모든 플러그인 목록을 보여줍니다.")

    # `run` 명령어
    parser_run = subparsers.add_parser("run", help="특정 플러그인을 실행합니다.")
    parser_run.add_argument("name", help="실행할 플러그인의 이름")

    args = parser.parse_args()
    
    plugins = scan_plugins()

    if args.command == "list":
        list_plugins(plugins)
    elif args.command == "run":
        run_plugin(plugins, args.name)

if __name__ == "__main__":
    main()
