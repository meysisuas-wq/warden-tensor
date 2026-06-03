from setuptools import setup, find_packages

setup(
    name="warden-tensor",
    version="1.0.0",
    description="Next-Generation Security Surveillance & Threat Detection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="WardenTensor Team",
    author_email="team@wardentensor.io",
    url="https://github.com/meysisuas-wq/warden-tensor",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.115.0", "uvicorn[standard]>=0.32.0", "pydantic>=2.10.0",
        "sqlalchemy>=2.0.35", "asyncpg>=0.30.0", "redis>=5.2.0",
        "torch>=2.5.0", "opencv-python-headless>=4.10.0",
    ],
)
