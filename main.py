import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from auth import INFLUENCERS, authenticate_user, register_user, get_user_data, check_db_connection


st.set_page_config(page_title="Postly", page_icon="✦", layout="wide",
                   initial_sidebar_state="collapsed")

# ── Google Font ──
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# ════════════════════════  CSS BLOCK 1 — Base & 3D Scene  ════════════════════════
st.markdown("""<style>
*,*::before,*::after{box-sizing:border-box}
:root{
  --neon:#a78bfa; --neon2:#6366f1; --neon3:#c084fc;
  --glow:rgba(167,139,250,.45); --surface:rgba(15,10,40,.7);
}
.stApp{
  background:#05020f;
  font-family:'Outfit',sans-serif;
  min-height:100vh;
  overflow-x:hidden;
}
#MainMenu,footer,header{visibility:hidden}
.stDeployButton{display:none}

/* ── Starfield ── */
.starfield{position:fixed;inset:0;pointer-events:none;z-index:0}
.starfield .star{
  position:absolute;width:2px;height:2px;background:#fff;border-radius:50%;
  animation:twinkle var(--d,4s) ease-in-out infinite var(--del,0s);
}
@keyframes twinkle{0%,100%{opacity:.15;transform:scale(.8)}50%{opacity:.9;transform:scale(1.3)}}

/* ── 3D Floating Rings ── */
.ring-scene{position:fixed;inset:0;pointer-events:none;perspective:900px;z-index:0}
.ring{
  position:absolute;border-radius:50%;
  border:2px solid rgba(167,139,250,.12);
  animation:spinRing var(--sp,20s) linear infinite;
}
.ring-1{width:500px;height:500px;top:-120px;left:-120px;border-color:rgba(99,102,241,.10);--sp:25s}
.ring-2{width:350px;height:350px;bottom:-80px;right:-60px;border-color:rgba(192,132,252,.08);--sp:30s;animation-direction:reverse}
.ring-3{width:260px;height:260px;top:35%;left:55%;border-color:rgba(167,139,250,.06);--sp:22s}
@keyframes spinRing{to{transform:rotateX(70deg) rotateZ(360deg)}}

/* ── Ambient Glow ── */
.amb{position:fixed;border-radius:50%;filter:blur(120px);pointer-events:none;z-index:0}
.amb-1{width:600px;height:600px;top:-200px;left:-150px;background:radial-gradient(circle,rgba(99,102,241,.18),transparent 70%);animation:drift 12s ease-in-out infinite}
.amb-2{width:500px;height:500px;bottom:-180px;right:-100px;background:radial-gradient(circle,rgba(192,132,252,.14),transparent 70%);animation:drift 15s ease-in-out infinite reverse}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-30px)}}
</style>""", unsafe_allow_html=True)

# ════════════════════════  CSS BLOCK 2 — 3D Cards & Hero  ════════════════════════
st.markdown("""<style>
@keyframes fadeUp{from{opacity:0;transform:translateY(40px) rotateX(8deg)}to{opacity:1;transform:translateY(0) rotateX(0)}}
@keyframes borderGlow{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@keyframes float3d{0%,100%{transform:translateY(0) rotateX(0)}50%{transform:translateY(-8px) rotateX(2deg)}}

/* ── 3D Glass Card ── */
.card3d{
  position:relative;
  background:linear-gradient(145deg,rgba(20,15,50,.85),rgba(30,20,70,.65));
  border:1px solid rgba(167,139,250,.12);
  border-radius:24px;padding:44px 40px;
  box-shadow:0 4px 60px rgba(99,102,241,.10),0 1px 0 rgba(255,255,255,.04) inset;
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  animation:fadeUp .7s cubic-bezier(.22,1,.36,1);
  transform-style:preserve-3d;perspective:800px;
  transition:transform .4s,box-shadow .4s;
}
.card3d:hover{
  transform:translateY(-4px);
  box-shadow:0 12px 80px rgba(99,102,241,.18),0 1px 0 rgba(255,255,255,.06) inset;
}
.card3d::before{
  content:'';position:absolute;inset:-1px;border-radius:25px;padding:1px;
  background:linear-gradient(135deg,rgba(167,139,250,.25),transparent 40%,transparent 60%,rgba(192,132,252,.2));
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;
}

/* ── 3D Hero Title ── */
.hero3d{text-align:center;padding:10px 0 0;animation:fadeUp .5s ease-out;perspective:600px}
.hero3d .brand{
  font-size:3.8rem;font-weight:900;letter-spacing:-2px;line-height:1;
  background:linear-gradient(135deg,#fff 0%,#c084fc 40%,#6366f1 70%,#a78bfa 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  text-shadow:0 0 80px rgba(167,139,250,.3);
  animation:float3d 6s ease-in-out infinite;
  transform-style:preserve-3d;
}
.hero3d .sub{
  font-size:1rem;color:rgba(255,255,255,.35);margin-top:4px;
  font-weight:400;letter-spacing:2px;text-transform:uppercase;
}

/* ── Influencer Chips ── */
.chips{display:flex;justify-content:center;gap:14px;margin:22px 0 10px;flex-wrap:wrap}
.chip{
  position:relative;
  background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(192,132,252,.08));
  border:1px solid rgba(167,139,250,.18);
  border-radius:40px;padding:8px 22px;
  font-size:.75rem;font-weight:700;color:#c4b5fd;
  letter-spacing:1.5px;text-transform:uppercase;
  transition:all .35s cubic-bezier(.22,1,.36,1);
  cursor:default;
  box-shadow:0 2px 20px rgba(99,102,241,.06);
}
.chip::after{
  content:'';position:absolute;inset:0;border-radius:40px;
  background:linear-gradient(135deg,rgba(99,102,241,.15),transparent);
  opacity:0;transition:opacity .3s;
}
.chip:hover{
  transform:translateY(-3px) scale(1.04);
  box-shadow:0 8px 30px rgba(99,102,241,.2);
  border-color:rgba(167,139,250,.35);
}
.chip:hover::after{opacity:1}

/* ── Section Label ── */
.sec-label{
  font-size:.7rem;font-weight:700;text-transform:uppercase;
  letter-spacing:2px;color:rgba(167,139,250,.6);margin-bottom:18px;
  display:flex;align-items:center;gap:8px;
}
.sec-label .dot{width:6px;height:6px;border-radius:50%;background:#6366f1;
  box-shadow:0 0 8px rgba(99,102,241,.5);animation:pulse-sm 2s ease-in-out infinite}
@keyframes pulse-sm{0%,100%{box-shadow:0 0 4px rgba(99,102,241,.3)}50%{box-shadow:0 0 12px rgba(99,102,241,.6)}}
</style>""", unsafe_allow_html=True)

# ════════════════════════  CSS BLOCK 3 — Inputs, Buttons, Post  ════════════════════════
st.markdown("""<style>
/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
  gap:6px;background:rgba(255,255,255,.03);border-radius:14px;padding:5px;
  border:1px solid rgba(255,255,255,.05);
}
.stTabs [data-baseweb="tab"]{
  border-radius:11px;color:rgba(255,255,255,.45);
  font-weight:600;font-family:'Outfit',sans-serif;padding:10px 30px;
  transition:all .3s;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#6366f1,#7c3aed) !important;
  color:#fff !important;
  box-shadow:0 4px 20px rgba(99,102,241,.35);
}

/* ── Inputs ── */
.stTextInput>div>div>input,.stSelectbox>div>div>div{
  background:rgba(30,20,70,.6) !important;
  border:1px solid rgba(167,139,250,.2) !important;
  border-radius:14px !important;color:#e2e0ff !important;
  font-family:'Outfit',sans-serif !important;
  padding:14px 18px !important;font-size:.92rem !important;
  transition:all .3s;
}
.stTextInput>div>div>input:focus{
  border-color:#6366f1 !important;
  box-shadow:0 0 0 3px rgba(99,102,241,.18),0 0 30px rgba(99,102,241,.08) !important;
}
.stTextInput label,.stSelectbox label{
  color:#c4b5fd !important;font-weight:600 !important;
  font-family:'Outfit',sans-serif !important;font-size:.88rem !important;
  letter-spacing:.5px;
}

/* ── 3D Buttons ── */
div.stButton>button{
  background:linear-gradient(135deg,#6366f1 0%,#7c3aed 50%,#a855f7 100%) !important;
  color:#fff !important;border:none !important;
  border-radius:14px !important;padding:14px 36px !important;
  font-weight:700 !important;font-size:.92rem !important;
  font-family:'Outfit',sans-serif !important;
  letter-spacing:.5px;cursor:pointer;
  box-shadow:0 6px 25px rgba(99,102,241,.3),0 2px 0 rgba(255,255,255,.08) inset !important;
  transition:all .3s cubic-bezier(.22,1,.36,1) !important;
  transform-style:preserve-3d;
}
div.stButton>button:hover{
  transform:translateY(-3px) scale(1.02) !important;
  box-shadow:0 12px 40px rgba(99,102,241,.45),0 2px 0 rgba(255,255,255,.1) inset !important;
}
div.stButton>button:active{
  transform:translateY(0) scale(.98) !important;
  box-shadow:0 2px 10px rgba(99,102,241,.25) !important;
}

/* ── Post Card 3D ── */
.post3d{
  position:relative;
  background:linear-gradient(160deg,rgba(20,15,55,.9),rgba(10,8,30,.8));
  border:1px solid rgba(167,139,250,.1);
  border-radius:20px;padding:32px;margin-top:24px;
  box-shadow:0 8px 50px rgba(0,0,0,.4),0 1px 0 rgba(255,255,255,.03) inset;
  animation:fadeUp .6s ease-out;overflow:hidden;
  transform-style:preserve-3d;
}
.post3d::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,#6366f1,#a855f7,#c084fc,#6366f1);
  background-size:300% 100%;animation:borderGlow 4s ease infinite;
}
.post3d::after{
  content:'';position:absolute;top:3px;left:20%;right:20%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(167,139,250,.2),transparent);
}
.post3d .p-label{
  font-size:.7rem;font-weight:700;text-transform:uppercase;
  letter-spacing:2px;color:#a78bfa;margin-bottom:16px;
  display:flex;align-items:center;gap:8px;
}
.post3d .p-label .glow-dot{
  width:6px;height:6px;border-radius:50%;background:#a855f7;
  box-shadow:0 0 10px rgba(168,85,247,.6);
}
.post3d .p-body{
  font-size:.95rem;line-height:1.8;color:rgba(255,255,255,.82);
  white-space:pre-wrap;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
  background:rgba(5,2,15,.97) !important;
  border-right:1px solid rgba(167,139,250,.08);
}
section[data-testid="stSidebar"] .stMarkdown p{
  color:rgba(255,255,255,.7) !important;font-family:'Outfit',sans-serif;
}

/* ── Misc ── */
.stAlert{border-radius:14px !important}
.stTextArea textarea{
  background:rgba(30,20,70,.6) !important;
  border:1px solid rgba(167,139,250,.2) !important;
  border-radius:14px !important;color:#e2e0ff !important;
  font-family:'Outfit',sans-serif !important;
  font-size:.92rem !important;line-height:1.8 !important;
}
.stTextArea textarea:focus{
  border-color:#6366f1 !important;
  box-shadow:0 0 0 3px rgba(99,102,241,.18) !important;
}
.stTextArea label{
  color:#c4b5fd !important;font-weight:600 !important;
  font-family:'Outfit',sans-serif !important;font-size:.88rem !important;
}
hr{border-color:rgba(167,139,250,.08) !important}
[data-baseweb="select"]>div{
  background:rgba(30,20,70,.6) !important;
  border-color:rgba(167,139,250,.2) !important;border-radius:14px !important;
}
/* Force ALL text inside selectbox to be bright white */
.stSelectbox div[data-baseweb="select"],
.stSelectbox div[data-baseweb="select"] div,
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] p,
.stSelectbox [role="combobox"],
.stSelectbox [role="combobox"] div,
.stSelectbox [role="combobox"] span,
[data-baseweb="select"] [aria-live],
[data-baseweb="select"] [aria-live] div,
[data-baseweb="select"] [aria-live] span{
  color:#fff !important;
  -webkit-text-fill-color:#fff !important;
  opacity:1 !important;
}
/* Arrow icon */
.stSelectbox svg path{fill:#c4b5fd !important;stroke:#c4b5fd !important}
.stSelectbox svg{color:#c4b5fd !important}
/* Alignment fix */
.stSelectbox [data-baseweb="select"]>div{
  display:flex !important;align-items:center !important;
  min-height:48px !important;padding:0 14px !important;
}
/* Dropdown menu */
[data-baseweb="popover"] ul{
  background:rgba(20,12,55,.97) !important;
  border:1px solid rgba(167,139,250,.18) !important;
  border-radius:12px !important;
}
[data-baseweb="popover"] li{
  background:transparent !important;
  color:#e2e0ff !important;
  -webkit-text-fill-color:#e2e0ff !important;
}
[data-baseweb="popover"] li:hover,[data-baseweb="popover"] li[aria-selected="true"]{
  background:rgba(99,102,241,.25) !important;
}
.stSpinner>div{color:#a78bfa !important}

/* ── Influencer Active Badge ── */
.inf-active{
  display:inline-flex;align-items:center;gap:10px;
  background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(124,58,237,.08));
  border:1px solid rgba(99,102,241,.15);
  border-radius:40px;padding:10px 24px;margin-bottom:22px;
  box-shadow:0 2px 20px rgba(99,102,241,.06);
}
.inf-active .live{
  width:8px;height:8px;border-radius:50%;background:#6366f1;
  box-shadow:0 0 8px rgba(99,102,241,.5);
  animation:pulse-sm 2s ease-in-out infinite;
}
.inf-active span{font-size:.88rem;font-weight:600;color:#c4b5fd;letter-spacing:.5px}

/* ── Share Box ── */
.share-box{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(167,139,250,.08);
  border-radius:16px;padding:22px 28px;margin-top:24px;text-align:center;
}
.share-box h4{color:rgba(255,255,255,.6);font-weight:600;margin:0 0 8px;font-size:.95rem}

@media(max-width:768px){
  .hero3d .brand{font-size:2.4rem}
  .card3d{padding:28px 24px}
}
</style>""", unsafe_allow_html=True)

# ════════════════════════  Background Elements  ════════════════════════
# Stars
import random
stars_html = '<div class="starfield">'
for i in range(60):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    d = round(random.uniform(2, 6), 1)
    dl = round(random.uniform(0, 5), 1)
    s = random.choice([1, 2, 3])
    stars_html += f'<div class="star" style="left:{x}%;top:{y}%;width:{s}px;height:{s}px;--d:{d}s;--del:{dl}s"></div>'
stars_html += '</div>'
st.markdown(stars_html, unsafe_allow_html=True)

# 3D Rings & Ambient
st.markdown("""
<div class="ring-scene">
  <div class="ring ring-1"></div>
  <div class="ring ring-2"></div>
  <div class="ring ring-3"></div>
</div>
<div class="amb amb-1"></div>
<div class="amb amb-2"></div>
""", unsafe_allow_html=True)

# ════════════════════════  Hero  ════════════════════════
st.markdown("""
<div class="hero3d">
  <div class="brand">Postly</div>
  <div class="sub">Murli Dharan</div>
</div>
<div class="chips">
  <div class="chip">Influencer 1</div>
  <div class="chip">Influencer 2</div>
  <div class="chip">Influencer 3</div>
</div>
""", unsafe_allow_html=True)

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "French", "Spanish", "Chinese", "Russian"]


def login_page():
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:

        # DB status check
        with st.spinner("Connecting to database..."):
            db_ok, db_msg = check_db_connection()
        if not db_ok:
            st.error(f"Database connection issue: {db_msg}")
            st.info("The app may not work properly until the database is accessible.")

        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            username = st.text_input("Username", key="login_username",
                                     placeholder="Enter your username")
            password = st.text_input("Password", type="password",
                                     key="login_password",
                                     placeholder="Enter your password")
            st.write("")
            if st.button("Sign In →", use_container_width=True):
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    with st.spinner("Signing in..."):
                        success, msg = authenticate_user(username, password)
                    if success:
                        with st.spinner("Loading your profile..."):
                            user_data = get_user_data(username)
                        if user_data:
                            st.session_state['logged_in'] = True
                            st.session_state['username'] = username
                            st.session_state['influencer'] = user_data['influencer']
                            st.rerun()
                        else:
                            st.error("Could not load user profile. Please try again.")
                    else:
                        st.error(f"Sign in failed: {msg}")

        with tab2:
            new_username = st.text_input("Username", key="reg_username",
                                         placeholder="Choose a username")
            new_password = st.text_input("Password", type="password",
                                         key="reg_password",
                                         placeholder="Create a password")
            influencer = st.selectbox("Influencer Style",
                                      options=list(INFLUENCERS.keys()))
            st.write("")
            if st.button("Create Account →", use_container_width=True):
                if not new_username or not new_password:
                    st.error("Please fill in all fields")
                elif len(new_password) < 4:
                    st.error("Password must be at least 4 characters")
                else:
                    with st.spinner("Creating your account..."):
                        success, msg = register_user(new_username, new_password,
                                                     INFLUENCERS[influencer])
                    if success:
                        st.success("Account created! Switch to 'Sign In' tab to continue.")
                    else:
                        st.error(f"Registration failed: {msg}")



def main_app():
    user_data = get_user_data(st.session_state['username'])
    if not user_data:
        st.error("Session expired. Please login again.")
        st.session_state['logged_in'] = False
        st.rerun()

    fs = FewShotPosts(user_data['dataset'])

    # ── Config Card ──


    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("Topic", options=fs.get_tags())
    with col2:
        selected_length = st.selectbox("Length", options=length_options)
    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    st.write("")
    if st.button("⚡ Generate Post", use_container_width=True):
        with st.spinner("Crafting your post…"):
            post = generate_post(selected_length, selected_language,
                                 selected_tag, user_data['dataset'])
            st.session_state['generated_post'] = post
            st.session_state['show_post'] = True
            st.session_state['edit_mode'] = False
            st.rerun()


    # ── Generated Post ──
    if st.session_state.get('show_post') and st.session_state.get('generated_post'):
        if 'edit_mode' not in st.session_state:
            st.session_state['edit_mode'] = False

        if not st.session_state['edit_mode']:
            content = st.session_state["generated_post"]
            st.markdown(
                f'<div class="post3d">'
                f'<div class="p-label"><span class="glow-dot"></span>Generated Post</div>'
                f'<div class="p-body">{content}</div></div>',
                unsafe_allow_html=True
            )
            col_a, col_b, col_c = st.columns([1, 1, 2])
            with col_a:
                if st.button("✏️ Edit"):
                    st.session_state['edit_mode'] = True
                    st.rerun()
            with col_b:
                if st.button("🔄 Regenerate"):
                    with st.spinner("Regenerating…"):
                        post = generate_post(selected_length, selected_language,
                                             selected_tag, user_data['dataset'])
                        st.session_state['generated_post'] = post
                        st.rerun()
        else:
            st.markdown("#### ✏️ Edit Your Post")
            edited_post = st.text_area("Edit:", value=st.session_state['generated_post'],
                                       height=200, label_visibility="collapsed")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 Save", use_container_width=True):
                    st.session_state['generated_post'] = edited_post
                    st.session_state['edit_mode'] = False
                    st.success("Saved!")
                    st.rerun()
            with c2:
                if st.button("✖ Cancel", use_container_width=True):
                    st.session_state['edit_mode'] = False
                    st.rerun()

        st.markdown('<div class="share-box"><h4>🔗 Ready to publish?</h4></div>', unsafe_allow_html=True)
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            st.link_button("Open LinkedIn →", "https://www.linkedin.com/login", use_container_width=True)


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['show_post'] = False

    if not st.session_state['logged_in']:
        login_page()
    else:
        with st.sidebar:
            uname = st.session_state['username']
            st.markdown(
                f'<div style="padding:20px 0">'
                f'<div style="font-size:.7rem;color:rgba(255,255,255,.35);text-transform:uppercase;letter-spacing:2px;font-weight:700">Session</div>'
                f'<div style="font-size:1.2rem;color:#c4b5fd;font-weight:800;margin-top:6px">{uname}</div>'
                f'</div>', unsafe_allow_html=True)
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                for k in ['logged_in', 'show_post', 'edit_mode']:
                    st.session_state[k] = False
                st.rerun()
        main_app()


if __name__ == "__main__":
    main()
