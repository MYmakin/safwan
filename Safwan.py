import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Page configuration
st.set_page_config(page_title="Business Analytics Dashboard", layout="wide", page_icon="📊")

st.markdown(
    """
    <style>
    :root {
        --background-color: #f5f7fa;
        --font-family: 'Arial', sans-serif;
        --primary-color: #4caf50; /* Green for primary highlights */
        --secondary-color: #3f51b5; /* Blue for secondary highlights */
        --tertiary-color: #ff9800; /* Orange for accents */
        --text-color: #34495e; /* Dark grey for text */
        --card-background: #ffffff; /* White for card backgrounds */
        --box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Elevated shadow */
        --border-radius: 12px; /* Slightly larger for a modern look */
        --padding: 12px;
        --hover-color: rgba(63, 81, 181, 0.1); /* Hover effect for cards */
    }

    body {
        background-color: var(--background-color);
        font-family: var(--font-family);
    }

    .block-container {
        padding: 2rem;
    }

    .sidebar .sidebar-content {
        background-color: var(--secondary-color);
        color: white;
    }

    .sidebar .sidebar-content a {
        color: white;
        text-decoration: none;
    }

    .sidebar .sidebar-content a:hover {
        color: var(--tertiary-color);
        text-decoration: underline;
    }

    .title {
        color: var(--primary-color);
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        font-size: 2rem;
    }

    .subheader {
        color: var(--secondary-color);
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        font-size: 1.5rem;
    }

    .metric {
        text-align: center;
        font-size: 1.1rem;
        color: var(--text-color);
        background-color: var(--card-background);
        padding: var(--padding);
        border-radius: var(--border-radius);
        margin: 5px;
        box-shadow: var(--box-shadow);
        transition: transform 0.2s, background-color 0.2s;
    }

    .metric:hover {
        transform: translateY(-5px);
        background-color: var(--hover-color);
    }

    .metric h4 {
        margin: 0;
        font-size: 1rem;
        color: var(--secondary-color);
    }

    .metric p {
        margin: 5px 0 0;
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--primary-color);
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

    .title {
        font-family: 'Poppins', sans-serif;
        color: #ffffff; /* Set the color of the title to white */
        background: linear-gradient(90deg, #000000, #212121); /* Dark gradient background */
        padding: 20px 30px;
        border-radius: 10px;
        text-align: center;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Darker shadow for better contrast */
        margin-bottom: 30px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25); /* Slightly darker shadow */
    }

    .title span {
        color: #F39C12; /* Keeping the orange color for highlights */
        font-weight: 700;
    }

    @media (max-width: 768px) {
      .title {
        font-size: 1.8rem;
        padding: 15px 20px;
      }
    }
    </style>

    <div class='title'>Welcome to <span>Flytec Tours & Travels</span> Dashboard</div>
    """,
    unsafe_allow_html=True
)


# Define navigation options
options = st.sidebar.radio(
    label="Choose a section:",
    options=["Overview", "Top Transactions", "Data Preview"],
    index=0,  # Default selection
    format_func=lambda x: f"🔹 {x}",  # Add an icon prefix for better UI
    horizontal=False,  # Ensures vertical radio button layout
)

# Additional spacing for aesthetics with enhanced styling
st.sidebar.markdown(
    """
    <style>
    hr {
        border: 0;
        border-top: 1px solid #ddd;
        margin: 20px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    <hr>
    """,
    unsafe_allow_html=True
)

# File upload section
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

# Helper function to check required columns
def validate_columns(df, required_columns):
    return all(col in df.columns for col in required_columns)

# Helper function to convert DataFrame to CSV
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

if uploaded_file:
    try:
        # Read uploaded file
        df = pd.read_csv(uploaded_file)

        # Required columns for analysis
        required_columns = ['Profit', 'Sale', 'Payment Mode','Net Cost']

        if validate_columns(df, required_columns):
            # Data preprocessing
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
            df['Sale'] = pd.to_numeric(df['Sale'], errors='coerce')
            df['Net Cost'] = pd.to_numeric(df['Net Cost'], errors='coerce')

            # Compute metrics
            total_net_cost=df['Net Cost'].sum()
            total_profit = df['Profit'].sum()
            total_sales = df['Sale'].sum()
            cash_payment = df[df['Payment Mode'].str.contains('CASH', case=False, na=False)]['Sale'].sum()
            card_payment = df[df['Payment Mode'].str.contains('CARD', case=False, na=False)]['Sale'].sum()
            refund = df[df['Payment Mode'].str.contains('REFUND', case=False, na=False)]['Sale'].sum()
            stc_pay = df[df['Payment Mode'].str.contains('STCPAY', case=False, na=False)]['Sale'].sum()
            cash_card = df[df['Payment Mode'].str.contains('CASH/+CARD', case=False, na=False)]['Sale'].sum()
            average_profit = df['Profit'].mean()

            # Count transactions by payment mode
            transaction_count = df[df['Payment Mode'].str.contains('CASH|CARD|REFUND', case=False, na=False)]['Payment Mode'].value_counts()

            # Navigation options
            if options == "Overview":
                st.markdown("<h2 class='subheader'>Key Metrics Overview</h2>", unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                col1.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Total Net Cost</h4>
                        <p>SAR {total_net_cost:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col2.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Total Sales</h4>
                        <p>SAR {total_sales:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col3.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Total Profit</h4>
                        <p>SAR {total_profit:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col4.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Average Profit</h4>
                        <p>SAR {average_profit:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("<h3 class='subheader'>Payment Breakdown</h3>", unsafe_allow_html=True)
                col1, col2, col3,col4 = st.columns(4)
                col1.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Cash Payments</h4>
                        <p>SAR {cash_payment:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col2.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Card Payments & STCPAY</h4>
                        <p>SAR {card_payment:,.2f} & SAR {stc_pay:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col3.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Refunds</h4>
                        <p>SAR {refund:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col4.markdown(
                    f"""
                    <div class='metric'>
                        <h4>Cash + Card Payments</h4>
                        <p>SAR{cash_card:,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                style_metric_cards()


            elif options == "Top Transactions":

                # Styled Subheader

                st.markdown("<h2 style='color: #2E86C1;'>Top Transactions</h2>", unsafe_allow_html=True)

                # Interactivity: Number of Top Transactions

                st.write("### Customize Number of Transactions")

                num_transactions = st.slider("Select the number of top transactions to display:", 1, 20, 5)

                # Top Transactions by Sale

                st.write(f"### Top {num_transactions} Transactions by Sale")

                top_sales = df.nlargest(num_transactions, 'Sale')

                st.dataframe(top_sales)

                # Visualize Top Transactions by Sale

                st.write("#### Sales Chart")

                st.bar_chart(
                    top_sales.set_index('Date')['Sale'])  # Replace 'Transaction ID' with the relevant column

                # Top Transactions by Profit

                st.write(f"### Top {num_transactions} Transactions by Profit")

                top_profit = df.nlargest(num_transactions, 'Profit')

                st.dataframe(top_profit)

                # Visualize Top Transactions by Profit

                st.write("#### Profit Chart")

                st.bar_chart(top_profit.set_index('Date')[
                                 'Profit'])  # Replace 'Transaction ID' with the relevant column



            elif options == "Data Preview":

                # Styled Subheader
                st.markdown("<h2 style='color: #2E86C1;'>Data Explorer</h2>", unsafe_allow_html=True)

                # Interactive Filter Section
                st.write("### Interactive Data Filtering")

                # Multiselect to choose columns
                selected_columns = st.multiselect(
                    "Select columns to view:",
                    options=df.columns.tolist(),
                    default=df.columns.tolist()
                )

                # Apply selected columns filter
                filtered_df = df[selected_columns]

                # Optional Search by Keyword
                keyword = st.text_input("Search for a keyword (case-insensitive):")

                if keyword:
                    # Filtering rows based on keyword match in any column
                    filtered_df = filtered_df[
                        filtered_df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
                    ]

                # Display the number of rows after filtering
                st.markdown(f"*Found {filtered_df.shape[0]} rows matching the criteria.*", unsafe_allow_html=True)

                # Display Filtered Dataframe with an option to see more rows
                st.write("### Filtered Dataframe")
                st.dataframe(filtered_df.head(10))  # Show first 10 rows for better performance

                # Data Summary Section with expand functionality
                st.write("### Data Summary")
                with st.expander("See Summary Statistics"):
                    st.write(filtered_df.describe())

                # Download Filtered Data
                st.write("### Download Filtered Data")


                # Function to convert dataframe to CSV format
                @st.cache_data
                def convert_df_to_csv(dataframe):
                    return dataframe.to_csv(index=False).encode('utf-8')


                # Generate the CSV for download
                csv_data = convert_df_to_csv(filtered_df)

                # Style the download button
                st.markdown(
                    """
                    <style>
                    .download-btn {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 20px;
                        border-radius: 5px;
                        font-size: 1rem;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
                    }
                    .download-btn:hover {
                        background-color: #45a049;
                    }
                    </style>
                    """, unsafe_allow_html=True
                )

                # Display the download button
                st.download_button(
                    label="Download Filtered Data as CSV",
                    data=csv_data,
                    file_name="filtered_data.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download-btn",
                    help="Click to download the filtered data as a CSV file.",
                )

            # Download processed data
            csv_download = convert_df_to_csv(df)
            st.sidebar.download_button(
                label="Download Processed CSV",
                data=csv_download,
                file_name="processed_data.csv",
                mime="text/csv",
            )
        else:
            st.error(f"The uploaded CSV must include the following columns: {', '.join(required_columns)}.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to proceed.")