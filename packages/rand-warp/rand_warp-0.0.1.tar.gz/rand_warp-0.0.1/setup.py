from setuptools import setup

setup(
    name='rand_warp',
    version='0.0.1',
    author='xuguodong',
    author_email='xuguodong03@gmail.com',
    url='https://google.com',
    description='randomly warp an image',
    packages=['rand_warp'],
    install_requires=['numpy', 'scikit-image', 'opencv-python'],
    entry_points={}
)

