from setuptools import setup 

setup(
    name="CCMetagen",
    version="1.2",
    url="https://github.com/vrmarcelino/CCMetagen",
    description="Microbiome classification pipeline",
    license="GPL-3.0",
    keywords="Metagenomics Classifier",
    classifiers=[
        'Development Status :: 5 - Alpha',
        'License :: OSI Approved :: GPL',
        'Programming Language :: Python :: 3.6'
        ],
    install_requires=['pandas', 'ete3'],
    packages=['ccmetagen'],
    scripts=['tools/CCMetagen.py', 'tools/CCMetagen_merge.py']
)
