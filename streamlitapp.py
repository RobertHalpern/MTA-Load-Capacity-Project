import streamlit as st
# import pandas as pd

# def main():
#     # Set the title of the web page
#     st.title('Your Website Title Here')

#     # Instructions or description
#     st.write("Please upload a text file to view it as a table.")

#     # Create a file uploader widget in the sidebar
#     uploaded_file = st.sidebar.file_uploader("Choose a text file", type=["txt"])

#     if uploaded_file is not None:
#         try:
#             # Assuming the file is in a simple CSV-like format
#             # Create a DataFrame
#             df = pd.read_csv(uploaded_file)
            
#             # Display the DataFrame
#             st.write("Here's the data from your file:")
#             st.dataframe(df)

#             for row in df
#                 if column ['Detected'] > '2':
#                     st.write(f"Camera 1 detected {row['person_count']} persons.")

#         except Exception as e:
#             st.error(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Helper function to get color based on percentage full
def get_color(percentage):
    norm = mpl.colors.Normalize(vmin=0, vmax=100)
    color_map = mpl.colors.LinearSegmentedColormap.from_list("", ["white", "red"])
    return mpl.colors.rgb2hex(color_map(norm(percentage)))

def main():
    st.title('Subway Car Occupancy Visualization')

    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload your output.txt", type="txt")
    if uploaded_file is not None:
        # Read the data from the file, trimming spaces from headers
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()  # Strip whitespace from column headers

        # Debug: Print column names to help ensure they are what we expect
        st.write("Column names:", data.columns.tolist())

        # Assuming 200 is the max capacity of a subway car
        max_capacity = 200
        try:
            data['Percent Full'] = (data['Detected Count'] / max_capacity) * 100
            data['Color'] = data['Percent Full'].apply(get_color)
            
            # Displaying the DataFrame
            st.write("Data from uploaded file:")
            st.dataframe(data.style.applymap(lambda x: f'background-color: {x}' if isinstance(x, str) else ''))

            # Plotting
            fig, ax = plt.subplots()
            ax.bar(data['Source Camera'], data['Percent Full'], color=data['Color'])
            plt.xlabel('Source Camera')
            plt.ylabel('Percent Full')
            plt.title('Visualization of Subway Car Fullness')
            st.pyplot(fig)
        except KeyError as e:
            st.error(f"Column not found in data: {e}")

if __name__ == "__main__":
    main()
