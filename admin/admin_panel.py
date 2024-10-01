import pandas as pd
import os

def admin_panel():
    st.title("Admin Panel - Upload Dataset")

    # Text input for dataset name and description
    dataset_name = st.text_input("Enter dataset name")
    dataset_description = st.text_area("Dataset description")

    # File uploader for CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:", data.head())

        if st.button("Save Dataset"):
            data_path = f"datasets/{dataset_name}.csv"
            os.makedirs("datasets", exist_ok=True)
            data.to_csv(data_path, index=False)
            st.success(f"Dataset '{dataset_name}' saved successfully!")

if st.session_state['logged_in']:
    admin_panel()
