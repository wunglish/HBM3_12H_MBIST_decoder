#!/usr/bin/env python
# coding: utf-8

# ## HBM3_12H_Log_decoder-v03
## 16 Continuous Failing addresses
## CDC fail check box. Add fail mode minor crack
## Bank review summary on the display
## March failing start 0x0 or 0X1 
## Bank cartegory entire bank dead,Partially dead, funtional
## 'Gross'  Fail need check march and scan fail addr have to match..

import pandas as pd
import sys
import os
import re
import glob
import numpy as np
pd.set_option('display.max_rows', 100)
pd.set_option('max_colwidth', 1200)
import warnings
warnings.filterwarnings('ignore')

#log_file=sys.argv[1]

#log_dir='X:\\jeongwun\\SEC_HBM\\RMA_7units\\'
#log_file='S_ADDRdump_Read_SEC_RA_16CH_serialId2D_fail_site1_L8B5870003081801.log'
#log=log_dir+log_file

class HBM3_12H_ATE_log_decode:
    hbm_alpha_list=['A','B','C','D','E','F','G','H']
    ch_alpha_list=['A','B','C','D','E','F','G','H',
                   'I','J','K','L','M','N','O','P'] #used for bank number convert as well
    core_select_dict={'sid':[0,0,0,0,1,1,1,1,2,2,2,2],
                      'ch':[[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],
                            [0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],
                            [0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]],
                      'core':[1,2,3,4,5,6,7,8,9,10,11,12]}
    core_select_df=pd.DataFrame(core_select_dict)
    Addr_bank_beg16=[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
    def __init__(self,log_file):
        open_log_file=open(log_file)
        log_lines=open_log_file.readlines()
        self.fail_info_dict={'AID_FuseID':[],'Barcode':[],'Test_Date':[],'Test_Time':[],
                        'Testset':[],'HBM':[],'HBM_alpha':[],'CH':[],'CH_alpha':[],
                        'Addr_row_bin':[],'Addr_row_int':[],'Addr_row_str_int':[],'Addr_row_hex':[],
                        'Addr_Bank':[],'Addr_Bank_alpha':[],
                        'SID':[],'PCH':[],'Core':[]}
        for i in range (len(log_lines)):
            fail_info=re.findall('AID0FUSEID:\s[A-Z0-9]+|2DBARCODE:\s[A-Za-z0-9_]+',log_lines[i])
            if len(fail_info)==2:
                aid_fuseid=fail_info[0].replace('AID0FUSEID: ','')
                barcode=fail_info[1].replace('2DBARCODE: ','')
                continue
            fail_time=re.findall('\d\d\d\d-\d\d-\d\d|\d\d:\d\d:\d\d.\d+',log_lines[i])
            if len(fail_time)==2:
                test_date=fail_time[0]
                test_time=fail_time[1]
                continue
            tesetset_hbm_ch=re.findall('testset\d+|hbm\d|channel\d+',log_lines[i]) #cover testset morethan one digits         
            if len(tesetset_hbm_ch)==3:
                testset=tesetset_hbm_ch[0]
                hbm=tesetset_hbm_ch[1]
                hbm_int=int(hbm.replace('hbm',''))
                hbm_alpha=HBM3_12H_ATE_log_decode.hbm_alpha_list[hbm_int] #add hbm alpahbet list pick HBM from the list
                ch=tesetset_hbm_ch[2]
                ch_int=int(ch.replace('channel',''))
                continue
            row_addr=re.findall("Repair Row Address|15'b[01]+",log_lines[i])
            if len(row_addr)==2:
                row_addr_bin_full=row_addr[1]
                row_addr_bin=row_addr_bin_full.replace("15'b",'')
                row_addr_int=int(row_addr_bin,2) ##add row address decimal value
                row_addr_str_int=str(row_addr_int)
                row_addr_hex=hex(row_addr_int)   
                continue
            bank_addr=re.findall("Repair Bank Address|4'b[01][01][01][01]",log_lines[i])
            if len(bank_addr)==2:
                bank_addr_bin_full=bank_addr[1]
                bank_addr_bin=bank_addr_bin_full.replace("4'b",'')
                bank_addr_int=int(bank_addr_bin,2)
                continue
            sid=re.findall("Repair SID|2'b[01][01]",log_lines[i]) ########### 'Repair SID: 1'##
            if len(sid)==2:                                       ########### 'Repair SID: 1'##
                sid_bin_full=sid[1]                               #############################
                sid_bin=sid_bin_full.replace("2'b",'')            #############################
                sid_int=int(sid_bin,2)                            #############################
                continue                                          #############################  
            elif len(sid)==1:                                     #############################
                sid_int=int(re.findall("\d",log_lines[i])[0])  #############################
                continue                                          #############################
            pch=re.findall("Repair PCH|1'b[01]",log_lines[i])
            if len(pch) == 2:
                pch_bin_full=pch[1]
                pch_bin=pch_bin_full.replace("1'b",'')
                pch_int=int(pch_bin,2)
                ## fill dict ##
                # Core number # modified ==> core number picked up from the df 'core_select_df'
                core_select_sid_df=HBM3_12H_ATE_log_decode.core_select_df[HBM3_12H_ATE_log_decode.core_select_df['sid']==sid_int].reset_index()
                for i in range(len(core_select_sid_df)):
                    if ch_int in core_select_sid_df['ch'][i]:
                        self.fail_info_dict['Core'].append(int(core_select_sid_df['core'][i]))
                # Channel convert to Alphabet form # modified to pick ch list
                self.fail_info_dict['CH_alpha'].append(HBM3_12H_ATE_log_decode.ch_alpha_list[ch_int]+str(pch_int))
                # Bank convert to Alphabet form
                self.fail_info_dict['Addr_Bank_alpha'].append(HBM3_12H_ATE_log_decode.ch_alpha_list[bank_addr_int]+str(pch_int))
                self.fail_info_dict['AID_FuseID'].append(aid_fuseid)
                self.fail_info_dict['Barcode'].append(barcode)
                self.fail_info_dict['Test_Date'].append(test_date)
                self.fail_info_dict['Test_Time'].append(test_time)
                self.fail_info_dict['Testset'].append(testset)
                self.fail_info_dict['HBM'].append(hbm_int)
                self.fail_info_dict['HBM_alpha'].append(hbm_alpha)
                self.fail_info_dict['CH'].append(ch_int)
                self.fail_info_dict['Addr_row_bin'].append(row_addr_bin)
                self.fail_info_dict['Addr_row_int'].append(row_addr_int)
                self.fail_info_dict['Addr_row_str_int'].append(row_addr_str_int)
                self.fail_info_dict['Addr_row_hex'].append(row_addr_hex)
                self.fail_info_dict['Addr_Bank'].append(bank_addr_int)
                self.fail_info_dict['SID'].append(sid_int)
                self.fail_info_dict['PCH'].append(pch_int)    
                continue
        ##   self.fail_info_df ##      
        self.fail_info_df=pd.DataFrame(self.fail_info_dict)
        ##   self.log_review
        self.log_review= self.fail_info_df.groupby(['Barcode','Testset','HBM_alpha','CH_alpha','Core',
                                                              'Addr_Bank_alpha']).agg({'Addr_row_int': lambda x: list(x)})
        for i in range (len(self.log_review)):
            self.log_review['Addr_row_int'][i]=list(set(self.log_review['Addr_row_int'][i]))
            
        self.log_review = self.log_review.reset_index()
        
        self.log_review = self.log_review.rename(columns={'HBM_alpha': 'HBM','CH_alpha': 'Channel', 
                                                          'Addr_Bank_alpha': 'Bank','Addr_row_int':'Address_failed'})
        self.log_review['fail_addr_count'] = [len(c) for c in self.log_review['Address_failed']]
        ## self.log_bank_review + Bank risk assessment
        self.log_bank_review=self.log_review.groupby(['Barcode','HBM','Channel','Core','Bank']).agg({'Testset':lambda x: list(x),'Address_failed':lambda x: list(x),'fail_addr_count':lambda x: list(x)})
        self.log_bank_review=self.log_bank_review.reset_index()
        self.log_bank_review[['Test_failed','Addr_failed_common','Addr_failed_common_count','Bank_assess','Engr_comment']]=''
        for i in range(len(self.log_bank_review)):
            if len(self.log_bank_review['Testset'][i]) == 2 and 'testset0' in self.log_bank_review['Testset'][i]:
                self.log_bank_review['Test_failed'][i] = 'March & Scan'
                for j in range (len(self.log_bank_review['Address_failed'][i])):
                    if j == 0:
                        addr_failed= self.log_bank_review['Address_failed'][i][j]
                    else:
                        addr_failed_common=list(set(addr_failed).intersection(self.log_bank_review['Address_failed'][i][j]))
                        self.log_bank_review['Addr_failed_common'][i]=addr_failed_common
                        self.log_bank_review['Addr_failed_common_count'][i]=len(addr_failed_common)
                        if len(addr_failed_common) == 16 and addr_failed_common == HBM3_12H_ATE_log_decode.Addr_bank_beg16:
                            self.log_bank_review['Bank_assess'][i]='Grossly dead'
                        elif len(addr_failed_common) > 14 and addr_failed_common != HBM3_12H_ATE_log_decode.Addr_bank_beg16:
                            self.log_bank_review['Bank_assess'][i]='Grossly dead partially'
                        elif len(addr_failed_common) > 0 :
                            self.log_bank_review['Bank_assess'][i]='Dead partially'
                        elif len(addr_failed_common) == 0 :
                            self.log_bank_review['Bank_assess'][i]='Functional'
                        else:
                            self.log_bank_review['Engr_comment'][i]='Need_review'
            elif len(self.log_bank_review['Testset'][i]) == 2 and 'testset0' not in self.log_bank_review['Testset'][i]:
                self.log_bank_review['Test_failed'][i] = 'Scan'
                for j in range (len(self.log_bank_review['Address_failed'][i])):
                    if j == 0:
                        addr_failed= self.log_bank_review['Address_failed'][i][j]
                    else:
                        addr_failed_common=list(set(addr_failed).intersection(self.log_bank_review['Address_failed'][i][j]))
                        self.log_bank_review['Addr_failed_common'][i]=addr_failed_common
                        self.log_bank_review['Addr_failed_common_count'][i]=len(addr_failed_common)                        
                        self.log_bank_review['Bank_assess'][i]='Functional'
                            
            elif len(self.log_bank_review['Testset'][i]) == 1 and 'testset0' in self.log_bank_review['Testset'][i]:
                self.log_bank_review['Test_failed'][i] = 'March'
                self.log_bank_review['Bank_assess'][i]='Functional'
            elif len(self.log_bank_review['Testset'][i]) == 1 and 'testset0' not in self.log_bank_review['Testset'][i]:
                self.log_bank_review['Test_failed'][i] = 'Scan'
                self.log_bank_review['Bank_assess'][i]='Functional'
            else:
                self.log_bank_review['Engr_comment'][i] = 'Need_review'
        self.log_bank_review[['Failed_addr','Failed_addr_count']]=''
        for i in range(len(self.log_bank_review)):
            for j in range(len(self.log_bank_review['Address_failed'][i])):
                if j == 0:
                    addr_list=self.log_bank_review['Address_failed'][i][j]
                else:
                    addr_list=addr_list+self.log_bank_review['Address_failed'][i][j]
            self.log_bank_review['Failed_addr'][i]=list(set(addr_list))
            self.log_bank_review['Failed_addr_count'][i]=len(list(set(addr_list)))
        ## self.log_bank_review + Risk bank assess
        risk_bank_dict={'Barcode':[],'HBM':[],'Channel':[],'Core':[],'Bank':[],'Testset':[],
                'Address_failed':[],'fail_addr_count':[],'Test_failed':[],
                'Addr_failed_common':[],'Addr_failed_common_count':[],'Bank_assess':[],
                'Engr_comment':[],'Failed_addr':[],'Failed_addr_count':[]}
        for i in range (len(self.log_bank_review)):
            if (self.log_bank_review['Bank_assess'][i] == 'Grossly dead') or (self.log_bank_review['Bank_assess'][i] == 'Grossly dead partially'):
                if re.findall('\d',self.log_bank_review['Bank'][i])[0] == '0':
                    Bank_letter=re.findall('[A-Z]',self.log_bank_review['Bank'][i])[0]
                    risk_bank=Bank_letter+'1'
                    risk_bank_dict['Barcode'].append(self.log_bank_review['Barcode'][i])
                    risk_bank_dict['HBM'].append(self.log_bank_review['HBM'][i])
                    risk_bank_dict['Core'].append(self.log_bank_review['Core'][i])
                    risk_bank_dict['Channel'].append(self.log_bank_review['Channel'][i])
                    risk_bank_dict['Bank'].append(risk_bank)
                    risk_bank_dict['Testset'].append('')
                    risk_bank_dict['Address_failed'].append('')
                    risk_bank_dict['fail_addr_count'].append('')
                    risk_bank_dict['Test_failed'].append('')
                    risk_bank_dict['Addr_failed_common'].append('')
                    risk_bank_dict['Addr_failed_common_count'].append('')
                    risk_bank_dict['Bank_assess'].append('Risk')
                    risk_bank_dict['Engr_comment'].append(self.log_bank_review['Engr_comment'][i])
                    risk_bank_dict['Failed_addr'].append('')
                    risk_bank_dict['Failed_addr_count'].append('')
                
        risk_bank_df=pd.DataFrame(risk_bank_dict)           
        ##  self.log_bank_risk_review         
        self.log_bank_risk_review=pd.concat([self.log_bank_review,risk_bank_df]).reset_index(drop=True)
        self.log_bank_risk_review['Core']=[int(c) for c in self.log_bank_risk_review['Core'] ]
        ## self.log_bank_review_display
        self.log_bank_review_display=self.log_bank_risk_review[['HBM','Channel','Core',
                                                                'Bank','Test_failed','Bank_assess',
                                                                'Failed_addr','Failed_addr_count','Engr_comment']]
        ## self.log_bank_review_display2
        self.log_bank_review_display2=self.log_bank_review_display.copy()
        self.log_bank_review_display2['AID_FuseID']=self.fail_info_df['AID_FuseID'][0]
        self.log_bank_review_display2['Barcode']=self.fail_info_df['Barcode'][0]
        self.log_bank_review_display2=self.log_bank_review_display2.rename(columns={"Failed_addr_count": "No.Failed"})
        self.log_bank_review_display2=self.log_bank_review_display2.drop('Engr_comment', axis=1)
        ## self.log_core_review
        self.log_core_review = self.log_bank_review_display.groupby(['HBM','Core'],as_index = False).agg({'Channel':','.join,'Bank':','.join,'Test_failed':','.join,'Bank_assess':','.join})

       
       
#self.fail_info_df
#self.log_review
#self.log_bank_review
#self.log_bank_risk_review
#self.log_bank_review_display
#self.log_core_review