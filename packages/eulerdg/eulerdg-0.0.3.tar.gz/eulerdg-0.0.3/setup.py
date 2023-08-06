import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eulerdg",
    version="0.0.3",
    author="DUAN GAO",
    author_email="1481407566@qq.com",
    description="#本程序由高端设计编写，需要引用或者有建议请联系邮箱1481407566@qq.com#本程序模拟二代测序后的DNA碎片拼接过程，使用通常的暴风(brute force)算法耗费较多计算机算力#本程序使用欧拉回路算法加以个人改进，意图提供有竞争力的运算速度",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
