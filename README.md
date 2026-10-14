# Transistor → Qubit Learning Lab

An interactive educational simulator for the EDC Assignment #2, **“From Transistors to Qubits: A Hybrid Learning Framework for Understanding Quantum Computing through Semiconductor Concepts.”**

## Features

- **Module A — Transistor switch:** change input voltage, switching threshold, supply voltage, load resistance, and see an LED-like output and illustrative current.
- **Module B — Logic gates:** NOT, AND, OR, NAND, NOR, and XOR with truth tables.
- **Module C — Quantum simulator:** initial states `|0⟩` and `|1⟩`; X, H, Y, and Z gates; amplitudes; measurement probabilities; repeatable shot simulation; optional two-qubit CNOT basis-state demo.
- **Module D — Classical vs quantum:** side-by-side conceptual comparison and NOT/X demonstration.
- **Module E — Noise:** classical noisy voltage plot, threshold classification errors, and explanations of bit-flip, phase-flip, depolarizing noise, decoherence, and error correction.
- **Assessment:** six-question self-check with explanations.

## Requirements

- Python 3.10 or newer recommended
- VS Code (or another Python editor)
- Internet connection for installing packages and deploying

## Run locally in VS Code

1. Extract the ZIP.
2. Open the extracted `Transistor_To_Qubit_Simulator` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use:
   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   .venv\Scripts\python.exe -m streamlit run app.py
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```

5. Streamlit prints a local URL, normally `http://localhost:8501`. Open it in your browser.

## Publish to GitHub

Create an empty repository on GitHub first. Do not add a README there if you plan to push this folder's existing README.

From the project folder terminal:

```bash
git init
git add .
git commit -m "Build Transistor-to-Qubit Learning Lab"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own repository URL. GitHub stores the source code; it does **not** automatically host a running Streamlit app.

## Deploy the app online with Streamlit Community Cloud

1. Push the project to GitHub using the steps above.
2. Sign in to Streamlit Community Cloud with your GitHub account.
3. Select **Create app** / **Deploy an app**.
4. Choose your repository, branch `main`, and main file path `app.py`.
5. Deploy. Streamlit installs packages from `requirements.txt`.
6. Open the generated public app URL and test every module.

Deployment screens may change. If deployment fails, inspect the app logs; the most common causes are a wrong repository/branch/file path or a missing dependency.

## Project structure

```text
Transistor_To_Qubit_Simulator/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

## Important scientific and project limitations

- The transistor section is a simplified threshold model, not a device-level BJT/MOSFET simulator and not a real breadboard measurement.
- The quantum section is a small NumPy state-vector simulation. It does not require IBM Quantum credentials or a real quantum computer.
- Measurement results are simulated by sampling the state probabilities.
- The classical noise plot is not a physical model of quantum decoherence. The app explains the conceptual comparison separately.
- The project brief suggests a physical circuit and IBM Quantum Composer/Qiskit. This software-only implementation covers the requested learning modules but does not claim to have physically built a circuit or run on quantum hardware.

## Suggested submission checks

- [ ] Run `streamlit run app.py` locally.
- [ ] Test each module and all controls.
- [ ] Push the project to your own GitHub repository.
- [ ] Deploy with Streamlit Community Cloud if a live link is required.
- [ ] Rename the final ZIP to your student ID, as required by the assignment.
- [ ] Include screenshots of the working app if your instructor requests evidence.
