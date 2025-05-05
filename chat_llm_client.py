import requests
import json
import time

BASE_URL = "http://localhost:8080"  # Change to your server's IP if testing remotely


def chat(chat_str, stream_in=True):
    fix_llm_payload = {"messages": [{"role": "user", "content": chat_str}], "stream": stream_in}
    fixed_string = ""
    print("Time now: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    try:
        if stream_in:
            with requests.post(f"{BASE_URL}/chatllm", json=fix_llm_payload,
                               stream=True) as response:
                print("\nStreaming response:")
                buffer = b""
                for chunk in response.iter_content(chunk_size=1):  # 逐字节处理
                    if chunk:
                        buffer += chunk
                        if buffer.endswith(b"\n\n"):  # SSE事件结束标志
                            try:
                                event = buffer.decode('utf-8').strip()
                                if event.startswith("data:"):
                                    content = event[5:].strip()
                                    if content:
                                        # print(content, end="", flush=True)
                                        fixed_string += content
                            except UnicodeDecodeError:
                                pass  # 忽略中间解码错误
                            buffer = b""
        else:
            response = requests.post(f"{BASE_URL}/chatllm", json=fix_llm_payload)
            response.raise_for_status()
            fixed_string = response.json().get("corrected_text", "")
            # print("Sync response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    # print("Time now: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return fixed_string


if __name__ == "__main__":
    print(chat("Hello, what's your name? please speak with me in Chinese"))  # Test streaming
