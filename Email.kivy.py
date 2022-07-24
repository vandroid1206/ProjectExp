from email.mime import text
import kivy
import os
import  json
from kivy import app
import datetime

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.lang import Builder
from kivymd.uix import label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, MDRectangleFlatButton , MDRectangleFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.expansionpanel import MDExpansionPanel , MDExpansionPanelTwoLine
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.icon_definitions import md_icons
from kivymd.uix.toolbar import MDToolbar

#email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


Dir = os.path.dirname(__file__)

class Email(MDApp):
    def build(self):
        global  filee , t , t2,signed_up,b,lab,button,Data,Data_file,Month
        Month = datetime.datetime.now().strftime("%B")
        b = MDScreen(md_bg_color=(211/255, 205/255, 205/255, 1.00/255))
        lab = label.MDLabel(text="Sign-Up" , pos_hint={"center_y":0.9},halign="center",theme_text_color="ContrastParentBackground")
        t = MDTextField(hint_text="Enter your email",pos_hint={"center_y":.8},widget_style="ios")
        t2 = MDTextField(hint_text="Enter your name" , pos_hint={"center_y":0.5},widget_style="android")
        button = MDRectangleFlatButton(text="Sign-Up" , theme_text_color="Custom",text_color=(1, 0, 0, 1),line_color=(0, 0, 1, 1),pos_hint={"center_y":0.2 , "center_x":0.5})
        if os.path.exists(os.path.join(Dir , "account.json")):
            if os.path.exists(os.path.join(Dir , "Data.json")):
                Data_file = open(os.path.join(Dir , "Data.json") , "r")
                Data = json.loads(Data_file.read())
            else:
                Data_file = open(os.path.join(Dir , "Data.json") , "w")
                Data = {}
                Data_file.write(json.dumps(Data))
                Data_file.close()
                Data_file = open(os.path.join(Dir , "Data.json") , "r")
            print("exists")
            bottomnav = MDBottomNavigation()
            currTool = MDToolbar(title="Current Month"+" - "+Month,type="top",pos_hint={"center_y":0.95})
            curr = MDBottomNavigationItem(name="CurrentMonth",text="Current Month",icon="square-edit-outline")
            New = MDFloatingActionButton(icon="pen-plus" , pos_hint={"center_x":.9,"center_y":.1})
            All = MDBottomNavigationItem(name="All months",text="All months",icon="calendar-month-outline")
            bottomnav.add_widget(curr)
            bottomnav.add_widget(All)
            li = MDList(pos_hint={"center_y":0.5})
            scroll = ScrollView(pos_hint={"center_y":0.43})
            try:
                for i in Data[Month]:
                    li.add_widget(MDExpansionPanel(content=MDRectangleFlatIconButton(text="Button" , icon="pencil",line_color=(0,0,0,0)),panel_cls=MDExpansionPanelTwoLine(text=str(i[0]),secondary_text="Price : " +str(i[1])+", Date : "+str(i[2]))))
            except:
                pass
            scroll.add_widget(li)
            curr.add_widget(currTool)
            curr.add_widget(scroll)
            curr.add_widget(New)
            b.add_widget(bottomnav)
            New.bind(on_press=self.AddNew)
        else :
            b.add_widget(lab)
            b.add_widget(t)
            b.add_widget(t2)
            b.add_widget(button)
            filee = open(os.path.join(Dir , "account.json") , "w")
            button.bind(on_press=self.p)
        return b
    def p(self , event):
        global account
        account = {"id" :t._get_text(),
                    "name" : t2._get_text()}
        filee.write(json.dumps(account))
        print(account)
        filee.close()
        Email.stop(self)
    def AddNew(self , event):
        global ItemName , Cost,dialogue
        box = MDBoxLayout(orientation="vertical" , spacing="12dp" , height="70dp" , size_hint_y=None)
        ItemName = MDTextField(mode="rectangle",hint_text="Item Name")
        Cost = MDTextField(mode="rectangle",hint_text="Item Cost")
        box.add_widget(ItemName)
        box.add_widget(Cost)
        Cancel = MDFlatButton(text="Cancel" , text_color=self.theme_cls.primary_color)
        OK = MDFlatButton(text="OK",text_color=self.theme_cls.primary_color)
        dialogue = MDDialog(type="custom",content_cls=box,buttons=[Cancel , OK])
        OK.bind(on_press=self.OKK)
        Cancel.bind(on_press=self.canc)
        dialogue.open()
    def OKK(self,event):
        Data[Month].append([ItemName._get_text() , Cost._get_text(),datetime.datetime.now().strftime("%d")])
        Data_file = open(os.path.join(Dir , "Data.json") , "w")
        Data_file.write(json.dumps(Data))
        Data_file.close()
        dialogue.dismiss()
        # self.email()
        Email.stop(self)
    def canc(self,event):
        dialogue.dismiss()
    # def email(self) :
    #     filee = open(os.path.join(Dir , "account.json") , "r")
    #     account = filee.read()
    #     account = json.loads(account)
    #     message = account["name"]+" purchased "+ItemName._get_text()+" : "+str(Cost._get_text())

    #     sender_address = "mailsusingpython@gmail.com"
    #     reciever = account["id"]

    #     msg = MIMEMultipart()
    #     msg["From"] = sender_address
    #     msg["To"] = reciever
    #     msg["Subject"] = " "

    #     msg.attach(MIMEText(message , "plain"))

    #     session = smtplib.SMTP("smtp.gmail.com" , 587)
    #     session.starttls()
    #     session.login(sender_address , password)
    #     text = msg.as_string()
    #     session.sendmail(sender_address , reciever , text)
    #     session.quit()
    #     print("sent")
# Run the App
if __name__ == "__main__":
    Email.run()
    
