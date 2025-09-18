"""Setup script."""

from setuptools import setup, find_packages
from pudding import __version__

DESCRIPTION = """
Gelatin converts text to a structured format, such as XML, JSON or YAML.
""".strip()

# Run the setup.
setup(
    name="pudding",
    version=__version__,
    description="Transform text files to XML, JSON, or YAML",
    long_description=DESCRIPTION,
    author="Moritz Hille",
    author_email="moritz.hekxsler@gmail.com",
    package_dir={"pudding": "pudding"},
    packages=find_packages(),
    scripts=["scripts/pud"],
    python_requires=">=3.10",
    test_suite="tests",
    keywords=" ".join(
        [
            "pudding",
            "pud",
            "parser",
            "lexer",
            "xml",
            "json",
            "yaml",
            "generator",
            "syntax",
            "text",
            "transform",
        ]
    ),
    url="https://github.com/hekxsler/pudding",
    classifiers=[
        "Development Status :: 0 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML",
    ],
)
