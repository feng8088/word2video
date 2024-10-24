import os
import shutil
import subprocess
import tkinter as tk

from mutagen.mp3 import MP3
from pydub.utils import mediainfo
from tkinter import filedialog
from tkinter import messagebox
import moviepy.editor as mp
import cv2
import docx
import numpy as np
from io import BytesIO
import asyncio
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from moviepy.editor import CompositeAudioClip
from moviepy.config import change_settings
import threading
import tts as tts

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # 获取当前文件所在目录
        current_directory = os.path.dirname(os.path.abspath(__file__))

        self.title("小米坡 word文档转视频生成工具 v1.0")
        self.geometry("1000x800")
        self.resizable(False, False)  # 禁止调整窗口大小

        # 创建两个主容器
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.left_frame = tk.LabelFrame(self.main_frame, text="主功能区", padx=10, pady=10)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.LabelFrame(self.main_frame, text="关于", padx=10, pady=10)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # 左侧主功能区
        self.word_doc_frame = tk.LabelFrame(self.left_frame, text="Word 文档选项", padx=10, pady=10)
        self.word_doc_frame.pack(fill="x", padx=5, pady=5)

        self.word_doc_path = tk.StringVar()
        self.word_doc_entry = tk.Entry(self.word_doc_frame, textvariable=self.word_doc_path, width=40)
        self.word_doc_entry.pack(side="left", padx=5)

        self.word_doc_button = tk.Button(self.word_doc_frame, text="选择 Word 文档", command=self.choose_word_doc)
        self.word_doc_button.pack(side="left", padx=5)

        self.background_audio_frame = tk.LabelFrame(self.left_frame, text="背景音乐文件", padx=10, pady=10)
        self.background_audio_frame.pack(fill="x", padx=5, pady=5)

        self.background_audio_path = tk.StringVar(value="")
        self.background_audio_entry = tk.Entry(self.background_audio_frame, textvariable=self.background_audio_path, width=40)
        self.background_audio_entry.pack(side="left", padx=5)

        self.background_audio_button = tk.Button(self.background_audio_frame, text="选择背景音乐", command=self.choose_background_audio)
        self.background_audio_button.pack(side="left", padx=5)

        self.export_dir_frame = tk.LabelFrame(self.left_frame, text="视频导出目录", padx=10, pady=10)
        self.export_dir_frame.pack(fill="x", padx=5, pady=5)

        self.export_dir_path = tk.StringVar()
        self.export_dir_entry = tk.Entry(self.export_dir_frame, textvariable=self.export_dir_path, width=40)
        self.export_dir_entry.pack(side="left", padx=5)

        self.export_dir_button = tk.Button(self.export_dir_frame, text="选择导出目录", command=self.choose_export_dir)
        self.export_dir_button.pack(side="left", padx=5)

        self.volume_frame = tk.LabelFrame(self.left_frame, text="BGM音量控制", padx=10, pady=10)
        self.volume_frame.pack(fill="x", padx=5, pady=5)

        self.volume_frame2 = tk.LabelFrame(self.left_frame, text="配音音量控制", padx=10, pady=10)
        self.volume_frame2.pack(fill="x", padx=5, pady=5)


        self.background_volume_scale = tk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, resolution=1, length=400)
        self.background_volume_scale.set(50)
        self.background_volume_scale.pack(side="left", padx=5)


        self.narration_volume_scale = tk.Scale(self.volume_frame2, from_=0, to=100, orient=tk.HORIZONTAL, resolution=1, length=400)
        self.narration_volume_scale.set(100)
        self.narration_volume_scale.pack(side="left", padx=5)

        self.enable_subtitles_frame = tk.LabelFrame(self.left_frame, text="字幕设置", padx=10, pady=10)
        self.enable_subtitles_frame.pack(fill="x", padx=5, pady=5)

        self.enable_subtitles = tk.BooleanVar(value=True)
        self.enable_subtitles_checkbox = tk.Checkbutton(self.enable_subtitles_frame, text="启用字幕", variable=self.enable_subtitles)
        self.enable_subtitles_checkbox.pack(side="left", padx=5)

        self.progress_frame = tk.LabelFrame(self.left_frame, text="进度", padx=10, pady=10)
        self.progress_frame.pack(fill="x", padx=5, pady=5, expand=True)

        self.progress_text = tk.Text(self.progress_frame, height=10, width=60, yscrollcommand=True)
        self.progress_text_scrollbar = tk.Scrollbar(self.progress_frame, command=self.progress_text.yview)
        self.progress_text.config(yscrollcommand=self.progress_text_scrollbar.set)
        self.progress_text.pack(side="left", fill="x", expand=True)
        self.progress_text_scrollbar.pack(side="right", fill="y")

        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(fill="x", padx=5, pady=5)

        self.start_button = tk.Button(self.button_frame, text="开始生成", command=self.start_generation)
        self.start_button.pack(side="left", padx=5)

        self.view_button = tk.Button(self.button_frame, text="点击查看文件", command=self.open_export_dir)
        self.view_button.pack(side="left", padx=5)



        log_path = os.path.join(current_directory, "static", "logo.gif")
        self.logo_image = tk.PhotoImage(file=log_path)

        # Create Label with image
        self.logo_label = tk.Label(self.right_frame, image=self.logo_image)
        self.logo_label.pack(pady=10)

        # 右侧关于信息
        self.about_label = tk.Label(self.right_frame, text="小米坡 word文档转视频生成工具")
        self.about_label.pack(pady=10)

        self.version_label = tk.Label(self.right_frame, text="用户版本 ：v1")
        self.version_label.pack(pady=10)

    def choose_word_doc(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word 文档", "*.docx")])
        self.word_doc_path.set(file_path)

    def choose_export_dir(self):
        dir_path = filedialog.askdirectory()
        self.export_dir_path.set(dir_path)

    def choose_background_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("音频文件", "*.mp3;*.wav")])
        self.background_audio_path.set(file_path)

    def start_generation(self):
        # if datetime.now() >= datetime(2024, 4, 8, 23, 59, 59):
        #     print("内测已结束。")
        #     return
        thread = threading.Thread(target=self.generate_video_thread)
        thread.start()

    def generate_video_thread(self):
        word_doc_file = self.word_doc_path.get()
        export_dir = self.export_dir_path.get()
        background_audio_volume = self.background_volume_scale.get() / 100
        narration_volume = self.narration_volume_scale.get() / 100
        enable_subtitles = self.enable_subtitles.get()

        if not word_doc_file:
            messagebox.showerror("错误", "请选择 Word 文档")
            return
        if not export_dir:
            messagebox.showerror("错误", "请选择导出目录")
            return

        self.progress_text.insert(tk.END, "开始任务, 如果出现未知错误, 请关掉软件重新打开.\n")
        self.progress_text.insert(tk.END, "如果你导出要覆盖的已存在视频, 确保那个视频不被其它进程占用.\n")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            images, texts = self.get_images_and_texts(word_doc_file)
            audio_files = []
            print(len(texts))
            for i, text in enumerate(texts):
                print(i)
                audio_file = os.path.join(export_dir, f"audio_{i}.mp3")
                audio_files.append(audio_file)
                self.generate_audio(text, audio_file)
                self.progress_text.insert(tk.END, f"生成配音：{text}.\n")

            self.progress_text.insert(tk.END, "完成配音音频文件生成.\n")
            output_file = os.path.join(export_dir, "output_video.mp4")
            background_audio_file = self.background_audio_path.get()
            self.progress_text.insert(tk.END, "正在生成视频文件.\n")
            self.generate_video(images, texts, output_file, audio_files, background_audio_file, background_audio_volume, narration_volume, enable_subtitles)
            messagebox.showinfo("提示", "视频生成成功")
        except Exception as e:
            messagebox.showerror("错误", f"生成视频时出错：{e}")
        finally:
            loop.close()

    def open_export_dir(self):
        export_dir = self.export_dir_path.get()
        if not export_dir:
            messagebox.showerror("错误", "请选择导出目录")
            return
        os.startfile(export_dir)

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def get_images_and_texts(self, docx_file):
        images = []
        texts = []
        try:
            doc = docx.Document(docx_file)
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    texts.append(paragraph.text.strip())

            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    image_bytes = rel.target_part.blob
                    images.append(image_bytes)

            return images, texts
        except Exception as e:
            messagebox.showerror("错误", f"提取图片和文字内容时出错：{e}")
            return [], []

    def generate_audio(self, text, output_file):
        try:
            asyncio.run(tts.text_to_audio(text, '思思', 1.0, output_file))
        except Exception as e:
            messagebox.showerror("错误", f"生成音频时出错：{e}")
            return None

    def generate_video(self, images, texts, output_file, audio_durations, background_audio_file,
                       background_audio_volume, narration_volume, enable_subtitles):
        try:
            clips = []

            # srt字幕文件内容
            srt_content = ''
            srt_time1 = 0
            srt_time2 = 0

            for idx, image_bytes in enumerate(images):
                image_stream = BytesIO(image_bytes)
                image_array = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), -1)
                image_path = f"temp_image_{idx}.jpg"
                cv2.imwrite(image_path, image_array)

                duration = 5
                audio_path = ""
                if idx < len(audio_durations):
                    audio_path = audio_durations[idx]
                    audio_duration = self.get_audio_duration(audio_path)
                    if audio_duration > duration:
                        duration = audio_duration

                temp_str = str(idx) + '\n'
                srt_time2 = srt_time1 + duration
                # 添加字幕时间信息
                temp_str = temp_str + f"{int(srt_time1 // 3600):02d}:{int((srt_time1 // 60) % 60):02d}:{int(srt_time1 % 60):02d},{int((srt_time1 - int(srt_time1)) * 1000):03d} --> {int(srt_time2 // 3600):02d}:{int((srt_time2 // 60) % 60):02d}:{int(srt_time2 % 60):02d},{int((srt_time2 - int(srt_time2)) * 1000):03d}\n"
                temp_str = temp_str + texts[idx] + '\n'
                # 更新时间起点
                srt_time1 = srt_time2
                srt_content = srt_content + temp_str

                if audio_path != "":
                    audio_clip = AudioFileClip(audio_path).volumex(narration_volume)
                    clip = mp.ImageClip(image_path).set_duration(duration)
                    clip = clip.set_audio(audio_clip)

                    if idx > 0:
                        clip = clip.crossfadein(1)
                        previous_clip = clips[-1]
                        previous_clip = previous_clip.crossfadeout(1)
                        clips[-1] = previous_clip
                    clips.append(clip)
                    os.remove(image_path)

            # 保存字幕文件
            srt_file_path = output_file.replace(".mp4", ".srt")
            with open(srt_file_path, "w", encoding="utf-8") as srt_file:
                srt_file.write(srt_content)

            final_clip = mp.concatenate_videoclips(clips, method="compose")
            if os.path.exists(output_file):
                os.remove(output_file)
            final_clip.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")

            self.progress_text.insert(tk.END, "正在合并音频视频.\n")

            video_clip = VideoFileClip(output_file)
            original_audio_clip = video_clip.audio
            new_audio_clip = AudioFileClip(background_audio_file).volumex(background_audio_volume)
            final_audio_clip = CompositeAudioClip([original_audio_clip, new_audio_clip])
            video_clip_with_new_audio = video_clip.set_audio(final_audio_clip)

            file2 = output_file.replace(".mp4", "_with_audio.mp4")
            if os.path.exists(file2):
                os.remove(file2)
            video_clip_with_new_audio.write_videofile(file2, fps=24, codec="libx264", audio_codec="aac")

            if enable_subtitles:
                self.progress_text.insert(tk.END, "正在嵌入字幕.\n")
                file3 = output_file.replace(".mp4", "_with_audio_subtitles.mp4")
                if os.path.exists(file3):
                    os.remove(file3)

                # 拷贝一份到根目录
                current_directory = os.path.dirname(os.path.abspath(__file__))
                srt_file_name = "temp.srt"
                subtitles_file = os.path.join(current_directory, srt_file_name)
                shutil.copy(srt_file_path, subtitles_file)
                cmd_line = f'ffmpeg -i {file2} -vf subtitles={srt_file_name} {file3}'
                subprocess.call(cmd_line, shell=True)

                os.remove(subtitles_file)
                os.remove(output_file)
                os.remove(file2)

            self.progress_text.insert(tk.END, "Video successfully generated.\n")
        except Exception as e:
            self.progress_text.insert(tk.END, f"Error while generating video: {e}\n")
            messagebox.showerror("错误", f"生成视频时出错：{e}")

    def get_audio_duration(self, audio_file):
        try:
            audio = MP3(audio_file)
            return audio.info.length
        except Exception as e:
            print(f"{audio_file} err {e}")
            messagebox.showerror("错误", f"获取音频时长时出错：{e}")
            return None

if __name__ == "__main__":
    app = Application()
    app.mainloop()
