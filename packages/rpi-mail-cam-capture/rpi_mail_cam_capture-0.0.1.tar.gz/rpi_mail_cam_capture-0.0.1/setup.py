import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpi_mail_cam_capture",
    version="0.0.1",
    author="sahil panindre",
    author_email="sahil11panindre@gmail.com",
    description="You can capture through raspberry pi camera and mail the image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ultimus11/email_via_raspberry_pi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)