from setuptools import setup

def load_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements

setup(
    name='np_ringbuffer',
    version='1.0.0',
    description='A module for ring buffer operations using NumPy backend',
    author='See Leung',
    author_email='sleung852@gmail.com',
    packages=['np_ringbuffer'],
    install_requires=load_requirements(),
)