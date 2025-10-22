from time import sleep
from rich.console import Console, Group
from rich.live import Live
from rich.text import Text

def main():
    console = Console()

    # Define initial lines
    lines = [
        Text("Task A: pending", style="yellow"),
        Text("Task B: pending", style="yellow"),
        Text("Task C: pending", style="yellow"),
    ]

    # Group allows multiple renderables (like multiple lines)
    render_group = Group(*lines)

    # Create a Live display
    with Live(render_group, console=console, refresh_per_second=5) as live:
        # Simulate tasks updating over time
        for step in range(1, 4):
            sleep(1)
            # Update a specific line
            lines[step - 1] = Text(f"Task {chr(64 + step)}: done ✅", style="green")
            # Update the live display (Group auto-reflects changes)
            live.update(Group(*lines))

        # simulate a summary update
        sleep(1)
        lines.append(Text("All tasks complete!", style="bold blue"))
        live.update(Group(*lines))

    console.print("Finished!", style="bold green")


if __name__ == "__main__":
    main()
