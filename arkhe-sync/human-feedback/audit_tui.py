import asyncio
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

async def run_audit():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1)
    )
    layout["header"].update(Panel("🜏 Arkhe-Sync Audit TUI", style="cyan"))

    with Live(layout, refresh_per_second=4):
        while True:
            layout["body"].update(Panel("Observing human feedback and coherence scores..."))
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_audit())
