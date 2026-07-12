import numpy as np
import matplotlib.pyplot as plt

# Simulate displacement (mm) from 0 to 1.0
displacement = np.linspace(0, 1.0, 500)

# Solenoid force curve (JF-0530B typical profile)
# Force increases as the plunger reaches the end of its stroke
solenoid_force = 10 + 20 * (displacement)**1.5

# Paper resistance (Non-linear deformation model for 140 GSM Braille paper)
paper_resistance = np.zeros_like(displacement)
for i, d in enumerate(displacement):
    if d < 0.2:
        # Elastic region
        paper_resistance[i] = 40 * d
    elif d < 0.65:
        # Plastic deformation region (Yielding)
        paper_resistance[i] = 8 + 5 * (d - 0.2)
    else:
        # Strain hardening / Tearing region
        paper_resistance[i] = 10.25 + 100 * (d - 0.65)

# Create the plot
plt.figure(figsize=(9, 5))
plt.plot(displacement, solenoid_force, label='Solenoid Output Force (JF-0530B)', color='#1f77b4', linewidth=2.5)
plt.plot(displacement, paper_resistance, label='140 GSM Paper Resistance', color='#d62728', linestyle='--', linewidth=2.5)

# Highlight regions
plt.axvspan(0, 0.2, color='#2ca02c', alpha=0.15, label='Elastic Region (No permanent dot)')
plt.axvspan(0.2, 0.65, color='#ff7f0e', alpha=0.15, label='Plastic Region (Optimal Embossing)')
plt.axvspan(0.65, 1.0, color='#d62728', alpha=0.15, label='Tear Zone (Paper structural failure)')

# Mark ISO 17049 Target height
plt.axvline(x=0.5, color='black', linestyle=':', linewidth=2, label='ISO 17049 Target Height (0.5mm)')

# Annotations
plt.plot(0.5, 9.5, 'ko') # Point on paper resistance curve
plt.annotate('Target Embossing\nForce (~9.5 N)', xy=(0.5, 9.5), xytext=(0.55, 4),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

# Formatting
plt.title('BrailleSCARA End-Effector: Solenoid Force vs. Paper Deformation', fontsize=14, pad=15)
plt.xlabel('Embossing Pin Displacement (mm)', fontsize=12)
plt.ylabel('Force (Newtons)', fontsize=12)
plt.xlim(0, 0.9)
plt.ylim(0, 35)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.7)

plt.tight_layout()
plt.savefig('force_graph.png', dpi=300)
print("Graph generated successfully as force_graph.png")
