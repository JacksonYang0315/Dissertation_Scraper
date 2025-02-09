import pandas as pd

# Load the provided Excel file
file_path = 'Fully Remote Organizations.xlsx'  # Ensure this is the correct path to your downloaded file
data = pd.read_excel(file_path)

# Clean the data
cleaned_data = data.drop([0, 1]).reset_index(drop=True)
cleaned_data.columns = ["Company Name", "Company Size", "Website", "Overview", "Founded", "Industry", "Size", "Unknown"]
cleaned_data = cleaned_data.drop(columns=["Unknown"])

# Categorize the company size for easier stratification
cleaned_data['Company Size Category'] = pd.cut(cleaned_data['Size'], 
                                               bins=[0, 50, 200, 500, 1000, 5000], 
                                               labels=['1-50', '51-200', '201-500', '501-1000', '1001+'])

# Determine the number of unique categories in the 'Company Size Category'
unique_categories = cleaned_data['Company Size Category'].unique()

# Calculate the number of samples needed per category
samples_per_category = 100 // len(unique_categories)

# Perform equal sampling from each category
sampled_frames = []

for category in unique_categories:
    category_frame = cleaned_data[cleaned_data['Company Size Category'] == category]
    sampled_frame = category_frame.sample(n=min(samples_per_category, len(category_frame)), replace=False, random_state=42)
    sampled_frames.append(sampled_frame)

# Combine all sampled frames
equal_sampled_data = pd.concat(sampled_frames)

# If the total number of samples is less than 100, fill the gap by sampling additional companies proportionally from all categories
if len(equal_sampled_data) < 100:
    additional_samples_needed = 100 - len(equal_sampled_data)
    additional_samples = cleaned_data.sample(n=additional_samples_needed, replace=False, random_state=42)
    equal_sampled_data = pd.concat([equal_sampled_data, additional_samples])

# Save the new equally stratified sample to a new Excel file
equal_sampled_file_path = 'Equal_Stratified_Sample_Fully_Remote_Organizations.xlsx'
equal_sampled_data.to_excel(equal_sampled_file_path, index=False)

print(f"File saved as {equal_sampled_file_path}")