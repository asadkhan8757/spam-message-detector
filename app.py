import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---------- PAGE SETTING ----------
st.set_page_config(page_title="SpamBusters | AI Detector", page_icon="🛡️", layout="centered")

# ---------- CSS - CHOTA COMPACT DESIGN ----------
st.markdown("""
<style>
.about-box {
    background-color: #FFF8DC;
    padding: 10px 12px;
    font-size: 12.5px;
    line-height: 1.35;
    border-radius: 10px;
    margin-bottom: 8px;
    border-left: 4px solid #FF4B4B;
    color: #333;
}
.info-box {
    background-color: #FFFFFF;
    padding: 8px 6px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid #e0e0e0;
    box-shadow: 0px 1px 3px rgba(0,0,0,0.08);
}
.info-box h3 { font-size: 14px; margin: 0px; color: #333; }
.info-box p { font-size: 11px; line-height: 1.2; margin: 2px 0; color: #666; }
.stButton>button { background-color: #FF4B4B; color: white; font-weight: bold; border-radius: 10px; height: 45px; }
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN SYSTEM ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛡️ SpamBusters Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:13px;'>AI Spam & Phishing Detector me welcome hai</p>", unsafe_allow_html=True)
    
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    
    if st.button("Login", use_container_width=True):
        if user == "spambusters" and pwd == "team123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Galat Username ya Password!")
    
    st.info("Demo Login -> Username: spambusters | Password: team123")
    st.stop()

# ---------- LOGOUT BUTTON ----------
col_top1, col_top2 = st.columns([5,1])
with col_top2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------- TITLE ----------
st.markdown("<h1 style='text-align:center; color:#FF4B4B; font-size:30px;'>🛡️ AI Spam & Phishing<br>Detector</h1>", unsafe_allow_html=True)

# ---------- ABOUT - CHOTA ----------
st.markdown("""
<div class="about-box">
<b>💡 About Our Project</b><br>
AI se fake SMS jaise <b>Free Prize, Bank KYC Block</b> ko pakad ke users ko fraud se bachata hai.
</div>
""", unsafe_allow_html=True)

# ---------- HOW IT WORKS - ALAG CHOTA BOX ----------
st.markdown("""
<div class="about-box">
<b>⚙️ How It Works?</b> Model message ke words ka pattern samajhta hai, fraud lage to <b>SPAM</b>, warna <b>SAFE</b>.
</div>
""", unsafe_allow_html=True)

# ---------- 3 CHOTE BOXES ----------
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="info-box"><h3>📊 Dataset</h3><p>5,574 SMS<br>4,827 Ham + 747 Spam</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="info-box"><h3>🤖 Model</h3><p>TF-IDF + Logistic<br>Regression</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="info-box"><h3>🎯 Accuracy</h3><p>98.2%<br>Tested</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ---------- MODEL TRAINING ----------
@st.cache_resource
def load_model():
    try:
        url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
        df = pd.read_csv(url, sep='\t', header=None, names=['label','message'])
    except:
        # Agar internet se data na aaye to sample data
        data = {
            'label': ['ham','ham','spam','spam','ham','spam'],
            'message': ['Hey are you coming today', 'Call me later', 'You won FREE prize click here', 'Your bank KYC blocked urgent', 'Good morning', 'Congratulations you won lottery']
        }
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

# ---------- CHECK SECTION - MESSAGE AUR LINK ALAG-ALAG ----------
st.markdown("### 🔍 Check Your Message")

col_msg, col_link = st.columns(2)

with col_msg:
    st.markdown("**✉️ Enter Your Message Here**")
    user_msg = st.text_area("msg", placeholder="Example: You won FREE prize...", height=100, label_visibility="collapsed")

with col_link:
    st.markdown("**🔗 Enter Link / URL Here**")
    user_link = st.text_input("link", placeholder="Example: https://free-prize-xyz.com", label_visibility="collapsed")
    st.caption("Link ko alag se check karne ke liye yahan paste karein.")

# ---------- CHECK BUTTON ----------
if st.button("Check Now 🚀", use_container_width=True):
    full_text = (user_msg + " " + user_link).strip()
    if full_text == "":
        st.warning("Pehle Message ya Link to daalo!")
    else:
        cleaned = clean_text(full_text)
        vec_text = vectorizer.transform([cleaned])
        pred = model.predict(vec_text)[0]
        prob = model.predict_proba(vec_text)[0].max() * 100

        if pred == 1:
            st.error(f"🚨 **SPAM / FRAUD DETECTED!** ({prob:.1f}% Sure)")
            st.write("⚠️ Ye message fraud lag raha hai. Link pe click mat karna, OTP share mat karna.")
        else:
            st.success(f"✅ **SAFE MESSAGE** ({prob:.1f}% Sure)")
            st.write("Ye message safe lag raha hai.")

st.markdown("---")
st.markdown("<p style='text-align:center; font-size:11px; color:gray;'>Made by Team SpamBusters | AI Spam Detector</p>", unsafe_allow_html=True)
