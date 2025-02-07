import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import google.generativeai as genai


faq_questions = [
    "Give the eligibility criteria for ITR 1",
                "Give the eligibility criteria for ITR 2",
                "Give the eligibility criteria for ITR 3",
                "Give the eligibility criteria for ITR 4",
                "Give the eligibility criteria for ITR 5",
                "Give the eligibility criteria for ITR 6",
                "Give the eligibility criteria for ITR 7",
                "What are the tax-saving options under Section 80C?",
                "Who needs to file ITR?"
]


genai.configure(api_key="API_KEY")

def translate_text(text, target_lang):
    translator = Translator()
    return translator.translate(text, dest=target_lang).text

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "Could not generate a response."

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            return query
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Could not request results, please check your connection."

def main():
    st.set_page_config(page_title="Tax Assistant Chatbot", layout="wide")
    st.title("Tax Assistant Chatbot")
    st.write("Get ITR recommendations and tax-saving investment suggestions.")
    
    with st.sidebar:
        st.header("Enter Your Income Details")
        language = st.selectbox("Select Language", ["English", "Hindi", "Spanish", "French"])
        salary = st.number_input("Salary/Pension Income (₹)", min_value=0, step=1000)
        rental = st.number_input("Rental Income (₹)", min_value=0, step=1000)
        business = st.number_input("Business/Professional Income (₹)", min_value=0, step=1000)
        presumptive = st.number_input("Presumptive Income (₹)", min_value=0, step=1000)
        capital = st.number_input("Capital Gains (₹)", min_value=0, step=1000)
        foreign = st.number_input("Foreign Income (₹)", min_value=0, step=1000)
        crypto = st.number_input("Crypto Income (₹)", min_value=0, step=1000)
        directorship = st.radio("Are you a director in a company?", ["Yes", "No"])
        equity_shares = st.radio("Do you hold unlisted equity shares?", ["Yes", "No"])
        entity_type = st.selectbox("Select Entity Type", ["Individual", "Firm", "Company"])
        section_11_exemption = st.radio("Section 11 Exemption (for Trusts)?", ["Yes", "No"])
        special_filing = st.radio("Special Filing (Sec 139(4A), 139(4B), etc.)?", ["Yes", "No"])
        
        if st.button("Get ITR Recommendation and Tax-Saving Tips"):
            user_input = (
                f"Determine the correct ITR form based on: Salary={salary}, Rental={rental}, Business={business}, "
                f"Presumptive={presumptive}, Capital Gains={capital}, Foreign={foreign}, Crypto={crypto}, "
                f"Directorship={directorship}, Equity Shares={equity_shares}, Entity Type={entity_type}, "
                f"Section 11 Exemption={section_11_exemption}, Special Filing={special_filing}. "
                f"Suggest tax-saving investments under 80C, 80D, and 80E, including PPF, ELSS, NPS, insurance, and home loan benefits. "
                f"Ensure recommendations are precise and relevant."
            )
            response = get_gemini_response(user_input)
            st.session_state.response = response
    
    st.subheader("AI Recommendation")
    st.write(st.session_state.get("response", "Enter details in the sidebar to get recommendations."))
    
    st.subheader("Ask Your Queries")
    selected_question = st.selectbox("Select a common query:", ["Select a question"] + faq_questions)
    query_text = st.text_input("Type your question here:", value=selected_question if selected_question != "Select a question" else "")
    # query_text = st.text_input("Type your question here:")
    # query_text = st.text_input("Type your question here:")
    if st.button("Ask via Text"):
        if query_text:
            query_response = get_gemini_response(query_text)
            st.write("### Answer:")
            st.write(query_response)
    
    if st.button("Ask via Voice"):
        voice_query = recognize_speech()
        if voice_query:
            st.write(f"### You asked: {voice_query}")
            voice_response = get_gemini_response(voice_query)
            st.write("### Answer:")
            st.write(voice_response)

if __name__ == "__main__":
    main()
