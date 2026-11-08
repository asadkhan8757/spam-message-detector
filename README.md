# 🛡️ AI Spam & Phishing Detector - Team SpamBusters

> **Protecting Users from Digital Fraud.**

An AI-powered web application that detects whether an SMS message is **SPAM** or **SAFE** in just 1 second. Built as a Minor Project using Machine Learning.

### 🔴 Live Demo
**Live App Link:** `https://your-app-link.streamlit.app` *(Update after deployment)*

---

## 💡 About Our Project

Every day, millions of people receive fake messages like **Free Prize, Bank KYC Block, and Lottery Winner** scams. Our project uses Artificial Intelligence to detect and block these fraud messages before users become victims.

**How It Works?** Our model reads the words of a message and understands its pattern. If the message looks like a fraud or phishing attempt, it marks it as **SPAM**, otherwise **SAFE**.

---

## ✨ Features

- 🔐 Secure Team Login System
- 🤖 Real-time Spam Detection with Confidence Score
- 🕒 Recent Search History
- 📊 Dataset & Model Details in Separate Cards
- 🎨 Modern UI with Red Gradient Theme
- 📱 Mobile Friendly Design

## 📊 Dataset

| Detail | Value |
| :--- | :--- |
| **Dataset Name** | SMS Spam Collection |
| **Total Messages** | 5,574 SMS |
| **Ham (Safe)** | 4,827 |
| **Spam** | 747 |

## 🤖 Model Details

- **Vectorizer:** TF-IDF (Term Frequency - Inverse Document Frequency)
- **Algorithm:** Logistic Regression
- **Accuracy:** 98.2%
- **Library:** Scikit-Learn

## 🛠️ Tech Stack

- **Frontend:** Streamlit, HTML, CSS
- **Backend:** Python
- **ML:** Scikit-Learn, Pandas, NumPy
- **Deployment:** Streamlit Cloud

## 🚀 How to Run Locally

```bash
# 1. Install Requirements
pip install -r requirements.txt

# 2. Run the App
python -m streamlit run app.py
