from fetchURL import URLFetcher
from urlScraper import TextScraper
import streamlit as st
import langchain
from splitTexts_loadDocs import TextSplitterDocLoader
from vectordb import DeeplakeStorage
import sqlite3  
import time
from langchain.chat_models import ChatOpenAI
from ai_output import Output



st.set_page_config(layout="wide")


# Initialize SQLite database connection
def init_db():
    conn = sqlite3.connect('processed_urls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS processed_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_url TEXT UNIQUE,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn, c

# Check if a base URL is already processed
def is_url_processed(c, base_url):
    c.execute('SELECT * FROM processed_urls WHERE base_url = ?', (base_url,))
    return c.fetchone() is not None

# Insert the processed base URL into the database
def insert_processed_url(conn, c, base_url):
    c.execute('INSERT INTO processed_urls (base_url) VALUES (?)', (base_url,))
    conn.commit()


# Retrieve all processed URLs from the database
def get_all_processed_urls(c):
    c.execute('SELECT base_url FROM processed_urls')
    return [url[0] for url in c.fetchall()] 

# Delete the processed base URL from the database
def delete_processed_url(conn, c, base_url):
    c.execute('DELETE FROM processed_urls WHERE base_url = ?', (base_url,))
    conn.commit()


def sidebar_content(conn, c, processed_urls):
    
    #Display the processed base URLs in the sidebar
    st.sidebar.title("Base URLs in the Database")
    for url in processed_urls:
        st.write(url)
    options = processed_urls

    #Display option to delete a base URL
    selected_option = st.selectbox('Select an option to delete:', options)
    delete_button = st.button("Delete ", selected_option)
    if delete_button:
        if selected_option: 
            
            # Delete the selected base URL from the database
            with st.spinner(f"Deleting {selected_option} and its associated data..."):
                st.session_state['deep_lake'].delete_from_dataset(selected_option)
                delete_processed_url(conn, c, selected_option)
                st.success(f"Deleted {selected_option} successfully!")
                
                # Update state session if no processed base URLs are left
                if len(get_all_processed_urls(c))==0:
                    st.session_state['db'] = None
                    st.session_state['deep_lake'] = None
                    st.session_state['new_session'] = True
            time.sleep(1)
            st.rerun()


def display_chat():
    for i in range(len(st.session_state["assistant"])):
        with st.chat_message("Assistant"):
            st.write(f"{st.session_state['assistant'][i]}")
        if i < len(st.session_state["user"]):
            with st.chat_message("User"):
                st.write(f"{st.session_state['user'][i]}")  


    

st.title('DelvInDocs.AI🤖')

def main():
    conn, c = init_db()

    # Get all processed base URLs
    processed_urls = get_all_processed_urls(c)

    # Initialize session state
    if 'new_session' not in st.session_state:
        st.session_state['new_session'] = True
    if 'db' not in st.session_state:
        st.session_state['db'] = None
    if "assistant" not in st.session_state:
        st.session_state["assistant"]   =  ["Hello! I am Delvin. Let's Delve into the documents together. Please ask me anything."]
    if "user" not in st.session_state:
        st.session_state["user"] = []
    if 'deep_lake' not in st.session_state:
        st.session_state['deep_lake'] = None
    
    # Display the sidebar
    with st.sidebar:
        st.sidebar.empty()
        sidebar_content(conn, c, processed_urls)
        
    # Check if its a new session and load the data from the database
    if processed_urls and st.session_state['new_session']:

        progress_text = st.empty()
        progress_bar = st.empty()

        progress_text.text("Connecting to the database...")
        progress_bar.progress(0.3)

        st.session_state['deep_lake'] = DeeplakeStorage()

        progress_text.text("Loading data from the database...")
        progress_bar.progress(0.6)

        st.session_state['db'] = st.session_state['deep_lake'].load_dataset()

        if  st.session_state['db'] is not None:
            progress_text.text("Data loaded successfully...!!!")
            progress_bar.progress(1.0)

            progress_text.empty()
            progress_bar.success("Successfully loaded data!")
            time.sleep(2)
            progress_bar.empty()
            

        st.session_state['new_session'] = False        

    # Get the base URLs from the user
    base_urls = st.text_area("Please enter base URLs (one per line):", height=100)
    submit_button = st.button("Submit")

    # Process the base URLs
    if submit_button and base_urls :

        urls_list = [url.strip() for url in base_urls.splitlines() if url.strip()]
        all_docs = []
        total_urls = len(urls_list)

        progress_text = st.empty()
        progress_bar = st.empty()

        failed_urls = []
        
        for idx, base_url in enumerate(urls_list):
            
            # Check if the base URL is already processed
            if is_url_processed(c, base_url):

                progress_text.text(f"Data for {base_url} already exists in the database.")
                for prog in range(1, 100):
                    progress_bar.progress(prog/100)
                    time.sleep(0.003)

                time.sleep(1.2)
                progress_bar.empty()
                progress_text.empty()
                continue  

             
            #Fetch the child URLs from the base URL    
            progress_text.text(f"Fetching URLs for {idx+1}/{total_urls}: {base_url}...")
            for prog in range(1, 20):
                    progress_bar.progress(((idx + 1)/total_urls) * prog/100)
                    time.sleep(0.003) 
            urls = URLFetcher(base_url).fetch_urls()

            if len(urls) == 0:
                st.warning(f"Unable to fetch URLs for the base URL: {base_url}")
                failed_urls.append(base_url)
                continue  
            
            #Scrape the texts from the URLs
            progress_text.text(f"Gathering data from {idx+1}/{total_urls}: {base_url}...")
            for prog in range(21, 40):
                    progress_bar.progress(((idx + 1)/total_urls) * prog/100)
                    time.sleep(0.003) 
            texts = TextScraper(urls).fetch_texts()

            # Split the texts and load the documents
            progress_text.text(f"Loading data from {idx+1}/{total_urls}: {base_url} to the database...")
            for prog in range(41, 60):
                    progress_bar.progress(((idx + 1)/total_urls) * prog/100)
                    time.sleep(0.003) 
            docs = TextSplitterDocLoader(texts).split_texts_load_docs()

            #Create/Insert into the DeepLake database
            progress_text.text(f"Preparing data for use from {idx+1}/{total_urls}: {base_url}....")
            for prog in range(61, 80):
                    progress_bar.progress(((idx + 1)/total_urls) * prog/100)
                    time.sleep(0.003) 

            st.session_state['deep_lake'] = DeeplakeStorage()
            st.session_state['db'] = st.session_state['deep_lake'].create_dataset(docs, base_url)

            # Insert the processed URL into the database
            insert_processed_url(conn, c, base_url)
            
            #Get updated base URLs
            processed_urls = get_all_processed_urls(c)

        for prog in range(81, 100):
                progress_bar.progress(prog/100)
                time.sleep(0.003)
        progress_bar.success("Successfully gathered and stored data!")
        time.sleep(2)
        progress_text.empty()
        progress_bar.empty()
        
            
        st.sidebar.empty()  
        st.rerun()

    # Get user input  
    user_input = st.chat_input("What would you like to know?")

    #Appned user input and AI response to the session state
    if user_input:
        st.session_state["user"].append(user_input)
        if st.session_state['db'] is not None:
            conversation_history = list(zip(st.session_state["user"], st.session_state["assistant"]))
            ai_output = Output(st.session_state['db'], conversation_history).response(user_input, processed_urls)
        else:
            ai_output = "No data loaded. Please enter the base URLs...."
        st.session_state["assistant"].append(ai_output)    
    
    #Display the chat
    display_chat()
        

if __name__ == '__main__':
    main()