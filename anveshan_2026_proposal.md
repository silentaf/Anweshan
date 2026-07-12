# Anveshan 2026 — Project Proposal

## BrailleSCARA: A Precision SCARA Robot for Automated Braille & Tactile Graphics Production Using ADI Motor Control and Edge AI Vision

---

## 1. What Are We Building?

BrailleSCARA is a 4-DOF SCARA robot that converts printed text into Braille documents and draws tactile diagrams — enabling blind students to read textbooks and touch STEM illustrations for the first time, at a system cost under ₹1 Lakh.

**How it works — plain and simple:**

1. A camera reads the printed page. ADI's MAX78000 (hardware CNN accelerator) runs OCR on-chip — no laptop needed.
2. Software converts the recognized text to Bharati Braille encoding and generates dot coordinates following ISO 17049 spacing standards.
3. The SCARA arm picks a blank Braille paper sheet from a tray and places it on the embossing bed.
4. The arm moves to each dot position with ±0.05 mm accuracy using ADI's ADSP-CM419 + TMC4671 closed-loop FOC drive. A solenoid fires for 50 ms, pushing a 2 mm steel pin through the paper into an anvil hole, creating a raised dot.
5. After each dot, a force sensor read by ADI's AD7124-8 (24-bit ADC) verifies the dot formed correctly. If the dot is too shallow, the arm re-embosses it immediately.
6. For tactile diagrams (maps, graphs, geometric figures), the arm traces freeform paths with a spring-loaded ball stylus, creating raised lines that blind students can feel with their fingertips.
7. Completed pages are picked and sorted into output trays by page number.

**This workflow demonstrates all four competition capabilities:**

| Competition Task | How BrailleSCARA Does It |
|---|---|
| Pick and Place | Picks paper from feeder → places on embossing bed |
| Precision Insertion | Embosses each Braille dot at exact XY with controlled Z force |
| Sorting | Sorts completed pages into numbered output trays |
| Drawing Shapes/Figures | Draws tactile maps, math graphs, geometric constructions |

**Every capability serves a real purpose. Nothing is a demo for demo's sake.**

| Specification | Value |
|---|---|
| Arm reach | 400 mm |
| Repeatability | ±0.05 mm |
| Braille dot spacing | 2.5 mm (ISO 17049) |
| Dot height | 0.5 ± 0.1 mm (ISO 17049) |
| Embossing speed | >30 characters/min |
| Tactile line width | ~0.3 mm |
| System cost (excl. ADI boards) | <₹1 Lakh |

---

## 2. The Problem: Why This Matters

India has **15 million blind people** — more than any country on Earth. Only **1% can read Braille.** Not because they can't learn. Because the materials don't exist.

There are **25 Braille presses** for 1.4 billion people. A single Braille textbook costs 10–50× its printed version. The government's RPwD Act 2016 mandates accessible education materials, but the infrastructure to produce them simply isn't there.

But the harder, completely unsolved problem is **tactile graphics.**

Education is not just text — it is diagrams. The human heart. India's map. A parabola. A circuit schematic. A triangle construction. Sighted students see these on every page. **Blind students get nothing.**

Existing Braille machines (BrailleRAP, Index Braille) produce text only — rows of dots. They cannot draw freeform diagrams. The machines that CAN draw tactile graphics (ViewPlus Tiger, PIAF) cost **₹3–25 Lakh** and are found only in a handful of elite institutions.

**There is no device under ₹10 Lakh in India that can produce a touchable version of a science textbook diagram.**

A SCARA robot can solve this because it has the two things this problem needs: **precise XY positioning** (to place dots and trace paths) and **controlled Z-axis force** (to emboss paper without tearing it). ADI's motor control technology provides the sub-0.1 mm precision that ISO-compliant Braille requires.

---

## 3. Existing Solutions and How We're Different

### Literature Survey

| Solution | What It Does | Tactile Graphics? | Quality Check? | Edge AI? | Cost |
|---|---|---|---|---|---|
| **BrailleRAP** (open-source) | CNC-type Braille embosser using 3D printer frame + solenoid | ❌ Text only — fixed row embossing | ❌ None | ❌ None | ~₹30K |
| **Index Everest-D** (commercial) | Production Braille printer for institutions | ❌ Text only | ❌ None | ❌ None | ₹4.5–8L |
| **ViewPlus Tiger** (commercial) | Embosses text AND graphics using multi-pin head | ✅ Yes (matrix-based) | ❌ None | ❌ None | ₹10–25L |
| **PIAF** (commercial) | Heats special microcapsule paper to create raised images | ✅ Yes (heat-based) | ❌ None | ❌ None | ₹3–5L* |
| **Student SCARA projects** (general) | Pick-and-place colored blocks, draw logos | ❌ Not applied to Braille | ❌ Open-loop | ❌ Laptop-based | ₹40–80K |
| **BrailleSCARA (this project)** | **SCARA-based Braille + freeform tactile graphics** | **✅ Freeform paths** | **✅ Force-verified** | **✅ MAX78000** | **<₹1L** |

*PIAF requires special swell paper at ~₹50/sheet, making volume production impractical.

### What's Actually Novel (No Exaggeration)

**Novel Contribution 1: Affordable tactile graphics (<₹1 Lakh)**
This is the primary innovation. BrailleRAP and Index Braille cannot draw diagrams. ViewPlus Tiger can, but costs ₹10L+. Our SCARA traces arbitrary paths with a stylus, creating raised-line tactile diagrams on standard Braille paper. This capability does not exist at this price point. That's a fact, not a claim.

**Novel Contribution 2: Per-dot force verification**
Every Braille machine in existence — commercial and open-source — embosses dots blindly. Ours measures the force-displacement of every single dot using ADI's AD7124-8 (24-bit ADC) and a load cell. If a dot is too shallow, it re-embosses immediately. No existing Braille machine does this.

**Novel Contribution 3: On-chip OCR using MAX78000 hardware CNN**
Most student SCARA projects process vision on a laptop. Our system runs OCR and dot quality classification directly on ADI's MAX78000 hardware CNN accelerator — inference in <100 µs at <1 mW power. The robot reads a printed page without any external computer. This showcases ADI's edge AI silicon in a practical application.

**That's three genuine innovations. We won't pretend there are ten.**

---

## 4. Technology and Methodology

### Motor Control Architecture

The core of BrailleSCARA is ADI's precision motor control stack:

```
Position Command (from trajectory planner)
    ↓
ADSP-CM419 (outer loop @ 10 kHz)
  → Position PID → Velocity PID → Torque reference
    ↓
TMC4671 (inner loop, hardware FOC)
  → Clarke Transform → Park Transform → PI Current Control → SVPWM
    ↓
ADuM4135 (isolated gate drivers) → 3-phase H-bridge → BLDC motor
    ↑
AD8418A (current sense) → AD7380 (16-bit ADC) → current feedback
AS5047P (14-bit encoder) → position feedback
```

Four axes controlled simultaneously: Joint 1 (shoulder), Joint 2 (elbow), Z-axis (prismatic), and wrist rotation. All running closed-loop FOC for smooth, precise, silent operation.

### Braille Encoding Pipeline

```
Printed page → Camera → MAX78000 (hardware CNN: character recognition)
  → Unicode text → liblouis (Bharati Braille Grade 1/2 encoder)
  → 6-dot cell coordinates (ISO 17049: 2.5 mm dot spacing, 6.1 mm cell spacing)
  → Trajectory planner (S-curve velocity profiles to minimize vibration)
  → SCARA executes: move to (X,Y) → fire solenoid (50ms) → verify force → next dot
```

### Embossing Mechanism (Simple, Proven Design)

```
  ┌───────────────────┐
  │ 3D-printed mount  │ ← Bolts to SCARA Z-axis plate
  │  ┌─────────────┐  │
  │  │ 12V Push     │  │ ← JF-0530B solenoid (₹300)
  │  │ Solenoid     │  │
  │  │  ┌────────┐  │  │
  │  │  │ Return │  │  │ ← Spring returns pin after 50ms pulse
  │  │  │ Spring │  │  │
  │  │  │ + Pin  │  │  │ ← 2mm hardened steel pin
  │  └──┼────────┘──┘  │
  └─────┼──────────────┘
        ↓ (strikes paper)
  ┌─────────────────────┐
  │  Braille paper       │ ← 160 GSM standard Braille paper
  ├─────────────────────┤
  │  Anvil plate (steel) │ ← 3mm guide hole beneath paper
  └─────────────────────┘

  Result: Paper deforms into the anvil hole → raised dot on reverse side
  Force required: 2–5 N (well within solenoid capability)
```

This mechanism is identical to what BrailleRAP uses successfully. Nothing experimental.

### Quality Verification

**Force check (every dot):** AD7124-8 reads a force-sensitive resistor on the stylus mount. The expected force-displacement signature for a good dot is known. If measured force is below threshold → dot didn't form properly → re-emboss.

**Vision spot-check (per Braille cell):** After completing a 6-dot cell, MAX78000 camera captures a quick image. A lightweight CNN (3 conv + 2 FC layers, <200K weights, 8-bit quantized) classifies: PASS or FAIL. Logs quality score for the page.

### ADI IoT Telemetry

MAX32690's built-in BLE 5.2 streams motor health data (currents, temperatures from ADT7420, vibration from ADIS16470) to a Grafana dashboard via MQTT. This is useful for monitoring during long embossing runs, not an "innovation" — just good engineering practice.

---

## 5. High-Level Block Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING DASHBOARD                          │
│         Grafana + MQTT (motor health, quality metrics)          │
└───────────────────────────┬─────────────────────────────────────┘
                            │ BLE 5.2
┌───────────────────────────▼─────────────────────────────────────┐
│                     CONTROL & AI LAYER                           │
│                                                                   │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────────────┐  │
│  │  MAX78000     │   │  MAX32690    │   │  ADSP-CM419         │  │
│  │  HW CNN       │   │  Supervisor  │   │  Motor Control DSP  │  │
│  │  • OCR        │   │  • Braille   │   │  • FOC (4-axis)     │  │
│  │  • Dot QC     │   │    encoding  │   │  • Position PID     │  │
│  │  <100µs, <1mW │   │  • BLE comm  │   │  • Trajectory plan  │  │
│  └──────┬────────┘   └──────┬───────┘   └──────────┬──────────┘  │
│         │ SPI               │ SPI/I2C              │ PWM          │
└─────────┼───────────────────┼──────────────────────┼─────────────┘
          │                   │                      │
┌─────────▼───────────────────▼──────────────────────▼─────────────┐
│                    SENSING & DRIVE                                │
│                                                                   │
│  AD7124-8    AD8418A    AD7380    ADIS16470    ADT7420           │
│  (force)     (current)  (ADC)    (IMU)        (temp)            │
│                                                                   │
│  TMC4671 ×4 → ADuM4135 ×4 → H-Bridge ×4 → BLDC Motors ×4      │
│  ADP5054 (power) + ADuM5028 (isolation)                         │
└─────────────────────────────┬────────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                    SCARA ARM + WORKSTATION                        │
│                                                                   │
│  4-DOF Arm (J1, J2, Z, R) → End-Effector:                       │
│    • Solenoid stylus (Braille dots)                              │
│    • Ball stylus (tactile graphics)                              │
│    • Vacuum cup (paper handling)                                 │
│                                                                   │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Paper    │  │ Embossing  │  │ Camera   │  │ Output Trays  │  │
│  │ Feeder   │  │ Bed+Anvil  │  │ Station  │  │ (sorted)      │  │
│  └──────────┘  └────────────┘  └──────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

**ADI Products Used (12 — each genuinely needed):**

| # | Product | Why It's Needed |
|---|---|---|
| 1 | ADSP-CM419 | Motor control DSP — runs position/velocity PID at 10 kHz |
| 2 | TMC4671 ×4 | Hardware FOC — sinusoidal commutation per joint |
| 3 | MAX78000 | Hardware CNN — on-chip OCR and dot quality classification |
| 4 | MAX32690 | BLE 5.2 + task orchestration + Braille encoding |
| 5 | AD7124-8 | 24-bit ADC — force sensor readout for dot verification |
| 6 | AD8418A ×4 | Current sense — FOC phase current feedback |
| 7 | ADuM4135 ×4 | Isolated gate drivers — MOSFET H-bridge driving |
| 8 | AD7380 | 16-bit SAR ADC — high-speed current digitization |
| 9 | ADIS16470 | IMU — vibration monitoring during embossing |
| 10 | ADP5054 | Quad SMPS — multi-rail power for all electronics |
| 11 | ADuM5028 | Isolated DC-DC — gate driver power isolation |
| 12 | ADT7420 | Temperature sensor — motor thermal monitoring |

---

## 6. Plan of Action if Selected as Finalist

| Phase | Period | What We Build | Deliverable |
|---|---|---|---|
| **1: Motor Control** | Aug–Sep 2026 | Single-axis FOC on ADSP-CM419 + TMC4671. Verify closed-loop current and position control. | One motor spinning with tuned FOC |
| **2: Arm Assembly** | Sep–Oct 2026 | Mechanical SCARA arm (SolidWorks → 3D print → assemble). 4-axis coordinated motion. Inverse kinematics. | Arm moving to commanded XY positions |
| **3: Embossing** | Oct–Nov 2026 | Solenoid end-effector. First Braille dots on paper. Force verification via AD7124. MAX78000 CNN training on dot images. | First readable Braille word embossed |
| **4: Tactile Graphics** | Nov 2026 | Continuous path embossing with ball stylus. Bézier curve interpolation. First tactile diagram. | Touchable India map drawn by robot |
| **5: Integration** | Dec 2026 | Full pipeline: OCR → Braille → emboss → verify → sort. IoT dashboard. | End-to-end demo working |
| **6: Testing** | Jan 2027 | ISO 17049 compliance measurement. Speed benchmarking. Demo video. Final report. | Submission-ready package |

**Contingency:** If solenoid embossing has dot consistency issues, we switch to Z-axis force-controlled pressing (spring-loaded stylus, no solenoid). Only the end-effector changes — the arm, motor control, and software remain identical.

---

## 7. Tools, Evaluation Boards, and Platforms Required

### Hardware
| Item | Source |
|---|---|
| ADSP-CM419 EVAL board | ADI (requested) |
| TMC4671-EVAL ×4 | ADI (requested) |
| MAX78000FTHR | ADI (requested) |
| MAX32690 EVAL kit | ADI (requested) |
| AD7124-8 EVAL board | ADI (requested) |
| BLDC motors (42BLS) ×4 | Purchase (~₹8,000) |
| 14-bit magnetic encoders (AS5047P) ×4 | Purchase (~₹4,000) |
| 12V push solenoid (JF-0530B) | Purchase (₹300) |
| Force-sensitive resistor (FSR-402) | Purchase (₹200) |
| 3D printed parts + aluminum extrusion | Fabricate (~₹5,000) |
| Power supply (24V/10A) | Purchase (~₹2,000) |

### Software
| Tool | Purpose |
|---|---|
| C/C++ on FreeRTOS | ADSP-CM419 firmware: FOC, PID, IK, trajectory |
| PyTorch + ADI ai8x-training | Train CNN models for MAX78000 |
| Python + liblouis + Tesseract | Braille encoding pipeline |
| MATLAB/Simulink | Control system simulation and tuning |
| Gazebo + ROS2 | SCARA arm simulation |
| SolidWorks / Fusion 360 | Mechanical CAD |
| KiCad | Carrier board PCB design |
| Grafana + MQTT + InfluxDB | IoT monitoring dashboard |

---

## 8. Future Plans

1. **Open-source the design** — Publish mechanical CAD, firmware, and Braille software on GitHub so any school or NGO can replicate BrailleSCARA.
2. **Pilot in blind schools** — Partner with National Association for the Blind to test in 3–5 schools.
3. **Publish results** — Submit the force-verified embossing and MAX78000 vision pipeline as an IEEE conference paper.
4. **ADI reference design** — Propose BrailleSCARA as an ADI application note showcasing MAX78000 + ADSP-CM419 integration.

---

## 9. Team (SVNIT Surat)

| Role | Member | Department | Responsibility |
|---|---|---|---|
| **Team Lead / AI** | **Aman Gupta** | 3rd Yr Electronics & VLSI | MAX78000 CNN, edge AI vision, system architecture |
| **Firmware** | **Aman Rana** | 3rd Yr Electronics & VLSI | FOC firmware, PID control loops, trajectory planner |
| **Electronics** | **Dhyan Modi** | 3rd Yr Electronics & VLSI | PCB design, ADI board integration, power distribution |
| **Software** | **Anushka Kasle** | 3rd Yr Electronics & VLSI | Braille encoding pipeline, Python OCR, IoT dashboard |
| **Mechanical** | **Tanmay Singh** | 2nd Yr Engineering Physics | SCARA arm CAD, 3D printing, end-effector mechanics |
| **Faculty Mentor** | **Dr. Anand D. Darji** | Professor, Dept. of Electronics Eng. | Project guidance, institutional support, lab access |

---

## 10. References

[1] Analog Devices, "MAX78000 — AI Microcontroller with Hardware CNN Accelerator." analog.com/en/products/max78000.html

[2] Analog Devices, "TMC4671 — Hardware FOC Servo Controller." analog.com/en/products/tmc4671.html

[3] Analog Devices, "ADSP-CM419 Mixed-Signal Control Processor." analog.com/en/products/adsp-cm419.html

[4] ISO 17049:2013, "Accessible design — Application of braille on signage, equipment and appliances."

[5] Dept. of Empowerment of PwD, "Accessible Learning Materials (DALM Project)," Ministry of Social Justice, 2025.

[6] Government of India, "Rights of Persons with Disabilities Act, 2016."

[7] BrailleRAP Open-Source Braille Embosser. braillerap.org

[8] Zhang, Y. et al. (2022). "IK Solution and Trajectory Planning of a SCARA Robot." Machines, 10(8), 648.

---

*Video demonstration will be uploaded separately per submission guidelines.*
