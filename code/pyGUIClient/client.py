import tkinter as tk
import login
import main

root = tk.Tk()
root.withdraw()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

table = {}
table[
    "admin"
] = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"  # username=admin, password=sha256(123456)

server_ip_list = ["127.0.0.1"]

login_window = login.Login(
    username_password_table=table,
    server_ip_list=server_ip_list,
    screen_width=screen_width,
    screen_height=screen_height,
)
state, user, server_ip = login_window.run()
if state == False:
    exit(1)

main_window = main.Main(
    user=user,
    server_ip=server_ip,
    screen_width=screen_width,
    screen_height=screen_height,
)
main_window.run()
