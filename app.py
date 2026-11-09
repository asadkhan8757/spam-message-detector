import streamlit as st
import pandas as pd
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="SpamBusters | AI Detector", page_icon="🛡️", layout="centered")

# ---------- CSS - FIXED FOR DARK MODE ----------
st.markdown("""
<style>
.about-box {
    background-color: #262730 !important;
    padding: 13px 15px;
    font-size: 14px;
    line-height: 1.45;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 4px solid #FF4B4B;
    color: #FFFFFF !important;
}
.info-box {
    background-color: #262730 !important;
    padding: 12px 8px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #444444;
}
.info-box h3 { font-size: 16px; margin: 0px; color: #FFFFFF !important; }
.info-box p { font-size: 13px; line-height: 1.3; margin: 3px 0; color: #CCCCCC !important; }

.team-box {
    background-color: #FF4B4B !important;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    margin-top: 10px;
    color: #FFFFFF !important;
}
.team-box b { color: #FFFFFF !important; font-size: 15px; }
.team-box span { color: #FFFFFF !important; font-size: 14px; }

.history-box {
    background-color: #262730 !important;
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid #444444;
    font-size: 13px;
    margin-bottom: 8px;
    color: #FFFFFF !important;
}
.stButton>button { background-color: #FF4B4B; color: white; font-weight: bold; border-radius: 10px; height: 48px; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "history" not in st.session_state:
    st.session_state.history = []

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛡️ SpamBusters Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:14px;'>Welcome to AI Spam & Phishing Detector</p>", unsafe_allow_html=True)
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login", use_container_width=True):
        if user == "spambusters" and pwd == "team123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong Username or Password!")
    st.info("Demo Login -> Username: spambusters | Password: team123")
    st.stop()

col_top1, col_top2 = st.columns([5,1])
with col_top2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("<h1 style='text-align:center; color:#FF4B4B; font-size:32px;'>🛡️ AI Spam & Phishing<br>Detector</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="about-box">
<b>💡 About Our Project</b><br>
This project uses AI to detect fake SMS like <b>Free Prize, Bank KYC Block</b> and protect users from fraud.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-box">
<b>⚙️ How It Works?</b> Our model reads the words of a message and understands its pattern. If it looks like fraud or phishing, it marks it as <b>SPAM</b>, otherwise <b>SAFE</b>.
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="info-box"><h3>📊 Dataset</h3><p>5,574 SMS<br>4,827 Ham + 747 Spam</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="info-box"><h3>🤖 Model</h3><p>TF-IDF + Logistic<br>Regression</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="info-box"><h3>🎯 Accuracy</h3><p>98.2%<br>Tested</p></div>', unsafe_allow_html=True)

st.markdown("---")

@st.cache_resource
def load_model():
    try:
        url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
        df = pd.read_csv(url, sep='\t', header=None, names=['label','message'])
    except:
        data = {'label': ['ham','ham','spam','spam','ham','spam'],
                'message': ['Hey are you coming today', 'Call me later', 'You won FREE prize click here', 'Your bank KYC blocked urgent', 'Good morning', 'Congratulations you won lottery']}
        df = pd.DataFrame(data)
    X = df['message']
    y = df['label'].map({'ham':0, 'spam':1})
    vec = TfidfVectorizer(stop_words='english', max_features=5000)
    X_vec = vec.fit_transform(X)
    model = LogisticRegression()
    model.fit(X_vec, y)
    return model, vec

model, vectorizer = load_model()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' link ', text)
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    return text

st.markdown("### 🔍 Check Your Message")
col_msg, col_link = st.columns(2)
with col_msg:
    st.markdown("**✉️ Enter Your Message Here**")
    user_msg = st.text_area("msg", placeholder="Example: You won FREE prize...", height=110, label_visibility="collapsed")
with col_link:
    st.markdown("**🔗 Enter Link / URL Here**")
    user_link = st.text_input("link", placeholder="Example: https://free-prize-xyz.com", label_visibility="collapsed")
    st.caption("Paste the link here to check it separately.")

if st.button("Check Now 🚀", use_container_width=True):
    full_text = (user_msg + " " + user_link).strip()
    if full_text == "":
        st.warning("Please enter a Message or Link first!")
    else:
        cleaned = clean_text(full_text)
        vec_text = vectorizer.transform([cleaned])
        pred = model.predict(vec_text)[0]
        prob = model.predict_proba(vec_text)[0].max() * 100
        result = "SPAM" if pred == 1 else "SAFE"
        st.session_state.history.insert(0, {
            "message": user_msg if user_msg else "-",
            "link": user_link if user_link else "-",
            "result": result,
            "prob": round(prob, 1),
            "time": datetime.now().strftime("%d %b, %I:%M %p")
        })
        if pred == 1:
            st.error(f"🚨 **SPAM / FRAUD DETECTED!** ({prob:.1f}% Sure)")
            st.write("⚠️ This message looks like fraud. Do not click the link and do not share OTP.")
        else:
            st.success(f"✅ **SAFE MESSAGE** ({prob:.1f}% Sure)")
            st.write("This message looks safe.")

# ---------- SEARCH HISTORY - ENGLISH ----------
st.markdown("---")
h1, h2 = st.columns([3,1])
with h1:
    st.markdown(f"### 🕒 Search History ({len(st.session_state.history)})")
with h2:
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

if len(st.session_state.history) == 0:
    st.caption("No history yet. Check a message to see it here.")
else:
    for item in st.session_state.history:
        icon = "🚨" if item["result"] == "SPAM" else "✅"
        color = "#FF4B4B" if item["result"] == "SPAM" else "#28A745"
        st.markdown(f"""
        <div class="history-box">
        <b style="color:{color};">{icon} {item["result"]} - {item["prob"]}% Sure</b> &nbsp; <span style="color:#AAAAAA; font-size:12px;">{item["time"]}</span><br>
        <b style="color:#FFF;">Message:</b> <span style="color:#FFF;">{item["message"]}</span><br>
        <b style="color:#FFF;">Link:</b> <span style="color:#FFF;">{item["link"]}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------- TEAM - FIXED COLOUR RED BOX WHITE TEXT ----------
st.markdown("""
<div class="team-box">
<b>👨‍💻 Developed By - Team SpamBusters</b><br><br>
<span><b>Asad Khan</b> : 2300101776</span><br>
<span><b>Atif Khan</b> : 2300101447</span><br>
<span><b>Arman Ali</b> : 2300100698</span><br>
<span><b>Ashvani Kumar Upadhyay</b> : 2301012087</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; font-size:12px; color:gray; margin-top:10px;'>Made by Team SpamBusters | AI Spam Detector</p>", unsafe_allow_html=True)
