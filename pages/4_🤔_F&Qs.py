import streamlit as st


st.set_page_config(page_title="GradeGraph", page_icon="📊")
st.title("🤔 Frequently Asked Questions")
st.markdown("")

# Add a larger emoji above and below the name in the sidebar using HTML and CSS
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 10.5rem;">📊</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 2.5rem;">GradeGraph</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 1.5rem;">"Developed by Data Science Students"</span></div>', unsafe_allow_html=True)


# Question 1
st.subheader("Q1: What is GradeGraph?")
st.write("A1: GradeGraph is an application who converts result pdfs into cleaned excel file with insightful visuals that provides student academic performance. It helps students, educators, and parents gain insights into academic progress.")

# Question 2
st.subheader("Q2: How can I access GradeGraph?")
st.write("A2: GradeGraph is a web-based platform, so you can access it through your web browser. Simply visit our website and create an account to get started. Our webiste url is : gradegraph.streamlit.app")

# Question 3
st.subheader("Q3: Is GradeGraph free to use?")
st.write("A3: Yes, GradeGraph is free. This is made by students for students use.")

# Question 4
st.subheader("Q4: Can I use GradeGraph as a teacher or parent?")
st.write("A4: Absolutely! GradeGraph is designed for students, teachers, and parents. It offers tools for students to track their progress, teachers to analyze student data, and parents to see about their child's performance.")

# Question 5
st.subheader("Q5: How do I contact GradeGraph support?")
st.write("A5: You can reach out to our support team through our website's 'Contact Us' page. We are here to assist you with any questions or issues you may have.")


# Footer
st.markdown("---")
st.markdown('<div style="text-align: center;">© 2023 GradeGraph</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">For more information Follow us on <a href="https://github.com/ganeshmohane/GradeGraph">GitHub</a></div>', unsafe_allow_html=True)
