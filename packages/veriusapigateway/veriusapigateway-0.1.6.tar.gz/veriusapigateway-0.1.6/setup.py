import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="veriusapigateway",
    version="0.1.6",
    author="Verius Technologhy",
    author_email="info@verius.ai",
    description="API Gateway for accessing Verius Web Services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/veriusai/veriusapigateway/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
