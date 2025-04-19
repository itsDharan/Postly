import streamlit as st
import json 
from few_shot import FewShotPosts
from post_generator import generate_post
from auth import INFLUENCERS, authenticate_user, register_user
from auth import authenticate_user, register_user, get_user_data
import webbrowser

# Custom CSS styling
st.markdown(
    """
    <style>
        .centered-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #1A73E8;
        }
        .subtitle {
            font-size: 18px;
            font-weight: bold;
            color: #008CBA;
            text-align: center;
            margin-top: -5px;
            line-height: 1.3;
        }
        body {
            background-color: #f5f5f5;
        }
        div.stButton > button {
            background-color: #008CBA;
            color: white;
            border-radius: 10px;
            font-size: 10px;
            margin-top: 5px;
        }
        .influencer-display {
            font-size: 20px;
            font-weight: bold;
            color: #1A73E8;
            margin-bottom: 20px;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# Main Title
st.markdown("<h1 class='centered-title'>LinkedIn Post Generator</h1>", unsafe_allow_html=True)

# Subtitle
st.markdown('<p class="subtitle">KHUSHBU_RANI<br>MURLI_DHARAN<br>AMMAR_ADIL</p>', unsafe_allow_html=True)

# Options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "French", "Spanish", "Chinese", "Russian"]

def login_page():
    st.title("Login / Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                # Get user data directly from MongoDB instead of JSON file
                user_data = get_user_data(username)
                if user_data:
                    st.session_state['influencer'] = user_data['influencer']
                    st.rerun()
                else:
                    st.error("User data not found")
            else:
                st.error("Invalid username or password")

    with tab2:
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        influencer = st.selectbox("Select Influencer", options=list(INFLUENCERS.keys()))
        if st.button("Register"):
            if register_user(new_username, new_password, INFLUENCERS[influencer]):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")

# ... (keep your existing CSS and layout code)

def main_app():
    # Get user data including dataset name
    user_data = get_user_data(st.session_state['username'])
    if not user_data:
        st.error("User data not found. Please login again.")
        st.session_state['logged_in'] = False
        st.rerun()
    
    # Initialize FewShotPosts with the user's dataset
    fs = FewShotPosts(user_data['dataset'])
    
    # Display influencer
    st.markdown(f'<div class="influencer-display">Influencer: {user_data["influencer_name"]}</div>', unsafe_allow_html=True)

    # Post generation options
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("Title", options=fs.get_tags())
    with col2:
        selected_length = st.selectbox("Length", options=length_options)
    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    if st.button("Generate Post"):
        post = generate_post(
            selected_length, 
            selected_language, 
            selected_tag,
            user_data['dataset']  # Pass the dataset name
        )
        st.session_state['generated_post'] = post
        st.session_state['show_post'] = True
        st.session_state['edit_mode'] = False
        st.rerun()

    # ... (rest of your existing main_app code)

    if 'show_post' in st.session_state and st.session_state['show_post']:
        st.markdown("### Generated Post :")

        if 'edit_mode' not in st.session_state:
            st.session_state['edit_mode'] = False

        if not st.session_state['edit_mode']:
            st.markdown(f'<div class="post-editor">{st.session_state["generated_post"]}</div>', unsafe_allow_html=True)
            if st.button("Edit"):
                st.session_state['edit_mode'] = True
                st.rerun()
        else:
            edited_post = st.text_area("Edit your post:", value=st.session_state['generated_post'], height=200)
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Save Changes"):
                    st.session_state['generated_post'] = edited_post
                    st.session_state['edit_mode'] = False
                    st.success("Post updated successfully!")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state['edit_mode'] = False
                    st.rerun()

        # LinkedIn login prompt
        st.markdown("---")
        st.markdown("### Ready to share your post?")
        if st.button("Login with LinkedIn to Share"):
            webbrowser.open_new_tab("https://www.linkedin.com/login")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['show_post'] = False

    if not st.session_state['logged_in']:
        login_page()
    else:
        st.sidebar.write(f"Logged in as: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['show_post'] = False
            st.session_state['edit_mode'] = False
            st.rerun()
        main_app()
        
if __name__ == "__main__":
    main()
