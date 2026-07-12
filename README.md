# BrailleSCARA: Precision Braille & Tactile Graphics Robot

This repository contains the software, AI models, and analysis scripts for **BrailleSCARA**, a 4-DOF precision SCARA robot designed to convert printed text into Braille documents and draw tactile diagrams for the visually impaired.

This project is submitted for the **Anveshan 2026** competition by Team SVNIT Surat.

## Key Features
- **Affordable Tactile Graphics:** Capable of tracing arbitrary paths with a stylus to create raised-line tactile diagrams (maps, graphs) on standard Braille paper.
- **Edge AI OCR & Quality Check:** Utilizes ADI's MAX78000 hardware CNN accelerator for on-chip Optical Character Recognition (OCR) and dot quality classification, eliminating the need for a PC.
- **Force Verification:** Uses ADI's AD7124-8 (24-bit ADC) and a load cell to measure force-displacement of every single dot. Automatically re-embosses shallow dots.
- **Precision Motor Control:** Sub-0.1 mm precision using ADI's ADSP-CM419 DSP and TMC4671 Hardware FOC controllers.

## Repository Contents

### 1. `ai_model/`
Contains the lightweight Convolutional Neural Network (CNN) designed for the MAX78000. 
- Used for visual spot-checking of embossed Braille cells.
- Trained to classify PASS/FAIL for dot formation quality.

### 2. `generate_force_graph.py`
A mathematical simulation script that models the theoretical force applied by a standard push solenoid against the non-linear yield resistance of 140 GSM Braille paper.
- Demonstrates the expected operating window for plastic deformation without tearing the paper.
- Validates the embossing mechanism's feasibility.

## Future Plans

### Technical Roadmap (Phase 2 & 3)
- Integration of the physical ADSP-CM419 + TMC4671 closed-loop FOC drive.
- Translation pipeline utilizing `liblouis` for Bharati Braille conversion.
- Full Gazebo simulation of the pick-and-place and embossing routines.

### Long-Term Impact
- **Open-source the design:** Publish mechanical CAD and firmware on GitHub so NGOs can replicate it.
- **Pilot in blind schools:** Partner with the National Association for the Blind to test in 3-5 schools.
- **Publish results:** Submit the force-verified embossing workflow to an IEEE conference.

## Team (SVNIT Surat)
- **Aman Gupta:** Team Lead / Edge AI (MAX78000)
- **Aman Rana:** Firmware (FOC, Trajectory)
- **Dhyan Modi:** Electronics (ADI Integration)
- **Anushka Kasle:** Software (Braille Encoding)
- **Tanmay Singh:** Mechanical (SCARA CAD)
- **Dr. Anand D. Darji:** Faculty Mentor
