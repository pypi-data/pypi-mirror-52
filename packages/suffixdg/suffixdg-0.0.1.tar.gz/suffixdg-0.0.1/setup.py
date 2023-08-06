import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="suffixdg",
    version="0.0.1",
    author="DUAN GAO",
    author_email="1481407566@qq.com",
    description='1.本程序由高端设计编写，需要引用及任何改进意见请联系邮箱1481407566qq.com。2.DNA功能域是隐藏在DNA序列中具有特定功能的重要区域，通过多条DNA序列比对容易发现。3.DNA序列比对需要耗费大量的计算机算力，本程序依托分支界定的suffix算法，和个人精心设计的程序代码，意图提供有竞争力的运算速度解决DNA比对问题。',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
