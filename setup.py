from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="saludtotal",
    version="1.0.0",
    author="SaludTotal Development Team",
    author_email="info@saludtotal.com",
    description="Sistema de gestión de pacientes para la clínica SaludTotal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saludtotal/sistema-gestion-pacientes",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "saludtotal=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
