from ui.cli import show_header, console
from utils.memory import Memory
from models.openrouter import OpenRouterClient
from config import SYSTEM_PROMPT, DEFAULT_MODEL

def build_messages(system_prompt, history, prefs, user_input, mem):
    summary = mem.summarize_long_term()
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "system", "content": f"Conversation summary: {summary}"})

    if prefs.get("tone"):
        messages.append({"role": "system", "content": f"User prefers {prefs['tone']} tone."})

    if prefs.get("name"):
        messages.append({"role": "system", "content": f"User’s name is {prefs['name']}."})

    messages.extend(history[-5:])  # keep last 5 messages
    messages.append({"role": "user", "content": user_input})
    return messages

def run_cli(voice_mode=False):
    show_header()
    mem = Memory()
    prefs = mem.load_prefs()
    history = mem.load_history()

    client = OpenRouterClient()

    console.print("[bold cyan]Hello Artchen! Type something to chat.[/bold cyan]\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break

            # Add user message to memory
            mem.add_message("user", user_input)

            # Build messages for API
            messages = build_messages(SYSTEM_PROMPT, history, prefs, user_input, mem)

            # Get AI response
            response = client.chat(messages, DEFAULT_MODEL)

            if response:
                console.print(f"[green]Artia:[/green] {response}")
                mem.add_message("assistant", response)
            else:
                console.print("[red]Error: No response from API[/red]")

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Exiting...[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    run_cli(voice_mode=False)
