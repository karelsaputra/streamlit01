import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("""# Network Partner SLA Checker""")

url = "https://raw.githubusercontent.com/karelsaputra/streamlit01/main/HASIL AKHIR processed.csv
df = pd.read_csv(url)
# FM
distinct_fm_partners_list = df['FM partner'].dropna().unique().tolist()
# Count the occurrences of each distinct FM partner
partner_counts_fm = df['FM partner'].value_counts().to_dict()

# LM
distinct_lm_partners_list = df['LM partner'].dropna().unique().tolist()
# Count the occurrences of each distinct FM partner
partner_counts_lm = df['LM partner'].value_counts().to_dict()
# Display the distinct FM partners and their counts in a table

fm_partner_table = []
for fm_partner in distinct_fm_partners_list:
    count1 = partner_counts_fm.get(fm_partner, 0)
    fm_partner_table.append({'FM Partner': fm_partner, 'Count': count1})

# Display the distinct FM partners and their counts in a table
lm_partner_table = []
for lm_partner in distinct_lm_partners_list:
    count1 = partner_counts_lm.get(lm_partner, 0)
    if count1 > 0:  # Exclude rows with count equal to 0
        lm_partner_table.append({'LM Partner': lm_partner, 'Count': count1})

# Create a DataFrame from the sample data
df1 = pd.DataFrame(fm_partner_table)
df2 = pd.DataFrame(lm_partner_table)

# Group by 'FM Partner' and count True/False values
fmgrouped1 = df.groupby('FM partner')['FM between SLA'].value_counts().unstack(fill_value=0)
# Rename column headers
fmgrouped1.rename(columns={True: 'Between SLA', False: 'Outside SLA'}, inplace=True)
# Calculate the percentage and create the new column
fmgrouped1['Outside SLA (%)'] = (
            (fmgrouped1['Outside SLA'] / (fmgrouped1['Outside SLA'] + fmgrouped1['Between SLA'])) * 100).round(2)
fmgrouped1['Between SLA (%)'] = (
            (fmgrouped1['Between SLA'] / (fmgrouped1['Outside SLA'] + fmgrouped1['Between SLA'])) * 100).round(2)
# Format the percentage columns with a "%" symbol
fmgrouped1['Outside SLA (%)'] = fmgrouped1['Outside SLA (%)'].apply(lambda x: f'{x:.1f}%')
fmgrouped1['Between SLA (%)'] = fmgrouped1['Between SLA (%)'].apply(lambda x: f'{x:.1f}%')

# Group by 'FM Partner' and count True/False values
fmgrouped2 = df.groupby('FM partner')['FM 0 to max'].value_counts().unstack(fill_value=0)
# Rename column headers
fmgrouped2.rename(columns={True: 'Between SLA', False: 'Outside SLA'}, inplace=True)
# Calculate the percentage and create the new column
fmgrouped2['Outside SLA (%)'] = (
            (fmgrouped2['Outside SLA'] / (fmgrouped2['Outside SLA'] + fmgrouped2['Between SLA'])) * 100).round(2)
fmgrouped2['Between SLA (%)'] = (
            (fmgrouped2['Between SLA'] / (fmgrouped2['Outside SLA'] + fmgrouped2['Between SLA'])) * 100).round(2)
# Format the percentage columns with a "%" symbol
fmgrouped2['Outside SLA (%)'] = fmgrouped2['Outside SLA (%)'].apply(lambda x: f'{x:.1f}%')
fmgrouped2['Between SLA (%)'] = fmgrouped2['Between SLA (%)'].apply(lambda x: f'{x:.1f}%')

# Group by 'FM Partner' and count True/False values
lmgrouped1 = df.groupby('LM partner')['LM between SLA'].value_counts().unstack(fill_value=0)
# Rename column headers
lmgrouped1.rename(columns={True: 'Between SLA', False: 'Outside SLA'}, inplace=True)
# Calculate the percentage and create the new column
lmgrouped1['Outside SLA (%)'] = (
            (lmgrouped1['Outside SLA'] / (lmgrouped1['Outside SLA'] + lmgrouped1['Between SLA'])) * 100).round(2)
lmgrouped1['Between SLA (%)'] = (
            (lmgrouped1['Between SLA'] / (lmgrouped1['Outside SLA'] + lmgrouped1['Between SLA'])) * 100).round(2)
# Format the percentage columns with a "%" symbol
lmgrouped1['Outside SLA (%)'] = lmgrouped1['Outside SLA (%)'].apply(lambda x: f'{x:.1f}%')
lmgrouped1['Between SLA (%)'] = lmgrouped1['Between SLA (%)'].apply(lambda x: f'{x:.1f}%')

# Group by 'FM Partner' and count True/False values
lmgrouped2 = df.groupby('LM partner')['LM 0 to max'].value_counts().unstack(fill_value=0)
# Rename column headers
lmgrouped2.rename(columns={True: 'Between SLA', False: 'Outside SLA'}, inplace=True)
# Calculate the percentage and create the new column
lmgrouped2['Outside SLA (%)'] = (
            (lmgrouped2['Outside SLA'] / (lmgrouped2['Outside SLA'] + lmgrouped2['Between SLA'])) * 100).round(2)
lmgrouped2['Between SLA (%)'] = (
            (lmgrouped2['Between SLA'] / (lmgrouped2['Outside SLA'] + lmgrouped2['Between SLA'])) * 100).round(2)
# Format the percentage columns with a "%" symbol
lmgrouped2['Outside SLA (%)'] = lmgrouped2['Outside SLA (%)'].apply(lambda x: f'{x:.1f}%')
lmgrouped2['Between SLA (%)'] = lmgrouped2['Between SLA (%)'].apply(lambda x: f'{x:.1f}%')

# Sidebar
# Create a dictionary to map table names to DataFrames
tables = {'FM Table between SLA': fmgrouped1, 'FM Table 0 to max SLA': fmgrouped2, 'LM Table between SLA': lmgrouped1,
          'LM Table 0 to max SLA': lmgrouped2}
st.sidebar.header('Filter View')
# def table_filter():
table_selection = st.sidebar.selectbox('Choose Table', list(tables.keys()))
selected_df = tables[table_selection]
# Choose a partner from the second column of the selected DataFrame
# partners_column = selected_df.columns[0]
partners = selected_df.index.values
partner_selection = st.sidebar.selectbox('Choose Partner', partners)

# Pie Chart Settings
colormap = plt.cm.viridis
cmap_colors = colormap([0.25, 0.60])
start_angle = 90
fig_size = (3,3)

# Logic Pie Chart
if table_selection == 'FM Table between SLA':
    fm_pie_table1 = fmgrouped1.loc[partner_selection, ['Outside SLA', 'Between SLA']]
    fm_pie_labels1 = fm_pie_table1.index.values
    fm_pie_sizes1 = fm_pie_table1.values
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=fig_size)
    ax.pie(fm_pie_sizes1, labels=fm_pie_labels1, autopct='%1.1f%%', colors=cmap_colors, startangle=start_angle)
    ax.set_title(f' {table_selection} | {partner_selection}')
    st.pyplot(fig)
elif table_selection == 'FM Table 0 to max SLA':
    fm_pie_table2 = fmgrouped2.loc[partner_selection, ['Outside SLA', 'Between SLA']]
    fm_pie_labels2 = fm_pie_table2.index.values
    fm_pie_sizes2 = fm_pie_table2.values
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=fig_size)
    ax.pie(fm_pie_sizes2, labels=fm_pie_labels2, autopct='%1.1f%%', colors=cmap_colors, startangle=start_angle)
    ax.set_title(f' {table_selection} | {partner_selection}')
    st.pyplot(fig)
elif table_selection == 'LM Table between SLA':
    lm_pie_table1 = lmgrouped1.loc[partner_selection, ['Outside SLA', 'Between SLA']]
    lm_pie_labels1 = lm_pie_table1.index.values
    lm_pie_sizes1 = lm_pie_table1.values
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=fig_size)
    ax.pie(lm_pie_sizes1, labels=lm_pie_labels1, autopct='%1.1f%%',colors=cmap_colors, startangle=start_angle)
    ax.set_title(f' {table_selection} | {partner_selection}')
    st.pyplot(fig)
elif table_selection == 'LM Table 0 to max SLA':
    lm_pie_table2 = lmgrouped2.loc[partner_selection, ['Outside SLA', 'Between SLA']]
    lm_pie_labels2 = lm_pie_table2.index.values
    lm_pie_sizes2 = lm_pie_table2.values
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=fig_size)
    ax.pie(lm_pie_sizes2, labels=lm_pie_labels2, autopct='%1.1f%%', colors=cmap_colors, startangle=start_angle)
    ax.set_title(f' {table_selection} | {partner_selection}')
    st.pyplot(fig)

st.write("Distinct FM Partners:")
st.dataframe(pd.DataFrame(fm_partner_table).sort_values(by='Count', ascending=True))

st.write("Distinct LM Partners:")
st.dataframe(pd.DataFrame(lm_partner_table).sort_values(by='Count', ascending=True))

st.write("""FM Table between SLA""")
st.dataframe(fmgrouped1)

st.write("""FM Table FM 0 to max SLA""")
st.dataframe(fmgrouped2)

st.write("""LM Table between SLA""")
st.dataframe(lmgrouped1)

st.write("""LM Table FM 0 to max SLA""")
st.dataframe(lmgrouped2)

