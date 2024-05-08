import streamlit as st


st.set_page_config(page_title="GradeGraph", page_icon="📊")
st.title("☎️Contact Us")


# Add a larger emoji above and below the name in the sidebar using HTML and CSS
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 10.5rem;">📊</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 2.5rem;">GradeGraph</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 1.5rem;">"Developed by Data Science Students"</span></div>', unsafe_allow_html=True)


# Embed Google Form using an iframe
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeElVKdMJjDsp7GaRpqOTJv5CDMiXvp4tRo_cNXl8lvMcgPPQ/viewform?embedded=true"
st.write(f'<iframe src="{google_form_url}" width="640" height="910" frameborder="0" marginheight="0" marginwidth="0">Loading...</iframe>', unsafe_allow_html=True)



# Footer
st.markdown("---")
st.markdown('<div style="text-align: center;">© 2023 GradeGraph</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">For more information Follow us on <a href="https://github.com/ganeshmohane/GradeGraph">GitHub</a></div>', unsafe_allow_html=True)
