import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from upload_file import upload_file, recieve_file
from download_file import download_file
from show_result import show_result
import logging


def set_log(scrolled_text, string):
    now = datetime.now()
    msg = now.strftime("[%Y-%m-%d %H:%M:%S] ") + string + '\n'
    scrolled_text.config(state="normal")
    scrolled_text.insert(tk.END, msg)
    scrolled_text.configure(state="disabled")
    scrolled_text.see(tk.END)
    logging.info(msg)


class Main:
    scrolled_text = None

    def __init__(
        self,
        user,
        server_ip,
        screen_width,
        screen_height,
        window_width=800,
        window_height=600,
    ):
        self.user = user
        self.server_ip = server_ip
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_width = window_width
        self.window_height = window_height
        self.result_file = None

        logging.basicConfig(filename='pyGUIClient.log',level=logging.INFO)

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
        style.configure("Custom.TButton", font=("Arial", 14, "bold"), padding=(10, 5))
        style.configure(
            "Custom.TScrolledText",
            background="white",
            foreground="black",
            font=("Arial", 14),
            padding=(10, 10),
        )

        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True)

        # 创建标题标签
        title_label = ttk.Label(frame, text="LOG AREA", style="Custom.TLabel")
        title_label.pack()

        # 创建文本框
        log_text = ScrolledText(frame, state="disabled", font=("Arial", 14))
        log_text.pack(fill=tk.BOTH, expand=True)

        Main.scrolled_text = log_text

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

        # 设置窗口宽度与文本框等宽
        window.update_idletasks()
        width = window.winfo_width()
        log_text.configure(width=width)

        window.mainloop()
