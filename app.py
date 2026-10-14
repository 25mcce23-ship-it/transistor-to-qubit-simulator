"""
Transistor-to-Qubit Simulator
Educational project based on the EDC Assignment #2 brief.
Run: streamlit run app.py
"""

import math
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Transistor → Qubit Learning Lab",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Styling ---------------------------------------
st.markdown("""
<style>
    .main {background-color: #f7f9fc;}
    .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
    .hero {
        padding: 1.6rem 1.8rem; border-radius: 18px;
        background: linear-gradient(120deg, #102a43, #176b87);
        color: white; margin-bottom: 1rem;
    }
    .hero h1 {color: white; margin-bottom: .25rem;}
    .hero p {color: #e4f4fa; font-size: 1.05rem;}
    .metric-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 1rem; min-height: 100px;
    }
    .small-note {font-size: .9rem; color: #52606d;}
    .pass {color: #137333; font-weight: 700;}
    .fail {color: #b3261e; font-weight: 700;}
    div[data-testid="stMetric"] {
        background: white; padding: 12px; border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------- Quantum math ---------------------------------
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

def clean_complex(z):
    if abs(z.imag) < 1e-10:
        return f"{z.real:.3f}"
    return f"{z.real:.3f}{z.imag:+.3f}i"

def state_probabilities(state):
    probs = np.abs(state) ** 2
    probs = probs / probs.sum()
    return probs

def apply_single_gate(state, gate):
    return gate @ state

def cnot_state(state):
    """Apply CNOT to a two-qubit state in basis order |00>, |01>, |10>, |11>."""
    cnot = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ], dtype=complex)
    return cnot @ state

def measure_state(state, rng):
    probs = state_probabilities(state)
    outcome = int(rng.choice([0, 1], p=probs))
    collapsed = np.zeros(2, dtype=complex)
    collapsed[outcome] = 1.0
    return outcome, probs, collapsed

def truth_table(gate_name):
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            if gate_name == "NOT":
                out = 1 - a
            elif gate_name == "AND":
                out = a & b
            elif gate_name == "OR":
                out = a | b
            elif gate_name == "NAND":
                out = 1 - (a & b)
            elif gate_name == "NOR":
                out = 1 - (a | b)
            elif gate_name == "XOR":
                out = a ^ b
            else:
                out = 0
            rows.append({"Input A": a, "Input B": b, "Output": int(out)})
    if gate_name == "NOT":
        return [{"Input A": 0, "Output": 1}, {"Input A": 1, "Output": 0}]
    return rows

# ----------------------------- Header ----------------------------------------
st.markdown("""
<div class="hero">
  <h1>⚛️ Transistor → Qubit Learning Lab</h1>
  <p>Explore how familiar semiconductor switching and digital logic connect to quantum states, gates, and measurement.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Learning path")
    page = st.radio(
        "Choose a module",
        [
            "Overview",
            "A · Transistor switch",
            "B · Logic-gate simulator",
            "C · Quantum simulator",
            "D · Classical vs quantum",
            "E · Noise & reflection",
            "Assessment",
        ],
    )
    st.divider()
    st.caption("EDC Assignment #2 • Educational simulation")
    st.caption("This is a software model, not a replacement for a physical breadboard experiment.")

# ----------------------------- Overview --------------------------------------
if page == "Overview":
    st.subheader("Four-level learning framework")
    st.write("Start with a deterministic switch, build logic, then compare a classical bit with a qubit.")
    cols = st.columns(4)
    cards = [
        ("1", "Transistor", "Input voltage controls an LED-like output."),
        ("2", "Logic gate", "Build a NOT gate and explore other truth tables."),
        ("3", "Bit → qubit", "Use amplitudes, X/H/Z gates, and measurement."),
        ("4", "Compare", "Contrast deterministic digital outputs with probabilistic quantum measurements."),
    ]
    for col, (n, title, body) in zip(cols, cards):
        with col:
            st.markdown(f"""<div class="metric-card"><h2>{n}</h2><h3>{title}</h3><p>{body}</p></div>""", unsafe_allow_html=True)

    st.subheader("Concept map")
    st.markdown("""
    | Classical electronics | Quantum computing |
    |---|---|
    | Transistor switch | Qubit as a quantum information unit |
    | Digital bit: 0 or 1 | State: \\(|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle\\) |
    | NOT gate | X gate flips \\(|0\\rangle\\leftrightarrow|1\\rangle\\) |
    | Logic-gate network | Quantum circuit |
    | Read digital output | Measure a quantum state |
    | Electrical noise | Quantum noise / decoherence |
    """)
    st.info("Important: a qubit is not simply a classical bit that is both 0 and 1. Its state is described by probability amplitudes; measurement returns a classical result.")
    st.subheader("How to use this project")
    st.markdown("""
    1. Open **A · Transistor switch** and change the input voltage and threshold.
    2. Open **B · Logic-gate simulator** and verify a truth table.
    3. Open **C · Quantum simulator**; compare X and H gate behaviour.
    4. Open **D · Classical vs quantum** for a side-by-side comparison.
    5. Open **E · Noise & reflection** and **Assessment** to consolidate learning.
    """)

# ----------------------------- Module A --------------------------------------
elif page == "A · Transistor switch":
    st.subheader("Module A — Transistor switch")
    st.write("A simplified model of a transistor driving an LED. The output switches when the input reaches the chosen threshold.")
    c1, c2 = st.columns([1, 1])
    with c1:
        vin = st.slider("Input / base-gate voltage (V)", 0.0, 5.0, 0.0, 0.1)
        threshold = st.slider("Switching threshold (V)", 0.5, 4.5, 2.0, 0.1)
        supply = st.slider("Supply voltage (V)", 3.0, 12.0, 5.0, 0.5)
        resistance = st.slider("Load resistance (Ω)", 220, 2200, 1000, 10)
        current_limit = st.slider("Illustrative maximum current (mA)", 1, 20, 10)
    is_on = vin >= threshold
    current_ma = min(max((supply - 2.0) / resistance * 1000, 0), current_limit) if is_on else 0.0
    with c2:
        st.markdown("### Circuit response")
        st.metric("Switch state", "ON" if is_on else "OFF")
        st.metric("Digital interpretation", "1" if is_on else "0")
        st.metric("Illustrative load current", f"{current_ma:.2f} mA")
        if is_on:
            st.success("The input crossed the threshold: the simplified switch is ON and the LED is lit.")
        else:
            st.warning("The input is below the threshold: the simplified switch is OFF and the LED is dark.")
        led_color = "#21c55d" if is_on else "#9ca3af"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:18px;background:white;border:1px solid #dbe3ea;border-radius:14px;padding:22px;">
          <div style="width:74px;height:74px;border-radius:50%;background:{led_color};box-shadow:0 0 {18 if is_on else 2}px {led_color};border:5px solid #d1d5db;"></div>
          <div><b>LED indicator</b><br><span style="color:#52606d">{'Lit' if is_on else 'Unlit'}</span></div>
        </div>
        """, unsafe_allow_html=True)
    st.caption("Model limitation: this is an educational threshold model, not a detailed BJT/MOSFET device simulation. The current estimate is illustrative.")
    st.markdown("**Try this:** raise the threshold above the input and observe the switch change from 1 to 0.")

# ----------------------------- Module B --------------------------------------
elif page == "B · Logic-gate simulator":
    st.subheader("Module B — Logic-gate simulator")
    gate = st.selectbox("Choose a logic gate", ["NOT", "AND", "OR", "NAND", "NOR", "XOR"])
    if gate == "NOT":
        a = st.radio("Input A", [0, 1], horizontal=True, key="not_a")
        out = 1 - a
        st.markdown(f"### Output: **{out}**")
        table = truth_table("NOT")
    else:
        c1, c2 = st.columns(2)
        with c1:
            a = st.radio("Input A", [0, 1], horizontal=True, key=f"{gate}_a")
        with c2:
            b = st.radio("Input B", [0, 1], horizontal=True, key=f"{gate}_b")
        if gate == "AND": out = a & b
        elif gate == "OR": out = a | b
        elif gate == "NAND": out = 1 - (a & b)
        elif gate == "NOR": out = 1 - (a | b)
        else: out = a ^ b
        st.markdown(f"### Output: **{out}**")
        table = truth_table(gate)
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.info("Classical logic gates are deterministic: the same input values always produce the same output.")
    st.markdown("**Connection to quantum computing:** the X gate is analogous to a NOT operation on computational basis states: X|0⟩ = |1⟩ and X|1⟩ = |0⟩. Not every classical gate has a direct one-qubit reversible quantum equivalent.")

# ----------------------------- Module C --------------------------------------
elif page == "C · Quantum simulator":
    st.subheader("Module C — Quantum simulator")
    st.write("Choose an initial one-qubit basis state, apply a gate, and inspect the amplitudes and measurement probabilities.")
    initial = st.radio("Initial state", ["|0⟩", "|1⟩"], horizontal=True)
    gate_name = st.selectbox("Apply gate", ["None", "X", "H", "Y", "Z"])
    repetitions = st.slider("Number of simulated measurements", 10, 2000, 500, 10)
    seed = st.number_input("Random seed (repeatable experiment)", min_value=0, max_value=999999, value=42, step=1)
    state = np.array([1, 0], dtype=complex) if initial == "|0⟩" else np.array([0, 1], dtype=complex)
    gates = {"None": I2, "X": X, "H": H, "Y": Y, "Z": Z}
    final_state = apply_single_gate(state, gates[gate_name])
    probs = state_probabilities(final_state)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("P(0)", f"{probs[0]*100:.1f}%")
    with c2:
        st.metric("P(1)", f"{probs[1]*100:.1f}%")
    with c3:
        st.metric("State norm", f"{np.linalg.norm(final_state):.3f}")
    st.markdown("#### State amplitudes")
    st.latex(r"|\psi\rangle = \alpha|0\rangle + \beta|1\rangle")
    st.write(f"α = `{clean_complex(final_state[0])}`")
    st.write(f"β = `{clean_complex(final_state[1])}`")
    st.bar_chart({"Probability": {"Outcome 0": float(probs[0]), "Outcome 1": float(probs[1])}})
    rng = np.random.default_rng(int(seed))
    samples = rng.choice([0, 1], size=int(repetitions), p=probs)
    count0 = int(np.sum(samples == 0))
    count1 = int(np.sum(samples == 1))
    st.markdown("#### Repeated measurement experiment")
    st.write(f"Out of **{repetitions}** simulated shots: **0 → {count0}**, **1 → {count1}**.")
    st.bar_chart({"Observed count": {"0": count0, "1": count1}})
    st.caption("The H gate creates an equal superposition from |0⟩. Measurement samples 0 and 1 with equal probability; a single measurement still returns only one classical result.")
    with st.expander("Optional: two-qubit CNOT demonstration"):
        control = st.radio("Control qubit", ["0", "1"], horizontal=True)
        target = st.radio("Target qubit", ["0", "1"], horizontal=True)
        basis_index = int(control) * 2 + int(target)
        two_state = np.zeros(4, dtype=complex)
        two_state[basis_index] = 1
        result = cnot_state(two_state)
        before = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"][basis_index]
        after_index = int(np.argmax(np.abs(result)))
        after = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"][after_index]
        st.write(f"Input: **{before}** → After CNOT: **{after}**")
        st.caption("Basis order used here is |00⟩, |01⟩, |10⟩, |11⟩. The first qubit is the control; the second is the target.")

# ----------------------------- Module D --------------------------------------
elif page == "D · Classical vs quantum":
    st.subheader("Module D — Classical circuit vs quantum circuit")
    st.markdown("""
    | Feature | Classical approach | Quantum approach |
    |---|---|---|
    | Information unit | Bit | Qubit |
    | State description | 0 or 1 | Amplitudes α and β |
    | Basic inversion | NOT gate | X gate on basis states |
    | Processing | Logic gates | Quantum gates |
    | Output | Digital output | Measurement result |
    | Ideal behaviour | Deterministic for fixed inputs | Measurement can be probabilistic |
    | Disturbance | Electrical/signal noise | Quantum noise and decoherence |
    """)
    st.markdown("### Compare a NOT operation with an X gate")
    bit = st.radio("Classical input bit", [0, 1], horizontal=True)
    classical_output = 1 - bit
    q_initial = np.array([1, 0], dtype=complex) if bit == 0 else np.array([0, 1], dtype=complex)
    q_output = X @ q_initial
    quantum_output = int(np.argmax(np.abs(q_output) ** 2))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Classical")
        st.metric("NOT output", classical_output)
        st.write("For an ideal classical NOT gate, the output is fixed.")
    with c2:
        st.markdown("#### Quantum")
        st.metric("X gate basis-state output", quantum_output)
        st.write("For input |0⟩ or |1⟩, the ideal X gate flips the basis state. For a general superposition, it transforms amplitudes.")
    st.warning("Analogy has limits: a transistor is a physical switching device, while a qubit is a quantum state. They are not the same kind of object.")

# ----------------------------- Module E --------------------------------------
elif page == "E · Noise & reflection":
    st.subheader("Module E — Noise & reflection")
    st.write("Explore a simple classical noisy signal and compare it conceptually with quantum errors.")
    ideal = st.slider("Ideal output voltage (V)", 0.0, 5.0, 3.3, 0.1)
    noise_amp = st.slider("Classical noise amplitude (± V)", 0.0, 2.0, 0.5, 0.1)
    samples_n = st.slider("Number of samples", 20, 500, 120, 10)
    seed = st.number_input("Noise seed", min_value=0, max_value=999999, value=7, step=1)
    rng = np.random.default_rng(int(seed))
    noise = rng.uniform(-noise_amp, noise_amp, int(samples_n))
    noisy_signal = ideal + noise
    x_axis = np.arange(int(samples_n))
    st.line_chart({"Ideal output": np.full(int(samples_n), ideal), "Noisy output": noisy_signal})
    low, high = 0.0, 5.0
    threshold = st.slider("Digital decision threshold (V)", 0.0, 5.0, 2.5, 0.1)
    bit_errors = int(np.sum((noisy_signal >= threshold) != (ideal >= threshold)))
    c1, c2, c3 = st.columns(3)
    c1.metric("Mean noisy voltage", f"{np.mean(noisy_signal):.2f} V")
    c2.metric("Noise standard deviation", f"{np.std(noise):.2f} V")
    c3.metric("Threshold classification errors", f"{bit_errors}/{samples_n}")
    st.markdown("### Quantum error concepts")
    st.markdown("""
    - **Bit-flip error:** changes the computational basis state, similar in effect to an unintended X operation.
    - **Phase-flip error:** changes the relative phase of a state; it may not change a basis-state measurement immediately.
    - **Depolarizing noise:** a model that replaces the state with a random Pauli error with some probability.
    - **Decoherence:** loss of quantum coherence through interaction with the environment.
    - **Quantum error correction:** encodes information across multiple physical qubits so errors can be detected and corrected without directly copying an arbitrary unknown qubit.
    """)
    st.warning("Classical voltage noise and quantum decoherence are not physically identical. This comparison is conceptual; the plotted noise model is classical only.")
    st.markdown("**Reflection prompt:** How can noise near a classical switching threshold cause a wrong bit, and why do quantum systems need additional care to preserve phase and coherence?")

# ----------------------------- Assessment ------------------------------------
elif page == "Assessment":
    st.subheader("Quick assessment")
    st.write("Answer these questions, then check your score. This is a formative self-check, not a formal examination.")
    questions = [
        ("What does a transistor switch represent in this learning framework?", ["A classical ON/OFF state", "A qubit superposition", "A measurement apparatus"], 0,
         "The transistor switch illustrates a classical ON/OFF state."),
        ("Which quantum gate flips |0⟩ and |1⟩?", ["H", "X", "Z"], 1,
         "X|0⟩ = |1⟩ and X|1⟩ = |0⟩."),
        ("What does the Hadamard gate do to |0⟩?", ["Creates equal-amplitude superposition", "Always outputs 1", "Deletes the qubit"], 0,
         "H|0⟩ = (|0⟩ + |1⟩)/√2."),
        ("What does a measurement return for one qubit?", ["Both 0 and 1 as a single result", "One classical outcome", "A voltage"], 1,
         "A measurement produces a classical outcome, 0 or 1."),
        ("Which is a quantum noise/error concept?", ["Load resistance", "Depolarizing noise", "LED current"], 1,
         "Depolarizing noise is a common quantum noise model."),
        ("Which statement is most accurate?", ["A qubit is exactly the same as a transistor", "A qubit state uses probability amplitudes", "Quantum gates are only AND/OR gates"], 1,
         "A qubit is described by amplitudes α and β, with |α|² + |β|² = 1."),
    ]
    answers = []
    for i, (question, options, correct, explanation) in enumerate(questions):
        choice = st.radio(f"{i+1}. {question}", options, key=f"quiz_{i}")
        answers.append(options.index(choice))
    if st.button("Check my answers", type="primary"):
        score = sum(a == q[2] for a, q in zip(answers, questions))
        st.metric("Score", f"{score}/{len(questions)}", f"{score/len(questions)*100:.0f}%")
        for i, (question, options, correct, explanation) in enumerate(questions):
            if answers[i] == correct:
                st.success(f"Q{i+1}: Correct. {explanation}")
            else:
                st.error(f"Q{i+1}: Review this. {explanation}")
        if score == len(questions):
            st.balloons()
    st.caption("Suggested extension: repeat the assessment after using all four learning levels and compare your conceptual understanding.")

st.divider()
st.caption("Transistor → Qubit Learning Lab | Built with Python, Streamlit and NumPy | For educational use")
