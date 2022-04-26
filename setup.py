import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='water_phantom_control',
    version='0.1',
    description='Control software for electro cylinder and stepper motors of the water phantom',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sebastian Schmidt',
    author_email='schm.seb@gmail.com',
    url="https://github.com/dosepix/water_phantom_control",
    project_urls={
        "Bug Tracker": "https://github.com/dosepix/water_phantom_control/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license='GNU GPLv3',
    packages=['water_phantom_control'],
    install_requires=[
        'pyserial',
        'pytrinamic @ git+https://github.com/trinamic/PyTrinamic.git@feature_feature_hierarchy_v2',
    ]
)
