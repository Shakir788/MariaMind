from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from utils.voice import listen_from_mic, speak

console = Console()

BANNER = """
   █████╗ ██████╗ ████████╗██╗███╗   ███╗      █████╗ ██╗
  ██╔══██╗██╔══██╗╚══██╔══╝██║████╗ ████║     ██╔══██╗██║
  ███████║██████╔╝   ██║   ██║██╔████╔██║     ███████║██║
  ██╔══██║██╔═══╝    ██║   ██║██║╚██╔╝██║     ██╔══██║██║
  ██║  ██║██║        ██║   ██║██║ ╚═╝ ██║     ██║  ██║██║
  ╚═╝  ╚═╝╚═╝        ╚═╝   ╚═╝╚═╝     ╚═╝     ╚═╝  ╚═╝╚═╝
"""

HELP = (
    "Type your message and press Enter.\n"
    "[voice] start/stop voice mode | [prefs] set name or tone | [quit] exit\n"
)

def show_header():
    console.print(Panel.fit(BANNER, title="Artia AI", subtitle="Your friendly AI friend"))
    console.print(HELP)

def cli_loop(ai_client, memory, voice_mode=False):
    """
    Command-line loop for interacting with Artia AI
    """
    show_header()
    console.print("Hello Artchen! Type something to chat.\n")

    while True:
        try:
            if voice_mode:
                console.print("[cyan]🎤 Voice mode active... speak now[/cyan]")
                user_input = listen_from_mic() or ""
            else:
                user_input = Prompt.ask("You")

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit"]:
                console.print("[red]Goodbye![/red]")
                break

            if user_input.lower() == "voice":
                voice_mode = not voice_mode
                console.print(f"Voice mode: {'ON' if voice_mode else 'OFF'}")
                continue

            if user_input.lower() == "prefs":
                console.print("[yellow]Preferences update coming soon...[/yellow]")
                continue

            # AI response
            response = ai_client.chat(user_input, memory)
            console.print(f"[bold green]Artia:[/bold green] {response}")

            if voice_mode:
                speak(response)

        except KeyboardInterrupt:
            console.print("\n[red]Interrupted by user. Exiting...[/red]")
            break
