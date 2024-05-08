import streamlit as st

# Set page configuration for mobile-friendliness and device theme
st.set_page_config(page_title="GradeGraph", page_icon="📊", layout="wide", use_browser_default_style=True)

# Add a title
st.title("Contact Us")

# Embed Google Form using an iframe
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeElVKdMJjDsp7GaRpqOTJv5CDMiXvp4tRo_cNXl8lvMcgPPQ/viewform?embedded=true"
st.markdown(f'<iframe src="{google_form_url}" width="100%" height="600" frameborder="0" marginheight="0" marginwidth="0">Loading...</iframe>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("© 2023 GradeGraph")
st.markdown("For more information Follow us on [GitHub](https://github.com/ganeshmohane/GradeGraph)")
