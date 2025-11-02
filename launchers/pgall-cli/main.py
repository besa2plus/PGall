import argparse
import json
import os
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.prompts.list import ListPrompt

# --- Custom Prompt for Hotkeys ---
class MenuPrompt(ListPrompt):
    """'l', 'r', 'q'와 같은 핫키를 지원하는 커스텀 리스트 프롬프트입니다."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_kb("l")(self.handle_hotkey("list"))
        self.register_kb("r")(self.handle_hotkey("run"))
        self.register_kb("q")(self.handle_hotkey("exit"))

    def handle_hotkey(self, action: str):
        def _(event) -> None:
            """핫키가 눌렸을 때 프롬프트를 즉시 종료하고 지정된 값을 반환합니다."""
            self.status["answered"] = True
            event.app.exit(result=action)
        return _

# 프로젝트의 루트 디렉토리를 찾습니다. (launchers/pgall-cli/main.py 기준)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = PROJECT_ROOT / "plugins"

# Rich Console 초기화
console = Console()

def scan_plugins():
    """`plugins` 디렉토리를 스캔하여 유효한 플러그인 목록을 반환합니다."""
    plugins = {}
    if not PLUGINS_DIR.exists():
        console.print(f"[red]에러: 플러그인 디렉토리를 '{PLUGINS_DIR}'에서 찾을 수 없습니다.[/red]")
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
                            console.print(f"[yellow]경고: '{manifest_path}'의 플러그인 명세에 'name' 속성이 없습니다.[/yellow]")
                except json.JSONDecodeError:
                    console.print(f"[yellow]경고: '{manifest_path}'를 파싱할 수 없습니다. 유효하지 않은 JSON입니다.[/yellow]")
                except Exception as e:
                    console.print(f"[yellow]경고: '{manifest_path}'를 읽는 중 예상치 못한 오류가 발생했습니다: {e}[/yellow]")
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
    table.add_column("언어", style="yellow")
    table.add_column("지원 OS", style="blue", justify="center")
    table.add_column("설명", style="white")

    for name, data in plugins.items():
        version = data.get('version', 'N/A')
        level = data.get('level', 'N/A')
        language = data.get('language', 'N/A')
        description = data.get('description', '')

        # OS 지원 정보 표시
        platforms = data.get('platforms', {})
        win = "✅" if platforms.get('windows') == 'supported' else '❌'
        mac = "✅" if platforms.get('macos') == 'supported' else '❌'
        linux = "✅" if platforms.get('linux') == 'supported' else '❌'
        os_support = f"W:{win} M:{mac} L:{linux}"
        
        table.add_row(name, version, level, language, os_support, description)

    console.print(table)

def get_script_path(plugin_path: str, script_name: str) -> str:
    """OS에 맞는 스크립트 경로를 반환 (e.g., install.sh or install.bat)"""
    base_path = Path(plugin_path)
    if os.name == 'nt':
        bat_script = base_path / f"{script_name}.bat"
        if bat_script.exists():
            return str(bat_script)
    
    sh_script = base_path / f"{script_name}.sh"
    return str(sh_script) if sh_script.exists() else None


def run_plugin(plugins, plugin_name):
    """표준 스크립트 규약(install.sh/run.sh)에 따라 플러그인을 실행합니다."""
    plugin = plugins.get(plugin_name)
    if not plugin:
        console.print(f"[red]에러: '{plugin_name}' 플러그인을 찾을 수 없습니다.[/red]")
        return

    plugin_path = plugin.get("path")

    # OS 호환성 체크
    platforms = plugin.get('platforms', {})
    current_os = platform.system().lower()
    
    supported = False
    if 'windows' in current_os and platforms.get('windows') == 'supported':
        supported = True
    elif 'darwin' in current_os and platforms.get('macos') == 'supported':
        supported = True
    elif 'linux' in current_os and platforms.get('linux') == 'supported':
        supported = True

    if not supported:
        win = "✅" if platforms.get('windows') == 'supported' else '❌'
        mac = "✅" if platforms.get('macos') == 'supported' else '❌'
        linux = "✅" if platforms.get('linux') == 'supported' else '❌'

        console.print(f"[yellow]⚠️  경고: 이 플러그인은 현재 OS({platform.system()})를 공식적으로 지원하지 않을 수 있습니다.[/yellow]")
        console.print(f"   지원 OS -> Windows: {win}, macOS: {mac}, Linux: {linux}")
        
        if not inquirer.confirm(message="계속 진행하시겠습니까?", default=False).execute():
            console.print("[red]실행이 취소되었습니다.[/red]")
            return
    
    console.print(Panel(f"🚀 플러그인 실행: [bold cyan]{plugin_name}[/bold cyan]", style="green"))

    # 1. 의존성 설치 (install.sh 또는 install.bat)
    install_script = get_script_path(plugin_path, "install")
    if install_script:
        console.print(f"[yellow]📦 의존성 설치 스크립트 실행: {os.path.basename(install_script)}...[/yellow]")
        try:
            subprocess.run([install_script], cwd=plugin_path, check=True, shell=True)
            console.print("[green]✅ 의존성 설치 완료[/green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ 의존성 설치 실패: {e}[/red]")
            return
    
    # 2. 플러그인 실행 (run.sh 또는 run.bat)
    run_script = get_script_path(plugin_path, "run")
    if not run_script:
        console.print(f"[red]❌ 에러: 실행 가능한 스크립트('run.sh' 또는 'run.bat')를 찾을 수 없습니다.[/red]")
        return

    console.print(f"[cyan]▶️  플러그인 실행: {os.path.basename(run_script)}...[/cyan]")
    try:
        subprocess.run([run_script], cwd=plugin_path, check=True, shell=True)
        console.print(Panel(f"⏹️  플러그인 종료: [bold cyan]{plugin_name}[/bold cyan]", style="blue"))
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ 플러그인 실행 실패: {e}[/red]")
    except KeyboardInterrupt:
        console.print(f"[yellow]⏹️  사용자에 의해 플러그인 실행이 중단되었습니다.[/yellow]")

def interactive_mode(plugins):
    """대화형 모드로 플러그인을 선택하고 실행합니다."""
    while True:
        console.clear()
        console.print(Panel("[bold cyan]🚀 PGall 대화형 모드[/bold cyan]", style="green", expand=False))
        console.print()
        
        console.print("[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
        console.print("[dim]⌨️  핫키: [cyan]L[/cyan]ist | [cyan]R[/cyan]un | [cyan]Q[/cyan]uit | [cyan]Enter[/cyan]로 선택 | [cyan]ESC, ←, Backspace[/cyan]로 뒤로가기[/dim]")
        console.print("[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")
        
        choices = [
            Choice(value="list", name="[L] 플러그인 목록 보기"),
            Choice(value="run", name="[R] 플러그인 실행"),
            Choice(value="exit", name="[Q] 종료"),
        ]
        
        action = MenuPrompt(
            message="원하는 작업을 선택하세요:",
            choices=choices,
            default="list",
            mandatory=False,
            keybindings={"skip": [{"key": "escape"}, {"key": "backspace"}]},
        ).execute()

        if not action: # ESC/Backspace 등을 눌러서 아무것도 선택하지 않았을 때
            continue

        if action == "list":
            list_plugins(plugins)
            console.input("\n[dim]Press Enter to continue...[/dim]")
            
        elif action == "run":
            if not plugins:
                console.print("[red]❌ 사용 가능한 플러그인이 없습니다.[/red]")
                console.input("\n[dim]Press Enter to continue...[/dim]")
                continue
            
            plugin_choices = [
                Choice(value=name, name=f"{name} - {data.get('description', 'N/A')}")
                for name, data in plugins.items()
            ]
            plugin_choices.append(Choice(value="back", name="← 뒤로가기"))

            selected_plugin = inquirer.select(
                message="실행할 플러그인을 선택하세요:",
                choices=plugin_choices,
                keybindings={"skip": [{"key": "escape"}, {"key": "left"}, {"key": "backspace"}]},
                mandatory=False
            ).execute()

            if selected_plugin and selected_plugin != "back":
                run_plugin(plugins, selected_plugin)
                console.input("\n[dim]Press Enter to continue...[/dim]")
            
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

    args = parser.parse_args()
    
    plugins = scan_plugins()

    if args.list:
        list_plugins(plugins)
    elif args.run:
        run_plugin(plugins, args.run)
    else:
        interactive_mode(plugins)

if __name__ == "__main__":
    main()
