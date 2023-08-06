import pathlib

import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name='scrapyd_egg_checksum',
    version='0.1.2',
    author="Xiaodong Ye",
    author_email="470504024@qq.com",
    url='https://github.com/ChristianYeah/scrapyd-egg-checksum',
    description="Get the checksum of eggs in case of building distributed scrapy clusters",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["scrapyd_egg_checksum"],
    install_requires=[
        'scrapy',
        'scrapyd',
    ],
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
