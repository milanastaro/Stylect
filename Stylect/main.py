# Sidebar Navigation (after login)
from app_pages import profile, settings, wardrobe
from app_pages import wardrobe
from turtle import st
from app_pages.user_auth import login_signup
from app_pages import chat_groups
from app_pages import admin_dashboard, color_analysis, marketplace, outfit_generator, social


st.sidebar.title("🌟 Stylect Menu")

username = st.session_state.user_info["username"]
admin_username = "milana"  # Replace with your admin username

# Core menu for all users
menu_options = [
    "🏠 Home",
    "👤 My Profile",
    "👚 My Wardrobe",
    "🤖 Style Me (Outfit Generator)",
    "🛍️ Shop",
    "🎨 Color Analysis",
    "📸 Style Feed",
    "💬 Chats & Groups",
    "⚙️ Settings"
]

# Add CEO/Admin if user is admin
if username == admin_username:
    menu_options.append("👩‍💼 CEO / Admin")

# Sidebar selector
section = st.sidebar.radio("Go to", menu_options)

# Logout
if st.sidebar.button("🚪 Log Out"):
    st.session_state.user_info = {}
    st.experimental_rerun()

# ---------------- PAGE ROUTING ----------------

if section == "🏠 Home":
    st.title("👗 Welcome to Stylect")
    st.markdown("""
        Stylect helps you style your wardrobe, analyze your color palette,
        shop and trade clothes, and connect with the fashion community.
        Use the sidebar to get started!
    """)

elif section == "👤 My Profile":
    profile.show()

elif section == "👚 My Wardrobe":
    wardrobe.shpow()

elif section == "🤖 Style Me (Outfit Generator)":
    outfit_generator.show()

elif section == "🛍️ Shop":
    marketplace.show()

elif section == "🎨 Color Analysis":
    color_analysis.show()

elif section == "📸 Style Feed":
    social.show()

elif section == "💬 Chats & Groups":
    chat_groups.show()

elif section == "⚙️ Settings":
    settings.show()

elif section == "👩‍💼 CEO / Admin":
    if username != admin_username:
        st.error("🚫 Access Denied: You do not have permission to view this page.")
    else:
        admin_dashboard.show()
