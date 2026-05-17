# --- HELPER FUNCTION: Indian Comma Formatting ---
import pandas as pd
def format_indian(num):
    if pd.isna(num):
        return "N/A"
    
    # Convert to integer first to remove the long trailing decimals
    num_str = str(int(num)) 
    
    if len(num_str) > 3:
        last_3 = num_str[-3:]
        rest = num_str[:-3]
        # Split the remaining numbers into chunks of 2
        rest_chunks = [rest[max(0, i-2):i] for i in range(len(rest), 0, -2)][::-1]
        return "₹ " + ",".join(rest_chunks) + "," + last_3
    
    return "₹ " + num_str

def custom_small_info(text):
    return f"""
                <div style="
                    background-color: rgba(64, 164, 244, 0.1); 
                    color: #40a4f4; 
                    padding: 12px; 
                    border-radius: 8px; 
                    font-size: 10px; /* <-- Your 10px font size is strictly enforced here! */
                ">
                    ℹ️ <i>{text}</i>
                </div>
                <br>
                """