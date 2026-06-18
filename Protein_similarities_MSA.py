import subprocess
from Bio import AlignIO
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# ==== 1. Run Clustal Omega for MSA ====
input_file = "PBP_all.fasta"
aligned_file = "PBP_all_aligned.fasta"

cmd = [
    "clustalo",  # or full path, e.g., "/home/helmi/clustal-omega/clustalo"
    "-i", input_file,
    "-o", aligned_file,
    "--force",
    "--auto",
    "--verbose"
]

subprocess.run(cmd, check=True)

# ==== 2. Read the MSA ====
alignment = AlignIO.read(aligned_file, "fasta")
ids = [record.id for record in alignment]
n = len(alignment)

# ==== 3. Compute Pairwise Percent Identity Matrix ====
matrix = []
for i in range(n):
    row = []
    for j in range(n):
        if i == j:
            identity = 100.0
        else:
            matches = sum(
                (a == b and a != '-' and b != '-')
                for a, b in zip(alignment[i].seq, alignment[j].seq)
            )
            total = sum(
                (a != '-' and b != '-')
                for a, b in zip(alignment[i].seq, alignment[j].seq)
            )
            identity = (matches / total * 100) if total else 0.0
        row.append(round(identity, 2))
    matrix.append(row)

# ==== 4. Save Identity Matrix to CSV ====
csv_file = "percent_identity_matrix.csv"
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([""] + ids)
    for i, row in enumerate(matrix):
        writer.writerow([ids[i]] + row)

print(f"✅ Percent identity matrix saved to: {csv_file}")

# ==== 5. Plot Heatmap ====
df = pd.DataFrame(matrix, index=ids, columns=ids)
plt.figure(figsize=(10, 8))

sns.heatmap(
    df,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu",
    vmin=0,
    vmax=100,
    cbar_kws={
        'label': 'Percent Identity (%)',
        'ticks': [0, 20, 40, 60, 80, 100]
    },
    annot_kws={
        "size": 14,
        "weight": "medium",
        "color": "#333333",
        "family": "sans-serif"
    },
    square=True
)

plt.title(
    "Pairwise Percent Identity Heatmap",
    fontsize=18,
    fontweight='bold',
    fontfamily='sans-serif',
    color='black'
)

plt.xticks(
    rotation=45,
    ha='right',
    fontsize=12,
    fontweight='bold',
    fontfamily='monospace',
    color='black'
)

plt.yticks(
    rotation=0,
    fontsize=12,
    fontweight='bold',
    fontfamily='monospace',
    color='black'
)

plt.tight_layout()
plt.savefig("percent_identity_heatmap.png", dpi=500)
plt.show()
