import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    data_files=['MLmetagenomics/abundance.txt'],
    name="MLmetagenomics",
    version="0.0.5",
    author="DUAN GAO",
    author_email="1481407566@qq.com",
    description="#本程序由高端设计编写，需要引用或者有建议请联系邮箱1481407566@qq.com本程序数据源为4000多名健康与患者的混合宏基因组测序结果，样本体内的微生物数量已经换算成相对百分比，总和接近1,使用4种机器学习的分类方法，线性回归，神经网络，SVM，random forest 建立模型，对新样本预测其患病与否",
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
