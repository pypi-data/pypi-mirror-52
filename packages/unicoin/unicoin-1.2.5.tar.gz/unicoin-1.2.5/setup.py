import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unicoin",
    version="1.2.5",
    author="Gennady Shutko",
    author_email="Duzive30@gmail.com",
    description="UniCoin Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://vk.com/@florydev-dokumentaciya-k-modulu-unicoin",
    packages=setuptools.find_packages(),
    classifiers=[
    	"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)