import pandas as pd
import re

# Step 1: Load and clean the log file
df = pd.read_csv("Android_2k.log_structured.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Clean timestamp (assuming there's a timestamp column)
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows with invalid timestamps
df = df.dropna(subset=['timestamp'])

# Step 2: Log Parsing (basic template mining using regex patterns)
def extract_template(log_message):
    # Replace numbers and hex codes with placeholders
    log_message = re.sub(r'\b\d+\b', '<NUM>', log_message)
    log_message = re.sub(r'0x[0-9A-Fa-f]+', '<HEX>', log_message)
    return log_message

if 'content' in df.columns:
    df['log_template'] = df['content'].astype(str).apply(extract_template)

# Step 3: Group logs by template
template_counts = df['log_template'].value_counts().reset_index()
template_counts.columns = ['log_template', 'count']

# Step 4: Save outputs
df.to_csv("cleaned_logs.csv", index=False)
template_counts.to_csv("log_templates.csv", index=False)

print("Log analysis completed. Outputs saved as cleaned_logs.csv and log_templates.csv")
