import streamlit as st
import requests

# =========================================
# PAGE SETTINGS
# =========================================

st.set_page_config(
    page_title="AI Feedback Analyzer",
    page_icon="🤖",
    layout="centered"
)

# =========================================
# LOGO
# =========================================

# Put logo.png in same folder as feedback.py


# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.main {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
}

h1 {
    color: white;
    text-align: center;
    font-size: 45px;
}

p {
    color: #cbd5e1;
    font-size: 18px;
}

.stTextArea textarea {
    background-color: #1e293b;
    color: white;
    border-radius: 15px;
    border: 2px solid #3b82f6;
    padding: 15px;
    font-size: 16px;
}

.stButton button {
    width: 100%;
    height: 55px;
    background: linear-gradient(to right, #2563eb, #3b82f6);
    color: white;
    border-radius: 12px;
    border: none;
    font-size: 20px;
    font-weight: bold;
}

.stButton button:hover {
    background: #2563eb;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================

st.title("🤖 AI Customer Feedback Analyzer")

st.write(
    "Analyze customer reviews using Azure AI Language Service"
)

# =========================================
# AZURE SETTINGS
# =========================================

API_KEY = "F73ZeoPetLJTLV1DVbmkosCQ1gB7FuW3JqsTCoblLGFusQXWQ1gWJQQJ99CEAC3pKaRXJ3w3AAAaACOGhk6m"

ENDPOINT = "https://language010.cognitiveservices.azure.com/"

# =========================================
# FUNCTION
# =========================================

def analyze_review(text):

    url = ENDPOINT + "/language/:analyze-text?api-version=2023-04-01"

    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "kind": "SentimentAnalysis",
        "analysisInput": {
            "documents": [
                {
                    "id": "1",
                    "language": "en",
                    "text": text
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    return response.json()

# =========================================
# INPUT BOX
# =========================================

review = st.text_area(
    "Enter Customer Feedback",
    height=220,
    placeholder="Type customer feedback here..."
)

# =========================================
# BUTTON
# =========================================

if st.button("Analyze Feedback"):

    if review.strip() == "":

        st.warning("Please enter feedback.")

    else:

        result = analyze_review(review)

        try:

            document = result["results"]["documents"][0]

            sentiment = document["sentiment"]

            scores = document["confidenceScores"]

            # =========================================
            # SHOW SENTIMENT
            # =========================================

            if sentiment == "positive":

                st.success(f"😊 Sentiment: {sentiment.upper()}")

            elif sentiment == "negative":

                st.error(f"😡 Sentiment: {sentiment.upper()}")

            else:

                st.info(f"😐 Sentiment: {sentiment.upper()}")

            # =========================================
            # CONFIDENCE SCORES
            # =========================================

            st.subheader("Confidence Scores")

            st.write(f"🟢 Positive: {scores['positive']*100:.2f}%")
            st.progress(int(scores['positive'] * 100))

            st.write(f"🟡 Neutral: {scores['neutral']*100:.2f}%")
            st.progress(int(scores['neutral'] * 100))

            st.write(f"🔴 Negative: {scores['negative']*100:.2f}%")
            st.progress(int(scores['negative'] * 100))

        except Exception as e:

            st.error("Error connecting to Azure.")

            st.write(result)

            st.write(e)