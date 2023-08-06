import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='motion_master_proto',
    version='3.0.0a1',
    author='Synapticon GmbH',
    author_email='support@synapticon.com',
    description="Protobuf API for the Synapticon Motion Master",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/synapticon/motion-master-proto",
    packages=setuptools.find_packages(),
    install_requires=['protobuf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
