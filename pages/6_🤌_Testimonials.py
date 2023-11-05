import streamlit as st


st.set_page_config(page_title="GradeGraph", page_icon="📊")
st.title("Testimonials or Feedbacks")


# Add a larger emoji above and below the name in the sidebar using HTML and CSS
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 10.5rem;">📊</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 2.5rem;">GradeGraph</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 1.5rem;">"Developed by Data Science Students"</span></div>', unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown('<div style="text-align: center;">© 2023 GradeGraph</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">Follow us on <a href="https://twitter.com/gradegraph">Twitter</a> and <a href="https://linkedin.com/company/gradegraph">LinkedIn</a></div>', unsafe_allow_html=True)
