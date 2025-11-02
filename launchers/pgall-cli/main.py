import argparse
import json
import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

# 프로젝트의 루트 디렉토리를 찾습니다. (launchers/pgall-cli/main.py 기준)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = PROJECT_ROOT / "plugins"

# Rich Console 초기화
console = Console()

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
        console.print("[yellow]설치된 플러그인이 없습니다.[/yellow]")
        return

    table = Table(title="🔌 사용 가능한 플러그인", box=box.ROUNDED)
    table.add_column("플러그인 이름", style="cyan", no_wrap=True)
    table.add_column("버전", style="magenta")
    table.add_column("레벨", style="green")
    table.add_column("설명", style="white")

    for name, data in plugins.items():
        version = data.get('version', 'N/A')
        level = data.get('level', 'N/A')
        description = data.get('description', '')
        table.add_row(name, version, level, description)

    console.print(table)

def run_plugin(plugins, plugin_name):
    """특정 플러그인을 실행합니다."""
    plugin = plugins.get(plugin_name)
    if not plugin:
        console.print(f"[red]에러: '{plugin_name}' 플러그인을 찾을 수 없습니다.[/red]")
        console.print("[yellow]사용 가능한 플러그인:[/yellow]")
        list_plugins(plugins)
        return

    console.print(Panel(f"🚀 플러그인 실행: [bold cyan]{plugin_name}[/bold cyan]", style="green"))

    plugin_path = plugin.get("path")
    scripts = plugin.get("scripts", {})
    
    # 1. 의존성 설치 (install 스크립트)
    install_script = scripts.get("install")
    if install_script:
        console.print(f"[yellow]📦 설치 스크립트 실행: '{install_script}'...[/yellow]")
        try:
            # shell=True를 사용하여 복잡한 명령어(예: pip install -r ...) 처리
            subprocess.run(install_script, cwd=plugin_path, check=True, shell=True)
            console.print("[green]✅ 설치 스크립트가 성공적으로 완료되었습니다.[/green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ 설치 스크립트 실행 중 오류 발생: {e}[/red]")
            return
        except FileNotFoundError:
            console.print(f"[red]❌ 에러: 명령어를 찾을 수 없습니다. '{install_script.split()[0]}' 명령어가 PATH에 있는지 확인해주세요.[/red]")
            return

    # 2. 플러그인 실행 (start 스크립트)
    start_script = scripts.get("start")
    if not start_script:
        console.print("[red]❌ 에러: 'plugin.json'에 'start' 스크립트가 정의되지 않았습니다.[/red]")
        return
        
    console.print(f"[cyan]▶️  시작 스크립트 실행: '{start_script}'...[/cyan]")
    try:
        subprocess.run(start_script, cwd=plugin_path, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ 시작 스크립트 실행 중 오류 발생: {e}[/red]")
    except FileNotFoundError:
        console.print(f"[red]❌ 에러: 명령어를 찾을 수 없습니다. '{start_script.split()[0]}' 명령어가 PATH에 있는지 확인해주세요.[/red]")
        return
    
    console.print(Panel(f"⏹️  플러그인 종료: [bold cyan]{plugin_name}[/bold cyan]", style="blue"))


def interactive_mode(plugins):
    """대화형 모드로 플러그인을 선택하고 실행합니다."""
    while True:
        console.clear()
        console.print(Panel("[bold cyan]🚀 PGall 대화형 모드[/bold cyan]", style="green", expand=False))
        console.print()
        
        action = inquirer.select(
            message="원하는 작업을 선택하세요:",
            choices=[
                Choice(value="list", name="📋 플러그인 목록 보기"),
                Choice(value="run", name="▶️  플러그인 실행"),
                Choice(value="exit", name="🚪 종료"),
            ],
            default="list",
        ).execute()
        
        console.print()  # 빈 줄 추가
        
        if action == "list":
            list_plugins(plugins)
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
            
        elif action == "run":
            if not plugins:
                console.print("[red]❌ 사용 가능한 플러그인이 없습니다.[/red]")
                console.print("\n[dim]Press Enter to continue...[/dim]")
                input()
                continue
            
            plugin_choices = [
                Choice(value=name, name=f"{name} [dim]- {data.get('description', 'N/A')}[/dim]")
                for name, data in plugins.items()
            ]
            
            selected_plugin = inquirer.select(
                message="실행할 플러그인을 선택하세요:",
                choices=plugin_choices,
            ).execute()
            
            console.print()  # 빈 줄 추가
            run_plugin(plugins, selected_plugin)
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
            
        elif action == "exit":
            console.clear()
            console.print("[green]👋 PGall을 종료합니다. 감사합니다![/green]")
            break


def main():
    """CLI 애플리케이션의 메인 로직입니다."""
    parser = argparse.ArgumentParser(
        description="PGall - 플러그인 갤러리 런처",
        epilog="옵션 없이 실행하면 대화형 모드로 진입합니다."
    )
    
    parser.add_argument("-l", "--list", action="store_true", help="사용 가능한 모든 플러그인 목록을 보여줍니다")
    parser.add_argument("-r", "--run", metavar="PLUGIN_NAME", help="특정 플러그인을 실행합니다")
    parser.add_argument("-i", "--interactive", action="store_true", help="대화형 모드로 실행합니다")

    args = parser.parse_args()
    
    plugins = scan_plugins()

    # 옵션이 하나도 없으면 대화형 모드로 실행
    if not (args.list or args.run or args.interactive):
        interactive_mode(plugins)
    elif args.list:
        list_plugins(plugins)
    elif args.run:
        run_plugin(plugins, args.run)
    elif args.interactive:
        interactive_mode(plugins)

if __name__ == "__main__":
    main()
