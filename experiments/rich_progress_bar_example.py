from time import sleep
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn

def main():
    # Create a Progress instance with some custom columns
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        TimeRemainingColumn()
    )

    # Use as a context manager (automatically starts & stops)
    with progress:
        task = progress.add_task("Working...", total=100)
        # simulate work in steps
        for i in range(100):
            sleep(0.1)
            progress.update(task, advance=1)

    print("All done!")

if __name__ == "__main__":
    main()
