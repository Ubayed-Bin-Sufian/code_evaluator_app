import streamlit as st
import openai
import streamlit.components.v1 as components

# Function to evaluate code using OpenAI API
def evaluate_code(code, api_key):

    # Initialize OpenAI API key 
    openai.api_key = api_key

    # Prompt construction for code evaluation
    prompt = f"""
    Hey there! Can you take a look at this code and tell me how good it is? We're going to check four things:

    1. Does it work right?
    2. Is it written nicely and easy to read?
    3. Does it run fast without using too much memory?
    4. Does it handle mistakes well, like when something unexpected happens?
    For each thing, give it a score from 1 to 10, where 1 is the worst and 10 is the best. Also, explain why you gave that score.

    Here's the code:
    {code}
    """
    # Send the prompt to OpenAI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )

    # Parse and return the evaluation result
    evaluation_result = response.choices[0].text.strip()
    return evaluation_result

# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'welcome'

# Function to determine age group
def get_age_group(age):
    try:
        age = int(age)
        if 5 <= age <= 11:
            return 'junior'
        elif 12 <= age <= 18:
            return 'senior'
        else:
            return None
    except ValueError:
        return None

# Function to move to the age group view
def set_view(view):
    st.session_state.view = view

# Python IDE function
def python_ide():
    st.subheader("Python IDE")
    code = st.text_area("Write your Python code below:", height=300)
    if st.button("Evaluate Code"):
        if code.strip():
            st.success("Code submitted successfully.")
            
            # Evaluate the code only after successful submission
            api_key_openai = st.secrets['api_key_openai']
            feedback = evaluate_code(code, api_key_openai)
            
            # Display the feedback
            st.markdown(f"**{feedback}**")
        else:
            st.warning("Please enter some code before submitting.")

# Welcome page
if st.session_state.view == 'welcome':
    st.title('Code Evaluator App')
    st.markdown("""
    Welcome to the Code Evaluator App. It evaluates code for different class categories (junior and senior).
    """)

    # Embed Giphy iframe
    components.html(
        """
        <iframe src="https://giphy.com/embed/bGgsc5mWoryfgKBx1u" width="210" height="210" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
        <p><a href="https://giphy.com/gifs/computador-gu-tecnology-bGgsc5mWoryfgKBx1u">via GIPHY</a></p>
        """,
        height=230
    )

    st.markdown("Click the button below to proceed.")
    st.button('Proceed', on_click=set_view, args=('age_input',))

# Age input page
elif st.session_state.view == 'age_input':
    st.subheader('Age Group Selector')
    st.markdown("""
    Age Group Selector categorizes into juniors or seniors.  
    - **Juniors:** 5-11 years  
    - **Seniors:** 12-18 years
    """)
    
    age_input = st.text_input('Enter your age:')
    if age_input:
        age_group = get_age_group(age_input)
        if age_group:
            set_view(age_group)
        else:
            st.write('Please enter a valid age between 5 and 18.')

# Junior theme page
elif st.session_state.view == 'junior':
    st.header('Welcome to the Junior Group!')
    st.write('This is content tailored for juniors aged 5-11 years.')
    st.balloons()
    python_ide()
    st.button('Back', on_click=set_view, args=('age_input',))

# Senior theme page
elif st.session_state.view == 'senior':
    st.header('Welcome to the Senior Group!')
    st.write('This is content tailored for seniors aged 12-18 years.')
    python_ide()
    st.button('Back', on_click=set_view, args=('age_input',))
