import setuptools
try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

with open("README.md", 'r') as fh:
    long_description = fh.read()

install_reqs = parse_requirements('requirements.txt', session=False)

setuptools.setup(
    name="rectif-ai",
    version="0.1",
    author="Sushil Thapa",
    author_email="mailsushilthapa@gmail.com",
    description="Rectif.ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sushil-Thapa/PyTorch-Hackathon-2019.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[str(ir.req) for ir in install_reqs if ir.match_markers()],
)