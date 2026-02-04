import streamlit as st
import json
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Spline+Sans:wght@400;500;600&display=swap');

    :root {
        --bg: #0b0f1a;
        --bg-2: #12182a;
        --card: #151c33;
        --card-2: #1b2544;
        --accent: #ff7a59;
        --accent-2: #3edbf0;
        --text: #f2f5ff;
        --muted: #9fb0d1;
        --border: #2a3555;
        --success: #2be6a8;
    }

    .stApp {
        background: radial-gradient(1200px 800px at 10% 0%, #1b2140 0%, var(--bg) 45%),
                    radial-gradient(1200px 800px at 90% 10%, #1a2b4d 0%, var(--bg) 55%);
        color: var(--text);
        font-family: "Spline Sans", sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: "Space Grotesk", sans-serif;
        letter-spacing: -0.02em;
    }

    .hero {
        padding: 24px 28px;
        border: 1px solid var(--border);
        background: linear-gradient(135deg, rgba(255,122,89,0.12), rgba(62,219,240,0.12));
        border-radius: 18px;
        margin-bottom: 16px;
        animation: fadeIn 0.7s ease;
    }

    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        animation: slideUp 0.6s ease;
    }

    .card-2 {
        background: var(--card-2);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px;
    }

    .pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(62,219,240,0.12);
        color: var(--accent-2);
        font-size: 12px;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .metric {
        font-family: "Space Grotesk", sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: var(--success);
    }

    .muted { color: var(--muted); }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Streamlit widget styling */
    .stTextArea textarea, .stTextInput input {
        background: #0f1426;
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    .stButton button {
        background: linear-gradient(135deg, var(--accent), #ffb24d);
        color: #1c120b;
        border-radius: 12px;
        border: none;
        padding: 10px 18px;
        font-weight: 600;
        font-family: "Space Grotesk", sans-serif;
        transition: transform 0.1s ease;
    }

    .stButton button:hover {
        transform: translateY(-1px);
    }

    .stTabs [data-baseweb="tab"] {
        background: #0f1426;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 10px 14px;
        color: var(--muted);
    }

    .stTabs [aria-selected="true"] {
        color: var(--text);
        border-color: var(--accent-2);
        background: rgba(62,219,240,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Workspace")
    st.markdown(
        """
        <div class="card-2">
            <div class="pill">Procurement</div>
            <div class="pill">PO Taxonomy</div>
            <div class="pill">LLM Ready</div>
            <div class="muted">Classify purchase order text into L1/L2/L3 categories.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### Example Inputs")
    example = st.selectbox(
        "Pick a quick example",
        [
            "Industrial valves for plant maintenance",
            "Annual software subscription for finance team",
            "Temporary staffing for warehouse operations",
            "Office chairs and standing desks",
        ],
    )
    use_example = st.button("Use Example")

left, right = st.columns([1.2, 1])

with left:
    st.markdown(
        """
        <div class="hero">
            <h1>PO L1-L2-L3 Classifier</h1>
            <div class="muted">Fast, structured categorization for purchase orders with clear, explainable output.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Input")
    if use_example:
        po_description = example
    else:
        po_description = ""
    po_description = st.text_area("PO Description", value=po_description, height=160)
    supplier = st.text_input("Supplier (optional)", placeholder="e.g., Acme Industrial Co.")
    classify_clicked = st.button("Classify")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Output")
    st.markdown(
        """
        <div class="muted">Results will appear here. Run a classification to populate.</div>
        """,
        unsafe_allow_html=True,
    )
    output_area = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

if classify_clicked:
    if not po_description.strip():
        st.warning("Please enter a PO Description")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)
        try:
            parsed = json.loads(result)
        except Exception:
            parsed = None

        with output_area.container():
            tabs = st.tabs(["Summary", "JSON", "Notes"])
            with tabs[0]:
                if parsed:
                    l1 = parsed.get("L1") or parsed.get("l1") or "Unknown"
                    l2 = parsed.get("L2") or parsed.get("l2") or "Unknown"
                    l3 = parsed.get("L3") or parsed.get("l3") or "Unknown"
                    st.markdown(
                        """
                        <div class="card-2">
                            <div class="muted">Top classification</div>
                            <div class="metric">L1: {}</div>
                            <div class="metric">L2: {}</div>
                            <div class="metric">L3: {}</div>
                        </div>
                        """.format(l1, l2, l3),
                        unsafe_allow_html=True,
                    )
                else:
                    st.error("Invalid model response")
                    st.text(result)
            with tabs[1]:
                if parsed:
                    st.json(parsed)
                else:
                    st.text(result)
            with tabs[2]:
                st.markdown(
                    """
                    <div class="card-2">
                        <div class="muted">Tips</div>
                        Provide clear product or service details, quantities, and scope for best accuracy.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
