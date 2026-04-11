import math
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

console = Console()

def run_monitor():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )

    epoch = 0
    with Live(layout, refresh_per_second=2, screen=True):
        while True:
            rem_factor = 1.0 + 0.05 * math.sin(epoch * 5 / 5400.0 * 2 * math.pi)
            epsilon = 0.95 * rem_factor

            header = Panel(Text("Arkhe-Sync v1.4.1-fast | Evolution & Hypergraph Monitor", style="bold cyan"))
            body = Panel(f"🜏 Global Coherence: 0.9997\n\nActive Wormholes: 14/14\nMean ε: {epsilon:.4f}\nREM Cycle Phase: {rem_factor:.2f}\nSkills Distilled: 4", title="Hypergraph Status")
            footer = Panel(f"Epoch: {epoch} | Nostr Peers: 3 | Consensus: OK", style="dim")

            layout["header"].update(header)
            layout["body"].update(body)
            layout["footer"].update(footer)

            epoch += 1
            time.sleep(0.5)

if __name__ == "__main__":
    run_monitor()
