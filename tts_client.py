import requests
import json
import time

BASE_URL = "http://localhost:8081"  # Change to your server's IP if testing remotely
import pygame

pygame.mixer.init()


def get_and_play_synthesize(text):
    synthesize_payload = {"text": text}
    print("Time now: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #
    with requests.post(f"{BASE_URL}/tts", json=synthesize_payload) as response:
        response.raise_for_status()
        print("Sync response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        wav_path = response.json().get("wav_path", "")
        print("WAV file path:", wav_path)
        if wav_path:
            pygame.mixer.music.load(wav_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # 如果音乐正在播放，则继续等待
                pygame.time.Clock().tick(10)


if __name__ == "__main__":
    get_and_play_synthesize("你我啊阿对哦山东方")  # Test streaming
