import streamlit as st
import pickle
import re
from datetime import datetime

st.set_page_config(page_title="SpamBusters | AI Detector", page_icon="🛡️")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
* { font-family: 'Poppins', sans-serif !important; }
h1 { font-size: 46px !important; font-weight: 800 !important; line-height: 1.2 !important; background: linear-gradient(90deg, #D31027 0%, #EA384D 50%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center !important; }
.stTextArea textarea { border-radius: 15px !important; border: 2px solid #e0e0e0 !important; font-size: 16px !important; }
.stButton>button { border-radius: 12px !important; font-weight: 700 !important; background: linear-gradient(90deg, #D31027, #EA384D) !important; color: white !important; border: none !important; padding: 10px 25px !important; }
.team-card { background: #1E1E1E; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #333; margin-top: 20px; }
.about-box { background: #FFF3CD; padding: 18px; border-radius: 12px; color: #333; border-left: 5px solid #D31027; }
.info-box { background: #FFFFFF; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #e0e0e0; box-shadow: 0px 2px 8px rgba(0,0,0,0.08); }
.info-box h3 { color: #D31027; margin: 0; font-size: 18px; }
.info-box p { color: #555; margin: 5px 0 0 0; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "history" not in st.session_state:
    st.session_state.history = []

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🔐 Team SpamBusters Login</h2>", unsafe_allow_html=True)
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "spambusters" and pwd == "team123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Username / Password")
    st.stop()

model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.title("🛡️ AI Spam & Phishing Detector")

# --- NEW ABOUT + DEFINITION ---
st.markdown("""
<div class="about-box">
<b>💡 About Our Project</b><br>
<b>Protecting Users from Digital Fraud.</b> Every day, millions of people receive fake messages like Free Prize, Bank KYC Block, and Lottery Winner scams. Our project uses Artificial Intelligence to detect and block these fraud messages before users become victims.
<br><br>
<b>How It Works?</b> Our model reads the words of a message and understands its pattern. If the message looks like a fraud or phishing attempt, it marks it as <b>SPAM</b>, otherwise <b>SAFE</b>.
</div>
""", unsafe_allow_html=True)

st.write("")

# --- NEW DATASET IN 3 SEPARATE BOXES ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="info-box"><h3>📊 Dataset</h3><p><b>5,574 SMS</b><br>SMS Spam Collection<br>4,827 Ham + 747 Spam</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="info-box"><h3>🤖 Model</h3><p><b>TF-IDF + Logistic<br>Regression</b><br>Text Classification<br>Machine Learning</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="info-box"><h3>🎯 Accuracy</h3><p><b>98.2%</b><br>Tested on<br>Real Messages</p></div>""", unsafe_allow_html=True)

st.write("")
msg = st.text_area("Enter Your Message Here:")
if st.button("Check Message"):
    if msg == "":
        st.warning("Please enter a message first!")
    else:
        clean_msg = re.sub(r'[^a-zA-Z ]', '', msg.lower())
        vec = vectorizer.transform([clean_msg])
        pred = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0].max() * 100
        result = "SPAM 🚨" if pred == 1 else "SAFE ✅"
        st.session_state.history.insert(0, {"msg": msg, "result": result, "prob": f"{prob:.1f}%", "time": datetime.now().strftime("%I:%M %p")})
        if pred == 1:
            st.error(f"🚨 SPAM DETECTED! ({prob:.1f}% Confidence)")
        else:
            st.success(f"✅ SAFE MESSAGE! ({prob:.1f}% Confidence)")
        st.progress(int(prob))

if st.session_state.history:
    st.markdown("### 🕒 Recent Search History")
    for h in st.session_state.history[:5]:
        color = "🔴" if "SPAM" in h["result"] else "🟢"
        st.markdown(f"{color} **{h['result']}** ({h['prob']}) - {h['time']}  \n> {h['msg'][:80]}...")
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

st.markdown("""
<div class="team-card">
<h3 style='color:white; margin:0;'>👨‍💻 Team SpamBusters</h3>
<p style='color:#FF6B6B; font-weight:600;'>Minor Project | SMS Spam Detection</p>
<p style='color:white;'>
<b>Asad Khan</b> (2300101776) &nbsp; | &nbsp; <b>Arman Ali</b> (2300100698)<br>
<b>Atif Khan</b> (2300101447) &nbsp; | &nbsp; <b>Ashvani Kumar Upadhyay</b> (2301012087)
</p>
<p style='color:#888; font-size:12px;'>Dataset: SMS Spam Collection | Model: TF-IDF + Logistic Regression</p>
</div>
""", unsafe_allow_html=True)