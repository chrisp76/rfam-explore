import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import sqlparse
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter

st.set_page_config(page_title="Rfam Database Explorer", layout="wide")

# Add custom CSS to improve text readability
st.markdown("""
<style>
/* Make SQL input text area more readable */
.stTextArea textarea {
    color: #FFFFFF !important;
    background-color: #1E1E1E !important;
    font-family: monospace !important;
    font-size: 14px !important;
}

/* Make filter fields wider and more readable */
.stSelectbox, .stTextInput {
    min-width: 100% !important;
}

/* Adjust sidebar width */
[data-testid="stSidebar"] {
    min-width: 350px !important;
    width: 350px !important;
}

/* Enhance styling for query results and syntax highlighting */
.highlight {
    background-color: #272822 !important;
    padding: 10px !important;
    border-radius: 5px !important;
}
.highlight pre {
    color: #F8F8F2 !important;
}
</style>
""", unsafe_allow_html=True)

# Add syntax highlighting CSS
def get_syntax_highlighted_sql(sql):
    formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
    highlighted = highlight(formatted_sql, SqlLexer(), HtmlFormatter(style='monokai'))
    return '<style>' + HtmlFormatter().get_style_defs(".highlight") + '</style>' + highlighted

# Connect to DuckDB
@st.cache_resource
def get_duckdb_connection():
    return duckdb.connect('direct_copy.duckdb')

conn = get_duckdb_connection()

st.title("Rfam Database Explorer")

# Sidebar for table selection
st.sidebar.header("Table Selection")
tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
table_names = [table[0] for table in tables]
selected_table = st.sidebar.selectbox("Choose a table", table_names)

if selected_table:
    st.header(f"{selected_table} Table")
    
    # Get column names
    columns = conn.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}'").fetchall()
    column_names = [col[0] for col in columns]
    
    # Sidebar for column selection
    selected_columns = st.sidebar.multiselect(
        "Select columns to display",
        column_names,
        default=column_names[:5]
    )
    
    # Advanced query builder
    st.sidebar.header("Filters")
    filter_conditions = []
    
    num_filters = st.sidebar.number_input("Number of filters", min_value=0, max_value=5, value=1)
    for i in range(num_filters):
        # Changed from 3 columns to 1 column per row for better readability
        st.sidebar.markdown(f"**Filter #{i+1}**")
        
        filter_column = st.sidebar.selectbox(
            "Column",
            ["None"] + column_names,
            key=f"filter_col_{i}"
        )
        
        operator = st.sidebar.selectbox(
            "Operator",
            ["=", "!=", ">", "<", "LIKE", "IN"],
            key=f"filter_op_{i}"
        )
        
        filter_value = st.sidebar.text_input(
            "Value",
            key=f"filter_val_{i}"
        )
        
        st.sidebar.markdown("---")
            
        if filter_column != "None" and filter_value:
            if operator == "LIKE":
                filter_conditions.append(f"{filter_column} LIKE '%{filter_value}%'")
            elif operator == "IN":
                values = [v.strip() for v in filter_value.split(',')]
                # Fixing the f-string backslash issue - avoid using replace in f-string
                quoted_values = []
                for val in values:
                    # Properly escape single quotes for SQL
                    safe_val = val.replace("'", "''")
                    quoted_values.append(f"'{safe_val}'")
                in_values_str = ",".join(quoted_values)
                filter_conditions.append(f"{filter_column} IN ({in_values_str})")
            else:
                filter_conditions.append(f"{filter_column} {operator} '{filter_value}'")
    
    where_clause = " AND ".join(filter_conditions)
    if where_clause:
        where_clause = "WHERE " + where_clause
    
    # Number of rows to display
    rows_to_display = st.sidebar.number_input("Number of rows to display", min_value=1, max_value=1000, value=10)
    
    # Execute query
    query = f"SELECT {', '.join(selected_columns)} FROM {selected_table} {where_clause} LIMIT {rows_to_display}"
    
    # Display formatted SQL
    st.subheader("Generated SQL Query")
    st.markdown(get_syntax_highlighted_sql(query), unsafe_allow_html=True)
    
    df = conn.execute(query).df()
    
    # Display basic statistics
    st.subheader("Table Statistics")
    col1, col2 = st.columns(2)
    with col1:
        total_rows = conn.execute(f"SELECT COUNT(*) FROM {selected_table}").fetchone()[0]
        st.metric("Total Rows", total_rows)
    with col2:
        filtered_rows = len(df)
        st.metric("Filtered Rows", filtered_rows)
    
    # Display the data
    st.subheader("Data Preview")
    st.dataframe(df)
    
    # Enhanced visualizations
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    if len(numeric_columns) > 0 or len(categorical_columns) > 0:
        st.subheader("Advanced Visualizations")
        viz_type = st.selectbox(
            "Choose visualization",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Histogram", "Pie Chart"],
            key="viz_selector"
        )
        
        if viz_type == "Bar Chart":
            x_col = st.selectbox("Select X axis", categorical_columns)
            y_col = st.selectbox("Select Y axis", numeric_columns)
            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            st.plotly_chart(fig)
            
        elif viz_type == "Line Chart":
            x_col = st.selectbox("Select X axis", df.columns)
            y_col = st.selectbox("Select Y axis", numeric_columns)
            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            st.plotly_chart(fig)
            
        elif viz_type == "Scatter Plot":
            x_col = st.selectbox("Select X axis", numeric_columns)
            y_col = st.selectbox("Select Y axis", numeric_columns)
            color_col = st.selectbox("Color by (optional)", ["None"] + list(categorical_columns))
            if color_col == "None":
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            else:
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col} by {color_col}")
            st.plotly_chart(fig)
            
        elif viz_type == "Box Plot":
            x_col = st.selectbox("Select grouping column", categorical_columns)
            y_col = st.selectbox("Select value column", numeric_columns)
            fig = px.box(df, x=x_col, y=y_col, title=f"Distribution of {y_col} by {x_col}")
            st.plotly_chart(fig)
            
        elif viz_type == "Histogram":
            col = st.selectbox("Select column", numeric_columns)
            bins = st.slider("Number of bins", min_value=5, max_value=50, value=20)
            fig = px.histogram(df, x=col, nbins=bins, title=f"Distribution of {col}")
            st.plotly_chart(fig)
            
        elif viz_type == "Pie Chart":
            col = st.selectbox("Select column", categorical_columns)
            values_col = st.selectbox("Select values", numeric_columns)
            fig = px.pie(df, names=col, values=values_col, title=f"{values_col} by {col}")
            st.plotly_chart(fig)
    
    # Custom SQL query with syntax highlighting
    st.subheader("Custom SQL Query")
    custom_query = st.text_area("Enter your SQL query", query)
    st.markdown(get_syntax_highlighted_sql(custom_query), unsafe_allow_html=True)
    
    if st.button("Run Query"):
        try:
            result_df = conn.execute(custom_query).df()
            st.dataframe(result_df)
        except Exception as e:
            st.error(f"Error executing query: {e}") 