import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment- By Kailee Zeltner, Due Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)


# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")


#Add a drop down for Category
Categories = {
    'Furniture' : ['Bookcases', 'Chairs', 'Furnishings', 'Tables'],
    'Office Supplies' : ['Applicanes', 'Art', 'Binders', 'Envelopes', 'Fasteners', 'Labels', 'Paper', 'Storage', 'Supplies'],
    'Technology' : ['Accessories', 'Copiers', 'Machines', 'Phones']
}

category = st.selectbox('Which category are you interested in?', list(Categories.keys()))

#Add a multi select for Sub Category
if category:
    subcategory = st.multiselect('Which sub-category are you interested in?:', Categories[category])
     # Show selected options
    st.write(f'You selected {category} with sub-categories: {subcategory}')


# Show a line chart of sales for the selected items
if subcategory:
    # Filter based on selected subcategories
    filtered_df = df[df['Sub_Category'].isin(subcategory)]
    
    # Group by month and sum the sales for each subcategory
    selected_sales = filtered_df.set_index('Order_Date').groupby([pd.Grouper(freq='M'), 'Sub_Category'])['Sales'].sum().unstack()
    
    # Show a line chart for the selected subcategories
    st.write(f"Line chart for {', '.join(filtered_df)}")
    st.line_chart(selected_sales)
    
st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
