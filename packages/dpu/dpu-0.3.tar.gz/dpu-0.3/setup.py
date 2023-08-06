from distutils.core import setup

setup(
    name = "dpu",
    packages = ["dpu"],
    version = "0.3",
    license="bsd-3-clause",
    description = "Data preprocessing utilities",
    author = "Kivanc Yuksel",
    author_email = "kivanc.yuksel@yandex.com",
    url = "https://github.com/kivancyuksel/dpu.git",
    download_url = "https://github.com/kivancyuksel/dpu/archive/v0.3.tar.gz",
    keywords = ["Preprocessing", "Augmentation", "Image Processing"],
    install_requires=[
          "imgaug>=0.2.9",
          "numpy>=1.16.4",
          "opencv-contrib-python>=4.1.1",
          "pandas>=0.24.2",
      ],
    classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3.7",
    ],
)
