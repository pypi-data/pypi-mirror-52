import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neuralnets",
    version="0.6",
    author="Joris Roels",
    author_email="jorisb.roels@ugent.be",
    description="A library, based on PyTorch, that implements basic neural network algorithms and useful functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JorisRoels/neuralnets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "augmentation",
        "torch",
        "torchvision",
        "future",
        "tensorboard",
        "numpy",
        "tifffile",
        "h5py",
        "scikit-image",
        "opencv-python"
    ]
)