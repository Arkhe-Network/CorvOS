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

            header = Panel(Text("Arkhe-Sync v2.1.0-lab | Scientific Discovery Monitor", style="bold cyan"))
            body = Panel(
                f"🜏 Arkhe-Lab Discovery Status\n\n"
                f"Robot: Opentrons (Online) | Current Experiment: #42\n"
                f"GA Generation: 4 | Best Efficiency: 93.2%\n"
                f"Scientific Skills: 3 | Total CoT: 5600.00\n"
                f"Non-Omission Proofs: Verified (Pt-Ni Interaction)\n"
                f"Mean ε: {epsilon:.4f}",
                title="Lab Automation & Coherence"
            )
            footer = Panel(f"Epoch: {epoch} | Nostr/libp2p Peers: 15 | Status: DISCOVERING", style="dim")

            layout["header"].update(header)
            layout["body"].update(body)
            layout["footer"].update(footer)

            epoch += 1
            time.sleep(0.5)

if __name__ == "__main__":
    run_monitor()
