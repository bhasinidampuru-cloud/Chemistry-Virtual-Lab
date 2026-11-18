import math
import streamlit as st

st.set_page_config(page_title="E-CELL | Virtual Electrochemistry Lab", page_icon="⚡", layout="wide")

# Standard reduction potentials (V), representative educational values.
ELECTRODES = {
    "Zn²⁺ / Zn": -0.76,
    "Fe²⁺ / Fe": -0.44,
    "Ni²⁺ / Ni": -0.25,
    "Cu²⁺ / Cu": 0.34,
    "Ag⁺ / Ag": 0.80,
    "Mg²⁺ / Mg": -2.37,
}

st.markdown("""
<style>
    .main {background: linear-gradient(180deg, #f5f8ff 0%, #ffffff 45%);}
    .hero {padding: 1.4rem 1.6rem; border-radius: 18px; color: white;
           background: linear-gradient(115deg,#102b58,#176b87); margin-bottom: 1rem;}
    .hero h1 {margin:0; color:white;}
    .hero p {margin:.35rem 0 0 0; color:#e4f4ff;}
    div[data-testid="stMetric"] {background:#f0f6ff; padding: .8rem; border-radius: 12px;}
    .note {padding: .8rem 1rem; border-left: 4px solid #1d83a5;
           background:#eef8fc; border-radius:8px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>⚡ E-CELL — Virtual Electrochemistry Lab</h1>
<p>Explore galvanic cells, calculate cell potential, and understand Gibbs free energy.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🧪 Lab navigation")
    page = st.radio("Choose a module", [
        "Home", "Galvanic Cell Simulator", "Nernst Calculator",
        "Gibbs Free Energy", "Theory Notes", "Knowledge Quiz"
    ])
    st.divider()
    st.caption("Engineering Chemistry • Electrochemistry")
    st.caption("Educational simulation — not a physical laboratory.")

if page == "Home":
    st.subheader("Welcome to E-CELL")
    st.write("A browser-based learning space for the fundamentals of electrochemistry.")
    cols = st.columns(4)
    modules = [
        ("🔋", "Galvanic cell", "Choose two half-cells and calculate standard EMF."),
        ("📐", "Nernst equation", "Explore cell potential under non-standard conditions."),
        ("⚡", "Gibbs energy", "Connect cell potential with reaction spontaneity."),
        ("📚", "Theory & quiz", "Revise key ideas and check your understanding."),
    ]
    for col, (emoji, title, desc) in zip(cols, modules):
        with col:
            st.markdown(f"### {emoji} {title}")
            st.write(desc)
    st.markdown('<div class="note"><b>How to begin:</b> Select a module from the left menu. Try the Daniell cell (Zn²⁺/Zn and Cu²⁺/Cu) first.</div>', unsafe_allow_html=True)
    st.subheader("Core equations")
    a, b, c = st.columns(3)
    a.latex(r"E^\circ_{cell}=E^\circ_{cathode}-E^\circ_{anode}")
    b.latex(r"E_{cell}=E^\circ_{cell}-\frac{RT}{nF}\ln Q")
    c.latex(r"\Delta G=-nFE_{cell}")

elif page == "Galvanic Cell Simulator":
    st.subheader("🔋 Galvanic Cell Simulator")
    st.write("Select two half-cells. The half-cell with the higher reduction potential acts as the cathode.")
    left, right = st.columns(2)
    names = list(ELECTRODES.keys())
    with left:
        first = st.selectbox("First half-cell", names, index=0)
    with right:
        second = st.selectbox("Second half-cell", names, index=3)
    if first == second:
        st.warning("Choose two different half-cells to form a cell.")
    else:
        e1, e2 = ELECTRODES[first], ELECTRODES[second]
        if e1 > e2:
            cathode, anode, ec, ea = first, second, e1, e2
        else:
            cathode, anode, ec, ea = second, first, e2, e1
        emf = ec - ea
        m1, m2, m3 = st.columns(3)
        m1.metric("Standard cell EMF", f"{emf:.2f} V")
        m2.metric("Cathode (reduction)", cathode)
        m3.metric("Anode (oxidation)", anode)
        st.success("Positive E°cell: the cell reaction in this direction is spontaneous under standard conditions." if emf > 0 else "The selected direction is not spontaneous under standard conditions.")
        st.markdown("**Electron flow:** anode → cathode through the external wire.")
        st.markdown("**Cell notation:**")
        st.code(f"{anode} || {cathode}")
        st.markdown("**Calculation**")
        st.latex(r"E^\circ_{cell}=E^\circ_{cathode}-E^\circ_{anode}")
        st.write(f"E°cell = {ec:.2f} − ({ea:.2f}) = **{emf:.2f} V**")
        st.caption("Values are representative standard reduction potentials in volts. This simplified simulator does not balance full ionic equations.")

elif page == "Nernst Calculator":
    st.subheader("📐 Nernst Equation Calculator")
    st.latex(r"E_{cell}=E^\circ_{cell}-\frac{RT}{nF}\ln Q")
    st.write("Enter the standard cell potential, temperature, electron count and reaction quotient.")
    c1, c2 = st.columns(2)
    with c1:
        e0 = st.number_input("Standard cell potential, E°cell (V)", value=1.10, step=0.01, format="%.4f")
        n = st.number_input("Number of electrons, n", min_value=1, max_value=20, value=2, step=1)
    with c2:
        temp = st.number_input("Temperature (K)", min_value=1.0, value=298.0, step=1.0)
        q = st.number_input("Reaction quotient, Q (must be > 0)", min_value=0.000001, value=1.0, format="%.6f")
    R, F = 8.314462618, 96485.33212
    e = e0 - (R * temp / (n * F)) * math.log(q)
    st.metric("Cell potential, Ecell", f"{e:.4f} V")
    st.caption(f"At {temp:g} K, (RT/nF) = {(R*temp/(n*F)):.6f} V.")
    st.info("When Q = 1, ln Q = 0, so Ecell = E°cell.")

elif page == "Gibbs Free Energy":
    st.subheader("⚡ Gibbs Free Energy Calculator")
    st.latex(r"\Delta G=-nFE_{cell}")
    c1, c2 = st.columns(2)
    with c1:
        n = st.number_input("Number of electrons, n", min_value=1, max_value=20, value=2, step=1, key="g_n")
    with c2:
        e = st.number_input("Cell potential, Ecell (V)", value=1.10, step=0.01, format="%.4f", key="g_e")
    F = 96485.33212
    dg = -n * F * e
    st.metric("Gibbs free-energy change", f"{dg/1000:.3f} kJ mol⁻¹")
    if dg < -1e-9:
        st.success("ΔG is negative: the represented reaction is spontaneous.")
    elif dg > 1e-9:
        st.warning("ΔG is positive: the represented reaction is non-spontaneous.")
    else:
        st.info("ΔG is zero: the system is at equilibrium.")

elif page == "Theory Notes":
    st.subheader("📚 Theory Notes")
    with st.expander("1. Oxidation and reduction", expanded=True):
        st.write("Oxidation is loss of electrons; reduction is gain of electrons. Oxidation occurs at the anode and reduction occurs at the cathode.")
    with st.expander("2. Galvanic cell"):
        st.write("A galvanic (voltaic) cell converts chemical energy from a spontaneous redox reaction into electrical energy. A Daniell cell uses zinc and copper half-cells connected by a wire and salt bridge.")
    with st.expander("3. Cell potential"):
        st.latex(r"E^\circ_{cell}=E^\circ_{cathode}-E^\circ_{anode}")
        st.write("A positive standard cell potential indicates spontaneity for the reaction direction represented under standard conditions.")
    with st.expander("4. Nernst equation"):
        st.latex(r"E_{cell}=E^\circ_{cell}-\frac{RT}{nF}\ln Q")
        st.write("R is the gas constant, T is temperature in kelvin, n is the number of electrons transferred, F is the Faraday constant and Q is the reaction quotient.")
    with st.expander("5. Gibbs free energy"):
        st.latex(r"\Delta G=-nFE_{cell}")
        st.write("Negative ΔG indicates a spontaneous reaction in the represented direction; zero indicates equilibrium; positive ΔG indicates a non-spontaneous direction.")

elif page == "Knowledge Quiz":
    st.subheader("🧠 Knowledge Quiz")
    questions = [
        ("Where does oxidation occur in a galvanic cell?", ["Cathode", "Anode", "Salt bridge", "External wire"], 1,
         "Oxidation (loss of electrons) occurs at the anode."),
        ("In a galvanic cell, electrons flow through the external circuit from:", ["Cathode to anode", "Anode to cathode", "Salt bridge to anode", "Cathode to salt bridge"], 1,
         "Electrons move from the anode to the cathode through the external wire."),
        ("Which expression gives standard cell potential?", ["E°anode − E°cathode", "E°cathode − E°anode", "nF/E", "−nFE"], 1,
         "Subtract the anode reduction potential from the cathode reduction potential."),
        ("For Q = 1, the Nernst equation gives:", ["Ecell = 0", "Ecell = E°cell", "ΔG = 0 always", "Ecell is negative"], 1,
         "Since ln(1) = 0, the correction term is zero."),
        ("A negative ΔG indicates:", ["Equilibrium", "Non-spontaneous direction", "Spontaneous direction", "No electron transfer"], 2,
         "A negative Gibbs free-energy change indicates spontaneity in the represented direction."),
    ]
    with st.form("quiz_form"):
        answers = []
        for i, (question, options, correct, explanation) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {question}**")
            answers.append(st.radio("Choose one:", options, key=f"quiz_{i}", index=None))
        submitted = st.form_submit_button("Submit answers")
    if submitted:
        score = sum(1 for answer, qdata in zip(answers, questions) if answer == qdata[1][qdata[2]])
        st.metric("Your score", f"{score} / {len(questions)}")
        for i, (answer, qdata) in enumerate(zip(answers, questions)):
            correct_answer = qdata[1][qdata[2]]
            if answer == correct_answer:
                st.success(f"Q{i+1}: Correct. {qdata[3]}")
            else:
                st.error(f"Q{i+1}: Correct answer: {correct_answer}. {qdata[3]}")

st.divider()
st.caption("E-CELL Virtual Electrochemistry Lab • Built with Python and Streamlit • For educational use")
