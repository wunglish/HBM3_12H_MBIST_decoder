#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import ipywidgets as wg
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
import warnings
warnings.filterwarnings('ignore')
from IPython.display import clear_output

class HBM_lib:
    lib = pd.read_csv('X:\\jeongwun\\SEC_HBM\\HBM_lib\\HBM_lib.csv', index_col=0, na_filter= False)
    lib = lib.reset_index(drop=True)
    lib_output = wg.Output()
    with lib_output:display(lib)

    Lib_df_hbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='Flex-start',border='',width='920px', height='',justify_content='Flex-start')
    Lib_df_hbox=wg.HBox(children=[lib_output], layout=Lib_df_hbox_layout)

    HBM_list=['A','B','C','D','E','F','G','H']
    HBM_select_box_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='50px', height='100px',justify_content='center')
    HBM_select_box=wg.SelectMultiple(options=HBM_list,
                                     value=[],
                                     rows=5,
                                     description='',
                                     disabled=False, layout=HBM_select_box_layout)

    Core_list=[1,2,3,4,5,6,7,8,9,10,11,12]
    Core_select_box_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='50px', height='100px',justify_content='center')
    Core_select_box=wg.SelectMultiple(options=Core_list,
                                      value=[],
                                      rows=5,
                                      description='',
                                      disabled=False, layout=Core_select_box_layout)

    Ch_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
    Ch_select_box_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='50px', height='100px',justify_content='center')
    Ch_select_box=wg.SelectMultiple(options=Ch_list,
                                      value=[],
                                      rows=5,
                                      description='',
                                      disabled=False , layout=Ch_select_box_layout)

    Bank_list=['A0','A1','B0','B1','C0','C1','D0','D1','E0','E1','F0','F1','G0','G1','H0','H1',
               'I0','I1','J0','J1','K0','K1','L0','L1','M0','M1','N0','N1','O0','O1','P0','P1']
    Bank_select_box_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='50px', height='100px',justify_content='center')
    Bank_select_box=wg.SelectMultiple(options=Bank_list,
                                      value=[],
                                      rows=5,
                                      description='',
                                      disabled=False, layout=Bank_select_box_layout)

    Defect_type_select_box_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='250px', height='100px',justify_content='center')
    Defect_type_select_box=wg.SelectMultiple(options=set(list(lib['Defect_type_PFA'])),
                                      value=[],
                                      rows=5,
                                      description='',
                                      disabled=False, layout=Defect_type_select_box_layout)

    Defect_location_select_box_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='160px', height='100px',justify_content='center')
    Defect_location_select_box=wg.SelectMultiple(options=set(list(lib['Defect_location_PFA'])),
                                      value=[],
                                      rows=5,
                                      description='',
                                      disabled=False, layout=Defect_location_select_box_layout)

    Search_btn_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='', width='120px', height='135px',justify_content='center')
    Search_btn = wg.Button(description='Search',disabled=False,button_style='success', layout=Search_btn_layout)

    open_Library_btn_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='', width='120px', height='50px',justify_content='center')
    open_Library_btn = wg.Button(description='Unselect all',disabled=False,button_style='info', layout=open_Library_btn_layout)
    
    save_lib_btn_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='', width='120px', height='130px',justify_content='center')
    save_lib_btn = wg.Button(description='Save LIB',disabled=False,button_style='primary', layout=save_lib_btn_layout)

    HBM_select_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='60px', height='135px',justify_content='center')
    HBM_select_vbox=wg.VBox([wg.Label(value="HBM"), HBM_select_box], layout=HBM_select_vbox_layout)

    Core_select_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='60px', height='135px',justify_content='center')
    Core_select_vbox=wg.VBox([wg.Label(value="Core"), Core_select_box], layout=Core_select_vbox_layout)

    Ch_select_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='60px', height='135px',justify_content='center')
    Ch_select_vbox=wg.VBox([wg.Label(value="Channel"), Ch_select_box], layout=Ch_select_vbox_layout)

    Bank_select_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='60px', height='135px',justify_content='center')
    Bank_select_vbox=wg.VBox([wg.Label(value="Bank"), Bank_select_box], layout=Bank_select_vbox_layout)

    Defect_type_select_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='260px', height='135px',justify_content='center')
    Defect_type_select_vbox=wg.VBox([wg.Label(value="Defect Type"), Defect_type_select_box], layout=Defect_type_select_vbox_layout)

    Defect_location_select_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='180px', height='135px',justify_content='center')
    Defect_location_select_vbox=wg.VBox([wg.Label(value="Defect Location"), Defect_location_select_box], layout=Defect_location_select_vbox_layout)

    Library_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='',width='130px', height='135px',justify_content='center')
    Library_vbox=wg.VBox(children=[open_Library_btn,Search_btn], layout=Library_vbox_layout)
    
    filter_select_hbox_layout=wg.Layout(display='flex',flex_flow='row',align_items='center',border='',width='920px', height='150px',justify_content='space-between')
    filter_select_hbox=wg.HBox(children=[HBM_select_vbox,Core_select_vbox,Ch_select_vbox,Bank_select_vbox,
                           Defect_type_select_vbox, Defect_location_select_vbox, Library_vbox, save_lib_btn], layout=filter_select_hbox_layout)

    lib_frame_vbox_layout=wg.Layout(display='flex',flex_flow='column',align_items='center',border='solid',width='100%', height='',justify_content='flex-start')
    lib_frame_vbox=wg.VBox(children=[filter_select_hbox,Lib_df_hbox], layout=lib_frame_vbox_layout)
