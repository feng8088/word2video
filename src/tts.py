import requests
import asyncio
import subprocess

def voice_list():
    res = [
{"中文名":"思思","原始名称":"思思","支持情绪":"不设置"},
    ]
    return res

def get_voice_config(voice_user):
    if voice_user == "思思":
        return {
            "port": 9821,
            "dl": "zh"
        }
    else:
        raise ValueError(f"Unknown voice user: {voice_user}")

def save_audio_from_response(audio_data, outfile):
    ffmpeg_path = 'ffmpeg.exe'
    command = [
        ffmpeg_path,
        '-i', 'pipe:0',  # 从标准输入读取
        '-acodec', 'libmp3lame',
        '-b:a', '192k',
        '-f', 'mp3',  # 强制输出格式为 MP3
        outfile
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate(input=audio_data)

async def text_to_audio(text, voice_user,rate,outfile):
    print(f"合成语音：{text},语速{rate}")
    retry_delay = 1
    max_retries = 5
    retries = 0

    config = get_voice_config(voice_user)
    url = f"http://127.0.0.1:{config['port']}"

    payload = {
        "text": text,
        "speed": rate,
        "text_language": config['dl']
    }

    while retries < max_retries:
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                save_audio_from_response(response.content, outfile)
                print(f"保存音频：{outfile}")
                break  # 成功执行就跳出循环
            else:
                retries += 1
                print(f"请求失败, 状态码: {response.status_code}, {retry_delay}秒后将自动重试(第{retries}次重试)。")
                await asyncio.sleep(retry_delay)
        except Exception as ex:
            retries += 1
            print(f"请求异常: {ex}, {retry_delay}秒后将自动重试(第{retries}次重试)。")
            await asyncio.sleep(retry_delay)
    else:
        print(f"经过{max_retries}次重试仍然失败,放弃执行。")
