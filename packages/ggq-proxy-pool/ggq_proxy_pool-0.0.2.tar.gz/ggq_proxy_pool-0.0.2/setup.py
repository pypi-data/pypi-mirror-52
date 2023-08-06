import setuptools

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ggq_proxy_pool",
    version="0.0.2",
    author="ggq",
    author_email="942490944@qq.com",
    description="爬虫代理IP池",
    long_description=long_description,
    long_description_context_type="text/markdown",
    url="https://github.com/ggqshr/proxy_pool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
