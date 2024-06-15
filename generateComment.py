import threading
import os
import time
import csv
import qianfan
import random
from openpyxl import Workbook
import names
from datetime import datetime, timedelta

os.environ["QIANFAN_AK"] = 'WelXiaDoSlc8Qc7DMZGdax2s'
os.environ["QIANFAN_SK"] = 'B4HN63Q6MHXqdnfFKzxreloQpMHWTWzb'
start_time = time.time()


def generate_comment(product, country, total_num):
    Comment = []

    def random_word():
        word = ['质量', '外观', '使用感受', '物流']
        return random.choice(word)

    def call_api():
        random = random_word()
        resp = qianfan.ChatCompletion().do(endpoint="ernie-speed-128k", messages=[{"role": "user",
                                                                                   "content": "您好，我有一个产品{}"
                                                                                              "在电商网站上出售，需要你模仿客户的语气用西班牙语帮我写1条50词左右有关产品{}的好评。"
                                                                                              "注意，不要输出中文！不要输出中文！不要输出中文！".format(
                                                                                       random, product)}])
        Comment.append(resp.body.get('result'))

    def parallel_requests(num):
        threads = []
        for i in range(num):
            thread = threading.Thread(target=call_api)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def is_spanish_character(char):
        # 判断字符是否是西班牙语字符
        if ('a' <= char <= 'z') or ('A' <= char <= 'Z') or ('0' <= char <= '9'):
            return True
        if char in "ñÑáéíóúÁÉÍÓÚüÜ¡¿ ,.!?":
            return True
        return False

    def filter_spanish_text(text):
        # 过滤文本中的非西班牙语字符
        return ''.join(filter(is_spanish_character, text))

    def generate_random_dates(start, end, count, date_format='%Y/%m/%d'):
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')

        random_date = ''
        for _ in range(count):
            random_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )
            random_date = (random_date.strftime(date_format))

        return random_date

    parallel_requests(total_num)

    filter_comment = []
    for i in range(total_num):
        filter_comment.append(filter_spanish_text(Comment[i]))

    local_file_path = 'comment.csv'
    file_path = 'comment.xlsx'
    # 创建并写入新的 CSV 文件
    with open(local_file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        header = [
            "商品Handle(必须)", "姓名(必须)", "评分(必须,分值为1-5)",
            "日期(格式：YYYY/MM/DD)", "国家", "内容",
            "点赞数", "图片链接地址[用英文,分割]"
        ]

        # 写入表头
        writer.writerow(header)

        # 写入数据，内容列填入内容列表中的数据
        for content in filter_comment:
            row = [
                product,  # 商品Handle(必须)
                names.get_full_name(),  # 姓名(必须)
                random.randint(4, 5),  # 评分(必须,分值为1-5)
                generate_random_dates('2024-01-01', '2024-6-5', 1),  # 日期(格式：YYYY/MM/DD)
                country,  # 国家
                content,  # 内容
                random.randint(45, 105),  # 点赞数
                ""  # 图片链接地址[用英文,分割]
            ]
            writer.writerow(row)

        def write_data_to_xlsx(xlsx_file):
            # 创建一个工作簿对象
            wb = Workbook()
            ws = wb.active

            # 写入表头
            ws.append(header)

            # 写入数据
            for i in filter_comment:
                r = [
                    product,  # 商品Handle(必须)
                    names.get_full_name(),  # 姓名(必须)
                    random.randint(4, 5),  # 评分(必须,分值为1-5)
                    generate_random_dates('2024-01-01', '2024-6-5', 1),  # 日期(格式：YYYY/MM/DD)
                    country,  # 国家
                    i,  # 内容
                    random.randint(45, 105),  # 点赞数
                    ""  # 图片链接地址[用英文,分割]
                ]
                ws.append(r)

            # 保存工作簿为XLSX文件
            wb.save(xlsx_file)

        write_data_to_xlsx(file_path)
        print(f"total_time_cost {time.time() - start_time}")
        current_directory = os.path.dirname(os.path.abspath(__file__))
        abs_file_path = os.path.join(current_directory, file_path)

        return abs_file_path


# path = generate_comment('iphone 15', 'MX',20)
# print(path)
