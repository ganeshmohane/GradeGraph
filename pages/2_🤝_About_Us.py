import streamlit as st

st.set_page_config(page_title="GradeGraph", page_icon="📊")

# Add a larger emoji above and below the name in the sidebar using HTML and CSS
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 10.5rem;">📊</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 2.5rem;">GradeGraph</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 1.5rem;">"Developed by Data Science Students"</span></div>', unsafe_allow_html=True)
st.title("🤝About Us")


st.write(
        "GradeGraph is an academic performance visualization platform designed to empower students, educators, and institutions by providing a data-driven approach to education."
    )

st.write(
        "We offer a user-friendly interface that allows you to analyze and visualize student academic performance data, offering valuable insights into trends, progress, and areas for improvement."
    )

st.write(
        "With GradeGraph, you can make informed decisions to enhance your academic journey."
    )



st.markdown('<br>', unsafe_allow_html = True)
st.title("And here is our...")
st.title("❤️ GradeGraph Team !!!")

team_members = [
    {
        "name": "AADITYA PRAJAPTI",
        "role": "Front-End Builder",
        "image_url": "img/aadi.jpg",
        "bio": "Aaditya, the mastermind behind GradeGraph's frontend, brings creativity and technical skill to the project. His expertise in building a user-friendly interface ensures a smooth experience for users",
        "social_media_url": "https://instagram.com/aaditya_0725"
    },
    
    {
        "name": "ANUJ MISHRA",
        "role": "Data Engineer",
        "image_url": "img/anuj.jpg",
        "bio": "Anuj, a dedicated data engineer, excels in collecting data and constructing systems to transform unstructured PDF data into organized formats. His strong work ethic and attention to detail drive his data management success",
        "social_media_url": "https://instagram.com/1008_anuj"
    },
    
    {
        "name": "GANESH MOHANE",
        "role": "Data Analyst",
        "image_url": "img/ganu.jpg",
        "bio": "Ganesh, a skilled data analyst, plays a crucial role in refining data extracted from PDFs. His data cleaning expertise ensures that the information presented to users is accurate and reliable.",
        "social_media_url": "https://instagram.com/ganeshmohanee"
    },
    
    {
        "name": "YASHWARDHAN PANDEY",
        "role": "Data Visuals Expert",
        "image_url": "img/yash.jpg",
        "bio": "Yashwardhan, our data visualization expert, creates compelling visuals from cleaned data. His ability to transform complex information into insightful graphics enhances the understanding of the data's patterns and trends.",
        "social_media_url": "https://instagram.com/yashwardhan_is_ded"
    },
]

# Create individual sections for team members with automatically determined image size
for team_member in team_members:
    st.image(team_member["image_url"], width=100)
    st.subheader(team_member["name"])
    st.write(f"**Role:** {team_member['role']}")
    st.write(team_member["bio"])

    insta_text = " [Follow on Instagram](" + team_member["social_media_url"] + ")"
    st.markdown(insta_text, unsafe_allow_html=True)
    st.markdown("---")














# Footer
st.markdown('<div style="text-align: center;">© 2023 GradeGraph</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">For more information Follow us on <a href="https://github.com/ganeshmohane/GradeGraph">GitHub</a></div>', unsafe_allow_html=True)
