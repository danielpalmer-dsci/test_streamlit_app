import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


st.title("Test DataFrame")

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


forecast_data = pd.read_csv('./forecast.csv')
forecast_data = forecast_data[['prime_item_nbr',
                               'week_ending',
                               'predict_training_pos_qty_per_pod',
                               'flagged_active_pod',
                               'aur_price',
                               'mf_training_data',
                               'create_date']]
historical_data = pd.read_csv('./raw_data.csv')
historical_data = historical_data[historical_data['prime_item_nbr'] != 'prime_item_nbr']
historical_data = historical_data[['prime_item_nbr',
                                   'week_ending',
                                   'pos_qty',
                                   'pos_sales',
                                   'aur_price',
                                   'traited_pods',
                                   'valid_pods',
                                   'OOS_pods',
                                   'OOS_pct_pods',
                                   'hist_on_hand_qty',
                                   'net_ship_qty',
                                   'flagged_active_pod',
                                   'pos_qty_per_pod',
                                   'pos_sales_per_pod',
                                   'mf_training_data']]
historical_data['prime_item_nbr'] = historical_data['prime_item_nbr'].astype('float64', errors='ignore')



item_attributes = pd.read_csv('./item_attributes.csv')
item_attributes = item_attributes[['prime_item_nbr',
                                   'prime_item_desc',
                                   'upc',
                                   'upc_desc',
                                   'buyer_full_name',
                                   'fineline_description',
                                   'dept_subcategory_description',
                                   'dept_category_description']]
item_attributes2 = pd.read_csv('./item_attribute_2.csv')
item_attributes2 = item_attributes2[['prime_item_nbr',
                                     'prime_item_desc',
                                     'upc',
                                     'upc_desc',
                                     'buyer_full_name',
                                     'fineline_description',
                                     'dept_subcategory_description',
                                     'dept_category_description']]
items = pd.concat([item_attributes, item_attributes2])

weeks = pd.read_csv('./wmt_weeks.csv')

full_data = pd.merge(forecast_data, historical_data, how='left', on=['prime_item_nbr', 'week_ending'])
full_data = pd.merge(full_data, items, how='left', on=['prime_item_nbr'])
full_data = pd.merge(full_data, weeks, how='left', on=['week_ending'])

groupings = ['prime_item_desc', 'upc', 'buyer_full_name', 'fineline_description', 'dept_subcategory_description', 'dept_category_description', 'this will fail', 'nick sucks dick']
time_periods = ['2020', '2021', '2022', 'L4', 'L13', 'L26', 'L52', 'N4', 'N13', 'N26', 'N52']
metrics = ['Sales', 'Units', 'YoY %CHG', 'YoY $CHG']



groupby_selected = st.multiselect('Item Groupings', groupings, ['dept_subcategory_description'])
timeframe_selected = st.multiselect('Time Frames', time_periods, ['L52', 'N52'])
metrics_selected = st.multiselect('Metrics', metrics, ['Sales'])
dos_selected = st.multiselect('DOS', [1,2,3,4,5,7,10,15], [3])
new_selction = st.multiselect('Help', [1,2,3,4,5,7,10,15], [3])

summary = full_data.groupby(groupby_selected).agg(Sales=pd.NamedAgg(column='pos_sales', aggfunc='sum')).reset_index()


selection = aggrid_interactive_table(df=summary)


summary2 = full_data.groupby(groupby_selected).agg(Units=pd.NamedAgg(column='pos_qty', aggfunc='sum')).reset_index()
selection2 = aggrid_interactive_table(df=summary2)



