import tkinter as tk
from tkinter import ttk
import hashlib
from PIL import Image, ImageTk
from tkinter import messagebox


def calc_sha256(string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode())
    return sha256_hash.hexdigest()


class Login:
    def __init__(
        self,
        username_password_table,
        server_ip_list,
        screen_width,
        screen_height,
        window_width=800,
        window_height=550,
    ):
        self.username_password_table = username_password_table
        self.server_ip_list = server_ip_list
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_width = window_width
        self.window_height = window_height

    def run(self):
        def validate_login():
            # 获取输入框的值
            username = username_entry.get()
            password = calc_sha256(password_entry.get())
            server_ip = server_ip_entry.get()

            if (
                username not in self.username_password_table
                or self.username_password_table[username] != password
            ):
                messagebox.showinfo('错误提示', 'Invalid username or password!')
                #error_label.config(text="Invalid username or password!")
            elif server_ip not in self.server_ip_list:
                messagebox.showinfo('错误提示', 'Invalid server IP!')
                #error_label.config(text="Invalid server IP!")
            else:
                # 修改状态、用户名和IP
                state_user_ip[0] = True
                state_user_ip[1] = username
                state_user_ip[2] = server_ip
                window.unbind("<Configure>")
                window.destroy()

        state_user_ip = [False, None, None]
        '''
        # 创建一个Style实例
        style = ttk.Style()

        # 设置框架的背景颜色为浅灰色
        style.configure("Custom.TFrame", background="light gray")
        '''
        # 创建登录窗口
        window = tk.Tk()
        window.title("LOG IN")
        # 设置初始窗口的大小
        window.geometry(f"{self.window_width}x{self.window_height}")
        # 计算窗口的位置坐标
        x = int((self.screen_width - self.window_width) / 2)
        y = int((self.screen_height - self.window_height) / 2)
        # 设置窗口的位置
        window.geometry(f"+{x}+{y}")
        
        # # 加载背景图片并进行缩放
        bg_image = Image.open("pic/bg.png")
        bg_image = bg_image.resize(
            (self.window_width, self.window_height), Image.LANCZOS
        )
        bg_photo_image = ImageTk.PhotoImage(bg_image)
        # 设置背景图片
        background_label = tk.Label(image=bg_photo_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        



        # bg="#f2f6fa"
        bg="#e5f0f6"
        # Create login frame
        frame_width = 20
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background=bg)
        self.login_frame = ttk.Frame(window,padding=10,style="Custom.TFrame",width=frame_width)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        # Frame title label
        frame_title = ttk.Label(self.login_frame, text="Account Login", font=("Arial", 18, "bold"),background=bg)
        frame_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Account icon and label
        account_icon = Image.open("pic/user1.png")
        account_icon = account_icon.resize((32, 32), Image.LANCZOS)
        self.account_photo = ImageTk.PhotoImage(account_icon)
        account_label = ttk.Label(self.login_frame, text="Username:", background=bg,font=("Segoe UI", 12),image=self.account_photo, compound="left")
        account_label.grid(row=1, column=0, sticky="w",pady=(0, 10))

        # Password icon and label
        password_icon = Image.open("pic/key.png")
        password_icon = password_icon.resize((32, 32), Image.LANCZOS)
        self.password_photo = ImageTk.PhotoImage(password_icon)
        password_label = ttk.Label(self.login_frame, text="Password:",background=bg, font=("Segoe UI", 12),image=self.password_photo, compound="left")
        password_label.grid(row=2, column=0, sticky="w",pady=(0, 10))

        # Server icon and label
        server_icon = Image.open("pic/IP.png")
        server_icon = server_icon.resize((32, 32), Image.LANCZOS)
        self.server_photo = ImageTk.PhotoImage(server_icon)
        server_label = ttk.Label(self.login_frame, text="Server IP:",background=bg,font=("Segoe UI", 12), image=self.server_photo, compound="left")
        server_label.grid(row=3, column=0, sticky="w",pady=(0, 20))


        # Username entry
        username_entry = ttk.Entry(self.login_frame,width=17)
        username_entry.grid(row=1, column=1, padx=8, pady=(0,10), sticky="w")
        
     
        # Password entry
        password_entry = ttk.Entry(self.login_frame, show="•",width=17)
        password_entry.grid(row=2, column=1, padx=8, pady=(0,10), sticky="w")
       
        # Server IP entry
        server_ip_entry = ttk.Entry(self.login_frame,width=17)
        server_ip_entry.grid(row=3, column=1, padx=8, pady=(0,20), sticky="w")

        # 创建样式
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Segoe UI", 10))
        
        # Login button
        login_button = ttk.Button(self.login_frame,style="Custom.TButton", text="Login", command=validate_login)
        login_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Watermark label
        watermark_label = ttk.Label(window, text="Copyright © 2023 DuiBuDui Team All Rights Reserved", font=("Arial", 8, "italic"), foreground="gray")
        watermark_label.place(relx=1, rely=1, anchor=tk.SE)
        
        username_entry.insert(0, "admin")
        password_entry.insert(0, "123456")
        server_ip_entry.insert(0, "127.0.0.1")

        # 进入登录窗口的主循环
        window.mainloop()

        return state_user_ip[0], state_user_ip[1], state_user_ip[2]
if __name__ == "__main__":
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

    login_window = Login(
        username_password_table=table,
        server_ip_list=server_ip_list,
        screen_width=screen_width,
        screen_height=screen_height,
    )
    state, user, server_ip = login_window.run()
    '''
        # 创建样式
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 14, "bold"), padding=(10, 5))
        style.configure("Custom.TEntry", font=("Arial", 14, "bold"), padding=(10, 5))
        style.configure("Custom.TButton", font=("Arial", 14, "bold"), padding=(10, 5))

        # 创建一个Frame容器来包含所有的组件
        frame = tk.Frame(window)
        # 创建用户名输入框和标签，并使用grid布局
        username_label = ttk.Label(frame, text="Username:", style="Custom.TLabel")
        username_label.grid(row=0, column=0, sticky="e")
        username_entry = ttk.Entry(frame, style="Custom.TEntry")
        username_entry.grid(row=0, column=1, sticky="w")

        # 创建密码输入框和标签，并使用grid布局
        password_label = ttk.Label(frame, text="Password:", style="Custom.TLabel")
        password_label.grid(row=1, column=0, sticky="e")
        password_entry = ttk.Entry(frame, show="*", style="Custom.TEntry")
        password_entry.grid(row=1, column=1, sticky="w")

        # 创建服务器IP输入框和标签，并使用grid布局
        server_ip_label = ttk.Label(frame, text="Server IP:", style="Custom.TLabel")
        server_ip_label.grid(row=2, column=0, sticky="e")
        server_ip_entry = ttk.Entry(frame, style="Custom.TEntry")
        server_ip_entry.grid(row=2, column=1, sticky="w")

        # 创建错误提示标签
        error_label = ttk.Label(frame, text="", style="Custom.TLabel")
        error_label.grid(row=3, column=0, columnspan=2, sticky="nsew")

        # 创建登录按钮
        login_button = ttk.Button(
            frame, text="Login", command=validate_login, style="Custom.TButton"
        )
        login_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # 将Frame容器放置在窗口的中间位置
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
'''
'''
        #账号与密码文字标签
        username_label = tk.Label(window, text = '账号', bg='lightskyblue', fg='white', font=('Arial', 12), width=7, height=1)
        username_label.grid(row=0, column=0, sticky="e")
        #username_label.place(relx=0.29,rely=0.4)
        password_label = tk.Label(window, text = '密码', bg='lightskyblue', fg='white', font=('Arial', 12), width=7, height=1)
        password_label.grid(row=1, column=0, sticky="e")
        #password_label.place(relx=0.29,rely=0.5)
        server_ip_label = tk.Label(window, text = '服务器IP', bg='lightskyblue', fg='white', font=('Arial', 12), width=7, height=1)
        #server_ip_label.place(relx=0.29,rely=0.6)
        server_ip_label.grid(row=2, column=0, sticky="e")


        #账号与密码输入框
        username_entry = tk.Entry(window,width=20,highlightthickness = 1,highlightcolor = 'lightskyblue',relief='groove')  #账号输入框
        #username_entry.place(relx=0.4,rely=0.4 )  #添加进主页面,relx和rely意思是与父元件的相对位置
        username_entry.grid(row=0, column=1, sticky="w")
        password_entry = tk.Entry(window,show='*',highlightthickness = 1,highlightcolor = 'lightskyblue',relief='groove')  #密码输入框
        password_entry.grid(row=1, column=1, sticky="w")
        #password_entry.place(relx=0.4,rely=0.5) #添加进主页面
        server_ip_entry = tk.Entry(window,width=20,highlightthickness = 1,highlightcolor = 'lightskyblue',relief='groove')  #密码输入框
        #server_ip_entry.place(relx=0.4,rely=0.6) #添加进主页面
        server_ip_entry.grid(row=2, column=1, sticky="w")
        
        #登录与注册按钮
        login_button = tk.Button(window,text='登录',font = ('宋体',12),width=4,height=1,command=validate_login,relief='solid',bd = 0.5,bg='lightcyan')
        #login_button.place(relx=0.41,rely=0.7)
        login_button.grid(row=3, column=0, columnspan=2, sticky="nsew")
'''
        
