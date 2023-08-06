import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="aime_text_postprocessing", version="0.0.4", author="TrinhQuan", author_email="quantv@aimesoft.com",
                 description="Base module for human detection", long_description=long_description,
                 url='https://github.com/jarklee/aime_text_postprocessing',
                 download_url='https://github.com/jarklee/aime_text_postprocessing/releases/download/0.0.4/aime_text_postprocessing-0.0.4.tar.gz',
                 install_requires=['romkan==0.2.1', 'mecab-python3==0.996.2', 'chardet==3.0.4'], long_description_content_type="text/plain",
                 packages=setuptools.find_packages(),
                 classifiers=["Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7",
                              "License :: OSI Approved :: MIT License"], )
