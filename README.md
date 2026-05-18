# 🎓 College Placement Dashboard & AI Assistant

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

## 📌 Overview
The **College Placement Dashboard** is a powerful, interactive web application designed for college management and placement cell staff. It provides an immediate, visual "big picture" of student placement metrics, tracking everything from overall placement percentages to branch-wise salary trends. 

To elevate the experience, the dashboard features an integrated **AI Placement Assistant** powered by LangChain and Google Gemini. Users can ask natural language questions (e.g., *"What is the highest package in CSE?"*) and instantly receive answers, complete with dynamic data tables that can be downloaded locally.

## ✨ Key Features
* **Dynamic Data Loading:** Users can input their own Google Sheets export URLs directly via the UI, keeping them in full control of the data without hardcoded links.
* **Automated KPI Scorecards:** Instantly calculates Total Students, Placement Rate, Highest CTC, and Average CTC directly from the raw data.
* **Interactive Visualizations:** Includes pie charts for placement status and bar charts for branch-wise average packages using Matplotlib.
* **Conversational AI Agent:** A LangChain Pandas DataFrame Agent translates plain English queries into Python code, runs the math locally, and returns precise answers without sending the entire dataset to the cloud.
* **Privacy-First Design:** Strips Out Personally Identifiable Information (PII) before the data ever touches the AI agent's logic.
* **Native CSV Downloads:** If the AI is asked for a specific list of students, it generates a native Streamlit dataframe that users can natively search, sort, and download as a CSV.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.9+ installed and a package manager like `pip` or `conda`.

2. Clone the Repository
```
Bash
git clone https://github.com/srikanth-khandavalli/placements-dashboard.git
cd placements-dashboard
```
3. Install Dependencies
It is highly recommended to use a virtual environment (like Conda).
```
Bash
pip install -r requirements.txt
```
(The requirements.txt includes: streamlit, pandas, matplotlib, st-gsheets-connection, langchain, langchain-experimental, langchain-google-genai).

4. Configure API Secrets
The AI assistant requires a Google Gemini API Key.

Create a hidden folder in the root directory named .streamlit.

Inside it, create a file named secrets.toml.

Add your key securely:
```
Ini, TOML
GEMINI_API_KEY = "your_actual_api_key_here"
```
Note: Ensure .streamlit/secrets.toml is in your .gitignore to prevent leaking keys!.

5. Run the Application
```
Bash
streamlit run dashboard.py
```
📊 Data Formatting Guide (Google Sheets)
Because this app bypasses complex Google Cloud Service accounts for simplicity, the Google Sheet must be set to "Anyone with the link" (Viewer).


Important: When pasting URLs into the dashboard, users must use the direct CSV export format, replacing the standard Google Drive link with the unique gid for each specific tab.

Format: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv&gid=YOUR_TAB_GID

🚧 Development Pitfalls & Solutions (Lessons Learned)
Documented for future reference and maintenance.

1. The "Dependency Hell" of PandasAI

Pitfall: Initial attempts to use pandasai threw massive build errors (ModuleNotFoundError: No module named 'pkg_resources') because it required an outdated version of Pandas (1.5.3) incompatible with modern setuptools.

Solution: Completely pivoted from PandasAI to LangChain and its create_pandas_dataframe_agent. LangChain is the modern industry standard and integrates flawlessly with modern Pandas 2.0+.

2. Streamlit's Disappearing Nested Buttons
Pitfall: We placed the AI Chat initialization inside an if st.button("Load AI Assistant"): block, which was nested inside a "Load Dashboard" button. When the user pressed "Enter" in the chat, the page re-ran, registered the buttons as False, and completely erased the chat interface.

Solution: Implemented Session State (st.session_state). We transformed the buttons into switches that permanently save a True state to Streamlit's memory, ensuring the UI survives page re-runs.

3. NameError on Agent Initialization
Pitfall: We tried pulling the AI Agent completely out of the button blocks to fix the disappearing issue. However, the app immediately crashed with a NameError: name 'ai_merged_data' is not defined because the AI tried to read the dataset before the user actually clicked "Load Dashboard".

Solution: Moved the AI initialization code to be indented inside the main if st.session_state.dashboard_loaded: block. This guarantees the data variables exist before the LangChain agent attempts to analyze them.

4. Mathematical Operations on Strings (Cannot perform reduction 'mean')

Pitfall: Attempting to calculate the average package (avg_ctc = placements_df['Package'].mean()) threw an error because the clerk typed values like "12.5 LPA" into Google Sheets, causing Pandas to treat the entire column as text.


Solution: Applied a data cleaning pipeline using Regex to strip non-numeric characters (.str.replace(r'[^\d.]', '', regex=True)), followed by pd.to_numeric() to force the column into mathematical floats.

5. merge() vs join() Type Crashes
Pitfall: Attempting to combine the student counts and placement counts using .join() threw the error: You are trying to merge on str and int64 columns. join() attempts to link columns to hidden row index numbers.


Solution: Replaced .join() with pd.merge(df1, df2, on='Branch', how='left'), which acts safely like a SQL LEFT JOIN and explicitly links matching string columns together.

6. The Pluralization Typo (KeyError)
Pitfall: A bug where the row numbers and calculations weren't appearing in the final UI. This happened because we sorted data into a singular placement_df variable but accidentally added our new columns to an older plural placements_df variable.


Solution: Standardized variable naming throughout the entire codebase, strictly ensuring pluralization (placements_df) was used everywhere to prevent fragmented memory.

7. Custom HTML CSS Mismatches
Pitfall: Tried to build a custom HTML "Copy" button (copy_component.html). However, because it was hardcoded with a white background, it clashed horribly with Streamlit's global Dark Mode theme.


Solution: Scrapped the custom HTML entirely and used Streamlit's native st.code() widget, which automatically handles clipboard security, line breaks, and natively adapts to both Light and Dark themes instantly.

8. Python String Syntax Errors (Apostrophes)

Pitfall: Extracting the column 'Parent's profile' caused a syntax crash because the apostrophe tricked Python into thinking the string ended prematurely.


Solution: Used double quotes " around that specific column name ("Parent's profile") to securely wrap the single quote.

9. Streamlit Markdown Line Breaks

Pitfall: Standard \n characters were not forcing text to the next line inside st.info() boxes.


Solution: Standardized on using Double Newlines (\n\n) for clean paragraph breaks, or wrapping text blocks in multi-line triple quotes """.

10. VS Code Conda Environment Activation

Pitfall: VS Code's terminal defaulted to the (base) environment upon every restart, failing to recognize installed packages.


Solution: Used the VS Code Command Palette (Ctrl + Shift + P) -> Python: Select Interpreter, and manually pointed the workspace to the exact path of the dashboards conda environment executable.