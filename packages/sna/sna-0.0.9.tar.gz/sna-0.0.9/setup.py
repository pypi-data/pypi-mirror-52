import setuptools

# get version
with open("sna/version", "r") as vf:
    version_ = vf.read()
    version_ = str(version_.split('"')[1])
# increment minor version
with open("sna/version", "w") as vf:
    v = [int(i) for i in version_.split(".")]
    v[2] = v[2] + 1
    new_version = ".".join([str(i) for i in v])
    vf.write('VERSION = "{}"'.format(new_version))

# get long description
long_description = ""
with open("README.md", "r") as fh:
    long_description += fh.read()


long_description += """## Sample Usage\n"""
long_description += """you can see the code samples\n"""

# get sample usage
with open("sna/sample.txt", "r") as fh:
    long_description += """\n```\nsample.txt\n```\n"""
    long_description += """```\n"""
    long_description += fh.read()
    long_description += """\n```"""

# get sample usage
with open("sna/sample.py", "r") as fh:
    long_description += """\n```\nsample.py\n```\n"""
    long_description += """\n```python3\n"""
    long_description += fh.read()
    long_description += """\n```\n"""


setuptools.setup(
    name="sna",
    version=version_,
    author="Erdem Aybek",
    author_email="eaybek@gmail.com",
    description=" ".join(["Search N Act"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eaybek/sna",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 1 - Planning",
    ],
    python_requires=">=3.6",
)
