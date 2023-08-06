from setuptools import setup

with open("README.md") as f:
    description = f.read()

setup(
    name='remoteunrar',
    version='0.9.2',
    author='M.Furkan',
    author_email='furkan@telegmail.com',
    py_modules=['remoteunrar'],
    url='https://github.com/muhammedfurkan/python-remoteunrar',
    license='MIT',
    description='Access rar file content hosted remotely without downloading the full file.',
    long_description=description,
    long_description_content_type="text/markdown",
    install_requires=["requests", "tabulate"],
    scripts=['bin/remoteunrar'],
    test_suite='test_remoteunrar',
    classifiers=(
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ),
)