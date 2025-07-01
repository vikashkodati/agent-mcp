import asyncio
import os
import sys
try:
    import termios
    import tty
    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False
from dotenv import load_dotenv
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from agents import set_tracing_disabled
from agents.exceptions import OutputGuardrailTripwireTriggered
from nasa_agent import NASAAgent
from stac_agent import STACAgent
from orbital_agent import OrbitalAgent
from mcp_config import MCPConfig
from logging_utils import LoggingUtils

load_dotenv()
set_tracing_disabled(True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

VERBOSE = os.getenv("VERBOSE", "false").lower() in ["true", "1", "yes"]


def getch():
    """Get a single character from stdin."""
    if not HAS_TERMIOS or not sys.stdin.isatty():
        # Fallback to regular input for non-interactive or unsupported terminals
        return input()
    
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except (OSError, AttributeError):
        # Fallback if termios operations fail
        return input()


def display_agent_menu(console: Console):
    agents = [
        ("NASA Space Data Agent", "Explore NASA's vast space and astronomy data"),
        ("STAC Earth Observation Agent", "Analyze satellite imagery and Earth observation data"),
        ("Orbital Mechanics Agent", "Track satellites and perform orbital calculations"),
        ("Quit", "Exit the application")
    ]

    selected = 0
    interactive_mode = HAS_TERMIOS and sys.stdin.isatty()

    while True:
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]🚀 Space Domain Agent Platform[/bold cyan]",
            border_style="cyan"
        ))

        if interactive_mode:
            console.print(
                "\n[bold]Choose a space domain agent (use ↑↓ arrows, Enter to select):[/bold]")

            for i, (name, description) in enumerate(agents):
                if i == selected:
                    console.print(
                        f"[bold green]→ {name}[/bold green] - [dim]{description}[/dim]")
                else:
                    console.print(
                        f"  [white]{name}[/white] - [dim]{description}[/dim]")

            console.print(
                "\n[dim]Use ↑/↓ arrows to navigate, Enter to select, 'q' to quit[/dim]")
        else:
            console.print("\n[bold]Choose a space domain agent:[/bold]")
            for i, (name, description) in enumerate(agents):
                console.print(f"[yellow]{i+1}[/yellow]. {name} - [dim]{description}[/dim]")
            console.print("[yellow]q[/yellow]. Quit")
            console.print("\n[dim]Enter your choice (1, 2, 3, or q):[/dim]")

        key = getch()

        if interactive_mode:
            if key == '\x1b':  # ESC sequence for arrow keys
                try:
                    key2 = getch()
                    if key2 == '[':
                        key3 = getch()
                        if key3 == 'A':  # Up arrow
                            selected = (selected - 1) % len(agents)
                        elif key3 == 'B':  # Down arrow
                            selected = (selected + 1) % len(agents)
                except:
                    pass
            elif key == '\r' or key == '\n':  # Enter
                if selected == 0:
                    return "1"
                elif selected == 1:
                    return "2"
                elif selected == 2:
                    return "3"
                else:
                    return "q"
            elif key.lower() == 'q':
                return "q"
        else:
            # Non-interactive mode - handle text input
            if key.strip() == '1':
                return "1"
            elif key.strip() == '2':
                return "2"
            elif key.strip() == '3':
                return "3"
            elif key.strip().lower() == 'q':
                return "q"


async def main():
    logger = LoggingUtils(verbose=VERBOSE)
    console = logger.console

    try:
        choice = display_agent_menu(console)

        if choice == "q":
            console.print(
                "\n[bold yellow]Thanks for using Space Domain Agent Platform! 🚀 Goodbye! 👋[/bold yellow]")
            return

        if choice == "1":
            agent_name = "NASA Space Data Agent"
            server_key = "nasa"
        elif choice == "2":
            agent_name = "STAC Earth Observation Agent"
            server_key = "stac"
        else:
            agent_name = "Orbital Mechanics Agent"
            server_key = "orbital"
            
        logger.print_welcome(agent_name)

        mcp_config = MCPConfig()
        logger.print_connecting()

        servers = await mcp_config.create_servers()
        
        async with servers[server_key] as active_server:
            logger.print_connected()
            
            # Create the appropriate agent based on user choice
            if choice == "1":
                selected_agent = NASAAgent(
                    mcp_servers=[active_server], verbose=VERBOSE)
            elif choice == "2":
                selected_agent = STACAgent(
                    mcp_servers=[active_server], verbose=VERBOSE)
            else:
                selected_agent = OrbitalAgent(
                    mcp_servers=[active_server], verbose=VERBOSE)
            
            while True:
                user_input = Prompt.ask(
                    f"\n[bold green]What can I help you explore today? (type 'quit' to exit)[/bold green]")

                if user_input.lower().strip() in ['quit', 'exit', 'q']:
                    logger.console.print(
                        "\n[bold yellow]Thanks for using Space Domain Agent Platform! 🚀 Goodbye! 👋[/bold yellow]")
                    break

                try:
                    await selected_agent.find_answer(user_input)
                except OutputGuardrailTripwireTriggered as e:
                    logger.console.print("\n" + "━" * 60)
                    logger.console.print(
                        "⚠️  [bold red]GUARDRAIL ACTIVATED[/bold red] ⚠️", justify="center")
                    logger.console.print("━" * 60)
                    logger.console.print(
                        "\n[bold red]❌ This response is not related to space domain topics.[/bold red]")
                    logger.console.print("\n" + "━" * 60)
                    if VERBOSE:
                        logger.console.print(f"[dim]Debug info: {e}[/dim]")

    except ValueError as e:
        console.print(f"\n[bold red]Configuration Error:[/bold red] {e}")
        console.print("\n[yellow]Please check your environment variables and try again.[/yellow]")
        console.print("\n[dim]Required environment variables:[/dim]")
        console.print("[dim]- OPENAI_API_KEY (from platform.openai.com)[/dim]")
        console.print("[dim]- NASA_API_KEY (from api.nasa.gov)[/dim]")
        console.print("[dim]- STAC_API_KEY (optional, for some STAC services)[/dim]")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        if VERBOSE:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")


if __name__ == "__main__":
    asyncio.run(main())
