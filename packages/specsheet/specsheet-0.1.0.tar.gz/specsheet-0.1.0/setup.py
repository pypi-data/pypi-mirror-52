from setuptools import setup

import versioneer

with open("README.rst", "rb") as f:
    readme = f.read().decode("utf-8")

setup(
    name="specsheet",
    packages=["specsheet"],
    entry_points={
        "console_scripts": ['specsheet = specsheet.command:main']
    },
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Command to produce navigable documentation from Gherkin feature files.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Edd Armitage",
    author_email="edward.armitage@gmail.com",
    url="https://gitlab.com/eddarmitage/spec-sheet",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.4',
    install_requires=["docopt"],
    setup_requires=[],
    tests_require=["pyfakefs", "nose2", "behave"],
)
