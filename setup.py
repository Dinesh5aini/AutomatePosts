from setuptools import setup, find_packages
from typing import List

def get_requirements(path: str) -> List[str]:
    with open(path, 'r') as file:
        requirements = [req.replace('\n', '') for req in file.readlines()]
        
    if '-e .' in requirements:
        requirements.remove('-e .')
    return requirements


setup(
    name='AutomatePosts',
    version='0.0.1',
    author='Dinesh',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)