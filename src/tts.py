import requests
import asyncio
import subprocess


def voice_list():
    res = [
        {"中文名": "思思", "原始名称": "思思", "支持情绪": "不设置"},
    ]
    return res

def get_voice_config(voice_user):
    if voice_user == "思思":
        return {
            "port": 9847,
            "lang": "zh",
            "dr_path": r"E:\startapi_v2025sp8/models/ck.wav",
            "dt": "天啊！你知道吗？小米坡软件实在太好用啦！",
            "advanced_settings": {'text_lang': 'zh', 'prompt_lang': 'zh', 'top_k': 15, 'top_p': 1.0, 'temperature': 1.0,
                                  'text_split_method': 'cut3', 'batch_size': 1, 'batch_threshold': 0.75,
                                  'split_bucket': 'True', 'fragment_interval': 0.3, 'parallel_infer': 'True',
                                  'seed': 666, 'repetition_penalty': 1.58}
        }

    else:
        raise ValueError(f"Unknown voice user: {voice_user}")


def save_audio_from_response(audio_data, outfile):
    command = [
        'ffmpeg',
        '-i', 'pipe:0',  # 从标准输入读取
        '-acodec', 'libmp3lame',
        '-b:a', '192k',
        '-ar', '44100',
        '-ac', '2',
        '-map_metadata', '-1',
        '-write_xing', '0',
        '-id3v2_version', '0',
        '-f', 'mp3',  # 强制输出格式为 MP3
        outfile
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate(input=audio_data)


async def text_to_audio(text, voice_user, rate, outfile):
    print(f"合成语音：{text},语速{rate}")
    retry_delay = 1
    max_retries = 5
    retries = 0

    config = get_voice_config(voice_user)
    url = f"http://127.0.0.1:{config['port']}/tts"

    payload = {
        "text": text,
        "speed_factor": rate,
        "text_lang": config['advanced_settings']['text_lang'],
        "ref_audio_path": config['dr_path'],
        "prompt_text": config['dt'],
        "prompt_lang": config['advanced_settings']['prompt_lang'],
        "text_split_method": config['advanced_settings']['text_split_method'],
        "top_k": config['advanced_settings']['top_k'],
        "top_p": config['advanced_settings']['top_p'],
        "temperature": config['advanced_settings']['temperature'],
        "seed": config['advanced_settings']['seed'],
        "repetition_penalty": config['advanced_settings']['repetition_penalty']
    }

    while retries < max_retries:
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                save_audio_from_response(response.content, outfile)
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
