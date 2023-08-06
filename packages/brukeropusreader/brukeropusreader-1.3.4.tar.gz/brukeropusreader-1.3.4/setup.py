from distutils.core import setup


setup(
    name="brukeropusreader",
    version="1.3.4",
    description="Bruker OPUS File Reader",
    author="QED",
    author_email="brukeropusreader-dev@qed.ai",
    packages=["brukeropusreader"],
    install_requires=["numpy>=1.13.3", "scipy>=0.19.1"],
    license="GPLv3",
    url="https://github.com/qedsoftware/brukeropusreader",
)
