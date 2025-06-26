import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📱 WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)

# --- FORMAT NOTE ---
st.markdown("""
<div style='background-color: #fff3cd; padding: 15px; border-left: 6px solid #ffecb5; border-radius: 5px; color: black;'>
    <strong>📌 Note:</strong><br>
    Please upload <strong>WhatsApp chat file where message timing is only in 24-hour format</strong>.<br>
    Do not use files in AM/PM format. <br>
    ✅ To export your chat: <em>WhatsApp → Open Chat → More → Export Chat → Without Media → Save as .txt</em>
</div>
""", unsafe_allow_html=True)

# --- FILE UPLOAD ---
uploaded_file = st.sidebar.file_uploader("📁 Upload your chat file (txt)")
if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)

    # --- USER SELECTION ---
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Analyze chat for:", user_list)

    if st.sidebar.button("🚀 Show Analysis"):

        # --- TOP STATS ---
        st.markdown("### 📊 Top Statistics")
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", num_messages)
        col2.metric("Words", words)
        col3.metric("Media", num_media)
        col4.metric("Links", num_links)

        # --- MONTHLY TIMELINE ---
        st.markdown("### 📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green', marker='o')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # --- DAILY TIMELINE ---
        st.markdown("### 📆 Daily Timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'], color='black', marker='.')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # --- ACTIVITY MAP ---
        st.markdown("### 📈 Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Most Active Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        with col2:
            st.write("Most Active Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # --- HEATMAP ---
        st.markdown("### 🔥 Weekly Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(heatmap, cmap='YlGnBu')
        st.pyplot(fig)

        # --- BUSY USERS ---
        if selected_user == "Overall":
            st.markdown("### 🏆 Most Active Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # --- WORDCLOUD ---
        st.markdown("### ☁️ Word Cloud")
        wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis('off')
        st.pyplot(fig)

        # --- COMMON WORDS ---
        st.markdown("### 🗣️ Most Common Words")
        common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_df[0], common_df[1], color='teal')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # --- EMOJI ANALYSIS ---
        st.markdown("### 😄 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            ax.axis('equal')
            st.pyplot(fig)

# Footer with contact info
st.markdown("""
    <div class="footer">
        Developed with ❤️ by <strong>Adnan Ahmad</strong><br>
        📧 Email: <a href="mailto:adnanask19@gmail.com">adnanask19@gmail.com</a> |
        📱 Linkedin: <a href="https://www.linkedin.com/in/aaskmee" target="_blank">Adnan Ahmad</a> |
        💻 GitHub: <a href="https://github.com/adnanaskh" target="_blank">adnanaskh</a>
    </div>
""", unsafe_allow_html=True)
