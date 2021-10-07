import dearpygui.dearpygui as dpg
from tkinter import messagebox
import tkinter as tk
import os,time,threading,datetime

import DataUse,API

Font0=r'NotoSerifTC-SemiBold.otf'
Font=r'hkon.ttc'
BS_LIST=[0,'Buy','Sell','Buy','Sell']
BS_LIST_CHI={'Buy':'買入','Sell':'賣出'}
BS_LIST_num={'Buy':1,'Sell':2,'CommonBuy':3,'CommonSell':4}
##{1:觸價Buy 2:觸價Sell 3:普通買進 4:普通賣出}

dpg.setup_registries()
with dpg.font_registry() : #字體設定
      with dpg.font( file = Font0, size = 17.5, default_font = True) as DefaultFont:
          dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
      with dpg.font( file = Font, size = 16, default_font = False) as FONT0001:
          dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)

##TABLE 文字  table_text_align_style={1 , 2}
##1.報價置中 其餘文字置右
##2.全體置中

table_text_align_style=1
if table_text_align_style==1:
    print("TABLE 文字對齊:報價置中,其餘置右")
##TABLE 顏色  table_text_col_style={1 , 2}
##1.白
##2.黑
table_text_col_style=2
if table_text_col_style==2:print("TABLE 文字:黑")
text_mid_align=0.33
#========================= THEME ========================
with dpg.theme(default_theme=True):
##    mvStyleVar_CellPadding= 每一格之間的間隙
    dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 0,0)# col/row 0~1
    dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize,0.05 )
##    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 20,3)
    if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5,0.5)# 調整 BUTTON 文字置中
    else:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)# 調整 BUTTON 文字置中
    dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0,0,0,0))
    dpg.add_theme_color(dpg.mvThemeCol_Border, (0,0,0,47))
    dpg.add_theme_color(dpg.mvThemeCol_Button, (92,92,117), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (37,37,38), category=dpg.mvThemeCat_Core)


DEEPBLUE=(5,177,255,255)
DEEPRED=(255,122,165,255)
with dpg.theme() as window_theme:
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,15,0)
with dpg.theme() as child_theme:
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,0,0)
with dpg.theme() as table_set_my_price_blue:
            dpg.add_theme_color(dpg.mvThemeCol_Button,(5,177,255,255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(5,177,255,255))
            dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing,0,10)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
with dpg.theme() as table_set_my_price_red:
            dpg.add_theme_color(dpg.mvThemeCol_Button,(255,122,165,255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255,122,165,255))
            dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing,0,10)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
           
with dpg.theme() as uplimit_table:
            dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,0,255))# BTN TEXT COL
            dpg.add_theme_color(dpg.mvThemeCol_Button, (246,14,8,255))
           
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.37,0.5)
with dpg.theme() as dnlimit_table:
            dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,0,255))# BTN TEXT COL
            dpg.add_theme_color(dpg.mvThemeCol_Button, (6,134,11,255))
            
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.37,0.5)
with dpg.theme() as down_print_uptable:#下跌文字顏色 uptable
     dpg.add_theme_color(dpg.mvThemeCol_Button, (247,164,203,255))
     dpg.add_theme_color(dpg.mvThemeCol_Text, (6,134,11,255))
with dpg.theme() as down_print_midtable:#下跌文字顏色 dntable
     dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,255))
     dpg.add_theme_color(dpg.mvThemeCol_Text, (6,134,11,255))

with dpg.theme() as up_print_uptable:# 上漲文字顏色 uptable
     dpg.add_theme_color(dpg.mvThemeCol_Text, (246,14,8,255))
     dpg.add_theme_color(dpg.mvThemeCol_Button, (247,164,203,255))
with dpg.theme() as up_print_midtable:# 上漲文字顏色  dntable
     dpg.add_theme_color(dpg.mvThemeCol_Text, (246,14,8,255))
     dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,255))
     

 
with dpg.theme() as no_change_print:# 不變文字顏色
     dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
     dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,255))
     
with dpg.theme() as table_text_col:
            dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL  
with dpg.theme() as table_btn_txtalign_mid:
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5,category=dpg.mvThemeCat_Core)# 調整 BUTTON 文字置中 #
with dpg.theme() as border_table_time_theme:
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (255,255,255,255))
with dpg.theme() as tick_time_theme:
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (37,37,38,255))
with dpg.theme() as table_tail_theme2:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (252,242,2,177))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (247,255,120,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.37,0.5)
with dpg.theme() as table_tail_theme_out_text:
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.08,0)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (247,255,120,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            
with dpg.theme() as table_tail_theme:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (252,242,2,177))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (247,255,120,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
##            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
with dpg.theme() as spec_theme_center:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
# FOCUS PRICE
with dpg.theme() as focus_test:
            a= 0,255,255,255
            b= 87,87,87,255
            dpg.add_theme_color(dpg.mvThemeCol_Text,a)# BTN TEXT COL
            dpg.add_theme_color(dpg.mvThemeCol_Button, b)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
##            dpg.add_theme_color(dpg.mvThemeCol_Border,(0,255,255,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.3,0.5)
with dpg.theme() as uplimit_table_bid:
            dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,0,255))# BTN TEXT COL
            dpg.add_theme_color(dpg.mvThemeCol_Button, (246,14,8,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(255,0,0,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.37,0.5)
with dpg.theme() as dnlimit_table_bid:
            dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,0,255))# BTN TEXT COL
            dpg.add_theme_color(dpg.mvThemeCol_Button, (6,134,11,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(255,0,0,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.37,0.5)
with dpg.theme() as uplimit_table_ask:
            dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,0,255))# BTN TEXT COL
            dpg.add_theme_color(dpg.mvThemeCol_Button, (246,14,8,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(0,255,255,255))
           
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.37,0.5)
with dpg.theme() as dnlimit_table_ask:
            dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,0,255))# BTN TEXT COL
            dpg.add_theme_color(dpg.mvThemeCol_Button, (6,134,11,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(0,255,255,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.37,0.5)

            
with dpg.theme() as deep_blue_focus_price_ask:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (250,250,2,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, DEEPBLUE)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(0,255,255,255))
with dpg.theme() as deep_red_focus_price_ask:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (250,250,2,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, DEEPRED)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(0,255,255,255))
with dpg.theme() as deep_red_focus_price_bid:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (250,250,2,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, DEEPRED)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(255,0,0,255))
with dpg.theme() as deep_blue_focus_price_bid:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (250,250,2,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, DEEPBLUE)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(255,0,0,255))
with dpg.theme() as mid_theme_focus_price_ask:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (250,250,2,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(0,255,255,255))
with dpg.theme() as mid_theme_focus_price_bid:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (250,250,2,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border,(255,0,0,255))
with dpg.theme() as mid_theme:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (250,250,2,179))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (227,235,28,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
with dpg.theme() as deep_red_theme:
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255,122,165,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as deep_red_theme_align:# FOR  table_text_align_style ==1 (使用 全體置右 報價置中)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255,122,165,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as deep_red_theme_align_border:# FOR  table_text_align_style ==1 (使用 全體置右 報價置中)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255,122,165,255))
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0) 
with dpg.theme() as red_theme:
            dpg.add_theme_color(dpg.mvThemeCol_Button, (247,164,203,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as red_theme_align:# FOR  table_text_align_style ==1 (使用 全體置右 報價置中)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (247,164,203,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
with dpg.theme() as red_theme_align_border:# FOR  table_text_align_style ==1 (使用 全體置右 報價置中)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (247,164,203,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
with dpg.theme() as deep_red_theme_out_text:
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.08,0)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255,122,165,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as red_theme_out_text:
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.08,0)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (247,164,203,255))
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as blue_theme_out_text:
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.08,0)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (104,212,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as deep_blue_theme_out_text:
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.08,0)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (5,177,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as blue_theme:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (105,138,224,255))#1
            dpg.add_theme_color(dpg.mvThemeCol_Button, (104,212,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as blue_theme_align:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (105,138,224,255))#1
            dpg.add_theme_color(dpg.mvThemeCol_Button, (104,212,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
with dpg.theme() as blue_theme_align_border:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (105,138,224,255))#1
            dpg.add_theme_color(dpg.mvThemeCol_Button, (104,212,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)       
with dpg.theme() as deep_blue_theme:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (50,78,151,255))#1
            dpg.add_theme_color(dpg.mvThemeCol_Button, (5,177,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
with dpg.theme() as deep_blue_theme_align:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (50,78,151,255))#1
            dpg.add_theme_color(dpg.mvThemeCol_Button, (5,177,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
with dpg.theme() as deep_blue_theme_align_border:
##            dpg.add_theme_color(dpg.mvThemeCol_Button, (50,78,151,255))#1
            dpg.add_theme_color(dpg.mvThemeCol_Button, (5,177,255,255))#2
            if table_text_col_style==2:dpg.add_theme_color(dpg.mvThemeCol_Text,(0,0,0,255))# BTN TEXT COL Black
            if table_text_align_style==1:dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.32,0.5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)

with dpg.theme() as Window_rounding:
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding,12)            
with dpg.theme() as Frame_rounding:
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,12)
#========================================================

def value_align(value,len_):# 將數字校正補0
    val_len=len(str(value))
    if val_len<len_:
        diff_=len_- val_len
        return str(value)+'0'*diff_
    return str(value)
class Style_01:
        
        def add_mouse_move_handler(self,s,data):
            
            
            if self._last_focus_table:
                      
                      last_item_ori_theme= dpg.get_item_disabled_theme(self._last_focus_table)
                      dpg.set_item_theme(self._last_focus_table,last_item_ori_theme)
                      dpg.set_item_font(self._last_focus_table,DefaultFont)
                      self._loop_start=0
            for i in self.dict_chose_list[str(self.now_tick_mode)]['button']:
                if dpg.is_item_hovered(i) :
                    
                    user_data=dpg.get_item_user_data(i)                  
                    self._last_focus_table=user_data[1]
                    dpg.set_item_theme(user_data[1],focus_test)
                    dpg.set_item_font(user_data[1],FONT0001)

                    return
            for updn in ['uplimit','dnlimit']:
              for i in self.dict_chose_list[updn]['button']:
                  if dpg.is_item_hovered(i) :
                        user_data=dpg.get_item_user_data(i)
                        self._last_focus_table=user_data[1]

                        dpg.set_item_theme(user_data[1],focus_test)
                        dpg.set_item_font(user_data[1],FONT0001)

                        return
        def add_hover_handler(self,s,data,app_data):
          
            child_id=self.offset+'tk'+str(self.now_tick_mode)+'_window'
            self.hover_child_id_time=child_id,time.time(),dpg.get_y_scroll(child_id)
            self.api_cls2.hover_child_id_time=child_id,time.time(),dpg.get_y_scroll(child_id)
            
            
##            print(dpg.is_item_toggled_open(s))
        def add_mouse_wheel_handler(self,s,data):# 可設定滾輪的移動STEP
           
            _id_,last_time,initial_y=self.hover_child_id_time
            _id2,_,_=self.api_cls2.hover_child_id_time
            if _id2!=_id_ or self.offset+'tk'+str(self.now_tick_mode)+'_window'!=_id_:return
            if data>0:
                data=1
            else:
                data=-1
            change=dpg.get_y_scroll(_id_)-data*self.wheel_change_step
            if (dpg.is_item_hovered(_id_)):
                
                if dpg.get_y_scroll(_id_)<=0 or dpg.get_y_scroll(_id_)>=dpg.get_y_scroll_max(_id_):pass
                else:
                    if change>0:
                        
                        if change>=dpg.get_y_scroll_max(_id_):change=dpg.get_y_scroll_max(_id_)
                        elif change<=0:
                            change=0
                        
                        dpg.set_y_scroll(_id_,change)
        def add_mouse_drag_handler(self,s,data,callback=add_hover_handler):
            
            y_change=data[2]
            
            _id_,last_time,initial_y=self.hover_child_id_time
            _id2,_,_=self.api_cls2.hover_child_id_time
            if _id2!=_id_ or self.offset+'tk'+str(self.now_tick_mode)+'_window'!=_id_:return
            if (time.time()-last_time)<5:
              
              y_change=y_change/3

              if 1:
                  change=dpg.get_y_scroll(_id_)+y_change
                  if self._last_hover_drag_mouse_y_scroll!=-1:
                    if abs(change-self._last_hover_drag_mouse_y_scroll)<20:return
                    if y_change>0:
                        # 往下拉
                      if change<self._last_hover_drag_mouse_y_scroll and self._last_hover_drag_mouse_y_scroll!=-1:return
                    elif y_change<0:# 往上拉 數值要減少 但是不減反增就跳過
                      if change>self._last_hover_drag_mouse_y_scroll and self._last_hover_drag_mouse_y_scroll!=-1:return
                  if change==self._last_hover_drag_mouse_y_scroll:return
                  self._last_hover_drag_mouse_y_scroll=change
                  
               
                  if change<=0:pass
                  elif change>=0:
                    dpg.set_y_scroll(_id_,change)
            

        def add_mouse_click_handler(self,s,data):
       
            if data==1 and self.right_trigger_del:
             for i in self.dict_chose_list[str(self.now_tick_mode)]['button']:
                if dpg.is_item_hovered(i) or dpg.is_item_focused(i):
                    
                    user_data=dpg.get_item_user_data(i)
                    if '刪' in str(user_data):
                        
                        child_id=self.offset+'tk'+str(self.now_tick_mode)+'_window'
                        print(dpg.is_item_focused(child_id),dpg.is_item_hovered(child_id))
                        self.submit(i,None,user_data)
                    break
        def _keyboard(self,s,data):
            child_id=self.offset+'tk'+str(self.now_tick_mode)+'_window'
          
            if data[0]==38:# up arrow
                 
                  change=dpg.get_y_scroll(child_id)-28
                  if change<=0:change=0
                  elif change>=dpg.get_y_scroll_max(child_id):
                      change=dpg.get_y_scroll_max(child_id)
                  dpg.set_y_scroll(child_id,change)
                  self._last_hover_drag_mouse_y_scroll=change
              
            if data[0]==40:# dn arrow
                  change=dpg.get_y_scroll(child_id)+28
                  if change<=0:change=0
                  elif change>=dpg.get_y_scroll_max(child_id):
                      change=dpg.get_y_scroll_max(child_id)
                  
                  dpg.set_y_scroll(child_id,change)
                  self._last_hover_drag_mouse_y_scroll=change
                
            if data[0]==27:#esc
                if self.build_check_box:
                 if dpg.is_item_shown(self.build_check_box):
                    dpg.delete_item(self.build_check_box)
                    self.build_check_box=''
        def warn_info(self,title, message,selection_callback):
          if not self.build_check_box:
                with dpg.mutex():

                    viewport_width = dpg.get_viewport_client_width()
                    viewport_height = dpg.get_viewport_client_height()

                    with dpg.window(label=title, modal=True,width=200,show=False) as modal_id:
                        self.build_check_box=modal_id
                        
                    
                        dpg.add_text('  ')
                        dpg.add_same_line(spacing=30)
                        dpg.add_text(message)
                        dpg.add_text('  ')
                        dpg.add_same_line(spacing=50)
                        dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=selection_callback,id=self.warn_submit_ok)
                # guarantee these commands happen in another frame
                dpg.split_frame()
                width = dpg.get_item_width(modal_id)
                height = dpg.get_item_height(modal_id)
                dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])
                dpg.configure_item(modal_id,show=True)
                dpg.set_item_theme(self.warn_submit_ok,Frame_rounding)
                dpg.set_item_theme(modal_id,Window_rounding)
        def show_info(self,title, message, selection_callback,BS,price,user_data='',amount=0,trigger=0,common=0):# common= 普通買賣
          if not self.build_check_box:
            # guarantee these commands happen in the same frame
            with dpg.mutex():

                viewport_width = dpg.get_viewport_client_width()
                viewport_height = dpg.get_viewport_client_height()

                with dpg.window(label=title, modal=True, no_close=True,width=400,show=False) as modal_id:
                    # no_close =True 右上角的XX就會消失
                    with dpg.table(header_row=False):
                     
                        dpg.add_table_column(width_stretch=False,init_width_or_weight =0.2)
                        dpg.add_table_column(width_stretch=False,init_width_or_weight =0.8)
                        dict_=[[],[]]
                        dict_=['帳號','商品','當沖','買賣','價格','數量','時間']
                      
                        for row_ in range(0,7): 
                            with dpg.table_row():# 先ROW 再COL
                        
                                for col_ in range(0, 2):
                                    cnt=(dict_[row_])
                                    if col_==0:
                                        dpg.add_text(cnt)
                                    else:
                                        
                                        if '帳號' in str(cnt):
                                            cnt= dpg.get_value(self.account_chose_id)
                                            
                                        elif '商品' in str(cnt):
                                            cnt=self.code_name
                                        elif '當沖' in str(cnt):
                                            cnt=dpg.get_value(self.cond_day_trade)
                                        elif '買賣' in str(cnt):
                                            order_type=dpg.get_value(self.ORDER_TYPE)
                                            if dpg.get_value(self.gp0_show)==False:
                                                gp0_cnt=(dpg.get_item_label(self.gp0_show))# 代表為CHECKBOX
                                            else:
                                                gp0_cnt=(dpg.get_value(self.gp0_show))
                                            cnt=BS_LIST_CHI[BS]+gp0_cnt+order_type
                                        elif '價格' in str(cnt):
                                            cnt=price
                                        elif '時間' in str(cnt):
                                            cnt=datetime.datetime.now().strftime("%H:%M:%S")
                                        elif '數量' in str(cnt):
                                            if amount:
                                                cnt=amount
                                            else:
                                                cnt=dpg.get_value(self.trade_unit_amount)
                                                amount=cnt
                                        dpg.add_text(cnt)
                    
                    self.build_check_box=modal_id

                    dpg.add_text('  ')
                    dpg.add_same_line(spacing=115)
                    dpg.add_text(message)
                    

                    dpg.add_text('  ')
                    dpg.add_same_line(spacing=100)
                    
                    dpg.add_button(label="Ok", width=75, user_data=(modal_id, True,BS,price,amount,trigger,common,user_data), callback=selection_callback,id=self.show_info_ok)
                    dpg.add_same_line(spacing=20)
                    dpg.add_button(label="Cancel", width=75, user_data=(modal_id, False,BS,price,amount,trigger,common,user_data), callback=selection_callback,id=self.show_info_cancel)
                    dpg.set_item_theme(self.show_info_ok,Frame_rounding)
                    dpg.set_item_theme(self.show_info_cancel,Frame_rounding)
                    dpg.set_item_theme(modal_id,Window_rounding)
                    

            # guarantee these commands happen in another frame
            dpg.split_frame()
            width = dpg.get_item_width(modal_id)
            height = dpg.get_item_height(modal_id)
            dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])
            dpg.configure_item(modal_id,show=True)
        def _loop_chg_col(self,id_,change_var):# 不停更換顏色
            change_col_list=[2,0,1,2,0,1]# 先上升再下降 255,12,12,255
            initial=[255,12,12,255]
            while self._loop_start:
             
              for idx in change_col_list:
                  while self._loop_start:
                      change=30
                      if idx<0:
                          change=-30
                      initial[idx]+=change
                      with dpg.theme() as chg_theme:
                            dpg.add_theme_color(change_var,(initial[0],initial[1],initial[2],initial[3]))
                      dpg.set_item_theme(id_,chg_theme)
                      if initial[idx]>=255:
                          
                          break
                      time.sleep(1)
                
        def on_selection_warn(self,sender, unused, user_data):
               
                self.build_check_box=''
                dpg.delete_item(user_data[0])
        def on_selection(self,sender, unused, user_data):
                bs=BS_LIST_num[user_data[2]]
                price=(user_data[3])
                common=0
                bs_num=0
                amount=user_data[4]
                _user_data_=user_data[7]
                if len(user_data)>4:
                  if user_data[4] and user_data[5]: # 4 /5  = amount / trigger 
                    del self.trigger_dict[bs][price]
                    self.before_quote(trigger=1)
                    self._refresh_trigger(0,0,dn_refresh=1)
                  elif user_data[4] and user_data[6]:    # 4 /6  = amount / common 
                    amount=user_data[4]
                    common=1
                    bs_num=BS_LIST_num['Common'+user_data[2]]
                print(user_data)
                if user_data[1]:
                    print("User selected 'Ok'")
                    '''submit place_order'''
                    self.Order(BS_LIST[bs],amount,price)
                    if common :
                        
                        print(_user_data_,bs_num not in self.trigger_dict,price not in self.trigger_dict)        
                        if bs_num not in self.trigger_dict:return 
                        if price not in self.trigger_dict[bs_num]:
                            self.trigger_dict[bs_num][price]=amount,self.close,0
                        else:
                            exist_amount,_entry_close,deal_amount=self.trigger_dict[bs_num][price]
                            amount+=exist_amount
                            self.trigger_dict[bs_num][price]=amount,_entry_close,deal_amount
                        if len(_user_data_)>5:
                            if _user_data_[3] in self.dict_chose_list[_user_data_[5]]['common'][bs_num]:
                               
                                dpg.configure_item( _user_data_[3],label=str(amount)+'('+str(len(self.trigger_dict[bs_num]))+')')
                                if bs_num==3:
                                    tag_id=_user_data_[3]-1
                                else:
                                    tag_id=_user_data_[3]+1
                                dpg.configure_item( tag_id,label='D')
                        else:
                            

                                dpg.configure_item( _user_data_[3],label=str(amount)+'('+str(len(self.trigger_dict[bs_num]))+')')
                                
                                if bs_num==3:
                                    tag_id=_user_data_[3]-1
                                else:
                                    tag_id=_user_data_[3]+1
                                dpg.configure_item( tag_id,label='D')
                        threading.Thread(target=self._refresh_trigger,args=(0,0,),kwargs={'dn_refresh':1}).start()
                        self.before_quote(common=1)
                else:
                    print("User selected 'Cancel'")

             
                self.build_check_box=''
                dpg.delete_item(user_data[0])
        #===== DEAL =====
        def Order(self,bs,amount,price):
            print('★  ',datetime.datetime.now().strftime("%H:%M:%S"),bs,price,amount)
            '''api.place_order()''' 
        def double_click_button(self,sender,app_data,user_data):
            print(app_data,user_data)
        def __init__(self,api,api_cls2):
            
            self._loop_start=0# 不停更換THEME顏色的FLAG
            self._last_focus_table=0# 最後停留在哪個表格的HOVER
            self.___checkbug=0
            
            self.offset=str(time.time())[6:14]#
            self.dict_tick_vol={}
            print("New Offset:",self.offset)
            # id set
            self.show_info_ok=self.offset+'show_info_submit_ok'
            self.show_info_cancel=self.offset+'show_info_submit_cancel'
            self.warn_submit_ok=self.offset+'warn_submit_ok'
            self.trade_tick_time=self.offset+'trade_tick_time'
            self.ask_sum=self.offset+'ask_sum'
            self.bid_sum=self.offset+'bid_sum'
            self.ask_trigger_tag=self.offset+'ask_trigger_tag'
            self.ask_trigger=self.offset+'ask_trigger'
            self.bid_trigger_tag=self.offset+'bid_trigger_tag'
            self.bid_trigger=self.offset+'bid_trigger'

            self.ask_common=self.offset+'ask_common'
            self.bid_common=self.offset+'bid_bid_common'
            self.tick_time=self.offset+'tick_time'
            self.tick_change=self.offset+'tick_change'

            self.trade_unit_amount=self.offset+'trade_unit_amount'
            self.align_center=self.offset+'align_center'
            self.cond_day_trade=self.offset+'cond_day_trade'
            self.ORDER_TYPE=self.offset+'ORDER_TYPE'
            self.code_name_id=self.offset+'code_name'
            self.code_text=self.offset+'code_text'
            self.account_chose_id=self.offset+'account_chose'

            self.code_combo=self.offset+'code_combo'

            self.uplimit_price=self.offset+'uplimit_price'
            self.dnlimit_price=self.offset+'dnlimit_price'
            self.uplimit_float_input=self.offset+'uplimit_float_input'
            self.dnlimit_float_input=self.offset+'dnlimit_float_input'
            #==
            
            self.api_cls2=api_cls2# 主要接收行情的中心
            
            self._last_hover_drag_mouse_y_scroll=-1
            self.wheel_change_step=28# 滾輪移動STEP 原始滑鼠滾輪=87 / times
            self.hover_child_id_time=0,0,0# for drag mouse use
            self.right_trigger_del=1# 右鍵觸發 Button選項 刪單
            self.trigger_dict={1:{},2:{},3:{},4:{}}# 每次新的contract都要更新 1=buy 2=sell 3:普通買進 4:普通賣出
            self.col_name=['觸價','刪','買進','買未成交','報價','賣未成交','賣出','刪','觸價']
            self.click_list=[]
            self.uplow_sign=[' ','▲','▽']
            self.build_check_box=''# msg box id
            self.account_chose='Temp_FUT_Account-001'
            
            self.dict_chose_list={}
            self.code_name='test code name'
            self.snap_=''
            self.last_close=0
            self.change_price=0
            self.change_rate=0
            self.now_contract=''
            self.double_trigger=1 # 1:雙擊  0:單擊 任何單式 單擊觸發下單
            self.close=''
            self.quote=''
            self.subscribe=1 # 用以截斷行情            
            self.col=9   # 原始欄位數
            self.api=api
            self.submit_before_ask=1# 下單前詢問
            self.account_list=['stock_0002','future0001']#
            # 一開始就訂閱 加權指數
            if self.api:
                self.account_list=[]
                self.account=self.api_cls2.account
                
                for type_ in self.account:
                    acc_name=self.account[type_][2]
                    self.account_list.append(acc_name)
                self.api_cls2.style_v1_list.append(self)

                
                self.index_001=self.api_cls2.index_001
                self.Tse_day=self.api_cls2.Tse_day

                self.index001_snap=self.api_cls2.index001_snap

                self.index_close=self.api_cls2.index_close
                self.index_change_price=self.api_cls2.index_change_price
                self.index_change_rate=self.api_cls2.index_change_rate
                self.index_last_close=self.api_cls2.index_last_close
                
                self.TXFContract=self.api_cls2.TXFContract
                self.txf_snap=self.api_cls2.txf_snap
                self.txf_change_price=self.api_cls2.txf_change_price
                self.txf_change_rate=self.api_cls2.txf_change_rate

                self.txf_close=self.api_cls2.txf_close
                self.txf_last_close=self.api_cls2.txf_last_close

            self.now_tick_mode=''
            
            self.now_code=''
            self._style='Style01'
            self.chose_list=['五檔','5','10','20']
            self.dict_chose_list={}

            for i in self.chose_list:
                self.dict_chose_list[i]={}
            self.Main()
            self.Make_tk_window(self.SN,self.chose_list)
            time.sleep(0.5)
            threading.Thread(target=self._run_time_count).start()
            allitem=set(dpg.get_all_items())
            if api_cls2:
                for already in self.api_cls2.item_dict:
                    allitem-=set(self.api_cls2.item_dict[already])
                self.api_cls2.item_dict[self]=allitem
                for i in allitem:
                    nowitem_theme=dpg.get_item_theme(i)
                    if nowitem_theme:
                        dpg.set_item_disabled_theme(i,nowitem_theme)
        def _run_time_count(self):
            while 1:
              Time=datetime.datetime.now()
              dpg.set_value(self.tick_time,'       '+Time.strftime("%H:%M:%S"))
              time.sleep(1)
      
       
        def make_updn_table(self,updn):
          height=55
          
          if 'dn' in updn:
              height=75
          with dpg.child(id=self.offset+'tk'+str(updn)+'_window',show=True, parent=self.SN,width=700, height=height):#,border =False

             with dpg.table(height=0,header_row=False):

                   dpg.add_table_column(width_stretch=False,init_width_or_weight =0.8)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =0.5)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =0.8)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =1.6)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =1.6)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =1.6)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =0.8)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =0.5)
                   dpg.add_table_column(width_stretch=False,init_width_or_weight =0.8)
                   col=self.col
                   
                   if 1:
                     row=2
                     if 'dn' in updn:row=3
                     
                     if updn not in self.dict_chose_list:self.dict_chose_list[updn]={}
                     self.dict_chose_list[updn]['button']=[]
                     self.dict_chose_list[updn]['trig']={}
                     self.dict_chose_list[updn]['trig'][1]=[]
                     self.dict_chose_list[updn]['trig'][2]=[]
                     self.dict_chose_list[updn]['common']={}
                     self.dict_chose_list[updn]['common'][3]=[]
                     self.dict_chose_list[updn]['common'][4]=[]
                     
                     for i in range(0, row):
                        
                        with dpg.table_row():
                         index_=0
                         base_index=dpg.last_item()
                         
                         for j in range(0, 9):
                             width_=150
                             close_index=index_+(4-index_%9)+base_index+1
                             my_id_=base_index+1+index_
                             
                             bs=1
                             if index_%9>=5:
                                 bs=2
                             if i==1 and j==col//2:
                                 id_chose=self.uplimit_float_input
                                 if 'dn' in updn:
                                     id_chose=self.dnlimit_float_input
                                 
                                 myid=dpg.add_input_float(label=updn+'_float_input',width=125,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),format="%.2f",max_value =999999,callback=self.submit,id=id_chose)
                                 id_chose=''
                             else:
                                 if i==0 and j==col//2:
                                      id_chose=self.uplimit_price
                                      if 'dn' in updn: id_chose=self.dnlimit_price
                                      
                                      myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit,id=id_chose)
                                 elif i==0 and j==col//2-1 and 'dn' in updn:
                                     myid=dpg.add_button(label='跌停',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit)
                                 elif i==0 and j==col//2+1 and 'up' in updn:
                                     myid=dpg.add_button(label='漲停',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit)
                                 elif  'dn' in updn and i==2:
                                     
                                     if index_%9==0:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn,self.bid_trigger),callback=self.submit,id=self.bid_trigger)
                                     elif index_%9==1:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn,self.bid_trigger_tag),callback=self.submit,id=self.bid_trigger_tag)
                                     elif index_%9==2:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn,self.bid_common),callback=self.submit,id=self.bid_common)
                                     elif index_%9==3:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit,id=self.bid_sum)
                                     elif index_%9==5:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit,id=self.ask_sum)
                                     elif index_%9==6:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn,self.ask_common),callback=self.submit,id=self.ask_common)
                                     elif index_%9==7:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn,self.ask_trigger_tag),callback=self.submit,id=self.ask_trigger_tag)
                                     elif index_%9==8:
                                           myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn,self.ask_trigger),callback=self.submit,id=self.ask_trigger)
                                     elif j==col//2:
                                           myid=dpg.add_button(label='Tick time',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit,id=self.trade_tick_time)
                                           
                                     else: myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit)
                                 else: myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j],updn),callback=self.submit)
                             self.dict_chose_list[updn]['button'].append(myid)
                             
                             if j<col//2 :
                                 if   'up'in updn: dpg.set_item_theme(myid,red_theme)
                                 elif 'dn'in updn: dpg.set_item_theme(myid,deep_red_theme)
                                 if index_%9==3 :
                                     if   'up'in updn:dpg.set_item_theme(myid,red_theme_align_border)# 無線條

                             elif j==col//2 :

                                 if table_text_align_style==1:
                                     if   'up' in updn: dpg.set_item_theme(myid,deep_blue_theme_align)
                                     elif 'dn' in updn: dpg.set_item_theme(myid,deep_red_theme_align)
                                 else:
                                   if   'up' in updn: dpg.set_item_theme(myid,deep_blue_theme)
                                   elif 'dn' in updn: dpg.set_item_theme(myid,deep_red_theme)
                             elif j>col//2:
                                 if    'up' in updn:  dpg.set_item_theme(myid,deep_blue_theme)
                                 elif  'dn' in updn:  dpg.set_item_theme(myid,blue_theme)
                                 if index_%9==5 :
                                     if 'dn'in updn: dpg.set_item_theme(myid,blue_theme_align_border)# 無線條
                             
                             if i==0 and j==col//2 or ( i==0 and j==col//2-1 and 'dn' in updn)  or ( i==0 and j==col//2+1 and 'up' in updn):
                                if  'up' in updn :  dpg.set_item_theme(myid,uplimit_table)
                                elif'dn' in updn :  dpg.set_item_theme(myid,dnlimit_table)
                             if i==1 and j==col//2 :# 價格 Float input 
                                if 'up' in updn:dpg.set_item_theme(myid,table_set_my_price_blue)
                                else:dpg.set_item_theme(myid,table_set_my_price_red)
                             if i==2 and 'dn' in str(updn):
                                
                                 dpg.set_item_theme(myid,table_tail_theme)
                                 if 'Tick time' in str(dpg.get_item_label(myid)):
                                    dpg.set_item_theme(self.trade_tick_time,table_tail_theme2)
                             find_out=re.findall('[012678]',str(index_%9))
                             if find_out :
                                 
                                 find_out=int(find_out[0])
                                 
                                     
                                 if i==2:dpg.set_item_theme(myid,table_tail_theme_out_text) 
                                 elif find_out>=5:
                                     if 'up' in updn:dpg.set_item_theme(myid,deep_blue_theme_out_text)
                                     else:dpg.set_item_theme(myid,blue_theme_out_text)
                                     if find_out==6:self.dict_chose_list[updn]['common'][4].append(myid)
                                     else:self.dict_chose_list[updn]['trig'][2].append(myid)
                                 else:
                                     if 'dn' in updn :dpg.set_item_theme(myid,deep_red_theme_out_text)
                                     else:
                                       dpg.set_item_theme(myid,red_theme_out_text)
                                     if find_out==2:self.dict_chose_list[updn]['common'][3].append(myid)
                                     else:self.dict_chose_list[updn]['trig'][1].append(myid)
##                                 dpg.configure_item(myid,label=1)    
                             
                             index_+=1
                        
        def Make_tk_window(self,SN,chose_list):
            
            self.make_updn_table('uplimit')
            
            for set_value in chose_list:
               height=250 
               if not re.findall('五|5',str(set_value)):
                             height=350
               with dpg.child(id=self.offset+'tk'+str(set_value)+'_window', parent=SN,height=height,width=700,show=False):
                 
                  
           
                  with dpg.table(header_row=False,  row_background=False, height=height,width=0, freeze_rows=0, freeze_columns=0):

                       dpg.add_table_column(width_stretch=False,label="   觸價",init_width_or_weight =0.8)
                       dpg.add_table_column(width_stretch=False,label="  刪",init_width_or_weight =0.5)
                       dpg.add_table_column(width_stretch=False,label="   買進",init_width_or_weight =0.8)
                       dpg.add_table_column(width_stretch=False,label="Header 4",init_width_or_weight =1.6)
                       dpg.add_table_column(width_stretch=False,label="報價",init_width_or_weight =1.6)
                       dpg.add_table_column(width_stretch=False,label="Header 6",init_width_or_weight =1.6)
                       dpg.add_table_column(width_stretch=False,label="   賣出",init_width_or_weight =0.8)
                       dpg.add_table_column(width_stretch=False,label="  刪",init_width_or_weight =0.5)
                       dpg.add_table_column(width_stretch=False,label="   觸價",init_width_or_weight =0.8)
                       col=self.col
                       
                       self.dict_chose_list[str(set_value)]['button']=[]
                       self.dict_chose_list[str(set_value)]['child']=[self.offset+'tk'+str(set_value)+'_window_child']
                       self.dict_chose_list[str(set_value)]['spec']=[] # 特殊標籤 / OHLC
                       with dpg.clipper(id=self.offset+'tk'+str(set_value)+'_window_child'):
                         if '五' in str(set_value):
                             
                             _set_value=5
                         else:_set_value=int(set_value)
                         row=(_set_value)*2+1
                         
                         for i in range(0, row):
                            
                            with dpg.table_row():
                             index_=0
                             base_index=dpg.last_item()
                             
                             for j in range(0, 9):
                                 width_=150
 
                                 close_index=index_+(4-index_%9)+base_index+1
                                 my_id_=base_index+1+index_
                                 
                                 bs=1
                                 if index_%9>=5:
                                     bs=2
                                 myid=dpg.add_button(label='',width=width_,user_data=(index_,close_index,bs,my_id_,self.col_name[j]),callback=self.submit)
                                 self.dict_chose_list[str(set_value)]['button'].append(myid)
                                 
                                 if j<col//2 :
                                     if   i>row//2: dpg.set_item_theme(myid,deep_red_theme)
                                     elif i<row//2: dpg.set_item_theme(myid,red_theme)
                                     if index_%9==3 and i<row//2 :
                                         if abs(i-row//2)>5:dpg.set_item_theme(myid,red_theme_align_border)# 無線條
                                         else :
                                             self.dict_chose_list[str(set_value)]['spec'].append(myid)
                                       
                                 elif j==col//2 :

                                     if table_text_align_style==1:
                                         if   i>row//2: dpg.set_item_theme(myid,deep_red_theme_align)
                                         elif i<row//2: dpg.set_item_theme(myid,deep_blue_theme_align)
                                          
                                     else:
                                       if   i>row//2: dpg.set_item_theme(myid,deep_red_theme)
                                       elif i<row//2: dpg.set_item_theme(myid,deep_blue_theme)
                                 elif j>col//2:
                                     if   i>row//2: dpg.set_item_theme(myid,blue_theme)
                                     elif i<row//2: dpg.set_item_theme(myid,deep_blue_theme)
                                     if index_%9==5 and i>row//2 :
                                         if  abs(i-row//2)>5 :dpg.set_item_theme(myid,blue_theme_align_border)# 無線條
                                         else :
                                             self.dict_chose_list[str(set_value)]['spec'].append(myid)
                                 if i==row//2 :
                                     
                                     dpg.set_item_theme(myid,mid_theme)
                                     if index_%9==3 :
                                                 self.dict_chose_list[str(set_value)]['spec'].append(myid)
##                                                 dpg.set_item_theme(myid,spec_theme_center)
                                                 
                                     if index_%9==5 :
                                         self.dict_chose_list[str(set_value)]['spec'].append(myid)
##                         
                                 find_out=re.findall('[012678]',str(index_%9))
                                 if find_out and i!=row//2:
                                     find_out=int(find_out[0])
                                     if find_out>=5:

                                         if i<row//2:dpg.set_item_theme(myid,deep_blue_theme_out_text)
                                         else: dpg.set_item_theme(myid,blue_theme_out_text)
                                     else:
                                         if i>row//2:dpg.set_item_theme(myid,deep_red_theme_out_text)
                                         else:dpg.set_item_theme(myid,red_theme_out_text)
                                 index_+=1
                              
            for set_value in chose_list:
                now_show_id=self.offset+'tk'+str(set_value)+'_window'
                dpg.configure_item(now_show_id,show=True)
                
                dpg.configure_item(now_show_id,show=False)
                dpg.add_hover_handler(callback=self.add_hover_handler,parent=self.offset+'tk'+str(set_value)+'_window')
            first_tk_id=self.offset+'tk'+str(chose_list[0])+'_window'
            
            dpg.configure_item(first_tk_id, show=True)
            self.make_updn_table('dnlimit')
         
        def TickChange(self,sender,app_data):
            self._last_hover_drag_mouse_y_scroll=-1
          
            
            set_value=(dpg.get_value(sender))
            
            if self.now_tick_mode==set_value:return
            self.subscribe=0
            self.now_tick_mode=set_value
            
            now_show_id=self.offset+'tk'+str(set_value)+'_window'           
            self.subscribe=1
            self.quote=''
         
            self.before_quote()
            for i in self.chose_list:
                _id=self.offset+'tk'+str(i)+'_window'
                if dpg.is_item_shown(_id) and _id!=now_show_id:
                    dpg.configure_item(_id,show=False)

            self._Update_spec_label()
            dpg.configure_item(now_show_id,show=True)
            
            self.set_align_center_yscroll(_id=now_show_id)

        def _refresh_common(self,btn,price,del_all=0 ,dn_refresh=0, common=0,all=0):
                        bid_common_sum=0
                        ask_common_sum=0

                        for trg_ in range(3,5):# 刷新 普通單
                                    if not dn_refresh:
                                        
                                        if trg_==3:# bid 買進端
                                                com_tag_id=btn-2
                                                com_tag_del=btn-3
                                                
                                             
                                        else:
                                                com_tag_id=btn+2
                                                com_tag_del=btn+3
                                        if price in self.trigger_dict[trg_]:
                                            
                                            dpg.configure_item(com_tag_del,label="D")
                                            
                                            total_amount,avg_entry_close_,deal_amount=self.trigger_dict[trg_][price]
                                            

                                            dpg.configure_item(com_tag_id,label=str(total_amount)+'('+str(len(self.trigger_dict[trg_]))+')')
                                            
                                        else:
                                            dpg.configure_item(com_tag_id,label='')
                                            if price not in self.trigger_dict[trg_-2]:
                                                dpg.configure_item(com_tag_del,label="")
                                            
                                    
                                    for pp in self.trigger_dict[trg_]:
                                        
                                        total_amount,avg_entry_close_,deal_amount=self.trigger_dict[trg_][pp]
                                        if trg_==3:
                                                bid_common_sum+=int(total_amount)
                                        else:
                                                ask_common_sum+=int(total_amount)
                                    
                                    if bid_common_sum:
                                       dpg.configure_item(self.bid_common,label=str(bid_common_sum)+'('+str(len(self.trigger_dict[3]))+')')
                                       dpg.configure_item(self.bid_trigger_tag,label='D')
                                    else:
                                       dpg.configure_item(self.bid_common,label="")
                                    if ask_common_sum:
                                       dpg.configure_item(self.ask_trigger_tag,label='D') 
                                       dpg.configure_item(self.ask_common,label=str(ask_common_sum)+'('+str(len(self.trigger_dict[4]))+')')
                                    else:
                                       dpg.configure_item(self.ask_common,label="")
                                    
                        return bid_common_sum,ask_common_sum
        def _refresh_trigger(self,btn,price,del_all=0,dn_refresh=0, common=0):

                    bidvol,askvol=0,0
                    if del_all:
                        dpg.configure_item(self.ask_trigger_tag,label='')
                        dpg.configure_item(self.ask_trigger,label='')
                   
                        dpg.configure_item(self.bid_trigger_tag,label='')
                        dpg.configure_item(self.bid_trigger,label='')
                        return
                    if dn_refresh or common: # 下盤更新
                        
                        bid_common_sum,ask_common_sum=self._refresh_common(btn,price,dn_refresh=1)      
                        for trg_ in range(1,3):# 刷新 觸價單
                            for _price in self.trigger_dict[trg_]:
                                total_amount,avg_entry_close_,_=self.trigger_dict[trg_][_price]
                                if trg_==1 :
                                                bidvol+=int(total_amount)
                                else:
                                                askvol+=int(total_amount)
                            
                        if askvol:
                               dpg.configure_item(self.ask_trigger_tag,label='D')
                               dpg.configure_item(self.ask_trigger,label=str(askvol)+'('+str(len(self.trigger_dict[2]))+')')
                        else:
                            dpg.configure_item(self.ask_trigger,label='')

                            if not ask_common_sum:
                               bs_=2
                               for trg_updn in ['uplimit','dnlimit']:
                                            for trg_each in self.dict_chose_list[trg_updn]['trig'][bs_]:
                                              dpg.configure_item(trg_each,label='') 
                                  
                                            for trg_each in self.dict_chose_list[trg_updn]['common'][bs_+2]:
                                               dpg.configure_item(trg_each,label='')
                                   
                               dpg.configure_item(self.ask_trigger_tag,label='')
                              
                                
                        if bidvol:
                               dpg.configure_item(self.bid_trigger_tag,label='D')
                               dpg.configure_item(self.bid_trigger,label=str(bidvol)+'('+str(len(self.trigger_dict[1]))+')')
                        else:
                            dpg.configure_item(self.bid_trigger,label='')
                            
                                          
                            if not bid_common_sum:
                                   bs_=1
                                   for trg_updn in ['uplimit','dnlimit']:
                                            for trg_each in self.dict_chose_list[trg_updn]['trig'][bs_]:
                                              dpg.configure_item(trg_each,label='') 
                                  
                                            for trg_each in self.dict_chose_list[trg_updn]['common'][bs_+2]:
                                               dpg.configure_item(trg_each,label='')
                                   
                                   dpg.configure_item(self.bid_trigger_tag,label='')
                              

                        return
                 
                    self._refresh_common(btn,price)
                    
                    
                    for trg_ in range(1,3):# 刷新 觸價單 個別欄位 
                                    if trg_==1:# bid 買進端
                                            trg_tag_id=btn-3
                                            trg_id=btn-4
                                    else:
                                            trg_tag_id=btn+3
                                            trg_id=btn+4
                                    if price in self.trigger_dict[trg_]:
                                        
                                        dpg.configure_item(trg_tag_id,label="D")
                                        total_amount,avg_entry_close_,_=self.trigger_dict[trg_][price]
                                        dpg.configure_item(trg_id,label=str(total_amount))

                                        
                                    else:
                                        dpg.configure_item(trg_id,label='')
                                        if price not in self.trigger_dict[trg_+2]:
                                           dpg.configure_item(trg_tag_id,label="")
                                        
                                    for pp in self.trigger_dict[trg_]:
                                       total_amount,avg_entry_close_,_=self.trigger_dict[trg_][pp]
                                       if trg_==1 :
                                            bidvol+=int(total_amount)
                                       else:
                                            askvol+=int(total_amount)
                    
                    if askvol:
                       dpg.configure_item(self.ask_trigger_tag,label='D')
                       dpg.configure_item(self.ask_trigger,label=str(askvol)+'('+str(len(self.trigger_dict[2]))+')')
                    if bidvol:
                       dpg.configure_item(self.bid_trigger_tag,label='D')
                       dpg.configure_item(self.bid_trigger,label=str(bidvol)+'('+str(len(self.trigger_dict[1]))+')')    
                    
                    
        def before_quote(self,mode=0,new_contract=0,trigger=0,common=0):# 在他還沒取得任何quote 報價的時候 先更新
                    if not self.quote or mode or trigger:
                        
                        if mode:
                            mode=self.offset+'tk'+str(mode)+'_window'
                        else:
                            mode=self.now_tick_mode
                        if 1:

                          
                          if not trigger and not common and not self.___checkbug:
                            _,self.snap_=self.api.snap(self.now_contract)
                            if str(self.snap_).isdigit():return

                            self.change_price=self.snap_.change_price
                            self.change_rate=self.snap_.change_rate
                            self._Update_spec_label(new_contract=new_contract)

                        if str(self.snap_).isdigit() and not trigger  and not common: return
                        if self.snap_ or trigger or common:
                            close=self.close
                            if self.snap_:
                                self.close=self.snap_.close
                                close=self.snap_.close# 暫時設定收盤價為 此價
                            contract=self.now_contract
                            allbtn=len(self.dict_chose_list[str(mode)]['button'])
                            row_=allbtn//self.col
                            row_index=0
                            if new_contract:
                                self.dict_tick_vol={}
                            #取 數字對齊
                             
                            price_print=[0]*row_
                            
                            if str(close)+'0' in self.dict_tick_vol:
                                close=str(close)+'0'
                            elif  str(close) in self.dict_tick_vol:
                                close=str(close)
                            len_=len(str(close))
                            _tick_diff=DataUse.tick_unit(float(close),contract)
                            if not self.___checkbug:
                                
                                dpg.configure_item(self.uplimit_float_input,step=_tick_diff,max_value=float(contract.limit_up)  -_tick_diff , default_value =float(contract.limit_up)-_tick_diff*5)
                                dpg.configure_item(self.dnlimit_float_input,step=_tick_diff,min_value=float(contract.limit_down)+_tick_diff , default_value =float(contract.limit_down)+_tick_diff*5)
                            if self.___checkbug:
                                print('recov')
                            price_print[row_//2]=close
                            Nprice=float(close)
                            # ticktype 都暫時設定為 2
                            ticktype=2
                            if ticktype==1:#代表剛剛在BID成交 那網上的價格顯示會重複出現一次價格
                                price_print[row_//2+1]=close
                            elif ticktype==2:#代表剛剛在ASK成交 那網上的價格顯示會重複出現一次價格
                                price_print[row_//2-1]=close
                            for idx01 in range(row_//2-1,-1,-1):
                                if price_print[idx01]:continue
                                tick_diff=DataUse.tick_unit(Nprice,contract)
                                tick_diff2=DataUse.tick_unit(Nprice+tick_diff,contract)
                                if tick_diff2==tick_diff:#兩邊確認無誤就算共識價
                                    Nprice+=tick_diff
                                elif tick_diff2!=tick_diff:
                                    Nprice+=tick_diff# 往上加的還是算原來的TICK DIFF
                                choseprice=value_align(round(Nprice,2),len_)
                                price_print[idx01]=choseprice
##                                price_print[idx01]=round(Nprice,2)
                            Nprice=float(close)
                            for idx01 in range(row_//2+1,row_):
                                if price_print[idx01]:continue
                                tick_diff=DataUse.tick_unit(Nprice,contract)
                                tick_diff2=DataUse.tick_unit(Nprice-tick_diff,contract)
                                if tick_diff2==tick_diff:#兩邊確認無誤就算共識價
                                    Nprice-=tick_diff
                                elif tick_diff2!=tick_diff:
                                    Nprice-=tick_diff2# 往下扣除的要用第二種DIFF 去扣

                                choseprice=value_align(round(Nprice,2),len_)
                                price_print[idx01]=choseprice
##                                price_print[idx01]=round(Nprice,2)
                        if not self.___checkbug:
                          Time=datetime.datetime.utcfromtimestamp(int(str(self.snap_.ts)[:10]))
                        if self.___checkbug:
                            print('recov')
                            Time=datetime.datetime.now()
                            print('delete')
                        dpg.configure_item(self.trade_tick_time,label=Time.strftime("%H:%M:%S"))
##                        dpg.set_value(self.trade_tick_time,'       '+Time.strftime("%H:%M:%S"))
 
                        if 1:
                        
                          for idx_btn,btn in enumerate(self.dict_chose_list[str(self.now_tick_mode)]['button']):
                            if not self.subscribe:
                                break
                            # 委買量
                            
                            if idx_btn%9==3 and row_index>row_//2 and not trigger and not common:
                                
        ##                        dpg.configure_item(btn,label=i['BidVolume'][row_index-(row_//2+1)])# 改變中間欄位數字
                                 
                                 if price_print[row_index] in self.dict_tick_vol:
                                      dpg.configure_item(btn,label=self.dict_tick_vol[price_print[row_index]])# 改變中間欄位數
                                 else:
                                      dpg.configure_item(btn,label='')
                            # 報價
                            if idx_btn%9==self.col//2:
                                # 中間填值
                                dpg.configure_item(btn,label=price_print[row_index])# 改變中間欄位數字
                                if row_index!=row_//2:self._refresh_trigger(btn,price_print[row_index],common=common)
                                        
                            # 委賣量
                            if idx_btn%9==5  and row_index<=row_//2-1  and not trigger  and not common:
                                      if price_print[row_index] in self.dict_tick_vol :
                                      dpg.configure_item(btn,label=self.dict_tick_vol[price_print[row_index]])# 改變中間欄位數字
                                else:
                                      dpg.configure_item(btn,label='')

                            if idx_btn%9==8:
                                row_index+=1

        def submit(self,s,app_data,user_data):

            if self.now_contract:
                if '刪' in str(user_data):
                    if 'dnlimit' in str(user_data) and( self.ask_trigger in str(user_data) or self.bid_trigger in str(user_data)):
                       
                       if  user_data[3]<user_data[1]:#刪除 bid 端
                            self.trigger_dict[1]={}
                            self.trigger_dict[3]={}
                       elif user_data[3]>user_data[1]:# 刪除ask端
                            self.trigger_dict[2]={}
                            self.trigger_dict[4]={}
                       self.before_quote(trigger=1)
                       
                       self._refresh_trigger(0,0,dn_refresh=1)
                       
                       return
                    
                    myid=user_data[3]
                    bs=user_data[2]
                    index_close=int(user_data[1])
                    close=dpg.get_item_label(index_close)
                   
                 
                    if 'limit_float_input' in  str(dpg.get_item_label(index_close)):
                                close=str(round(dpg.get_value(index_close),2))
                    
                    if user_data[3]<user_data[1]:#代表他是偏向買方的欄位 / 觸價部分
                                        trigger_id=user_data[3]-1
                                        trigger_id2=user_data[3]+1
                    else:
                                        trigger_id=user_data[3]+1
                                        trigger_id2=user_data[3]-1
                                        
                    if close in self.trigger_dict[bs]:
                                  del self.trigger_dict[bs][close]
                                  
                    if close in self.trigger_dict[bs+2]:
                                  
                                  del self.trigger_dict[bs+2][close]

                    dpg.configure_item(myid,label="")
                    dpg.configure_item(trigger_id,label="")
                    dpg.configure_item(trigger_id2,label="")
                    self._refresh_trigger(0,0,dn_refresh=1)
            
                    
                
            self.click_list.append(user_data[3])
            # 判斷要連續兩次點擊 才會出現後續動作
            if len(self.click_list)>=2:
             if self.click_list[-1]==self.click_list[-2]:
                
                self.click_list.clear()
                
                
                if self.now_contract:
                    
                    value_= int(user_data[0])%9
                    
                    if re.findall('[0268]',str(value_)):
                            bs=user_data[2]
                            
                            index_close=int(user_data[1])
                            close=dpg.get_item_label(index_close)# 中間的價格 而非現在成交價

                            if 'limit_float_input' in  str(close):
                                close=str(round(dpg.get_value(index_close),2))
                                print(dpg.get_item_label(index_close))
                            
                             
                            if not close or ':' in str(close):return
                         
                            if  '觸價' in str(user_data[4]):
                                if self.close==float(close) or abs(self.close-float(close))<=0.0000001:
                                    self.warn_info("錯誤",'成交價無法設定觸價單',self.on_selection_warn)
                                    return 
                                exist_amount=0
                                amount=dpg.get_value(self.trade_unit_amount)
                                if close in self.trigger_dict[bs]:
                                     exist_amount,entry_close,_=self.trigger_dict[bs][close]
                                     self.trigger_dict[bs][close]=exist_amount+amount,entry_close,''
                                else:
                                     self.trigger_dict[bs][close]=int(amount),self.close,''
                                if user_data[3]<user_data[1]:#代表他是偏向買方的欄位
                                    trigger_tag_id=user_data[3]+1
                                else:
                                    trigger_tag_id=user_data[3]-1
                                total_amount=amount+exist_amount
                                dpg.configure_item(trigger_tag_id,label="D")
                                dpg.configure_item(user_data[3],label=str(total_amount))
                                
                                self._refresh_trigger(0,0,dn_refresh=1)

                            elif self.submit_before_ask :
                                self.show_info('下單確認','是否確定送出此筆委託單 ?',self.on_selection,BS_LIST[int(user_data[2])],close,user_data=user_data, common=1)

                            

        
    

        
        def _change_col_ofchg(self,changeprice,_spec_id,title):
            try:
                    uplow=0
                    uptheme=[up_print_uptable,up_print_midtable]
                    dntheme=[down_print_uptable,down_print_midtable]
                    updn=0
                    if '成交' in str(title):
                        updn=1
                    if float(changeprice)>0:
                        uplow=1
                        dpg.set_item_theme(_spec_id,uptheme[updn])
                        
                            
                    elif  float(changeprice)<0:
                        uplow=2
                        dpg.set_item_theme(_spec_id,dntheme[updn])
                    else:
                        uplow=0
                        dpg.set_item_theme(_spec_id,no_change_print)
                    changeprice=round(changeprice,2)
                    dpg.configure_item(_spec_id,label=title+' '+self.uplow_sign[0]+ str(changeprice))
##                   self.uplow_sign=['','▲','▽']
##                    dpg.configure_item(_spec_id,label=title+' '+self.uplow_sign[uplow]+ str(changeprice))
            except:pass
        def _Update_spec_label(self,quote='',new_contract=0):
           if self.api:
            if not quote and quote!=0:
                quote=self.quote
            O,H,L,A=0,0,0,0
            if isinstance(quote,self.api.sj.backend.solace.tick.TickSTKv1) or isinstance(quote,self.api.sj.backend.solace.tick.TickFOPv1):
                O=round(quote.open,1)
                H=round(quote.high,1)
                L=round(quote.low,1)
                A=round(quote.avg_price,1)
            if self.api and self.dict_chose_list:
             for j,cnt in enumerate(self.dict_chose_list[str(self.now_tick_mode)]['spec']):# 特標籤 /0~11
                _spec_id=cnt
                if quote==0 and j>=8:break
                if not self.now_contract and j>=5:break
                if j==0:
                    dpg.configure_item(_spec_id,label='加權 '+ str(self.index_close))
                elif j==1:
                   
                    self._change_col_ofchg(self.index_change_price,_spec_id,' ')
##                    dpg.configure_item(_spec_id,label=str(round(self.index_change_price,2)))
                elif j==2:
                    dpg.configure_item(_spec_id,label='期指 '+ str(self.txf_close))
                elif j==3:
                    self._change_col_ofchg(self.txf_change_price,_spec_id,' ')
##                    dpg.configure_item(_spec_id,label=str(round(self.txf_change_price,2)))
                    
                elif j==4:
                    uplow=0
                    diffprice=self.txf_close-self.index_close

                    self._change_col_ofchg(diffprice,_spec_id,'價差 ')
##                    dpg.configure_item(_spec_id,label='價差 '+str(round(diffprice,2)))
                elif j==5:
                    
                    if  self.change_price:changeprice=round(self.change_price,2)
                    elif self.close and self.last_close:
                        changeprice=str(round(self.close-self.last_close,2))
                    else:
                        changeprice=round(self.snap_.change_price,2)
                    
##                   self.uplow_sign=['','▲','▽']
##                    dpg.configure_item(_spec_id,label='成交價 '+self.uplow_sign[uplow]+ str(changeprice))
                    self._change_col_ofchg(changeprice,_spec_id,'成交價 ')
                    
                    
                elif j==6:
                    dpg.configure_item(_spec_id,label='')
                elif j==7:
                    dpg.configure_item(_spec_id,label='')
                
                elif j==8:
                      if not O: 
                           if 'Open' in quote: O=str(quote.get('Open'))
                           else:
                               O=self.snap_.open
                      dpg.configure_item(_spec_id,label='開 '+str(O))
                elif j==9:
                    if not H:
                      if 'High' in quote: H=str(quote.get('High')[0])
                      else:
                           H=self.snap_.high
                    dpg.configure_item(_spec_id,label='高 '+str(H))
                elif j==10:
                    if not L:
                      if 'Low' in quote: L=str((quote.get('Low')[0]))
                      else:
                           L=self.snap_.low
                    dpg.configure_item(_spec_id,label='低 '+str(L))
                elif j==11:
                    if not A: 
                      if 'AvgPrice' in quote:A=str(round(quote.get('AvgPrice')[0],1))
                      else:
                           A=round(self.snap_.average_price,1)
                    dpg.configure_item(_spec_id,label='平 '+str(A))
        def change_option(self,contract):
            ticks_now_subscribe=self.api.api.ticks(contract,date=self.Tse_day[0].strftime("%Y-%m-%d"),last_cnt=1,query_type=self.api.sj.constant.TicksQueryType.LastCount)
            self.last_close=float(ticks_now_subscribe['close'][0])
            dpg.configure_item(self.uplimit_price,label=contract.limit_up)
            dpg.configure_item(self.dnlimit_price,label=contract.limit_down)
        
            dpg.configure_item(self.cond_day_trade,items=self.order_cond_stock,default_value =self.order_cond_stock[0],show=True)
            
            gp0_list=['gp0000','gp0001','gp0002','gp0003','gp0004']# 不可現股當沖/ 可當沖(禁止先賣) / 可現股當沖 / 期貨沖銷平倉自動 / 上櫃股
           
            dpg.configure_item(self.trade_unit_amount,label='單位')
            if 'OES' in str(contract.exchange):
                dpg.configure_item(self.cond_day_trade,show=False)
                for i in gp0_list:
                    dpg.configure_item(self.gp0_dict[i],show=False)
                dpg.configure_item(self.gp0_dict['gp0004'],show=True)
                dpg.configure_item(self.trade_unit_amount,label='數量')
                self.gp0_show=self.gp0_dict['gp0004']
            elif isinstance(contract,self.api.sj.contracts.Future):
                dpg.configure_item(self.cond_day_trade,items=self.order_day_trade,default_value=self.order_day_trade[0],show=True)
                
                for i in gp0_list:
                    dpg.configure_item(self.gp0_dict[i],show=False)
                dpg.configure_item(self.gp0_dict['gp0003'],show=True)
                dpg.configure_item(self.trade_unit_amount,label='口數')
                self.gp0_show=self.gp0_dict['gp0003']
            elif 'OnlyBuy' in str(contract.day_trade):
                for i in gp0_list:
                    dpg.configure_item(self.gp0_dict[i],show=False)
                dpg.configure_item(self.gp0_dict['gp0001'],show=True)
                self.gp0_show=self.gp0_dict['gp0001']
            elif 'No' in str(contract.day_trade):
                for i in gp0_list:
                    dpg.configure_item(self.gp0_dict[i],show=False)
                dpg.configure_item(self.gp0_dict['gp0000'],show=True)
                self.gp0_show=self.gp0_dict['gp0000']
            elif 'Yes' in str(contract.day_trade):
                for i in gp0_list:
                    dpg.configure_item(self.gp0_dict[i],show=False)
                dpg.configure_item(self.gp0_dict['gp0002'],show=True)
                self.gp0_show=self.gp0_dict['gp0002']
                
        def getcode(self,s,app_data):
         
            if self.now_contract:

                    dpg.configure_item(self.SN,label="Shioaji Neutron ")
                    self.api_cls2.unsubscribe(self.now_contract)

                    self.trigger_dict={1:{},2:{},3:{},4:{}}
                    self.snap_=''
                    self.code_name=''
                    self.change_price=0
                    self.quote=''
                    self.close=''
                    self.now_contract=''
                    self.now_code=''
'
            
            
                
            if len(str(app_data))>=4 and self.api:
                
                
                  contract=self.api.GetContractFromCode(app_data)
                  if contract:
                    self.now_contract=contract
                    self.now_code=contract.code
                    self.before_quote(new_contract=1)
                    self.change_option(contract)
                    self._Update_spec_label()
                    
                  
                    self.api_cls2.subscribe(contract)

                    
                    name=contract.name
                    for idx in range(0,len(self.account_list)):
                            if self.account['future'][2] in self.account_list[idx]:
                                break
                    dpg.configure_item(self.account_chose_id,default_value=self.account_list[idx])
                    if isinstance(contract,self.api.sj.contracts.Future):# 期貨
                        if contract.delivery_month.isdigit():
                            name=contract.name+' '+contract.delivery_month[-2:]
                        else:
                            name=contract.name+' '+contract.delivery_month
                        
                    elif isinstance(contract,self.api.sj.contracts.Option):
                        extra_name=''
                        find_w=re.findall('[0-9]',contract.code[:3])
                        if find_w:#代表周選
                            extra_name='W'+find_w[0]
                        symbol=contract.symbol[-7:]
                        if contract.symbol[-7:-6]=='0':
                            symbol= contract.symbol[-6:]
                        name=contract.name[:3]+extra_name+' '+contract.delivery_month[-2:]+' '+symbol
                    else:
                        for idx in range(0,len(self.account_list)):
                            if self.account['stock'][2] in self.account_list[idx]:
                                break
                    dpg.configure_item(self.account_chose_id,default_value=self.account_list[idx])
                    self.code_name=name
                    dpg.configure_item(self.SN,label="*Shioaji Neutron "+name)
                    dpg.set_value(self.code_name_id,name)
                

        def align_center_yscroll(self,sender):
             
             _id=self.offset+'tk'+str(self.now_tick_mode)+'_window'

            
             dpg.set_y_scroll(_id,dpg.get_y_scroll_max(_id)//2)
        def set_align_center_yscroll(self,_id=''):# for change tick type use
              
              if _id:
                  time.sleep(0.05)
                  dpg.set_y_scroll(_id,dpg.get_y_scroll_max(_id)//2)
                  return
              
              _id=self.offset+'tk'+str(self.now_tick_mode)+'_window'
              
              dpg.set_y_scroll(_id,dpg.get_y_scroll_max(_id)//2)
             
        def set_code_input(self,sender,app_data):
           
            dpg.set_value(self.code_text,app_data)
        def Main(self):
          with dpg.window(label="Shioaji Neutron",width=695,height=650) as self.SN:
            dpg.add_key_down_handler(callback=self._keyboard)

            dpg.add_mouse_click_handler(callback=self.add_mouse_click_handler)
            dpg.add_mouse_drag_handler(callback=self.add_mouse_drag_handler)
            dpg.add_mouse_wheel_handler(callback=self.add_mouse_wheel_handler)
            dpg.add_mouse_move_handler(callback=self.add_mouse_move_handler)
            dpg.add_text("帳號")
            dpg.add_same_line()
            
            dpg.add_combo(id=self.account_chose_id,items=self.account_list,default_value=self.account_list[0],width=150)
            dpg.add_same_line(spacing=430,xoffset =70)
            dpg.add_button(label="更新")
            dpg.add_same_line()
            dpg.add_button(label="設定")
            dpg.add_same_line()
            dpg.add_button(label="庫存")
 
            dpg.add_text("商品")
            dpg.add_same_line()
            dpg.add_combo(id=self.code_combo,items=['hi',1234,2555,3558,5554,5,6],height_mode  =0,pos =[139,57],callback=self.set_code_input,width=30,no_preview =True)
            dpg.add_input_text(hint ='Code' ,id=self.code_text,width=100,callback=self.getcode)
            dpg.add_same_line(spacing=100,xoffset =70)
            dpg.add_input_text(hint='Code name',readonly  =True,width=150,id=self.code_name_id)
            self.order_type=['ROD',"IOC","FOK"]
            self.order_cond_stock=['現股','融資','融券']
            self.order_day_trade=['不當沖','當沖']
            self.FuturesOCType=['自動','新倉','平倉']
            self.ODD=['整股','零股']
            dpg.add_same_line()
            
            
            dpg.add_combo(items=self.order_type,width=80,default_value =self.order_type[0],id=self.ORDER_TYPE)
            dpg.add_same_line()
            dpg.add_combo(items=self.order_cond_stock,width=80,default_value =self.order_cond_stock[0],id=self.cond_day_trade)
            dpg.add_same_line()
            
            with dpg.group():
             self.gp0_list=[]
             gp0_list=['gp0000','gp0001','gp0002','gp0003','gp0004']
             self.gp0_dict={}
             for _gp in gp0_list:
                 self.gp0_list.append((self.offset+_gp))
                 self.gp0_dict[_gp]=self.offset+_gp
             dpg.add_text('不可現股當沖',id=self.offset+'gp0000',show=False)
             dpg.add_same_line()
             dpg.add_checkbox(label='現股當沖(暫停先賣後買)',id=self.offset+'gp0001',show=False)
             dpg.add_same_line()
             dpg.add_checkbox(label='現沖賣',id=self.offset+'gp0002')
             dpg.add_same_line()
             dpg.add_combo(id=self.offset+'gp0003',items=self.FuturesOCType,width=80,default_value =self.FuturesOCType[0],show=False)
             dpg.add_same_line()
             dpg.add_radio_button(id=self.offset+'gp0004',items=self.ODD,default_value =self.ODD[0],show=False,horizontal=True)
             self.gp0_show=self.offset+'gp0004'
           

           
            dpg.add_radio_button(label='',id=self.tick_change,items=self.chose_list,callback=self.TickChange,default_value=0,horizontal=True)
            dpg.add_same_line(spacing =20)
            dpg.add_input_text(hint="   TICK TIME",id=self.tick_time,readonly =True,width=100)
            dpg.add_same_line(spacing =9)
            dpg.add_input_int(label='單位',width=120,id=self.trade_unit_amount,default_value=1)
            dpg.add_same_line(spacing =100)
            dpg.add_button(label='置中',width=40,id=self.align_center,callback=self.align_center_yscroll)
            dpg.set_item_theme(self.tick_time,tick_time_theme)
            dpg.set_item_theme(self.tick_change,Frame_rounding)
            
            with dpg.table(show=True,width=690) as TABLETITLE:

                   dpg.add_table_column(width_stretch=False,label="   觸價",init_width_or_weight =0.8)
                   dpg.add_table_column(width_stretch=False,label="  刪",init_width_or_weight =0.5)
                   dpg.add_table_column(width_stretch=False,label="   買進",init_width_or_weight =0.8)
                   dpg.add_table_column(width_stretch=False,label="       買未成交",init_width_or_weight =1.6)
                   dpg.add_table_column(width_stretch=False,label="            報價",init_width_or_weight =1.6)
                   
                   dpg.add_table_column(width_stretch=False,label="       賣未成交",init_width_or_weight =1.6)
                   dpg.add_table_column(width_stretch=False,label="   賣出",init_width_or_weight =0.8)
                   dpg.add_table_column(width_stretch=False,label="  刪",init_width_or_weight =0.5)
                   dpg.add_table_column(width_stretch=False,label="   觸價",init_width_or_weight =0.8)

                   self.now_tick_mode='五檔'
   
class API_INFO:
    def subscribe(self,contract):
        if contract.code in self.now_subscribe:return
        self.now_subscribe.append(contract.code)
        for alw in self.always_sub:
            if contract.code==alw:
                self.api.api.quote.subscribe(contract, quote_type='bidask')
                return
        self.api.api.quote.subscribe(contract, quote_type='tick',version = self.api.sj.constant.QuoteVersion.v1)   
        self.api.api.quote.subscribe(contract, quote_type='bidask')
    def unsubscribe(self,contract):
        dup=0
        for v1 in self.style_v1_list:
            if v1.now_code==contract.code:
                dup+=1
        if dup>1:return 
        if contract.code==self.TXFContract.code:
                        
                        self.api.api.quote.unsubscribe(contract, quote_type='bidask')
                        self.now_subscribe.remove(contract.code)
        else:
                        self.api.api.quote.unsubscribe(contract, quote_type='bidask')
                        self.api.api.quote.unsubscribe(contract, quote_type='tick')
                        self.now_subscribe.remove(contract.code)
    def __init__(self,api):
        self.api=api
        self.hover_child_id_time=0,0,0# 一次指控置一個滾輪或滑鼠的上下滾動
        self.item_dict={}# 存放個別物件的 item
        self.style_v1_list=[]# 已經登錄的STYLE 01
        self.now_subscribe=[]# 已經SUBSCRIBE的商品
        if api:
                
                self.account={}
                for acc in self.api.api.list_accounts():
                    if 'stock' in str(acc.account_type).lower():
                        combine='Stock-'+str(acc.account_id)
                        self.account['stock']=acc,acc.account_id,combine
                    elif 'future' in str(acc.account_type).lower():
                        combine='Future-'+str(acc.account_id)
                        self.account['future']=acc,acc.account_id,combine
                self.api.api.quote.set_quote_callback(self.quote_bid_ask)
                self.api.api.quote.set_on_tick_stk_v1_callback(self.quote_v1)
                self.api.api.quote.set_on_tick_fop_v1_callback(self.quote_v1)
                
                self.index_001=self.api.api.Contracts.Indexs.TSE.TSE001
                self.Tse_day=self.api.get_tse_tradeday(lastday=5)# 得到前5天有交易的日期
                tick=self.api.api.ticks(self.index_001,date=datetime.datetime.now().strftime("%Y-%m-%d"),last_cnt=1,query_type=self.api.sj.constant.TicksQueryType.LastCount)
                
                self.api.api.quote.subscribe(self.index_001, quote_type='tick')

                _,self.index001_snap=self.api.snap(self.index_001)
                ticks_indexs=self.api.api.ticks(self.index_001,date=self.Tse_day[0].strftime("%Y-%m-%d"),last_cnt=1,query_type=self.api.sj.constant.TicksQueryType.LastCount)
                if tick['ts']:
                    self.Tse_day.insert(0,datetime.datetime.now())
                    ticks_indexs=tick
                self.index_close=ticks_indexs['close'][0]
                self.index_change_price=self.index001_snap.change_price
                self.index_change_rate=self.index001_snap.change_rate
                self.index_last_close=ticks_indexs['close'][0]# 昨日 加權指數收盤價
                
                self.TXFContract=self.api.GetContractFromCode(self.api.Get_Nearmonth_TXF())
                _,self.txf_snap=self.api.snap(self.TXFContract)
                self.txf_change_price=self.txf_snap.change_price
                self.txf_change_rate=self.txf_snap.change_rate

                self.api.api.quote.subscribe(self.TXFContract, quote_type='tick',version = self.api.sj.constant.QuoteVersion.v1) 
                ticks_txf=self.api.api.ticks(self.TXFContract,date=self.Tse_day[0].strftime("%Y-%m-%d"),last_cnt=1,query_type=self.api.sj.constant.TicksQueryType.LastCount)
                self.txf_close=ticks_txf['close'][0]
                self.txf_last_close=ticks_txf['close'][0]# 昨日 台指期貨收盤價

                self.always_sub=[self.TXFContract.code,self.index_001.code]
    def quote_v1(self,exchange, tick):
        code=tick.code
        if self.TXFContract.code==str(code):
                            self.txf_close=float(tick.close)
                            self.txf_change_price=tick.price_chg
                            self.txf_change_rate=tick.pct_chg 
                            for v1 in self.style_v1_list:
                                v1.txf_close=self.txf_close
                                v1.txf_change_price= self.txf_change_price
                                v1.txf_change_rate=self.txf_change_rate
                                
                            for v1 in self.style_v1_list:
                                    if not v1.now_contract:
                                        threading.Thread(target=v1._Update_spec_label,kwargs={'quote':0}).start()
                                    
                                
                                    elif  v1.now_contract.code==self.TXFContract.code==code:
                                        v1.quote=tick
                                        v1.close=float(tick.close)
                                        v1.change_price=tick.price_chg
                                        v1.change_rate=tick.pct_chg 
                                    
                                        threading.Thread(target=v1._Update_spec_label,kwargs={'quote':tick}).start()
                                    

        elif self.index_001.code==str(code):
                            
                            self.index_close=float(tick.close)
                            self.index_change_price=tick.price_chg
                            self.index_change_rate=tick.pct_chg 

                            for v1 in self.style_v1_list:
                                    
                                    
                                        v1.index_close=self.index_close
                                        v1.index_change_price=self.index_change_price
                                        v1.index_change_rate=self.index_change_rate
                                        
                                        threading.Thread(target=v1._Update_spec_label,kwargs={'quote':0}).start()

        for _v1 in self.style_v1_list:
            if _v1.now_contract:

              if tick.code==_v1.now_contract.code:
                        _v1.quote=tick
                        
                        _v1.close=float(tick.close)

                        for bs_ in range(1,3):
                          for i in _v1.trigger_dict[bs_]:# 各種PRICE
                         
                              amonut,entry_close,_=_v1.trigger_dict[bs_][i]

                              if float(i)==_v1.close or abs(_v1.close-float(i))<=0.000001 or (float(entry_close)<=float(i) and float(i)<=_v1.close) or  (float(entry_close)>=float(i) and float(i)>=_v1.close):
                                  # 以 avg_entry_close 來判定是否穿過價格
                                  if _v1.submit_before_ask:
                                     
                                      _v1.show_info('下單確認(觸價單)','是否確定送出此筆委託單 ?',_v1.on_selection,BS_LIST[bs_],i,amount=amonut,trigger=1)
                        _v1.change_price=tick.price_chg
                        _v1.change_rate=tick.pct_chg
                        threading.Thread(target=_v1._Update_spec_label,kwargs={'quote':tick}).start()

                        
    def quote_bid_ask(self,topic,quote):
            
                    code=''
                    try:code=quote['Code']
                    except:
                         code=re.findall('\/(\d+)',str(topic))
                         if code:
                             code=str(code[0])
                    if      self.TXFContract.code==str(code) and 'Close' in quote:
                            self.txf_close=float(quote['Close'][0])
                            self.txf_change_price=float(quote['DiffPrice'][0])
                            self.txf_change_rate=float(quote['DiffRate'][0])
                            for v1 in self.style_v1_list:
                                v1.txf_close=self.txf_close
                                v1.txf_change_price= self.txf_change_price
                                v1.txf_change_rate=self.txf_change_rate

                            for v1 in self.style_v1_list:
                                    if not v1.now_contract:
                                        threading.Thread(target=v1._Update_spec_label,kwargs={'quote':0}).start()
                                    
                                
                                    elif  v1.now_contract.code==self.TXFContract.code==code:
                                        v1.quote=quote
                                        v1.close=float(quote['Close'][0])
                                        v1.change_price=float(quote['DiffPrice'][0])
                                        v1.change_rate=float(quote['DiffRate'][0])
                                    
##                                        self._Update_spec_label(quote=quote)
                                        threading.Thread(target=v1._Update_spec_label,kwargs={'quote':quote}).start()
                                    
                            return
                    elif    self.index_001.code==str(code) and 'Close' in quote:
                            
                            self.index_close=float(quote['Close'])
                            self.index_change_price=float(quote['DiffPrice'])
                            self.index_change_rate=float(quote['DiffRate'])

                            for v1 in self.style_v1_list:
                                    
                                    
                                        v1.index_close=self.index_close
                                        v1.index_change_price=self.index_change_price
                                        v1.index_change_rate=self.index_change_rate
                                        
                                        threading.Thread(target=v1._Update_spec_label,kwargs={'quote':0}).start()

                            return
                    
                    
                    for v1 in self.style_v1_list:
                            if v1.now_contract:
                                      
                                        if code==v1.now_contract.code:
                                    
                                            v1.now_quote=quote
                                          
                                            threading.Thread(target=self.refresh_bidask,args=(v1,quote,)).start()
                
                     
                    
    def refresh_bidask(self,_self,quote):

                        i=quote
                        allbtn=len(_self.dict_chose_list[str(_self.now_tick_mode)]['button'])
                        row_=allbtn//_self.col
                        row_index=0
                        _self.dict_tick_vol={}
                        contract=_self.now_contract
                        
                        #取 數字對齊
                        len_=0
                        for ch_ in i['AskPrice']:
                            if len(str(ch_))>len_:
                                len_=len(str(ch_))
                        for ch_2 in range(0,len(i['AskPrice'])):
                            if len(str(i['AskPrice'][ch_2]))<len_:
                                 i['AskPrice'][ch_2]=(str(i['AskPrice'][ch_2])+'0')
                            else:
                                i['AskPrice'][ch_2]=str(i['AskPrice'][ch_2])
                        for ch_2 in range(0,len(i['BidPrice'])):
                            if len(str(i['BidPrice'][ch_2]))<len_:
                                 i['BidPrice'][ch_2]=(str(i['BidPrice'][ch_2])+'0')
                            else:
                                i['BidPrice'][ch_2]=str(i['BidPrice'][ch_2])
                        if i['AskPrice'][0]==0:return
                        for _volidx,j in enumerate(i['AskPrice']):
                            _self.dict_tick_vol[j]=i['AskVolume'][_volidx]
                        for _volidx,j in enumerate(i['BidPrice']):
                            _self.dict_tick_vol[j]=i['BidVolume'][_volidx]
                        ask_sum=sum(i['AskVolume'])
                        bid_sum=sum(i['BidVolume'])
                       
                        dpg.configure_item(_self.ask_sum,label=ask_sum)
                        dpg.configure_item(_self.bid_sum,label=bid_sum)
                        close=i['AskPrice'][0]# 暫時設定收盤價為 此價
                        
                        if _self.close:
                                close=_self.close
                                if len(str(close))<len_:
                                    close=str(close)+'0'
                        if '五檔' in str(_self.now_tick_mode):
                            price_print=i['AskPrice'][::-1]+[close]+i['BidPrice']
                        
                        else:
                            price_print=[0]*row_
                            
                            price_print[row_//2]=str(close)
                            
                            
                            if abs(float(i['AskPrice'][0])-float(close))<abs(float(i['BidPrice'][0])-float(close)):
                                ticktype=2
                            else:
                                ticktype=1
                            if ticktype==1:#   代表剛剛在BID成交 向上的價格顯示會重複出現一次價格
                                price_print[row_//2+1]=str(close)
                            elif ticktype==2:# 代表剛剛在ASK成交 向下的價格顯示會重複出現一次價格
                                price_print[row_//2-1]=str(close)
                            Nprice=float(close)
                            for idx01 in range(row_//2-1,-1,-1):
                                if price_print[idx01]:continue
                                tick_diff=DataUse.tick_unit(Nprice,contract)
                                tick_diff2=DataUse.tick_unit(Nprice+tick_diff,contract)
                                if tick_diff2==tick_diff:#兩邊確認無誤就算共識價
                                    Nprice+=tick_diff
                                elif tick_diff2!=tick_diff:
                                    Nprice+=tick_diff# 往上加的還是算原來的TICK DIFF
                                choseprice=value_align(round(Nprice,2),len_)
                                price_print[idx01]=choseprice
##                                price_print[idx01]=round(Nprice,2)
                            Nprice=float(close)
                            for idx01 in range(row_//2+1,row_):
                                if price_print[idx01]:continue
                                tick_diff=DataUse.tick_unit(Nprice,contract)
                                tick_diff2=DataUse.tick_unit(Nprice-tick_diff,contract)
                                if tick_diff2==tick_diff:#兩邊確認無誤就算共識價
                                    Nprice-=tick_diff
                                elif tick_diff2!=tick_diff:
                                    Nprice-=tick_diff2# 往下扣除的要用第二種DIFF 去扣
                                choseprice=value_align(round(Nprice,2),len_)
                                price_print[idx01]=choseprice
##                                price_print[idx01]=round(Nprice,2)
                        dpg.configure_item(_self.trade_tick_time,label=i['Time'].split('.')[0])

       
                        if 1:
##                        try:
                          for idx_btn,btn in enumerate(_self.dict_chose_list[str(_self.now_tick_mode)]['button']):
                            if not _self.subscribe :
                              
                                return
                            
                            # 委買量
                            if idx_btn%9==3 and row_index>row_//2:
                                

                                     if price_print[row_index] in _self.dict_tick_vol:
                                          dpg.configure_item(btn,label=_self.dict_tick_vol[price_print[row_index]])# 改變中間欄位數
                                     else:
                                          dpg.configure_item(btn,label='')

                            # 報價
                            if idx_btn%9==_self.col//2:
                                # 中間填值

                                  dpg.configure_item(btn,label=price_print[row_index])# 改變中間欄位數字
                                  if row_index!=row_//2:_self._refresh_trigger(btn,price_print[row_index])

                            # 委賣量
                            if idx_btn%9==5  and row_index<=row_//2-1:
        
##                                try:
                                   if price_print[row_index] in _self.dict_tick_vol:
                                      dpg.configure_item(btn,label=_self.dict_tick_vol[price_print[row_index]])# 改變中間欄位數字
                                   else:
                                      dpg.configure_item(btn,label='')

                                  
                            if idx_btn%9==8:
                                row_index+=1


_myapi=API.API()
_myapi.Login_api(ACCOUNT,PASSWORD,ca_path=ca_path)
_api_info=API_INFO(_myapi)
def NEW_SN(s):
   Style_01(_myapi,_api_info) 
with dpg.window(label='MAIN'):
    dpg.add_button(label='New SN',callback=NEW_SN)
    
dpg.start_dearpygui()
