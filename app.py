
import math
import streamlit as st

st.set_page_config(
    page_title="E-CELL | Virtual Electrochemistry Lab",
    page_icon="⚡",
    layout="wide",
)

# ---------- Styling ----------
st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; margin-bottom: 0;}
.sub-title {font-size: 18px; opacity: .8; margin-top: 0;}
.card {
    padding: 1.1rem 1.2rem;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,.25);
    background: rgba(128,128,128,.06);
    margin-bottom: 1rem;
}
.result {
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,.3);
}
.small {font-size: 0.9rem; opacity: .75;}
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
E0 = {
    "Zn²⁺/Zn": -0.76,
    "Fe²⁺/Fe": -0.44,
    "Cu²⁺/Cu": 0.34,
    "Ag⁺/Ag": 0.80,
}

IONS = {
    "Zn²⁺/Zn": ("Zn²⁺", 2),
    "Fe²⁺/Fe": ("Fe²⁺", 2),
    "Cu²⁺/Cu": ("Cu²⁺", 2),
    "Ag⁺/Ag": ("Ag⁺", 1),
}

def cell_potential(cathode, anode):
    return E0[cathode] - E0[anode]

def reaction_quotient(cathode, anode, cathode_conc, anode_conc):
    # For the educational metal-ion/metal cell model:
    # M_cathode^(z+) + M_anode(s) -> M_cathode(s) + M_anode^(z+)
    return anode_conc / cathode_conc

def n_for_pair(cathode, anode):
    zc = IONS[cathode][1]
    za = IONS[anode][1]
    # LCM for electron balancing
    return math.lcm(zc, za)

def nernst(E0cell, n, Q, T):
    R = 8.314
    F = 96485
    return E0cell - (R*T/(n*F))*math.log(Q)

# ---------- Header ----------
st.markdown('<div class="main-title">⚡ E-CELL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Virtual Electrochemistry Laboratory • Engineering Chemistry</div>', unsafe_allow_html=True)

st.sidebar.title("🧪 Laboratory")
page = st.sidebar.radio(
    "Select module",
    ["🏠 Home", "🔋 Galvanic Cell", "🧮 Nernst Equation", "⚡ Gibbs Free Energy",
     "💧 Electrolysis", "📚 Theory", "📝 Quiz", "📄 Experiment Report"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Students**")
st.sidebar.write("G. Likitha")
st.sidebar.write("RA2611030050100")
st.sidebar.write("B. Tarun Ram Kiran")
st.sidebar.write("RA261103005086")

# ---------- Home ----------
if page == "🏠 Home":
    st.success("Welcome to E-CELL — an interactive virtual electrochemistry laboratory.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Experiments", "4")
    c2.metric("Calculators", "2")
    c3.metric("Assessment", "1 quiz")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Aim")
    st.write("To study electrochemical cells and understand cell potential, the Nernst equation, Gibbs free energy and electrolysis through an interactive simulation.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🧭 Lab workflow")
    st.write("1. Choose an experiment → 2. Enter/select conditions → 3. Run the simulation → 4. Observe calculations → 5. Record the result.")

    st.info("Educational simulation only. It is intended for learning and does not reproduce every physical laboratory effect.")

# ---------- Galvanic Cell ----------
elif page == "🔋 Galvanic Cell":
    st.header("🔋 Galvanic Cell Simulator")
    st.write("Build a simple metal/metal-ion electrochemical cell and observe the predicted cell potential.")

    col1, col2 = st.columns(2)
    with col1:
        anode = st.selectbox("Select anode (oxidation)", list(E0.keys()), index=0)
        anode_conc = st.number_input("Anode ion concentration (M)", 0.001, 10.0, 1.0, 0.001)
    with col2:
        cathode_options = [x for x in E0.keys() if x != anode]
        cathode = st.selectbox("Select cathode (reduction)", cathode_options, index=0)
        cathode_conc = st.number_input("Cathode ion concentration (M)", 0.001, 10.0, 1.0, 0.001)

    if st.button("▶ Run Galvanic Cell", type="primary"):
        e0 = cell_potential(cathode, anode)
        n = n_for_pair(cathode, anode)
        q = reaction_quotient(cathode, anode, cathode_conc, anode_conc)
        e = nernst(e0, n, q, 298.15)

        st.subheader("🧪 Virtual Cell")
        a, b, c = st.columns(3)
        a.metric("Anode", anode)
        b.metric("Cathode", cathode)
        c.metric("E°cell", f"{e0:.3f} V")

        st.markdown(f"""
        <div class="card">
        <b>Electron flow:</b> {anode} → {cathode}<br>
        <b>Anode process:</b> Oxidation<br>
        <b>Cathode process:</b> Reduction<br>
        <b>Cell notation:</b> {anode.split('/')[0]} | {anode.split('/')[0]}²⁺ || {cathode.split('/')[0]}²⁺ | {cathode.split('/')[0]}
        </div>
        """, unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        r1.metric("n", n)
        r2.metric("Q", f"{q:.4g}")
        r3.metric("Ecell at 298 K", f"{e:.3f} V")

        if e0 > 0:
            st.success("Spontaneous as written under standard conditions.")
        else:
            st.warning("Not spontaneous as written under standard conditions.")

# ---------- Nernst ----------
elif page == "🧮 Nernst Equation":
    st.header("🧮 Nernst Equation Simulator")
    st.latex(r"E = E^\circ - \frac{RT}{nF}\ln Q")
    c1, c2 = st.columns(2)
    with c1:
        e0 = st.number_input("E°cell (V)", value=1.10, step=0.01, format="%.3f")
        n = st.number_input("Number of electrons, n", min_value=1, value=2, step=1)
    with c2:
        q = st.number_input("Reaction quotient, Q", min_value=0.000001, value=1.0, step=0.1)
        T = st.number_input("Temperature (K)", min_value=1.0, value=298.15, step=1.0)

    if st.button("Calculate Ecell", type="primary"):
        e = nernst(e0, int(n), q, T)
        st.success(f"Cell potential = **{e:.4f} V**")
        st.caption(f"Using R = 8.314 J mol⁻¹ K⁻¹ and F = 96485 C mol⁻¹.")

# ---------- Gibbs ----------
elif page == "⚡ Gibbs Free Energy":
    st.header("⚡ Gibbs Free Energy Calculator")
    st.latex(r"\Delta G = -nFE")
    e = st.number_input("Cell potential, E (V)", value=1.10, step=0.01)
    n = st.number_input("Number of electrons, n", min_value=1, value=2, step=1)

    if st.button("Calculate ΔG", type="primary"):
        dg = -int(n) * 96485 * e
        dg_kj = dg / 1000
        st.metric("ΔG", f"{dg_kj:.2f} kJ mol⁻¹")
        if dg < 0:
            st.success("ΔG < 0 → reaction is thermodynamically spontaneous.")
        elif dg > 0:
            st.warning("ΔG > 0 → reaction is non-spontaneous as written.")
        else:
            st.info("ΔG = 0 → system is at equilibrium.")

# ---------- Electrolysis ----------
elif page == "💧 Electrolysis":
    st.header("💧 Electrolysis Simulator")
    st.write("Explore the basic idea of electrolysis: electrical energy drives a non-spontaneous chemical reaction.")

    electrolyte = st.selectbox("Electrolyte", ["CuSO₄(aq)", "NaCl(aq)", "Water with inert electrolyte"])
    electrode = st.selectbox("Electrode material", ["Copper", "Platinum (inert)", "Carbon (inert)"])
    voltage = st.slider("Applied voltage (V)", 0.0, 10.0, 2.0, 0.1)

    if st.button("▶ Start Electrolysis", type="primary"):
        st.progress(min(voltage/10, 1.0))
        if electrolyte == "CuSO₄(aq)":
            cathode = "Cu²⁺ + 2e⁻ → Cu(s)"
            anode = "Cu(s) → Cu²⁺ + 2e⁻" if electrode == "Copper" else "Water/anion oxidation occurs at the anode (simplified model)."
        elif electrolyte == "NaCl(aq)":
            cathode = "2H₂O + 2e⁻ → H₂ + 2OH⁻ (simplified)"
            anode = "2Cl⁻ → Cl₂ + 2e⁻ (simplified)"
        else:
            cathode = "2H₂O + 2e⁻ → H₂ + 2OH⁻"
            anode = "2H₂O → O₂ + 4H⁺ + 4e⁻"

        c1, c2 = st.columns(2)
        c1.info("**Cathode (reduction)**\n\n" + cathode)
        c2.info("**Anode (oxidation)**\n\n" + anode)
        st.success(f"Simulation running at {voltage:.1f} V.")

# ---------- Theory ----------
elif page == "📚 Theory":
    st.header("📚 Theory")
    with st.expander("Galvanic cell"):
        st.write("A galvanic (voltaic) cell converts chemical energy from a spontaneous redox reaction into electrical energy. Oxidation occurs at the anode and reduction occurs at the cathode.")
    with st.expander("Standard cell potential"):
        st.write("E°cell = E°cathode − E°anode. A positive E°cell indicates a spontaneous reaction under standard conditions.")
    with st.expander("Nernst equation"):
        st.write("The Nernst equation gives cell potential under non-standard conditions using temperature, electron number and reaction quotient.")
    with st.expander("Gibbs free energy"):
        st.write("ΔG = −nFE. A negative ΔG corresponds to a spontaneous electrochemical reaction as written.")
    with st.expander("Electrolysis"):
        st.write("Electrolysis uses an external electrical source to drive a non-spontaneous redox reaction.")

# ---------- Quiz ----------
elif page == "📝 Quiz":
    st.header("📝 Self-Assessment Quiz")
    questions = [
        ("Where does oxidation occur?", ["Anode", "Cathode", "Salt bridge", "Voltmeter"], "Anode"),
        ("For a spontaneous galvanic cell, E°cell is usually:", ["Negative", "Zero", "Positive", "Undefined"], "Positive"),
        ("The Nernst equation accounts for:", ["Only color", "Non-standard conditions", "Only pressure", "Only mass"], "Non-standard conditions"),
        ("The SI unit commonly used for cell potential is:", ["J", "V", "Pa", "mol"], "V"),
        ("In electrolysis, electrical energy is used to drive a:", ["Spontaneous reaction only", "Non-spontaneous reaction", "Neutralization only", "Combustion"], "Non-spontaneous reaction"),
    ]
    score = 0
    answers = []
    for i, (q, opts, ans) in enumerate(questions, 1):
        choice = st.radio(f"{i}. {q}", opts, key=f"q{i}")
        answers.append(choice)
    if st.button("Submit Quiz", type="primary"):
        score = sum(a == questions[i][2] for i, a in enumerate(answers))
        st.success(f"Score: {score}/{len(questions)}")
        st.write("Review the Theory section for any questions you missed.")

# ---------- Report ----------
elif page == "📄 Experiment Report":
    st.header("📄 Experiment Report Generator")
    st.write("Fill in the details and generate a ready-to-copy experiment record.")

    student = st.text_input("Student name", "G. Likitha")
    reg = st.text_input("Registration number", "RA2611030050100")
    experiment = st.selectbox("Experiment", [
        "Determination of cell potential of a galvanic cell",
        "Verification of Nernst equation",
        "Calculation of Gibbs free energy",
        "Study of electrolysis"
    ])
    observation = st.text_area("Observation", "The simulated cell produced a positive cell potential under the selected conditions.")
    result = st.text_area("Result", "The electrochemical behavior was studied successfully using the virtual laboratory.")

    report = f"""E-CELL — VIRTUAL ELECTROCHEMISTRY LAB

Student: {student}
Registration No.: {reg}

Experiment: {experiment}

AIM:
To study the selected electrochemical experiment using the E-CELL virtual laboratory.

THEORY:
Electrochemical reactions involve oxidation and reduction. In a galvanic cell, a spontaneous redox reaction generates electrical energy. Cell potential can be calculated using standard reduction potentials and, under non-standard conditions, the Nernst equation.

PROCEDURE:
1. Open the required E-CELL module.
2. Select the experimental conditions.
3. Enter the required values.
4. Run the simulation.
5. Record the displayed calculations and observations.
6. State the final result.

OBSERVATION:
{observation}

RESULT:
{result}

CONCLUSION:
The selected electrochemical concept was successfully demonstrated using the virtual laboratory.

"""
    st.download_button(
        "⬇️ Download Report (.txt)",
        report,
        file_name="E-CELL_Experiment_Report.txt",
        mime="text/plain"
    )
    st.text_area("Report preview", report, height=420)

st.markdown("---")
st.caption("E-CELL Virtual Electrochemistry Lab • Engineering Chemistry • Educational simulation")
