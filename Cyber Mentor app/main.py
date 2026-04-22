import customtkinter as ctk
import json, os, sys, requests, webbrowser, io, gspread
from tkinter import messagebox
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import socket
import threading

import sys
import os

# --- SPLASH SCREEN BOSHQARUVI ---
try:
    import pyi_splash
    # Rasm ustida matn ko'rsatish
    pyi_splash.update_text("CyberMentor tizimi ishga tushmoqda...")
except ImportError:
    pass

# Qolgan barcha importlar shu yerda davom etadi...
import customtkinter as ctk
# ... (gspread, oauth2client va h.k.)

# --- RESURS YO'LI FUNKSIYASI (EXE uchun) ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- GLOBAL KONFIGURATSIYA ---
ADMIN_MASTER_PASS = "avazbek64123@"
SHEET_NAME = "CyberMentor_DB" 
JSON_KEYFILE = resource_path("creds.json") 
ICON_PATH = resource_path("app_icon.ico")

CREATOR_BOT_TOKEN = "8663565746:AAFJp3umdKLkbUa6e4shgzowpJlsrUI-DZs"
TEACHER_BOT_TOKEN = "8668588458:AAEU6oYk2dbymM5zkkYTn38Eque8Pc5g6BY"

CREATOR_CHAT_ID = "6433872696"
FRIEND_CHAT_ID = "5590284457"
TEACHER_CHAT_ID = "398496906"

# --- TIL LUG'ATI ---
LANG_DATA = {
    "uz": {
        "login_title": "🔒 TIZIMGA KIRISH",
        "name_ph": "Ism Sharif",
        "group_ph": "Guruh raqami",
        "btn_login": "KIRISH",
        "btn_admin": "🔐 ADMIN PANELGA KIRISH",
        "dash": "🏠 DASHBOARD",
        "start_test": "📝 TESTNI BOSHLASH",
        "support": "🎧 SUPPORT & ALOQA",
        "mode": "🌓 REJIMNI O'ZGARTIRISH",
        "lang_btn": "🇺🇿 UZ | EN 🇬🇧",
        "exit": "🚪 CHIQISH",
        "my_results": "Mening Natijalarim",
        "no_q": "Savollar yuklanmagan!",
        "q_text": "Savol",
        "finish_msg": "✅ TEST YAKUNLANDI",
        "result_label": "Natija",
        "wiki_btn": "📖 WIKIPEDIYADAN O'QISH",
        "back_dash": "DASHBOARDGA QAYTISH",
        "admin_title": "Admin Boshqaruv Paneli",
        "add_q": "➕ YANGI SAVOL QO'SHISH",
        "clear_dash": "🗑 DASHBOARDNI TOZALASH",
        "change_pw": "🔑 PAROLNI O'ZGARTIRISH",
        "save": "SAQLASH",
        "feedback_ph": "Xabar yozing (Taklif yoki muammo):",
        "send_creator": "📩 Yaratuvchiga yuborish",
        "send_teacher": "🎓 Ustozga yuborish",
        "btn_about": "ℹ️ DASTUR HAQIDA",
        "about_title": "CyberMentor — Tizim haqida",
        "about_content": (
            "🏛 Muassasa: Farg'ona davlat texnika universiteti\n"
            "👤 Muallif: 641-23 guruh talabasi Isoqjonov Avazbek\n\n"
            "CyberMentor — Axborot xavfsizligi va IT sohasidagi bilimlarni test orqali "
            "mustahkamlash uchun yaratilgan maxsus platformadir.\n\n"
            "🧠 Psixologik aspekt:\n"
            "Dastur foydalanuvchining temperamentini tahlil qiladi. "
            "Xolerik va Sangviniklar tezkor qaror qabul qilishda, Flegmatik va "
            "Melanxoliklar esa chuqur tahliliy vazifalarda ustunlik qilishadi.\n\n"
            "🎯 Maqsad: Ta'lim jarayonini avtomatlashtirish va shaffoflikni ta'minlash.\n"
            "📅 Versiya: 1.2.0 (2026)"
        )
    },
    "en": {
        "login_title": "🔒 SYSTEM LOGIN",
        "name_ph": "Full Name",
        "group_ph": "Group Number",
        "btn_login": "LOGIN",
        "btn_admin": "🔐 ADMIN PANEL LOGIN",
        "dash": "🏠 DASHBOARD",
        "start_test": "📝 START TEST",
        "support": "🎧 SUPPORT & FEEDBACK",
        "mode": "🌓 CHANGE MODE",
        "lang_btn": "🇬🇧 EN | UZ 🇺🇿",
        "exit": "🚪 EXIT",
        "my_results": "My Results",
        "no_q": "Questions not loaded!",
        "q_text": "Question",
        "finish_msg": "✅ TEST FINISHED",
        "result_label": "Result",
        "wiki_btn": "📖 READ ON WIKIPEDIA",
        "back_dash": "BACK TO DASHBOARD",
        "admin_title": "Admin Control Panel",
        "add_q": "➕ ADD NEW QUESTION",
        "clear_dash": "🗑 CLEAR DASHBOARD",
        "change_pw": "🔑 CHANGE PASSWORD",
        "save": "SAVE",
        "feedback_ph": "Write a message (Suggestion or issue):",
        "send_creator": "📩 Send to Creator",
        "send_teacher": "🎓 Send to Teacher",
        "btn_about": "ℹ️ ABOUT APP",
        "about_title": "CyberMentor — About System",
        "about_content": (
            "🏛 Institution: Fergana State Technical University\n"
            "👤 Author: Student of group 641-23, Isoqjonov Avazbek\n\n"
            "CyberMentor is a platform designed to strengthen knowledge in "
            "Information Security and IT through specialized testing.\n\n"
            "🧠 Psychological Aspect:\n"
            "The program analyzes the user's temperament. "
            "Cholerics and Sanguines excel in fast decision-making, while "
            "Phlegmatics and Melancholics perform better in deep analysis.\n\n"
            "🎯 Purpose: Automating education and ensuring transparency.\n"
            "📅 Version: 1.2.0 (2026)"
        )
    }
}

class CyberMentorUltimate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Neuro-Cyber Security Mentor")
        self.lang = "uz"
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.state("zoomed") 
        self.resizable(True, True) 
        
        try:
            if os.path.exists(ICON_PATH):
                self.iconbitmap(ICON_PATH)
                self.after(200, lambda: self.iconbitmap(ICON_PATH))
        except:
            pass

        self.current_mode = "dark"
        ctk.set_appearance_mode(self.current_mode)
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.last_function = self.show_login 
        self.user = None
        self.admin_active = False
        self.sheet = None

        if self.check_internet():
            self.connect_google_sheets()
            self.init_data()
            self.show_login()
        else:
            self.show_no_internet_error()

    def tr(self, key):
        return LANG_DATA[self.lang].get(key, key)

    def toggle_language(self):
        self.lang = "en" if self.lang == "uz" else "uz"
        if self.admin_active:
             self.show_admin_panel()
        elif self.user:
            self.show_user_dashboard()
        else:
            self.show_login()

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def run_with_check(self, func):
        if self.check_internet():
            self.last_function = func 
            func()
        else:
            self.show_no_internet_error()

    def show_no_internet_error(self):
        err_win = ctk.CTkToplevel(self)
        err_win.title("Error")
        err_win.geometry("400x250")
        err_win.attributes("-topmost", True)
        err_win.grab_set() 
        ctk.CTkLabel(err_win, text="🌐\nNo Internet!", font=("Segoe UI", 20, "bold"), text_color="#e74c3c").pack(pady=20)
        ctk.CTkLabel(err_win, text="Please check your connection.", font=("Segoe UI", 13)).pack(pady=5)
        
        def retry():
            if self.check_internet():
                if self.connect_google_sheets():
                    self.init_data()
                    err_win.destroy()
                    self.last_function() 
                else:
                    messagebox.showerror("Error", "Baza bilan bog'lanib bo'lmadi!")
            else:
                messagebox.showwarning("Error", "Still no internet!")
        
        ctk.CTkButton(err_win, text="Retry", command=retry, fg_color="#3498db").pack(pady=20)

    def toggle_mode(self):
        if self.current_mode == "dark":
            self.current_mode = "light"
            ctk.set_appearance_mode("light")
        else:
            self.current_mode = "dark"
            ctk.set_appearance_mode("dark")

    def connect_google_sheets(self):
        try:
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scope)
            client = gspread.authorize(creds)
            self.sheet = client.open(SHEET_NAME)
            self.ques_ws = self.sheet.worksheet("Лист1") 
            self.res_ws = self.sheet.worksheet("Лист2")  
            self.conf_ws = self.sheet.worksheet("Лист3") 
            self.global_res_ws = self.sheet.worksheet("Лист4")
            return True
        except Exception as e:
            return False

    def init_data(self):
        if not self.sheet: return
        try:
            # SAVOLLARNI YUKLASH (Лист1)
            records = self.ques_ws.get_all_records()
            self.questions = []
            for r in records:
                if r.get('Savol'):
                    self.questions.append({
                        "q": r['Savol'],
                        "o": [r['Var1'], r['Var2'], r['Var3'], r['Var4']],
                        "t": ["Xolerik", "Sangvinik", "Flegmatik", "Melanxolik"]
                    })
        except: self.questions = []
        
        try:
            # NATIJALARNI YUKLASH (Лист4) - MAJBURIY YANGILASH BILAN
            self.results = self.global_res_ws.get_all_records()
        except: self.results = []
        
        try: self.current_pass = str(self.conf_ws.acell('A1').value)
        except: self.current_pass = ADMIN_MASTER_PASS

    def save_to_db(self):
        try:
            header = ["Savol", "Var1", "Var2", "Var3", "Var4"]
            data_to_save = [header]
            for q in self.questions:
                data_to_save.append([q['q'], q['o'][0], q['o'][1], q['o'][2], q['o'][3]])
            self.ques_ws.clear()
            self.ques_ws.update('A1', data_to_save)
            self.conf_ws.update('A1', [[self.current_pass]])
            self.init_data()
        except Exception as e: print(f"Save error: {e}")

    def save_result_to_sheet(self, res):
        try: 
            row = [res['name'], res['group'], res['type'], res['date']]
            self.res_ws.append_row(row)
            self.global_res_ws.append_row(row) 
            self.init_data() # SAQLAGANDAN SO'NG DARHOL O'QISH
        except: pass

    def show_about_window(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title(self.tr("btn_about"))
        about_win.geometry("500x550")
        about_win.attributes("-topmost", True)
        
        f = ctk.CTkFrame(about_win, corner_radius=20)
        f.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(f, text=self.tr("about_title"), font=("Segoe UI", 22, "bold"), text_color="#3498db").pack(pady=20)
        ctk.CTkLabel(f, text=self.tr("about_content"), font=("Segoe UI", 14), justify="left", wraplength=420).pack(pady=10, padx=20)
        ctk.CTkButton(f, text="OK", command=about_win.destroy, width=120).pack(pady=20)

    def show_login(self):
        self.user = None
        self.admin_active = False
        for w in self.main_container.winfo_children(): w.destroy()
        
        ctk.CTkButton(self.main_container, text=self.tr("lang_btn"), command=self.toggle_language, width=120, fg_color="#16a085").place(relx=0.95, rely=0.05, anchor="ne")
        ctk.CTkButton(self.main_container, text=self.tr("btn_about"), command=self.show_about_window, width=120, fg_color="#34495e").place(relx=0.05, rely=0.05, anchor="nw")
        
        f = ctk.CTkFrame(self.main_container, width=400, height=580, corner_radius=30)
        f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text=self.tr("login_title"), font=("Segoe UI", 28, "bold")).pack(pady=35)
        self.e_name = ctk.CTkEntry(f, placeholder_text=self.tr("name_ph"), width=320, height=50, corner_radius=15)
        self.e_name.pack(pady=10)
        self.e_group = ctk.CTkEntry(f, placeholder_text=self.tr("group_ph"), width=320, height=50, corner_radius=15)
        self.e_group.pack(pady=10)
        ctk.CTkButton(f, text=self.tr("btn_login"), command=lambda: self.run_with_check(self.user_login), width=320, height=55, corner_radius=15, fg_color="#007AFF", font=("Segoe UI", 16, "bold")).pack(pady=20)
        ctk.CTkButton(f, text=self.tr("btn_admin"), command=lambda: self.run_with_check(self.admin_auth), fg_color="#34495e", hover_color="#2c3e50", width=320, height=45, corner_radius=12).pack(pady=10)

    def user_login(self):
        if self.e_name.get() and self.e_group.get():
            self.user = {"name": self.e_name.get(), "group": self.e_group.get()}
            self.admin_active = False
            self.init_data()
            self.show_user_dashboard()
        else: messagebox.showwarning("Xato", "To'ldiring!")

    def show_user_dashboard(self):
        self.init_data() # USER DASHBOARDGA KIRGANDA HAM YANGILASH
        for w in self.main_container.winfo_children(): w.destroy()
        sidebar = ctk.CTkFrame(self.main_container, width=280, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="👤", font=("Arial", 80)).pack(pady=(20, 10))
        ctk.CTkLabel(sidebar, text=self.user['name'], font=("Segoe UI", 18, "bold")).pack()
        
        ctk.CTkButton(sidebar, text=self.tr("dash"), command=lambda: self.run_with_check(self.show_user_dashboard), height=45).pack(pady=(40, 5), padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("start_test"), command=lambda: self.run_with_check(self.start_test), height=45, fg_color="#27ae60").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("support"), command=lambda: self.run_with_check(self.show_support), height=45, fg_color="#8e44ad").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("btn_about"), command=self.show_about_window, height=45, fg_color="#34495e").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("lang_btn"), command=self.toggle_language, height=45, fg_color="#16a085").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("mode"), command=self.toggle_mode, height=45, fg_color="#3d3d3d").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("exit"), command=lambda: messagebox.askyesno("Exit", "Confirm?") and self.show_login(), fg_color="#c0392b", height=45).pack(pady=5, padx=20, fill="x")

        self.content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=40, pady=40)
        ctk.CTkLabel(self.content, text=self.tr("my_results"), font=("Segoe UI", 28, "bold")).pack(anchor="w")
        res_frame = ctk.CTkScrollableFrame(self.content, height=500, corner_radius=20)
        res_frame.pack(fill="both", expand=True, pady=20)
        
        user_history = [r for r in self.results if str(r.get('name', '')) == self.user['name']]
        for r in reversed(user_history):
            f = ctk.CTkFrame(res_frame, corner_radius=10)
            f.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(f, text=f"📊 {r.get('type', 'Unknown')}").pack(side="left", padx=20, pady=10)
            ctk.CTkLabel(f, text=f"📅 {r.get('date', '')}", text_color="gray").pack(side="right", padx=20)

    def show_support(self):
        for w in self.content.winfo_children(): w.destroy()
        ctk.CTkLabel(self.content, text=self.tr("support"), font=("Segoe UI", 32, "bold")).pack(anchor="w")
        sup_frame = ctk.CTkFrame(self.content, corner_radius=25); sup_frame.pack(fill="both", expand=True, pady=20)
        ctk.CTkLabel(sup_frame, text=self.tr("feedback_ph"), font=("Segoe UI", 16)).pack(pady=(20, 5), padx=30, anchor="w")
        self.txt_feedback = ctk.CTkTextbox(sup_frame, height=180, corner_radius=15)
        self.txt_feedback.pack(fill="x", padx=30, pady=10)
        btn_container = ctk.CTkFrame(sup_frame, fg_color="transparent"); btn_container.pack(pady=10)
        ctk.CTkButton(btn_container, text=self.tr("send_creator"), command=lambda: self.run_with_check(lambda: self.send_feedback("Yaratuvchi")), fg_color="#27ae60", width=220).pack(side="left", padx=10)
        ctk.CTkButton(btn_container, text=self.tr("send_teacher"), command=lambda: self.run_with_check(lambda: self.send_feedback("Ustoz")), fg_color="#34495e", width=220).pack(side="left", padx=10)
        
        contact_box = ctk.CTkFrame(sup_frame, fg_color="transparent"); contact_box.pack(pady=20)
        ctk.CTkButton(contact_box, text="🔹 @isoqjonov05", command=lambda: webbrowser.open(f"https://t.me/isoqjonov05"), fg_color="#0088cc", width=250).pack(side="left", padx=10)
        ctk.CTkButton(contact_box, text="🔹 @Ataxanova_Z", command=lambda: webbrowser.open(f"https://t.me/Ataxanova_Z"), fg_color="#0088cc", width=250).pack(side="left", padx=10)

    def send_feedback(self, target):
        text = self.txt_feedback.get("1.0", "end-1c").strip()
        if not text: return
        report = f"KIMGA: {target}\nKIMDAN: {self.user['name']}\nGuruh: {self.user['group']}\nSana: {datetime.now()}\n\nMatn: {text}"
        try:
            file_obj = io.BytesIO(report.encode('utf-8')); file_obj.name = f"Feedback_{target}.txt"
            if target == "Yaratuvchi":
                requests.post(f"https://api.telegram.org/bot{CREATOR_BOT_TOKEN}/sendDocument", 
                              files={'document': file_obj}, data={'chat_id': CREATOR_CHAT_ID, 'caption': f"📩 Yaratuvchi uchun yangi xabar!"})
            else:
                requests.post(f"https://api.telegram.org/bot{TEACHER_BOT_TOKEN}/sendDocument", 
                              files={'document': file_obj}, data={'chat_id': TEACHER_CHAT_ID, 'caption': f"🎓 Ustoz uchun yangi xabar!"})
                file_obj.seek(0)
                requests.post(f"https://api.telegram.org/bot{TEACHER_BOT_TOKEN}/sendDocument", 
                              files={'document': file_obj}, data={'chat_id': FRIEND_CHAT_ID, 'caption': f"🎓 Ustoz uchun yangi xabar!"})
                file_obj.seek(0)
                requests.post(f"https://api.telegram.org/bot{CREATOR_BOT_TOKEN}/sendDocument", 
                              files={'document': file_obj}, data={'chat_id': CREATOR_CHAT_ID, 'caption': f"🎓 Ustozga yuborilgan xabar nusxasi"})
            messagebox.showinfo("Success", "Sent!"); self.txt_feedback.delete("1.0", "end")
        except: messagebox.showerror("Error", "Bot error!")

    def start_test(self):
        if not self.questions:
            messagebox.showwarning("Error", self.tr("no_q"))
            return
        self.q_idx = 0; self.scores = {"Xolerik": 0, "Sangvinik": 0, "Flegmatik": 0, "Melanxolik": 0}
        self.run_test()

    def run_test(self):
        for w in self.content.winfo_children(): w.destroy()
        if self.q_idx < len(self.questions):
            q = self.questions[self.q_idx]
            ctk.CTkLabel(self.content, text=f"{self.tr('q_text')} {self.q_idx+1}/{len(self.questions)}", font=("Arial", 14)).pack()
            ctk.CTkLabel(self.content, text=q["q"], font=("Segoe UI", 22, "bold"), wraplength=700).pack(pady=40)
            for i, opt in enumerate(q["o"]):
                ctk.CTkButton(self.content, text=opt, height=55, corner_radius=12, command=lambda t=q["t"][i]: self.run_with_check(lambda: self.ans(t))).pack(pady=6, fill="x")
        else: self.run_with_check(self.finish_test)

    def ans(self, t): self.scores[t] += 1; self.q_idx += 1; self.run_test()

    def finish_test(self):
        res_type = max(self.scores, key=self.scores.get)
        new_res = {"name": self.user['name'], "group": self.user['group'], "type": res_type, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
        self.save_result_to_sheet(new_res)
        msg = f"{self.tr('finish_msg')}\n👤: {self.user['name']}\n👥: {self.user['group']}\n📊 {self.tr('result_label')}: {res_type}"
        try:
            requests.get(f"https://api.telegram.org/bot{CREATOR_BOT_TOKEN}/sendMessage?chat_id={CREATOR_CHAT_ID}&text={msg}")
            requests.get(f"https://api.telegram.org/bot{TEACHER_BOT_TOKEN}/sendMessage?chat_id={TEACHER_CHAT_ID}&text={msg}")
            requests.get(f"https://api.telegram.org/bot{TEACHER_BOT_TOKEN}/sendMessage?chat_id={FRIEND_CHAT_ID}&text={msg}")
        except: pass
        self.show_detailed_result(res_type)

    def show_detailed_result(self, res_type):
        for w in self.content.winfo_children(): w.destroy()
        INFO_DATA = {
            "Xolerik": {
                "uz": [
                    "Siz o'ta faol, shijoatli va tezkor qaror qabul qiluvchi shaxssiz. Ichki quvvatingiz (energiyangiz) juda yuqori bo'lib, har qanday to'siqni shiddat bilan yengishga moyilsiz. Siz boshqalarni o'z ortingizdan ergashtira oladigan tabiiy yetakchisiz. Sizning xarakteringiz kutilmagan va o'ta krizisli vaziyatlarda soniyalar ichida to'g'ri reaksiya berishni talab qiladigan sohalar uchun yaratilgan. To'xtab qolish yoki bir joyda depsinish siz uchun emas, siz doimiy harakat va natija odamisiz.",
                    "I.P. Pavlov tahlili bo'yicha sizning nerv sistemangiz: Kuchli, muvozanatsiz va yuqori darajada harakatchan. Qo'zg'alish jarayonlari tormozlanishdan ancha ustun turadi, bu esa sizga chaqmoqdek tezkorlik beradi. Siz stressli holatlarda 'qotib' qolmasdan, darhol qarshi choralar ko'rasiz. Kuchli irodangiz va o'ziga bo'lgan ishonchingiz tufayli eng murakkab texnik muammolarni ham jasorat bilan hal qilasiz. Biroq, hissiyotlaringizni nazorat qilish professional o'sishingiz uchun juda muhim.",
                    "Kiber-xavfsizlikda siz uchun eng mos yo'nalishlar: Incident Response (Kiber-hujumlarga tezkor javob berish), Red Teaming (Tizimga hujum simulyatsiyasini o'tkazish) va Offensive Security (Pentesting). Krizis vaqtida tizimni real vaqt rejimida himoya qilish yoki dushman hujumini qaytarishda sizga teng keladigani topilmaydi. Shuningdek, Security Operations Center (SOC) ichida eng yuqori darajadagi tahdidlarni bartaraf etuvchi mutaxassis bo'lishingiz mumkin.",
                    "Mutaxassis maslahati: Professional mahoratingizni oshirish uchun sabr-toqatni mashq qiling. 'Ethical Hacking' yo'nalishidagi eng murakkab sertifikatlarni (OSCP, OSEP) olishga intiling. Ishni boshlashdan oldin strategik reja tuzishni o'rganing, bu sizning tezligingizni aniqlik bilan birlashtiradi. Jamoa bilan ishlashda boshqalarning fikriga ham quloq tutish sizni yanada kuchli yetakchiga aylantiradi. Doimiy o'zgaruvchan texnologiyalar olami sizning tabiatimgizga mos."
                ],
                "en": [
                    "You are a highly active, ambitious, and fast decision-maker. Your internal energy levels are immense, and you tend to overcome any obstacle with sheer force. You are a natural leader capable of motivating others. Your character is built for environments that require split-second reactions during unexpected crises. Stagnation is your enemy; you are a person of constant motion and results.",
                    "According to Pavlov's analysis: You have a strong, unbalanced, and highly mobile nervous system. Excitatory processes dominate inhibition, providing you with lightning-fast reaction times. In stressful situations, instead of freezing, you act immediately. Your strong will and self-confidence allow you to tackle the most complex technical challenges with courage. However, managing emotional outbursts is key to your professional growth.",
                    "Best Cybersecurity roles: Incident Response (Real-time attack mitigation), Red Teaming (Offensive simulation), and Penetration Testing. Your speed is invaluable when protecting systems during live breaches. You would excel as a Tier 3 analyst in a Security Operations Center (SOC), neutralizing advanced persistent threats (APTs) in real-time.",
                    "Expert Advice: To enhance your professional skills, practice patience and strategic planning. Aim for advanced certifications like OSCP or OSEP. Learn to draft a roadmap before diving into a task to combine your speed with precision. In team settings, listening to diverse perspectives will make you a more effective leader. The ever-evolving tech world is your perfect playground."
                ]
            },
            "Sangvinik": {
                "uz": [
                    "Siz o'ta kirishuvchan, optimistik va har qanday sharoitga tez moslashuvchan shaxssiz. Yangi bilimlarni hayratlanarli darajada tez o'zlashtirasiz va jamoada ishlashda haqiqiy master hisoblanasiz. Kayfiyatingiz barqaror va qiyinchiliklarga tabassum bilan qaraysiz. Atrofdagilar bilan tez til topishasiz, bu esa sizni har qanday korporativ muhitning eng qadrli a'zosiga aylantiradi. Sizning ijtimoiy zakovatingiz texnik bilimlaringiz bilan uyg'unlashsa, sizni to'xtatib bo'lmaydi.",
                    "Nerv sistemangiz: Kuchli, muvozanatli va harakatchan. Qo'zg'alish va tormozlanish jarayonlari bir-birini mukammal to'ldiradi. Bu xususiyat sizga o'ta murakkab texnik algoritmlardan ijtimoiy muloqotga yoki menejerlik vazifalariga soniyalar ichida o'tish imkonini beradi. Siz eng chidamli temperament egasiz va uzoq vaqt davomida yuqori ish samaradorligini pasaytirmay saqlab qola olasiz. Charchoqqa chidamlilik va tez tiklanish sizning asosiy qurolingizdir.",
                    "Siz uchun ideal rollar: Social Engineering (Ijtimoiy muhandislik), IT Audit, Kiber-xavfsizlik bo'yicha menejerlik va GRC (Governance, Risk, and Compliance). Odamlarni tushunish va tizim kamchiliklarini muloqot orqali topishda tengsizsiz. Kompaniya xavfsizlik siyosatini ishlab chiqish va uni xodimlarga tushuntirishda sizdan yaxshisi yo'q. Shuningdek, kiber-xavfsizlik bo'yicha xalqaro konferensiyalarda ma'ruzachi bo'lishingiz mumkin.",
                    "Mutaxassis maslahati: Diqqatingizni bitta maqsadga uzoq vaqt jamlashni mashq qiling, chunki qiziqishingiz tez o'zgarishi mumkin. Pomodoro yoki boshqa taym-menejment texnikalaridan foydalaning. Jamoaviy loyihalarda yetakchilikni qo'lga oling va networking orqali xalqaro IT hamjamiyatida o'z o'rningizni toping. Bir ishni oxiriga yetkazish intizomini shakllantirish — sizning muvaffaqiyat garovingizdir. CISSP yoki CISM kabi boshqaruv sertifikatlarini maqsad qiling."
                ],
                "en": [
                    "You are a highly sociable, optimistic, and adaptable individual. You absorb new information with incredible speed and are a master of teamwork. Your mood is stable, and you face obstacles with a positive attitude. Your ability to connect with people makes you an asset to any corporate environment. When your social intelligence is paired with technical expertise, you become unstoppable.",
                    "Nervous system: Strong, balanced, and mobile. Excitatory and inhibitory processes complement each other perfectly. This allows you to switch from complex coding or technical tasks to management or social meetings seamlessly. You possess the most resilient temperament, capable of maintaining peak productivity over long periods. Endurance and quick recovery are your secret weapons.",
                    "Ideal Cybersecurity roles: Social Engineering, IT Auditing, Security Management, and GRC (Governance, Risk, and Compliance). You are unparalleled at identifying human-factor vulnerabilities and negotiating security measures. You are perfect for developing security policies and training employees. Furthermore, you would excel as a public speaker at international cybersecurity conferences.",
                    "Expert Advice: Focus on staying disciplined with single-tasking, as your interests might shift rapidly. Utilize time-management tools like Pomodoro. Take charge of team-based projects and leverage networking to build a global career. Aim for management-level certifications like CISSP or CISM to formalize your leadership potential. Consistency is the bridge between your goals and accomplishments."
                ]
            },
            "Flegmatik": {
                "uz": [
                    "Siz bosiq, sabr-toqatli va o'ta tartibli insonsiz. Hissiyotlarga berilmaslik, har bir qadamni yetti o'lchab bir kesish sizning asosiy tamoyilingizdir. Ishni oxirigacha yetkazishda sizda bor matonat boshqa hech bir temperamentda yo'q. Sizning xotirjamligingiz eng dahshatli kiber-hujumlar vaqtida ham tahlilni to'g'ri olib borishga yordam beradi. Siz shovqin-suronni yoqtirmaysiz, yolg'iz ishlash va chuqur konsentratsiya talab qilinadigan vazifalarda haqiqiy dahosiz.",
                    "Nerv sistemangiz: Kuchli, muvozanatli, ammo sust (inert). Sizga yangilikka ko'nikish uchun biroz vaqt kerak, ammo bir marta o'rgangan narsangizni hech qachon unutmaysiz. Stress ostida sovuqqonlik bilan ishlash qobiliyati sizning eng ulkan ustunligingizdir. Nerv tizimingiz monoton, uzoq davom etadigan va o'ta murakkab algoritmlar ustida charchamay ishlashni ta'minlaydi. Sizda 'texnik sabr' bor, bu esa kiber-xavfsizlikda juda noyob xususiyatdir.",
                    "Kiber-yo'nalish: Cryptography (Kriptografiya), Malware Analysis (Zararli dasturlar tahlili), Digital Forensics (Raqamli ekspertiza) va Security Architecture. Detallarga e'tibor va minglab qatorli loglarni tahlil qilish siz uchun qiyinchilik tug'dirmaydi. Siz tizim arxitekturasini shunday loyihalashtirasizki, u har qanday tashqi bosimga chiday oladi. Siz kiber-olamന്റെ eng ishonchli 'qalqoni' bo'lishga qodirsiz.",
                    "Mutaxassis maslahati: Tezkor o'zgarishlarga tayyor turish uchun kiber-simulyatsiyalar (Blue Teaming) va real vaqtli musobaqalarda ko'proq qatnashing. Analitik qobiliyatingizni Python, C++ va past darajadagi (Assembly) dasturlash tillari bilan boyiting. Sizdan mukammal xavfsizlik arxitektori yoki kriptograf chiqishi shubhasiz. O'z bilimlaringizni doimiy yangilab turishni va eng so'nggi kiber-tahdid tendensiyalarini kuzatishni odat qiling. SANS GIAC yoki GCFA sertifikatlariga e'tibor bering."
                ],
                "en": [
                    "You are a calm, patient, and methodical individual. Not being swayed by emotions and thinking through every detail is your core principle. Your persistence in finishing tasks is unmatched. This composure allows you to maintain analytical accuracy even during the most severe cyber incidents. You thrive in quiet environments where deep concentration and technical solitude are required.",
                    "Nervous system: Strong, balanced, but inert. You require time to adapt to new environments, but once you master a concept, it remains with you forever. Your ability to stay cool-headed under extreme pressure is your greatest asset. Your nervous system is designed for high endurance in some tedious yet complex tasks. You possess 'technical patience,' a rare and valuable trait in the cybersecurity world.",
                    "Cybersecurity direction: Cryptography, Malware Analysis, Digital Forensics, and Security Architecture. Your attention to detail and ability to parse through thousands of logs make you a master investigator. You design security frameworks that are resilient to external pressure. You are the 'shield' of the cyber world, ensuring long-term system integrity.",
                    "Expert Advice: Participate more in Blue Team simulations to improve your reaction to rapid changes. Enhance your analytical stack with Python, C++, and Assembly languages. You have the potential to become a top-tier security architect or cryptographer. Always stay updated with the latest threat intelligence reports. Focus on high-end technical certifications like SANS GIAC or GCFA to solidify your expertise."
                ]
            },
            "Melanxolik": {
                "uz": [
                    "Siz o'ta sezgir, intuitiv va chuqur tahliliy fikrlaydigan shaxssiz. Boshqalar mutlaqo sezmaydigan mayda detallarni va yashirin xavflarni oldindan ko'ra olish qobiliyatiga egasiz. Tasavvur olamingiz boy va mas'uliyatni juda chuqur his qilasiz. Sizning ichki sezgingiz kiber-xavfsizlikda 'oltinchi tuyg'u' bo'lib xizmat qiladi. Siz juda ehtiyotkorsiz, bu esa tizimlarni eng xavfsiz holatda saqlashga yordam beradi. Har bir ehtimoliy zaiflikni chuqur tahlil qilmaguncha tinchimaysiz.",
                    "Nerv sistemangiz: Sezgir (nozik) va kuchsizroq tip. Bu sizning tez charchashingizni anglatishi mumkin, ammo shu bilan birga tashqi muhitdagi eng kichik tebranishlarga ham o'ta sezgirligingizni bildiradi. Siz kiber-tahdidlarni juda erta bosqichda (Early Detection) aniqlashga qodirsiz. Sizning nerv tizimingiz yuqori aniqlikdagi va o'ta nozik yondashuv talab qiladigan vazifalarga mukammal darajada mos keladi. Sizning 'tahliliy sezgirligingiz' — bu sizning ustunligingiz.",
                    "Siz uchun mos rollar: OSINT (Ochiq manbalar bilan ishlash), Threat Intelligence (Tahdidlarni o'rganish), Vulnerability Research va Bug Bounty. Siz koddagi yoki tizimdagi eng kichik '0-day' zaifliklarni topishda juda muvaffaqiyatli bo'lasiz. Tahliliy hisobotlar yozishda va zaif nuqtalarni hujjatlashtirishda sizga teng keladigan mutaxassis yo'q. Kiber-razvedka yo'nalishi siz uchun eng ma'qul va qiziqarli sohadir.",
                    "Mutaxassis maslahati: O'zingizga bo'lgan ishonchni oshirish uchun muntazam ravishda CTF musobaqalarida qatnashing. Ish va dam olish muvozanatini (work-life balance) qat'iy saqlang, chunki sizning nerv sistemangiz dam olishga muhtoj. Kiber-psixologiya va kiber-razvedka yo'nalishlarida o'zingizni sinab ko'ring. Sizning ehtiyotkorligingiz tizimlarni eng ishonchli himoya bilan ta'minlaydi. O'z mahoratingizni jamoaviy muhitda namoyon qilishdan aslo cho'chimang. CREST yoki OSINT bo'yicha maxsus kurslarni o'rganing."
                ],
                "en": [
                    "You are an extremely sensitive, intuitive, and deeply analytical individual. You have the ability to foresee hidden risks and minor details that others overlook. Your imagination is vivid, and you carry a deep sense of responsibility. Your intuition serves as a 'sixth sense' in cybersecurity. Your cautious nature ensures that systems are kept in their most secure state, as you analyze every possible vulnerability thoroughly.",
                    "Nervous system: Sensitive and delicate. While this might lead to quicker fatigue, it translates to acute sensitivity toward environmental fluctuations. You are capable of 'Early Detection' of cyber threats. Your nervous system is perfectly suited for high-precision tasks requiring a delicate and meticulous approach. Your 'analytical sensitivity' is your superpower in identifying anomalies.",
                    "Ideal Cybersecurity roles: OSINT (Open Source Intelligence), Threat Intelligence, Vulnerability Research, and Bug Bounty hunting. You excel at finding minor '0-day' vulnerabilities in code or system logic. Your reports and documentation are of the highest quality, leaving no stone unturned. Cyber-intelligence is your ideal field of expertise.",
                    "Expert Advice: To boost your confidence, participate regularly in CTF competitions. Strictly maintain a healthy work-life balance to avoid burnout due to your sensitive nervous system. Explore cyber-psychology and advanced intelligence gathering. Your caution provides the most reliable protection for critical infrastructure. Don't be afraid to showcase your findings in team settings. Look into CREST or specialized OSINT certifications."
                ]
            }
        }
        
        cur_info = INFO_DATA.get(res_type, INFO_DATA["Xolerik"])[self.lang]
        scroll = ctk.CTkScrollableFrame(self.content, corner_radius=20)
        scroll.pack(fill="both", expand=True)
        ctk.CTkLabel(scroll, text=f"TEMPERAMENT: {res_type}", font=("Segoe UI", 26, "bold"), text_color="#007AFF").pack(pady=20)
        titles = ["📝 Description", "🔬 Analysis", "💻 Cyber-Role", "💡 Expert Advice"] if self.lang == "en" else ["📝 Umumiy tavsif", "🔬 Ilmiy tahlil", "💻 Kiber-xavfsizlikda o'rningiz", "💡 Mutaxassis maslahati"]
        for i, text in enumerate(cur_info):
            box = ctk.CTkFrame(scroll, corner_radius=15)
            box.pack(fill="x", pady=10, padx=20)
            ctk.CTkLabel(box, text=titles[i], font=("Segoe UI", 18, "bold"), text_color="orange").pack(anchor="w", padx=15, pady=5)
            ctk.CTkLabel(box, text=text, font=("Segoe UI", 15), wraplength=800, justify="left").pack(anchor="w", padx=15, pady=10)
        
        ctk.CTkButton(self.content, text=self.tr("wiki_btn"), command=lambda: webbrowser.open(f"https://uz.wikipedia.org/wiki/{res_type}"), fg_color="#34495e", height=45).pack(pady=(20, 5))
        ctk.CTkButton(self.content, text=self.tr("back_dash"), command=lambda: self.run_with_check(self.show_user_dashboard), fg_color="#007AFF", height=45).pack(pady=(5, 20))

    def admin_auth(self):
        top = ctk.CTkToplevel(self); top.title("🔐 Admin Auth"); top.geometry("380x350"); top.attributes("-topmost", True)
        top.update_idletasks(); top.geometry(f"+{(top.winfo_screenwidth()//2)-190}+{(top.winfo_screenheight()//2)-175}")
        ctk.CTkLabel(top, text="Admin PIN:", font=("Segoe UI", 20, "bold")).pack(pady=25)
        pw_frame = ctk.CTkFrame(top, fg_color="transparent"); pw_frame.pack(pady=5)
        self.e_pass = ctk.CTkEntry(pw_frame, width=220, height=45, show="*", corner_radius=10)
        self.e_pass.pack(side="left", padx=5)
        def toggle_pw_visibility():
            if self.e_pass.cget("show") == "*":
                self.e_pass.configure(show="")
                btn_eye.configure(text="👁️")
            else:
                self.e_pass.configure(show="*")
                btn_eye.configure(text="🙈")
        btn_eye = ctk.CTkButton(pw_frame, text="🙈", width=40, height=45, command=toggle_pw_visibility, fg_color="#3d3d3d")
        btn_eye.pack(side="left")
        def check_pw():
            if self.e_pass.get() == ADMIN_MASTER_PASS or self.e_pass.get() == self.current_pass:
                top.destroy(); self.admin_active = True; self.user = None
                self.run_with_check(lambda: [self.init_data(), self.show_admin_panel()])
            else: messagebox.showerror("Error", "Wrong PIN!")
        ctk.CTkButton(top, text=self.tr("btn_login"), command=check_pw, fg_color="#007AFF", width=220, height=45, corner_radius=10).pack(pady=30)

    def show_admin_panel(self):
        self.init_data() # HAR SAFAR ADMIN PANELGA KIRGANDA YANGILASH
        
        for w in self.main_container.winfo_children(): w.destroy()
        sidebar = ctk.CTkFrame(self.main_container, width=280); sidebar.pack(side="left", fill="y")
        
        ctk.CTkButton(sidebar, text=self.tr("lang_btn"), command=self.toggle_language, height=35, fg_color="#16a085").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("dash"), command=lambda: self.run_with_check(self.show_admin_panel), height=35).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text="SAVOLLAR / QUESTIONS", command=lambda: self.run_with_check(self.admin_questions_ui), height=35).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("btn_about"), command=self.show_about_window, height=35, fg_color="#34495e").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("mode"), command=self.toggle_mode, height=35, fg_color="#3d3d3d").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("change_pw"), command=self.change_pass_ui, fg_color="#8e44ad", height=35).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("clear_dash"), command=lambda: self.run_with_check(self.clear_global_dashboard), fg_color="#e67e22", height=35).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text=self.tr("exit"), command=lambda: messagebox.askyesno("Exit", "Confirm exit?") and self.show_login(), fg_color="#c0392b", height=35).pack(pady=5, padx=20, fill="x")
        
        self.adm_content = ctk.CTkFrame(self.main_container, fg_color="transparent"); self.adm_content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        ctk.CTkLabel(self.adm_content, text=self.tr("admin_title"), font=("Segoe UI", 32, "bold")).pack(anchor="w")
        
        self.res_scroll = ctk.CTkScrollableFrame(self.adm_content, height=500, corner_radius=15)
        self.res_scroll.pack(fill="both", expand=True, pady=20)
        
        self.loading_lbl = ctk.CTkLabel(self.res_scroll, text="🔄 Ma'lumotlar yuklanmoqda...", font=("Segoe UI", 16))
        self.loading_lbl.pack(pady=50)

        threading.Thread(target=self.load_results_async, daemon=True).start()

    def load_results_async(self):
        try:
            # KESHLANISHNI OLDINI OLISH UCHUN MAJBURIY QAYTA YUKLASH
            self.results = self.global_res_ws.get_all_records()
            self.after(0, self.render_admin_results)
        except:
            self.after(0, lambda: self.loading_lbl.configure(text="⚠️ Xatolik: Baza bilan bog'lanish uzildi."))

    def render_admin_results(self):
        self.loading_lbl.destroy()
        # OLDINGI ELEMENTLARNI TOZALASH
        for w in self.res_scroll.winfo_children(): w.destroy()
        
        if not self.results:
            ctk.CTkLabel(self.res_scroll, text="Hozircha natijalar yo'q.").pack(pady=20)
            return

        # BARCHA NATIJALARNI CHIQARISH (CHEKLOV YO'Q)
        for r in reversed(self.results):
            row = ctk.CTkFrame(self.res_scroll)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=str(r.get('name','-')), width=250).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=str(r.get('group','-')), width=100).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=str(r.get('type','-')), width=150, text_color="#007AFF").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=str(r.get('date','-')), width=150).pack(side="left", padx=10)

    def change_pass_ui(self):
        new_p = ctk.CTkInputDialog(text="New Password:", title="Password").get_input()
        if new_p: 
            self.current_pass = new_p
            self.run_with_check(self.save_to_db)
            messagebox.showinfo("OK", "Updated!")

    def admin_questions_ui(self):
        self.init_data()
        for w in self.adm_content.winfo_children(): w.destroy()
        ctk.CTkButton(self.adm_content, text=self.tr("add_q"), command=self.add_q_popup, fg_color="#27ae60").pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self.adm_content); scroll.pack(fill="both", expand=True)
        for i, q in enumerate(self.questions):
            f = ctk.CTkFrame(scroll); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{i+1}. {q['q'][:60]}...").pack(side="left", padx=10)
            ctk.CTkButton(f, text="🗑", width=40, fg_color="#c0392b", command=lambda idx=i: self.run_with_check(lambda: [self.questions.pop(idx), self.save_to_db(), self.admin_questions_ui()])).pack(side="right", padx=5)

    def add_q_popup(self):
        top = ctk.CTkToplevel(self); top.title("New Q"); top.geometry("550x620"); top.attributes("-topmost", True)
        ctk.CTkLabel(top, text="QUESTION TEXT:", font=("Arial", 14, "bold")).pack(pady=10)
        e_q = ctk.CTkTextbox(top, height=80, width=450); e_q.pack(pady=5)
        entries = []
        for lab in ["Xolerik:", "Sangvinik:", "Flegmatik:", "Melanxolik:"]:
            ctk.CTkLabel(top, text=lab).pack(pady=2)
            en = ctk.CTkEntry(top, width=450); en.pack(pady=5); entries.append(en)
        def save_q():
            q_text = e_q.get("1.0", "end-1c").strip()
            opts = [en.get().strip() for en in entries]
            if q_text and all(opts):
                self.questions.append({"q": q_text, "o": opts, "t": ["Xolerik", "Sangvinik", "Flegmatik", "Melanxolik"]})
                self.run_with_check(lambda: [self.save_to_db(), top.destroy(), self.admin_questions_ui()])
        ctk.CTkButton(top, text=self.tr("save"), command=save_q, fg_color="#27ae60", height=45, width=200).pack(pady=20)

    def clear_global_dashboard(self):
        if messagebox.askyesno("Confirm", "Barcha natijalarni o'chirishni xohlaysizmi?"):
            try:
                header = ["name", "group", "type", "date"]
                self.res_ws.clear()
                self.res_ws.append_row(header)
                self.global_res_ws.clear()
                self.global_res_ws.append_row(header)
                self.results = []
                self.show_admin_panel()
                messagebox.showinfo("OK", "Dashboard tozalandi!")
            except Exception as e:
                messagebox.showerror("Error", f"Xatolik: {e}")

if __name__ == "__main__":
    
    app = CyberMentorUltimate()
    
    # Dastur interfeysi tayyor bo'lgach splashni yopish
    try:
        import pyi_splash
        pyi_splash.close()
    except ImportError:
        pass
        
    app.mainloop()
    app = CyberMentorUltimate()
    app.mainloop()