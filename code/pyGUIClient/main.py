import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from upload_file import upload_file, recieve_file
from download_file import download_file
from show_result import show_result
from PIL import Image, ImageTk


def set_log(scrolled_text, string):
    now = datetime.now()
    prefix = now.strftime("[%Y-%m-%d %H:%M:%S] ")
    scrolled_text.config(state="normal")
    scrolled_text.insert(tk.END, prefix + string + "\n")
    scrolled_text.configure(state="disabled")
    scrolled_text.see(tk.END)


class Main:
    scrolled_text = None

    def __init__(
        self,
        user,
        server_ip,
        screen_width,
        screen_height,
        window_width=800,
        window_height=550,
    ):
        self.user = user
        self.server_ip = server_ip
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_width = window_width
        self.window_height = window_height
        self.result_file = None

    def run(self):
        def upload():
            file_path = filedialog.askopenfilename()
            if file_path:
                set_log(log_text, "uploading file: " + file_path)
                upload_file(file_path)

        def download():
            file_path = recieve_file()
            set_log(log_text, "downloading file: " + file_path)
            download_file(file_path)
            self.result_file = file_path

        def result():
            if self.result_file:
                set_log(log_text, "showing result: " + self.result_file)
                show_result(self.result_file)
            else:
                set_log(
                    log_text,
                    "error: No result file! Please upload file and download result first! ",
                )

        def exit_main():
            set_log(log_text, "exit")
            window.unbind("<Configure>")
            window.destroy()

        window = tk.Tk()
        window.title("File Manager")
        # 设置初始窗口的大小
        window.geometry(f"{self.window_width}x{self.window_height}")
        # 计算窗口的位置坐标
        x = int((self.screen_width - self.window_width) / 2)
        y = int((self.screen_height - self.window_height) / 2)
        # 设置窗口的位置
        window.geometry(f"+{x}+{y}")

        # 创建样式
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 14, "bold"), padding=(10, 5))
        style.configure("Custom.TEntry", font=("Arial", 14, "bold"), padding=(10, 5))
        style.configure("Custom.TButton", font=("Arial", 12, "bold"), padding=(10, 5),width=15)
        style.configure(
            "Custom.TScrolledText",
            background="white",
            foreground="black",
            font=("Arial", 14),
            padding=(10, 10),
        )

        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True)
        '''
        # 左边部分 - 插入图片
        left_frame = tk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        bg_image = Image.open("pic/hh1.png")
        bg_image = bg_image.resize((self.window_width // 2, self.window_height // 2), Image.LANCZOS)
        bg_photo_image = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(left_frame, image=bg_photo_image)
        bg_label.pack(anchor="nw")  # 使用anchor参数来设置标签在Frame中的对齐方式
        '''
        # 左边部分 - 插入图片
        left_frame = tk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        bg_image = Image.open("pic/hh1.png")
        bg_image = bg_image.resize((self.window_width // 2, self.window_height // 2), Image.LANCZOS)
        bg_photo_image = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(left_frame, image=bg_photo_image)
        bg_label.pack(side=tk.TOP, anchor="nw")

        # 下半部分 - 放置四个按钮
        button_frame = tk.Frame(left_frame, pady=20)
        button_frame.pack(side=tk.TOP, anchor="sw")

        
        upload_button = ttk.Button(
            button_frame, text="Upload File", style="Custom.TButton", command=upload
        )
        upload_button.grid(row=0, column=0, padx=10, pady=10)

        download_button = ttk.Button(
            button_frame,
            text="Download Result",
            style="Custom.TButton",
            command=download,
        )
        download_button.grid(row=0, column=1, padx=10, pady=10)

        show_result_button = ttk.Button(
            button_frame, text="Show Result", style="Custom.TButton", command=result
        )
        show_result_button.grid(row=1, column=0, padx=10, pady=10)

        exit_button = ttk.Button(
            button_frame, text="Exit", style="Custom.TButton", command=exit_main
        )
        exit_button.grid(row=1, column=1, padx=10, pady=10)


        '''
        # 右边部分 - 滚动文本框
        right_frame = tk.Frame(frame, width=self.window_width // 2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        '''
        right_frame = tk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 计算相对于窗口宽度的位置
        rel_width = 0.5  # 相对于窗口宽度的一半
        right_frame.place(relx=1.0, rely=0, relwidth=rel_width, relheight=1.0, anchor=tk.NE)

        # 创建标题标签
        title_label = ttk.Label(frame, text="LOG AREA", style="Custom.TLabel")
        title_label.pack()

        # 创建文本框
        log_text = ScrolledText(frame, state="disabled", font=("Arial", 14))
        log_text.pack(fill=tk.BOTH, expand=True)

        Main.scrolled_text = log_text
        '''
        # 创建按钮容器
        button_frame = tk.Frame(window)
        button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建按钮
        upload_button = ttk.Button(
            button_frame, text="Upload File", style="Custom.TButton", command=upload
        )
        upload_button.grid(row=0, column=0, padx=10, pady=10)

        download_button = ttk.Button(
            button_frame,
            text="Download Result",
            style="Custom.TButton",
            command=download,
        )
        download_button.grid(row=0, column=1, padx=10, pady=10)

        show_result_button = ttk.Button(
            button_frame, text="Show Result", style="Custom.TButton", command=result
        )
        show_result_button.grid(row=1, column=0, padx=10, pady=10)

        exit_button = ttk.Button(
            button_frame, text="Exit", style="Custom.TButton", command=exit_main
        )
        exit_button.grid(row=1, column=1, padx=10, pady=10)

        '''



        '''
        # 创建按钮容器
        button_frame = tk.Frame(window)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER)

        # 创建按钮
        upload_button = ttk.Button(
            button_frame, text="Upload File", style="Custom.TButton", command=upload
        )
        upload_button.pack(side=tk.LEFT, padx=10, pady=10)

        download_button = ttk.Button(
            button_frame,
            text="Download Result",
            style="Custom.TButton",
            command=download,
        )
        download_button.pack(side=tk.LEFT, padx=10, pady=10)

        show_result_button = ttk.Button(
            button_frame, text="Show Result", style="Custom.TButton", command=result
        )
        show_result_button.pack(side=tk.LEFT, padx=10, pady=10)

        exit_button = ttk.Button(
            button_frame, text="Exit", style="Custom.TButton", command=exit_main
        )
        exit_button.pack(side=tk.LEFT, padx=10, pady=10)
        '''
        '''
        # 设置窗口宽度与文本框等宽
        window.update_idletasks()
        width = window.winfo_width()
        log_text.configure(width=width)
        '''
        window.mainloop()
