# Copyright (c) 2018 Shoppimon LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

with open('VERSION') as f:
    version = f.read()

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='authoritah',
    version=version,
    description='Lightweight, framework agnostic, context based RBAC authorization library',
    author='Shahar Evron',
    author_email='shahar@shoppimon.com',
    url='https://github.com/shoppimon/authoritah',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    python_requires='>=3.5.0',
    packages=find_packages(),
    install_requires=['six'],
    tests_require=['pytest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
