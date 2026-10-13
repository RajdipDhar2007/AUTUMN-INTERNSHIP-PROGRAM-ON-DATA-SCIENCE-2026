import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="DuckDB SQL Explorer", page_icon="🦆", layout="wide")

st.markdown("""
<style>
    .title     { color: #e74c3c; font-size: 2rem; font-weight: 800; }
    .section   { color: #2980b9; font-size: 1.4rem; font-weight: 700; margin-top: 10px; }
    .subhead   { color: #8e44ad; font-size: 1.1rem; font-weight: 600; }
    .result-box{
        background: #f0f4ff;
        border-left: 5px solid #2980b9;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        color: #1a1a2e;
        margin-top: 6px;
    }
    .table-label {
        background: #eafaf1;
        border-left: 5px solid #27ae60;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 14px;
        color: #1a1a2e;
        margin: 8px 0 4px 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# helper functions for connection, queries, and table management
def get_con():
    if "con" not in st.session_state:
        st.session_state["con"] = duckdb.connect(database=":memory:")
    return st.session_state["con"]

def table_exists(con, name):
    res = con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?", [name]
    ).fetchone()
    return res[0] > 0

def run_query(con, sql):
    sql = sql.strip().rstrip(";")
    if not sql:
        return None, "Empty query."
    try:
        result = con.execute(sql)
        if result.description:
            return result.df(), None
        return None, "Query executed successfully (no rows returned)."
    except Exception as e:
        return None, str(e)

def show_current_table(con, label="📋 Current table state after operation:"):
    """Always show the live state of the employees table."""
    if table_exists(con, "employees"):
        st.markdown(f'<div class="table-label">{label}</div>', unsafe_allow_html=True)
        current = con.execute("SELECT * FROM employees").df()
        st.dataframe(current, use_container_width=True)
        st.caption(f"Rows: {len(current)} · Columns: {len(current.columns)}")
    else:
        st.warning("Table 'employees' does not exist anymore.")

def restore_table(con, df):
    con.execute("DROP TABLE IF EXISTS employees")
    con.register("_df_temp", df)
    con.execute("CREATE TABLE employees AS SELECT * FROM _df_temp")
    con.unregister("_df_temp")

#sidebar
with st.sidebar:
    st.title("🦆 DuckDB Explorer")
    st.markdown("---")
    st.markdown("**Sections**")
    st.markdown("""
- 📂 Upload & Preview
- 🏗️ DDL Queries
- ✏️ DML Queries
- 💬 Custom SQL
- 📊 Quick Stats
""")
    st.markdown("---")
    use_persistent = st.checkbox("💾 Use Persistent DB (duckdb_file.duckdb)")
    if use_persistent:
        if "persistent_con" not in st.session_state:
            st.session_state["persistent_con"] = duckdb.connect("duckdb_file.duckdb")
        st.success("Connected to persistent DuckDB.")
    st.markdown("---")
    st.caption("DuckDB SQL Explorer · Streamlit")

# main page
st.markdown('<p class="title">🦆 DuckDB SQL Explorer</p>', unsafe_allow_html=True)
st.markdown("Upload a CSV, then run DDL, DML, and advanced SQL queries interactively.")
st.divider()

# upload & preview
st.markdown('<p class="section">📂 Upload & Preview</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a CSV or Parquet file", type=["csv", "parquet"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_parquet(uploaded_file)

    st.session_state["df"] = df
    st.success(f"✅ **{uploaded_file.name}** loaded — {df.shape[0]} rows × {df.shape[1]} columns")

    st.markdown('<div class="table-label">📋 Uploaded dataset:</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    con = get_con()
    restore_table(con, df)
    st.session_state["table_ready"] = True

    if use_persistent and "persistent_con" in st.session_state:
        pcon = st.session_state["persistent_con"]
        restore_table(pcon, df)
        st.sidebar.success("Data saved to persistent DB as 'employees'.")

else:
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.info("Using previously uploaded data.")
    else:
        st.info("👆 Upload a CSV or Parquet file to begin.")
        st.stop()

st.divider()

con = get_con()
if not table_exists(con, "employees"):
    restore_table(con, df)

numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

#DDL
st.markdown('<p class="section">🏗️ DDL — Data Definition Language</p>', unsafe_allow_html=True)
st.markdown("Queries that define or change the **structure** of tables.")

ddl_queries = {
    "1. View current table structure": "DESCRIBE employees",
    "2. Add column (email)":           "ALTER TABLE employees ADD COLUMN IF NOT EXISTS email VARCHAR",
    "3. Rename salary → annual_salary":"ALTER TABLE employees RENAME salary TO annual_salary",
    "4. Rename annual_salary → salary":"ALTER TABLE employees RENAME annual_salary TO salary",
    "5. Drop column email":            "ALTER TABLE employees DROP COLUMN IF EXISTS email",
    "6. Show all tables in DB":        "SHOW TABLES",
}

ddl_choice = st.selectbox("Choose a DDL query", list(ddl_queries.keys()), key="ddl_sel")
ddl_sql    = ddl_queries[ddl_choice]
st.code(ddl_sql, language="sql")

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Run DDL Query", key="run_ddl"):
        result, msg = run_query(con, ddl_sql)
        if result is not None:
            # DESCRIBE / SHOW TABLES — show query result first
            st.markdown('<div class="table-label">🔍 Query result:</div>', unsafe_allow_html=True)
            st.dataframe(result, use_container_width=True)
        else:
            st.success(msg)
        # Always show table state after any DDL
        show_current_table(con)

with col2:
    if st.button("🔄 Restore Table", key="restore_ddl"):
        restore_table(con, df)
        st.success("✅ Table restored to original.")
        show_current_table(con)

st.divider()

#DML
st.markdown('<p class="section">✏️ DML — Data Manipulation Language</p>', unsafe_allow_html=True)
st.markdown("Queries that **read or change the data** inside the table.")

dml_queries = {
    "1. SELECT all rows":
        "SELECT * FROM employees",
    "2. SELECT specific columns":
        "SELECT name, department, salary FROM employees",
    "3. SELECT with WHERE (IT dept)":
        "SELECT * FROM employees WHERE department = 'IT'",
    "4. SELECT with multiple conditions (age<28 AND salary <65000)":
        "SELECT * FROM employees WHERE age <28 AND salary <65000",
    "5. SELECT ORDER BY salary DESC":
        "SELECT * FROM employees ORDER BY salary DESC",
    "6. SELECT with LIMIT 3":
        "SELECT * FROM employees ORDER BY salary DESC LIMIT 3",
    "7. Aggregate per department":
        """SELECT department,
       COUNT(*)             AS headcount,
       ROUND(AVG(salary),2) AS avg_salary,
       MAX(salary)          AS max_salary,
       MIN(salary)          AS min_salary,
       SUM(salary)          AS total_salary
FROM employees
GROUP BY department
ORDER BY total_salary DESC""",
    "8. INSERT a new employee":
        "INSERT INTO employees (id, name, age, salary, department) VALUES (6, 'Frank', 33, 72000, 'Finance')",
    "9. UPDATE salary for id=1":
        "UPDATE employees SET salary = 70000 WHERE id = 1",
    "10. UPDATE — 10% raise for IT":
        "UPDATE employees SET salary = salary * 1.10 WHERE department = 'IT'",
    "11. DELETE employee with id=6":
        "DELETE FROM employees WHERE id = 6",
    "12. DELETE all rows":
        "DELETE FROM employees WHERE 1=1",
    "13. Restore original data":
        "__restore__",
}

dml_choice = st.selectbox("Choose a DML query", list(dml_queries.keys()), key="dml_sel")
dml_sql    = dml_queries[dml_choice]

if dml_sql != "__restore__":
    st.code(dml_sql, language="sql")
else:
    st.info("This will restore the table back to the originally uploaded data.")

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Run DML Query", key="run_dml"):

        if dml_sql == "__restore__":
            restore_table(con, df)
            st.success("✅ Table restored to original uploaded data.")
            show_current_table(con)

        else:
            result, msg = run_query(con, dml_sql)

            # SELECT-type — show query result + current table below
            if result is not None:
                st.markdown('<div class="table-label">🔍 Query result:</div>', unsafe_allow_html=True)
                st.dataframe(result, use_container_width=True)
                st.caption(f"{len(result)} row(s) returned.")
                # For SELECT queries, current table = same as result (no change)
                # so only show separately if it was a non-full-table select
                if "WHERE" in dml_sql.upper() or "LIMIT" in dml_sql.upper() or "GROUP" in dml_sql.upper():
                    show_current_table(con, "📋 Full table for reference:")

            # Write operation — show success + always show updated table
            else:
                st.success(msg)
                show_current_table(con)

with col2:
    if st.button("🔄 Restore Table to Original", key="restore_dml"):
        restore_table(con, df)
        st.success("✅ Table restored.")
        show_current_table(con)

st.divider()

# custom SQL
st.markdown('<p class="section">💬 Custom SQL</p>', unsafe_allow_html=True)
st.markdown("Write and run any SQL query against the **employees** table.")

custom_sql = st.text_area(
    "Your SQL query",
    value="SELECT * FROM employees LIMIT 10",
    height=140,
    key="custom_sql"
)

if st.button("▶ Execute", key="run_custom", type="primary"):
    result, msg = run_query(con, custom_sql)
    if result is not None:
        st.markdown('<div class="table-label">🔍 Query result:</div>', unsafe_allow_html=True)
        st.dataframe(result, use_container_width=True)
        st.caption(f"{len(result)} row(s) returned.")
        st.download_button(
            "⬇️ Download Result as CSV",
            result.to_csv(index=False),
            "query_result.csv",
            "text/csv"
        )
    else:
        if "successfully" in str(msg).lower():
            st.success(msg)
            # Show updated table after any write custom query
            show_current_table(con)
        else:
            st.error(f"❌ {msg}")

st.divider()

# stats on numeric columns
st.markdown('<p class="section">📊 Quick Stats</p>', unsafe_allow_html=True)

if numeric_cols:
    selected_col = st.selectbox("Choose a numeric column", numeric_cols, key="stats_col")
    stats_sql = f"""
SELECT
    COUNT(*)                     AS row_count,
    ROUND(AVG({selected_col}), 2)    AS average,
    MIN({selected_col})          AS min_value,
    MAX({selected_col})          AS max_value,
    ROUND(STDDEV({selected_col}), 2) AS std_dev
FROM employees
"""
    st.code(stats_sql.strip(), language="sql")
    result, msg = run_query(con, stats_sql)
    if result is not None:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Row Count", int(result["row_count"][0]))
        c2.metric("Average",   result["average"][0])
        c3.metric("Min",       result["min_value"][0])
        c4.metric("Max",       result["max_value"][0])
        c5.metric("Std Dev",   result["std_dev"][0])
else:
    st.warning("No numeric columns available for stats.")