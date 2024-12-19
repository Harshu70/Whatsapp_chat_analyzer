import streamlit as st
import preprocesser, stats
import pathlib
import seaborn
import matplotlib.pyplot as plt

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("style.css")
load_css(css_path)

st.title("Whatsapp chat analyser")

uploaded_file = st.sidebar.file_uploader("choose a file")
st.sidebar.caption("please choose the chat file in the date format of dd/mm/yyyy, hh:mm")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocesser.preprocess(data)

    st.dataframe(df)

    #user dropdown
    userList = df['user'].unique().tolist()
    userList.remove('group_notification')
    userList.sort()
    userList.insert(0, "Overall")

    selectedUser = st.sidebar.selectbox("Analysis of ", userList)


    if st.sidebar.button("Analysis of"):
        msgNum, wordNum, mediaNum, linkNum = stats.fetchData(selectedUser, df)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.header("Total Message")
            st.title(msgNum)
        with c2:
            st.header("Total Words")
            st.title(wordNum)
        with c3:
            st.header("Media shared")
            st.title(mediaNum)
        with c4:
            st.header("Link shared")
            st.title(linkNum)
        
        st.title("Monthly Timeline")
        tl = stats.monthly(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(tl['time'], tl['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #actvity
        st.title("Activity Stats")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            bgDay = stats.weekly_stat(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(bgDay.index, bgDay.values, color='skyblue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            bgMonth = stats.monthly_stat(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(bgMonth.index, bgMonth.values, color='violet')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selectedUser != "Overall":
            st.markdown(f"### Messages from {selectedUser}")
            user_df = df[df['user'] == selectedUser][['date', 'message']]
            st.dataframe(user_df)
        else:
            st.title("User Contribution")
            perc = stats.most_active(df)
            st.dataframe(perc)

        st.title("Wordcloud")
        df_wc = stats.wrdCloud(selectedUser, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        cmn_words = stats.most_cmn_word(selectedUser, df)
        fig, ax = plt.subplots()
        ax.barh(cmn_words[0], cmn_words[1])
        st.title("Most Common Words")
        st.pyplot(fig)

        st.title("Weekly Heatmap")
        htMap = stats.heatMap(selectedUser, df)
        fig, ax = plt.subplots()
        ax = (seaborn.heatmap(htMap))
        st.pyplot(fig)




        

