import tkinter as tk
from tkinter import ttk
import hashlib
from PIL import Image, ImageTk


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
        window_height=600,
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
                error_label.config(text="Invalid username or password!")
            elif server_ip not in self.server_ip_list:
                error_label.config(text="Invalid server IP!")
            else:
                # 修改状态、用户名和IP
                state_user_ip[0] = True
                state_user_ip[1] = username
                state_user_ip[2] = server_ip
                window.unbind("<Configure>")
                window.destroy()

        state_user_ip = [False, None, None]

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

        # 加载背景图片并进行缩放
        bg_image = Image.open("pic/bg.png")
        bg_image = bg_image.resize(
            (self.window_width, self.window_height), Image.LANCZOS
        )
        bg_photo_image = ImageTk.PhotoImage(bg_image)
        # 设置背景图片
        background_label = tk.Label(image=bg_photo_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

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

        username_entry.insert(0, "admin")
        password_entry.insert(0, "123456")
        server_ip_entry.insert(0, "127.0.0.1")

        # 进入登录窗口的主循环
        window.mainloop()

        return state_user_ip[0], state_user_ip[1], state_user_ip[2]
