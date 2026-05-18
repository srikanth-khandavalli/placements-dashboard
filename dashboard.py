import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import matplotlib.pyplot as plt
from functions import format_indian, custom_small_info

st.title("College Placement Dashboard")

# --- SECTION 1: User Input Portal ---
st.info("""Please paste URLs of placement data Google Sheets below.\n
*Tap **'Load Dashboard'** to show AY:**2025-26** data*""") 
# st.markdown(custom_small_info("Tap 'Load Dashborad' for defaults:"), unsafe_allow_html=True)
student_url = st.text_input("Student Data CSV URL:")
placement_url = st.text_input("Placement Data CSV URL:")


# # Your main Spreadsheet ID
# SHEET_ID = "1ulWzuwver6sDcxyCys1ktVYLiNcF-3UjWmKgh0HMbT8"

# # Replace these with the actual numbers you found in the address bar!
# STUDENTS_GID = "1143547355"          # Example: usually 0 for the first tab
# PLACEMENTS_GID = "1324552366" # Example: the number for the second tab

# # Construct the special export URLs
# students_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={STUDENTS_GID}"
# placements_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={PLACEMENTS_GID}"
# #

# st.write("Student data example URL:")
# # This creates a theme-matching box with a copy button!
# st.code("https://docs.google.com/spreadsheets/d/1ulWzuwver6sDcxyCys1ktVYLiNcF-3UjWmKgh0HMbT8/export?format=csv&gid=1143547355", language="plaintext")

# st.write("Placement data example URL:")
# st.code("https://docs.google.com/spreadsheets/d/1ulWzuwver6sDcxyCys1ktVYLiNcF-3UjWmKgh0HMbT8/export?format=csv&gid=1324552366", language="plaintext")

student_url_default = "https://docs.google.com/spreadsheets/d/1ulWzuwver6sDcxyCys1ktVYLiNcF-3UjWmKgh0HMbT8/export?format=csv&gid=1143547355"
placement_url_default = "https://docs.google.com/spreadsheets/d/1ulWzuwver6sDcxyCys1ktVYLiNcF-3UjWmKgh0HMbT8/export?format=csv&gid=1324552366"

# # --- SECTION 2: Data Loading & Processing ---
# # The code inside this block only runs AFTER the user clicks the button
# if st.button("Load Dashboard"):

# 1. The Dashboard Toggle (Using the URLs from your text inputs)
if "dashboard_loaded" not in st.session_state:
    st.session_state.dashboard_loaded = False

if st.button("Load Dashboard"):
    st.session_state.dashboard_loaded = True

# 2. EVERYTHING lives inside this check!
if st.session_state.dashboard_loaded:

    # Check to make sure the user didn't leave the boxes blank
    if student_url and placement_url:
        try:
            # Show a loading spinner while Pandas fetches the web data
            with st.spinner("Downloading data from Google Sheets..."):
                student_df = pd.read_csv(student_url)
                placement_df = pd.read_csv(placement_url)
                # Show a success message
                st.success("Data loaded successfully!")
        except Exception as e:
            # If the link is broken or private, show a safe error message
            st.error("Failed to load data. Please check your URLs.")
            st.error(f"Technical details: {e}")

    else:
        # Warning if they click the button without pasting both links
        st.warning("URLs not provided loading default URLs.")
        student_df = pd.read_csv(student_url_default)
        placement_df = pd.read_csv(placement_url_default)        
    #
    #
    # try:
    #     # Merge the data (Using 'Regd. Number' based on your earlier screenshot)
    #     merged_data = pd.merge(student_df, placement_df, on='Regd. Number', how='left')
    #     # Display the dataframe
    #     st.header("2. Dashboard Overview")
    #     st.dataframe(merged_data.head(4))
    # except Exception as e:
    #     st.error(f"Failed to merge data, details:{e}")

    try:
        placement_df = placement_df.sort_values(by=['Regd. Number', 'Package'], ascending=[True, False])
        placement_df['uni_row_no'] = placement_df.groupby(['Regd. Number']).cumcount() + 1
        uni_placement_df = placement_df[placement_df['uni_row_no'] == 1]
        uni_placement_df = uni_placement_df.sort_values(by=['Branch','Regd. Number'], ascending=[True,True])
        # 1. Calculate the number of unique companies
        company_list_df = pd.DataFrame(placement_df['Company'].unique(), columns=['Company'])
        company_list_df = company_list_df.dropna()
        company_list_df = company_list_df.sort_values(by=["Company"],ascending=[True])
        st.header("List of Placement Companies:")
        st.dataframe(company_list_df)
        # st.dataframe(uni_placement_df)
    except Exception as e:
        st.error(f"Unique Placements Group by calculations error, details:{e}")   
    try:
        st.header("Key Performance Indicators")
        total_students =len(student_df)
        total_placements = len(placement_df)
        uni_placement = len(uni_placement_df)
        company_count = len(company_list_df)
        placement_rate  = (uni_placement / total_students)*100
        highest_ctc = pd.to_numeric(placement_df['Package'],errors='coerce').max()
        avg_ctc = pd.to_numeric(placement_df['Package'], errors='coerce').mean()
        st.divider()
        # Create 4 columns for a neat row of scorecards 1st set
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Students",value=total_students)
        with col2:
            st.metric(label="Total Placements",value=total_placements)
        with col3:
            st.metric(label="Students Placed",value=uni_placement)
        with col4:
            st.metric(label="Companies Visited",value=company_count)
        # Create 4 columns for a neat row of scorecards 2nd set
        # col1, col2, col3, col4 = st.columns(4)
        # The numbers act as ratios. The last two columns will be 50% wider than the first two!
        col2, col3, col4 = st.columns([1, 1.5, 1.5])
        with col2:
            st.metric(label="Placement Rate", value=f"{placement_rate:.1f}%")
        with col3:
            # Fill NaN with 0 if no highest CTC exists
            st.metric(label="Highest CTC", value=format_indian(highest_ctc) if pd.notnull(highest_ctc) else "N/A")
        with col4:
            st.metric(label="Average CTC", value=format_indian(avg_ctc) if pd.notnull(avg_ctc) else "N/A")

        st.divider()
    except Exception as e:
        st.error(f"KPI calculations error, details:{e}")          

    try:
        # This counts the students per branch and creates a clean dataframe
        branch_counts_df = student_df['Branch'].value_counts().reset_index()
        # Rename the columns to make them look nice on your dashboard
        branch_counts_df.columns = ['Branch', 'Total Students']
        # st.dataframe(branch_counts_df)

        branch_placement_df = placement_df['Branch'].value_counts().reset_index()
        branch_placement_df.columns = ['Branch', 'Total Placements']
        # st.dataframe(branch_placement_df)

        branch_uni_placement_df = uni_placement_df['Branch'].value_counts().reset_index()
        branch_uni_placement_df.columns = ['Branch', 'Students Placed']
        # st.dataframe(branch_uni_placement_df)

        # 1. Use pd.merge() to link them perfectly by the 'Branch' column
        final_table_df = pd.merge(branch_counts_df, branch_placement_df, on='Branch', how='left')
        final_table_df = pd.merge(final_table_df, branch_uni_placement_df, on='Branch', how='left')
        final_table_df = final_table_df[['Branch', 'Total Students', 'Total Placements', 'Students Placed']]
        # 3. Display the final clean table!
        st.header("Branch wise Analytics:")
        st.dataframe(final_table_df)
    except Exception as e:
        st.error(f"Total Stundets Group by calculations error, details:{e}")   

    # if st.button("Load AI Assistant"): #fails if nested in the above "if" block so commented
    # Merge the data (Using 'Regd. Number' based on your earlier screenshot)
    ai_student_df = student_df[['Regd. Number','Branch','Category','SSC (X class) Board','SSC (X class) Percentage '
                                ,'Are you Studied intermediate or Diploma after X class','Select your Intermediate/Diploma Board'
                                ,'INTERMEDIATE %','B.Tech CGPA New','History of Backlogs','Enter your AP EAPCET/AP ECET/TS EAMCET/TS ECET Rank'
                                ,'Engg. seat status','Are you a Day scholar/ Hostler?','Are you in WISE Programme?','Are you in C&DS Programme?'
                                ,'Which job do you prefer',"Parent's profile",'C&DS']]
    ai_placement_df = placement_df[['Regd. Number','Company','Package','Core/IT Sector','On/Off Campus']]
    ai_merged_data = pd.merge(ai_student_df, ai_placement_df, on='Regd. Number', how='left')
    # st.dataframe(ai_student_df.head(4))
    # st.dataframe(ai_placement_df.head(4))
    # st.dataframe(ai_merged_data.head(4))

###################


    st.divider()
    st.header("🤖 AI Placement Assistant")

    # Using \n\n for a clean line break in the info box as we discussed earlier!
    st.info("Ask me anything about the placement data! \n\n *(e.g., 'What is the average package for CSE?' or 'Show me the unplaced girls with no backlogs')*")

    try:
        # 1. Initialize the AI Brain
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=st.secrets["GEMINI_API_KEY"],
            temperature=0 # Low temperature keeps it factual
        )

        # 2. Create the LangChain Agent using your secure, merged data
        pandas_agent = create_pandas_dataframe_agent(
            llm, 
            ai_merged_data, 
            verbose=True, 
            allow_dangerous_code=True,
            handle_parsing_errors=True 
        )

        # 3. Initialize Chat Memory
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 4. Draw Previous Chat Bubbles and DataFrames
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "df" in message:
                    st.dataframe(message["df"])

        # 5. The Chat Input Box
        if prompt := st.chat_input("Ask a question about the placement data..."):
            
            # Show the user's question
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # --- INVISIBLE INSTRUCTIONS & DATA DICTIONARY ---
            secret_instructions = """
            \n\nINSTRUCTIONS FOR AI: 
            1. CRITICAL: If the user asks for a list, table, roster, or subset of students, DO NOT write or save any CSV files. 
            2. Instead, filter the dataframe and print out ONLY a clean, bulleted list of their 'Regd. Number' values directly in your text response.
            3. Keep your response direct, professional, and free of unnecessary introductory text (e.g., jump straight to the list of numbers).
            4. DATA DICTIONARY:
            - 'WISE Programme': A special empowerment program for female students.
            - 'C&DS': Stands for Career and Development Services.
            - 'Package': This represents the student's salary or CTC offer in LPA.
            - 'History of Backlogs': 0 means no backlogs, >0 means they have/had backlogs.
            """
            augmented_prompt = prompt + secret_instructions

            # 6. Generate AI Response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing placement data..."):
                    try:
                        # Run the agent with the hidden instructions
                        response = pandas_agent.run(augmented_prompt)
                        st.write(response)
                        
                        # Check if the AI generated a CSV file for us to display
                        extracted_df = None
                        if os.path.exists("temp_export.csv"):
                            extracted_df = pd.read_csv("temp_export.csv")
                            
                            # Display the native dataframe (users can hover to download!)
                            st.dataframe(extracted_df)
                            os.remove("temp_export.csv") # Clean up

                        # Save the response and the dataframe to memory
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": str(response),
                            **({"df": extracted_df} if extracted_df is not None else {})
                        })
                    
                    except Exception as e:
                        st.error(f"Sorry, I ran into an error analyzing that: {e}")

    except KeyError:
        st.warning("⚠️ Please add your GEMINI_API_KEY to your .streamlit/secrets.toml file.")