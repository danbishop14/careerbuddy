import streamlit as st
from streamlit_chat import message
from hugchat import hugchat

# Setting the Streamlit page configuration
st.set_page_config(page_title="Career Buddy", page_icon=":robot:")
st.markdown("<h1 style='text-align: center; color: black;'>Career Buddy</h1>", unsafe_allow_html=True)
st.markdown("Powered by [HuggingFace](https://github.com/huggingface) and [Streamlit](https://streamlit.com).")


st.write("---")
st.markdown("<h3 style='text-align: left; color: black;'>Enter your details:</h3>", unsafe_allow_html=True)

# Displaying the options for job title, industry, years of experience, accomplishments, and skills and technologies
col1, col2 = st.columns(2)
with col1:
    job_title = st.text_input('Job Title:', 'Software Engineer')
    current_job = st.checkbox('Is this your current job?')
    industry = st.selectbox(
        'Industry:',
        ('Finance', 'Healthcare', 'Technology', 'Marketing', 'Education', 'Retail', 'Manufacturing', 'Other'))

with col2:
    skills_technologies = st.text_area('Skills and Technologies:', 'Python, Java, Excel, Communication, Time Management, Problem Solving')
    years_experience = st.slider('Years of Experience:', 0, 10, 2)

st.markdown("---")
st.markdown("<h3 style='text-align: left; color: black;'>Start Chatting</h3>", unsafe_allow_html=True)

# Initialize session state if not already
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hi I'm JobBuddy, your personal AI-powered career coach. How may I help you?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
response_container = st.container()

# Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("Enter your message: ", "", key="input")
    return input_text

# Applying the user input box
with input_container:
    user_input = get_text()

# Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt, job_title, current_job, industry, skills_technologies, years_experience):
    chatbot = hugchat.ChatBot()

    # Contextualize the prompt with user's information.
    contextualized_prompt = (f"""As an AI-powered professional development coach, you assist users in their job search and resume enhancement. Users will interact by asking questions regarding their skills, job search, career advice, and more.

        The user provides the following context:

        Current Job Title: {job_title}
        Industry: {industry}
        Years of Experience: {years_experience}
        Skills and Technologies mastered: {skills_technologies}
        Current employment status: {current_job}
        
        Your goal is to provide insightful responses and actionable advice based on the user's input, to guide them in their career development journey.""")
            
    response = chatbot.chat(contextualized_prompt)
    return response

# Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input, job_title, current_job, industry, skills_technologies, years_experience)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))