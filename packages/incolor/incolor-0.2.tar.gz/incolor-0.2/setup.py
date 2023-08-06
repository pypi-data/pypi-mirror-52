from setuptools import setup, find_packages
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).parent


def readme() -> str:
    readme = REPO_ROOT / 'README.md'
    if readme.exists():
        return readme.read_text()
    return ''


def requirements() -> List[str]:
    requirements = REPO_ROOT / 'requirements.txt'
    if requirements.exists():
        r = requirements.read_text()
        return r.split()
    return []


setup(name='incolor',
      version='0.2',
      description='Add color codes to strings or print in color.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
      ],
      keywords='color',
      url='https://github.com/filwie/incolor',
      author='Filip Wiechec',
      author_email='filip.wiechec@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=requirements(),
      include_package_data=True,
      python_requires='>=3.6',
      zip_safe=False)
