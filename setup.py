from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-ai-tools",
    version="0.1.0",
    author="Mik",
    author_email="workwithme@mik.sh",
    url="https://github.com/mik1337/git-ai-tools",
    description="A collection of AI-powered Git tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "gitpython>=3.1.42",
        "click>=8.1.7",
        "requests>=2.31.0"
    ],
    entry_points={
        "console_scripts": [
            "git-ai=git_ai_tools.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 