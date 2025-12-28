from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mrwa",
    version="1.0.0",
    author="MRWA Team",
    description="Marathon Research & Workflow Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "flask-socketio>=5.3.5",
        "python-socketio>=5.10.0",
        "aiohttp>=3.9.1",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.1",
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
        ],
    },
)
