# E-CELL — Virtual Electrochemistry Lab

A browser-based educational application for introductory electrochemistry, built with **Python** and **Streamlit**.

## Modules
- **Galvanic Cell Simulator:** choose two representative half-cells; identify anode and cathode and calculate standard cell EMF.
- **Nernst Calculator:** calculate cell potential for user-supplied E°cell, electron count, temperature and reaction quotient.
- **Gibbs Free Energy:** calculate ΔG from n and Ecell and interpret the sign.
- **Theory Notes:** revise oxidation/reduction, galvanic cells, cell potential, the Nernst equation and Gibbs free energy.
- **Knowledge Quiz:** five-question self-check with score and feedback.

## Run on your computer

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the lab:

   ```bash
   streamlit run app.py
   ```

6. Streamlit will provide a local URL (usually `http://localhost:8501`). Open it in your browser.

## Publish using GitHub + Streamlit Community Cloud

1. Sign in to GitHub and create a **new public repository**, for example `e-cell-virtual-lab`.
2. Upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore` to the repository (or use **Add file → Upload files**).
3. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
4. Choose **Create app**, select your repository and branch (`main`), and set the main file path to `app.py`.
5. Select **Deploy**. Wait for the app to build, then open the generated public app URL.

GitHub stores and versions the source code. Streamlit Community Cloud runs and hosts the interactive app.

## Example: Daniell cell

The simulator includes Zn²⁺/Zn (−0.76 V) and Cu²⁺/Cu (+0.34 V).

- Cathode: Cu²⁺/Cu
- Anode: Zn²⁺/Zn
- E°cell = 0.34 − (−0.76) = **+1.10 V**

For the Nernst calculator, when E°cell = 1.10 V, n = 2, T = 298 K and Q = 1, Ecell = 1.10 V.

For n = 2 and Ecell = 1.10 V, ΔG ≈ **−212.27 kJ mol⁻¹**.

## Notes and limitations
- Standard reduction potentials are representative values in volts.
- The Nernst calculator expects a suitable positive reaction quotient Q and the correct electron count n to be entered by the user.
- This is a simplified educational model; it does not reproduce all physical laboratory effects or automatically balance arbitrary redox equations.
- Internet access is required for the hosted version.

## Project context
Prepared as the E-CELL — Virtual Electrochemistry Lab project for Engineering Chemistry / Electrochemistry.
