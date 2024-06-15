import streamlit as st
import os
from generateComment import generate_comment


def read_local_file(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        st.error("文件不存在")
        return None, None

    # 读取文件内容
    with open(file_path, 'r', encoding='latin1') as file:
        content = file.read()

    return content, file_path


st.set_page_config(page_title="CommentGenerator", page_icon="img/rephraise_logo.png", )


def main():
    st.image('img/image_banner.png')
    st.title("产品评论自动生成")
    st.subheader('测试版')

    # 获取用户输入
    product = st.text_input(label='产品名称', value="")
    country = st.text_input(label='目标国家', value='MX')
    num = st.number_input(label='生成数量(当前性能下建议单次生成不超过30条，否则可能出错)', value=20)

    if st.button("生成评论"):
        with st.spinner():
            file_path = generate_comment(product, country, num)
        content, download_path = read_local_file(file_path)
        if content and download_path:
            st.image('img/files.png')
            # st.text_area("文件内容(该文件直接在店铺后台对应商品处上传即可)", content, height=200)
            # 使用 st.download_button 生成下载链接
            with open(download_path, 'rb') as file:
                st.download_button(
                    label="下载文件",
                    data=file,
                    file_name=os.path.basename(download_path),
                    mime='text/plain'
                )


if __name__ == "__main__":
    main()
