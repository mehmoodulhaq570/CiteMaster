from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cite_master",  # Name of the package
    version="0.1.0",  # Version of the package
    author="Mehmood Ul Haq",  # Your name as the author
    author_email="mehmooulhaq1040@gmail.com",  # Your email
    description="A tool to automatically generate formatted citations from paper titles",  # Short description
    long_description=long_description,  # Long description from README
    long_description_content_type="text/markdown",  # Format of the README file
    url="https://github.com/mehmoodulhaq570/CiteMaster",  # URL to the project
    project_urls={
        "Documentation": "https://github.com/mehmoodulhaq570/CiteMaster#readme",
        "Source": "https://github.com/mehmoodulhaq570/CiteMaster",
        "Bug Tracker": "https://github.com/mehmoodulhaq570/CiteMaster/issues",
    },
    packages=find_packages(),  # Automatically find all packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum version of Python required
    install_requires=[  # List of dependencies for the package
        "requests>=2.25.1",
        "tqdm>=4.59.0",
        "beautifulsoup4>=4.9.3",  # If you're using BeautifulSoup for HTML parsing (adjust if different)
        "pandas>=1.2.4",  # If you're dealing with CSV files
    ],
    entry_points={  # Entry points to create command-line tools
        'console_scripts': [
            'cite-master=cite_master.main:main',  # Creates a CLI command 'cite-master'
        ],
    },
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    license="MIT",  # License for your package
)
