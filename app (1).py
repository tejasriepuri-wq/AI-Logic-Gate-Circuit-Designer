import itertools
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Logic Circuit Designer", page_icon="⚡", layout="wide")
st.title("⚡ AI-Based Logic Gate Circuit Designer")
st.write("Build a two-stage digital logic circuit, explore its truth table, and generate Verilog.")

GATES = ["AND", "OR", "XOR", "NAND", "NOR", "XNOR"]

def gate_output(gate, a, b):
    if gate == "AND":
        return a & b
    if gate == "OR":
        return a | b
    if gate == "XOR":
        return a ^ b
    if gate == "NAND":
        return 1 - (a & b)
    if gate == "NOR":
        return 1 - (a | b)
    if gate == "XNOR":
        return 1 - (a ^ b)

st.subheader("1. Design your circuit")
st.write("First gate uses inputs A and B. Its output connects to the second gate with input C.")

col1, col2 = st.columns(2)
with col1:
    gate1 = st.selectbox("Choose the first gate", GATES, index=0)
with col2:
    gate2 = st.selectbox("Choose the second gate", GATES, index=1)

st.subheader("2. Circuit diagram")
diagram = f"""
digraph Circuit {{
  rankdir=LR;
  A [shape=circle];
  B [shape=circle];
  C [shape=circle];
  G1 [shape=box, label="{gate1}"];
  G2 [shape=box, label="{gate2}"];
  T [shape=plaintext, label="Output Y"];
  A -> G1;
  B -> G1;
  G1 -> G2 [label="X"];
  C -> G2;
  G2 -> T;
}}
"""
st.graphviz_chart(diagram, use_container_width=True)

st.subheader("3. Truth table")
rows = []
for a, b, c in itertools.product([0, 1], repeat=3):
    x = gate_output(gate1, a, b)
    y = gate_output(gate2, x, c)
    rows.append({"A": a, "B": b, "C": c, "Intermediate X": x, "Output Y": y})

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)

st.subheader("4. Logic expression")
expressions = {
    "AND": "({} & {})",
    "OR": "({} | {})",
    "XOR": "({} ^ {})",
    "NAND": "~({} & {})",
    "NOR": "~({} | {})",
    "XNOR": "~({} ^ {})",
}
x_expr = expressions[gate1].format("A", "B")
y_expr = expressions[gate2].format(x_expr, "C")
st.code(f"X = {x_expr}\nY = {y_expr}")

st.subheader("5. Verilog code")
operators = {
    "AND": "&", "OR": "|", "XOR": "^",
    "NAND": "~&", "NOR": "~|", "XNOR": "~^"
}
verilog = f"""module logic_circuit(
    input A, input B, input C,
    output Y
);
wire X;
assign X = A {operators[gate1]} B;
assign Y = X {operators[gate2]} C;
endmodule
"""
st.code(verilog, language="verilog")
st.download_button("Download Verilog", verilog, file_name="logic_circuit.v")

st.subheader("6. Circuit explanation")
st.write(
    f"The {gate1} gate processes A and B to produce X. "
    f"The {gate2} gate processes X and C to produce the final output Y."
)
st.info("This version uses predefined logic rules. An actual AI model can be added next to interpret circuit requirements written in natural language.")
