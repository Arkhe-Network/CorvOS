import json
import matplotlib.pyplot as plt

def analyze_epoch(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    cycles = data['cycles']
    rewards = [c['reward'] for c in cycles]
    coherence = [c['coherence'] for c in cycles]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(rewards)
    plt.title('Rewards per Cycle')

    plt.subplot(1, 2, 2)
    plt.plot(coherence)
    plt.title('Coherence per Cycle')

    plt.tight_layout()
    plt.savefig('epoch_1442_analysis.png')
    print("Analysis complete: epoch_1442_analysis.png generated.")

if __name__ == "__main__":
    # analyze_epoch('report_1442.json')
    pass
