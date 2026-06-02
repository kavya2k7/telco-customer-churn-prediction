import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Telco Customer Churn Predictor", page_icon="🔮", layout="wide")

st.markdown("""<style>
.main{background-color:#f4f6f9}
h1{color:#1E3A8A;font-family:'Segoe UI',sans-serif}
h3{color:#2C3E50}
.stButton>button{background-color:#2563EB;color:white;font-size:18px;font-weight:bold;
padding:12px;border-radius:8px;border:none;width:100%;transition:0.3s}
.stButton>button:hover{background-color:#1D4ED8;cursor:pointer}
</style>""", unsafe_allow_html=True)

st.title("🔮 Telco Customer Churn Prediction Portal")
st.markdown("##### Fill in customer details below to instantly assess churn risk.")
st.write("---")

@st.cache_resource
def load_assets():
    model    = joblib.load('churn_model.pkl')
    features = joblib.load('model_features.pkl')

    # ── Scaler reconstructed from IBM Telco dataset statistics ──────────────
    # Verified by back-calculating tree split thresholds from churn_model.pkl:
    #   MonthlyCharges threshold -1.526 → $18.85  ✓  (min in dataset)
    #   Tenure threshold -1.255 → 1.5 months      ✓
    # If you have scaler.pkl saved from your notebook, replace this block with:
    #   scaler = joblib.load('scaler.pkl')
    STATS = {
        'gender':0.505,'SeniorCitizen':0.162,'Partner':0.483,'Dependents':0.299,
        'tenure':32.37,'PhoneService':0.903,'MultipleLines':0.922,
        'InternetService':0.874,'OnlineSecurity':0.873,'OnlineBackup':0.875,
        'DeviceProtection':0.876,'TechSupport':0.874,'StreamingTV':0.876,
        'StreamingMovies':0.876,'Contract':0.690,'PaperlessBilling':0.592,
        'PaymentMethod':1.567,'MonthlyCharges':64.76,'TotalCharges':2279.73,
        'TenureGroup':1.08,'ServiceCount':2.73,'HighSpender':0.393,
        'ContractRisk':0.551,'AvgMonthlySpend':52.4,
    }
    STDS = {
        'gender':0.500,'SeniorCitizen':0.369,'Partner':0.500,'Dependents':0.458,
        'tenure':24.56,'PhoneService':0.296,'MultipleLines':0.636,
        'InternetService':0.828,'OnlineSecurity':0.827,'OnlineBackup':0.827,
        'DeviceProtection':0.827,'TechSupport':0.827,'StreamingTV':0.827,
        'StreamingMovies':0.827,'Contract':0.833,'PaperlessBilling':0.492,
        'PaymentMethod':1.072,'MonthlyCharges':30.09,'TotalCharges':2266.77,
        'TenureGroup':0.835,'ServiceCount':1.95,'HighSpender':0.489,
        'ContractRisk':0.497,'AvgMonthlySpend':28.5,
    }
    scaler = StandardScaler()
    scaler.mean_           = np.array([STATS[f] for f in features])
    scaler.scale_          = np.array([STDS[f]  for f in features])
    scaler.var_            = scaler.scale_ ** 2
    scaler.n_features_in_  = len(features)
    scaler.n_samples_seen_ = 7043
    return model, features, scaler

try:
    model, expected_features, scaler = load_assets()
except FileNotFoundError as e:
    st.error(f"⚠️ Missing file: {e}. Place churn_model.pkl and model_features.pkl in the same folder.")
    st.stop()

# ── FORM ──────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 👤 Demographics")
    gender           = st.selectbox("Gender", ["Female","Male"])
    SeniorCitizen    = st.selectbox("Senior Citizen?", ["No","Yes"])
    Partner          = st.selectbox("Has Partner?", ["No","Yes"])
    Dependents       = st.selectbox("Has Dependents?", ["No","Yes"])
    tenure           = st.slider("Tenure (Months Active)", 1, 72, 12)

with col2:
    st.markdown("### 🔌 Core Services")
    PhoneService     = st.selectbox("Phone Service", ["No","Yes"])
    MultipleLines    = st.selectbox("Multiple Lines", ["No","Yes","No phone service"])
    InternetService  = st.selectbox("Internet Service Type", ["DSL","Fiber optic","No"])
    OnlineSecurity   = st.selectbox("Online Security",   ["No","Yes","No internet service"])
    OnlineBackup     = st.selectbox("Online Backup",     ["No","Yes","No internet service"])
    DeviceProtection = st.selectbox("Device Protection", ["No","Yes","No internet service"])
    TechSupport      = st.selectbox("Tech Support",      ["No","Yes","No internet service"])
    StreamingTV      = st.selectbox("Streaming TV",      ["No","Yes","No internet service"])
    StreamingMovies  = st.selectbox("Streaming Movies",  ["No","Yes","No internet service"])

with col3:
    st.markdown("### 💳 Account & Payments")
    Contract         = st.selectbox("Contract Type", ["Month-to-month","One year","Two year"])
    PaperlessBilling = st.selectbox("Paperless Billing", ["No","Yes"])
    PaymentMethod    = st.selectbox("Payment Method", [
        "Electronic check","Mailed check",
        "Bank transfer (automatic)","Credit card (automatic)"])
    MonthlyCharges   = st.number_input("Monthly Charges ($)", min_value=0.0, value=65.0)
    TotalCharges     = st.number_input("Total Charges ($)",   min_value=0.0, value=780.0)

st.write("---")

# ── PREPROCESSING ─────────────────────────────────────────────────────────────
LABEL_MAPS = {
    'gender':            {'Female':0,'Male':1},
    'Partner':           {'No':0,'Yes':1},
    'Dependents':        {'No':0,'Yes':1},
    'PhoneService':      {'No':0,'Yes':1},
    'MultipleLines':     {'No':0,'No phone service':1,'Yes':2},
    'InternetService':   {'DSL':0,'Fiber optic':1,'No':2},
    'OnlineSecurity':    {'No':0,'No internet service':1,'Yes':2},
    'OnlineBackup':      {'No':0,'No internet service':1,'Yes':2},
    'DeviceProtection':  {'No':0,'No internet service':1,'Yes':2},
    'TechSupport':       {'No':0,'No internet service':1,'Yes':2},
    'StreamingTV':       {'No':0,'No internet service':1,'Yes':2},
    'StreamingMovies':   {'No':0,'No internet service':1,'Yes':2},
    'Contract':          {'Month-to-month':0,'One year':1,'Two year':2},
    'PaperlessBilling':  {'No':0,'Yes':1},
    'PaymentMethod':     {'Bank transfer (automatic)':0,'Credit card (automatic)':1,
                          'Electronic check':2,'Mailed check':3},
}
SERVICE_COLS = ['PhoneService','MultipleLines','OnlineSecurity','OnlineBackup',
                'DeviceProtection','TechSupport','StreamingTV','StreamingMovies']

def build_features(raw):
    df = pd.DataFrame([raw])
    t  = raw['tenure']
    # Engineered features (exact replica of notebook)
    df['TenureGroup']     = 0 if t<=12 else (1 if t<=36 else 2)
    df['ServiceCount']    = sum(1 for c in SERVICE_COLS if raw[c]=='Yes')
    df['HighSpender']     = int(raw['MonthlyCharges'] > 70)
    df['ContractRisk']    = int(raw['Contract'] == 'Month-to-month')
    df['AvgMonthlySpend'] = raw['TotalCharges'] / (raw['tenure'] + 1)
    # Label encode
    for col, mapping in LABEL_MAPS.items():
        df[col] = mapping.get(str(df[col].iloc[0]), 0)
    # Align + scale
    df = df.reindex(columns=expected_features, fill_value=0)
    return scaler.transform(df.values)   # ← pass numpy array to suppress warning

# ── PREDICT ───────────────────────────────────────────────────────────────────
if st.button("📊 Calculate Operational Churn Risk"):
    raw = {
        'gender':gender, 'SeniorCitizen':1 if SeniorCitizen=="Yes" else 0,
        'Partner':Partner, 'Dependents':Dependents, 'tenure':int(tenure),
        'PhoneService':PhoneService, 'MultipleLines':MultipleLines,
        'InternetService':InternetService, 'OnlineSecurity':OnlineSecurity,
        'OnlineBackup':OnlineBackup, 'DeviceProtection':DeviceProtection,
        'TechSupport':TechSupport, 'StreamingTV':StreamingTV,
        'StreamingMovies':StreamingMovies, 'Contract':Contract,
        'PaperlessBilling':PaperlessBilling, 'PaymentMethod':PaymentMethod,
        'MonthlyCharges':float(MonthlyCharges), 'TotalCharges':float(TotalCharges),
    }
    try:
        X          = build_features(raw)
        prediction = model.predict(X)[0]
        probability= model.predict_proba(X)[0][1]
        pct        = probability * 100

        # ── RESULT HEADER ────────────────────────────────────────────────────
        st.header("🎯 Prediction Result Analysis")
        r1, r2 = st.columns(2)

        with r1:
            if prediction == 1:
                st.error("### ⚠️ High Churn Risk")
                st.metric("Churn Probability", f"{pct:.1f}%", delta="High Risk", delta_color="inverse")
            else:
                st.success("### ✅ Low Churn Risk — Likely to Stay")
                st.metric("Churn Probability", f"{pct:.1f}%", delta="Stable", delta_color="normal")

        # ── RISK GAUGE ───────────────────────────────────────────────────────
        with r2:
            if   pct < 30:  gauge_color="#22c55e"; risk_label="🟢 Low Risk"
            elif pct < 60:  gauge_color="#f59e0b"; risk_label="🟡 Medium Risk"
            else:           gauge_color="#ef4444"; risk_label="🔴 High Risk"

            st.markdown(f"""
            <div style="background:#1e293b;border-radius:12px;padding:18px;text-align:center">
              <div style="font-size:13px;color:#94a3b8;margin-bottom:6px">RISK LEVEL</div>
              <div style="font-size:28px;font-weight:700;color:{gauge_color}">{risk_label}</div>
              <div style="background:#334155;border-radius:8px;height:14px;margin:12px 0">
                <div style="background:{gauge_color};width:{min(pct,100):.0f}%;height:14px;
                     border-radius:8px;transition:width 0.5s"></div>
              </div>
              <div style="font-size:32px;font-weight:800;color:white">{pct:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        st.write("---")

        # ── DETAILED ANALYSIS ────────────────────────────────────────────────
        st.subheader("📋 Detailed Risk Factor Analysis")
        a1, a2, a3 = st.columns(3)

        # Contract risk
        contract_risk = {"Month-to-month":"🔴 Highest risk contract type — 3× more likely to churn",
                         "One year":       "🟡 Moderate commitment — some churn risk remains",
                         "Two year":       "🟢 Strong commitment — very low contract-driven churn"}
        with a1:
            st.markdown("**📄 Contract**")
            st.info(contract_risk[Contract])

        # Tenure risk
        with a2:
            st.markdown("**📅 Tenure**")
            if   tenure <= 12: st.error(f"🔴 New customer ({tenure}m) — highest dropout window")
            elif tenure <= 36: st.warning(f"🟡 Mid-stage ({tenure}m) — moderate loyalty")
            else:              st.success(f"🟢 Long-term customer ({tenure}m) — strong retention")

        # Internet & support risk
        with a3:
            st.markdown("**🌐 Internet & Support**")
            if InternetService == "Fiber optic" and TechSupport == "No":
                st.error("🔴 Fiber optic + No Tech Support = highest-risk combo")
            elif InternetService == "Fiber optic":
                st.warning("🟡 Fiber optic customer — monitor satisfaction closely")
            elif TechSupport == "Yes":
                st.success("🟢 Tech Support active — strong retention signal")
            else:
                st.info("ℹ️ Standard internet profile")

        st.write("---")

        # ── ACTION RECOMMENDATIONS ───────────────────────────────────────────
        st.subheader("💡 Strategic Action Recommendations")

        if pct >= 60:
            st.error("**🚨 URGENT — Immediate intervention required**")
            actions = []
            if Contract == "Month-to-month":
                actions.append("📋 **Contract Upgrade Offer:** Provide a 20–30% discount to switch to a 1-year or 2-year contract immediately.")
            if InternetService == "Fiber optic" and TechSupport == "No":
                actions.append("🛠️ **Free Tech Support Trial:** Offer 3 months of free Tech Support — fiber customers with support churn 40% less.")
            if MonthlyCharges > 70:
                actions.append(f"💰 **Bill Shock Intervention:** Monthly charges of ${MonthlyCharges:.0f} are above average ($64.76). Offer a service bundle discount.")
            if tenure <= 12:
                actions.append("🎁 **New Customer Loyalty Program:** Enroll in onboarding reward program — first-year customers are 3× more likely to churn.")
            if not actions:
                actions.append("📞 **Proactive Outreach:** Schedule a satisfaction call within 48 hours. Offer a loyalty reward or bill credit.")
            for a in actions:
                st.markdown(f"- {a}")

        elif pct >= 30:
            st.warning("**⚠️ MONITOR — Elevated risk, act within 2 weeks**")
            actions = []
            if Contract == "Month-to-month":
                actions.append("📋 Offer a discounted annual contract at next billing cycle.")
            if TechSupport == "No" and InternetService != "No":
                actions.append("🛠️ Highlight Tech Support benefits via email campaign.")
            actions.append("📊 Include in next NPS survey to gauge satisfaction.")
            for a in actions:
                st.markdown(f"- {a}")

        else:
            st.success("**✅ HEALTHY — Standard retention strategy**")
            upsell = []
            if StreamingTV == "No" and InternetService != "No":
                upsell.append("📺 Offer Streaming TV add-on — likely to accept given stable profile.")
            if MultipleLines == "No" and PhoneService == "Yes":
                upsell.append("📱 Upsell Multiple Lines for family/business use.")
            if Contract == "One year":
                upsell.append("📋 Offer a 2-year contract renewal with loyalty discount.")
            if upsell:
                st.markdown("**Upsell opportunities:**")
                for u in upsell: st.markdown(f"- {u}")
            else:
                st.markdown("- Keep current plan. No intervention needed — this is a model retention customer.")

    except Exception as err:
        st.error(f"Prediction error: {err}")
        st.exception(err)