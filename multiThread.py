import asyncio
import aiohttp
import os
import qianfan
import threading
import time

# 替换为你的百度智能云API密钥

os.environ["QIANFAN_AK"] = 'WelXiaDoSlc8Qc7DMZGdax2s'
os.environ["QIANFAN_SK"] = 'B4HN63Q6MHXqdnfFKzxreloQpMHWTWzb'

Comment = []


def call_api(product):
    # 这里替换为实际的 API 调用代码
    # 假设这是一个函数，发送请求并返回结果
    response = qianfan.ChatCompletion().do(endpoint="ernie-speed-128k", messages=[{"role": "user",
                                                                                   "content": "您好，我有一个产品{}"
                                                                                              "在电商网站上出售，需要你模仿客户的语气用西班牙语帮我写1条50词左右的好评。"
                                                                                              "注意，不要输出中文！不要输出中文！不要输出中文！".format(
                                                                                       product)}])
    Comment.append(response.body.get('result'))

start_time = time.time()
def parallel_requests():
    threads = []
    for i in range(10):
        thread = threading.Thread(target=call_api, args=['iphone 14 pro max'])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return "parallel done"


parallel_requests()
print(Comment)
print(f"total_time_cost {time.time() - start_time}")