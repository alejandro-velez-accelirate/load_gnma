import pandas as pd
from sqlalchemy import create_engine
import pymssql
import streamlit as st


database_p = "20.169.221.14:1433/Bayview_Automation"
userandpass = '//sa:3004222950A.b@'
engine = create_engine('mssql+pymssql:'+userandpass+database_p)


conn = pymssql.connect("20.169.221.14:1433","sa","3004222950A.b","Bayview_Automation")
cursor = conn.cursor()



emp_str = '                                                                                                                                                           '

def title_centered_h3(str_):
    title = st.markdown("""<h3 style='text-align: center'>""" + str(str_) +"""</h3>""",unsafe_allow_html =True)
    return title
def title_centered_h4(str_):
    title = st.markdown("""<h4 style='text-align: center'>""" + str(str_) +"""</h4>""",unsafe_allow_html =True)
    return title
def title_centered_h1(str_):
    title = st.markdown("""<h1 style='text-align: center'>""" + str(str_) +"""</h1>""",unsafe_allow_html =True)
    return title


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

z1,z2,z3,z4,z5 = st.columns(5)
with z3:

    st.image('acc.png')


title_centered_h1('Update GNMA data')

sql1 = """ SELECT DISTINCT([Unique Loan Id]) AS [Unique Loan Id] FROM [STG_MR].[MERGED] """
sql1_df = pd.read_sql(con=engine,sql=sql1)
list_loans = sql1_df['Unique Loan Id'].to_list()


loan_selector = st.selectbox('Select Loan Id',list_loans)



sql2  = """ SELECT [Action],[Notes 3rd Party],[Notes Internal], MAX([REPORT DATE]) AS _MAX  FROM [STG_MR].[MERGED] WHERE [Unique Loan Id] = """ + str(loan_selector) + """ GROUP BY [Action],[Notes 3rd Party],[Notes Internal] ORDER BY _MAX DESC """
sql2_df = pd.read_sql(con=engine,sql = sql2)


action = sql2_df.iloc[0,0]
Notes_3rd = sql2_df.iloc[0,1]
notes_internal = sql2_df.iloc[0,2]

if action == emp_str:
    action = ''
if Notes_3rd == emp_str:
    Notes_3rd = ''
if notes_internal == emp_str:
    notes_internal = ''






title_centered_h4('Action')
actions_ =st.text_input(value = action,label='action',label_visibility ='hidden')

title_centered_h4('Notes 3rd Party')
nostes3rd_ = st.text_input(value = Notes_3rd,label='Notes 3rd Party',label_visibility ='hidden')

title_centered_h4('Notes Internal')
notes_internal_ = st.text_input(value = notes_internal,label='Notes Internal',label_visibility ='hidden')

d1,d2,d3,d4,d5 =st.columns(5)


with d3:
    if st.button('Upload Notes'):
        cursor.execute("""
        UPDATE [STG_MR].[MERGED]  
        SET 
            [Action] = """ + """'""" + str(actions_) + """'""" + ""","""+ """ [Notes Internal] = '""" +  str(notes_internal_) + """'""" + """,[Notes 3rd Party] = """  + """'""" + str(nostes3rd_) + """'""" + """ WHERE [Unique Loan Id] = """ +str(loan_selector) + """ AND [REPORT DATE]  = """ + """'""" + str(sql2_df.iloc[0,3])[0:23] + """'""")
        conn.commit()
        conn.close()
        st.write("Updated")
        print("Done")












