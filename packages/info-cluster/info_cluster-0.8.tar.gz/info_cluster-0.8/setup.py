'''we use this setup.py to build wheels of info-clustering package
this kind of installation is more flexible and maintainable than `cmake install`
you can only choose one of the two installation methods.
before running this file, make sure psp dynamic lib exists in build directory
'''
import os
import sys
import platform
from setuptools import setup, Extension
from Cython.Build import cythonize # pylint: disable=import-error

IS_CENTOS = sys.platform == 'linux' and platform.platform().find('centos') >= 0

with open('README.md') as fh:
    LONG_DESCRIPTION = fh.read()

#pylint: disable=missing-docstring

def find_all_cpp(given_dir):
    cpp_list = []
    for i in os.listdir(given_dir):
        if i.find('cpp') > 0:
            cpp_list.append(os.path.join(given_dir, i))
    return cpp_list

def add_source_file(sourcefiles, cpp_file):
    if os.path.exists(cpp_file):
        sourcefiles.append(cpp_file)
    else:
        raise FileNotFoundError(cpp_file)

def set_up_cython_extension():
    extra_include_path = []
    extra_include_path.append(os.path.join(os.getcwd(), 'psp'))

    extra_lib_dir = []
    if sys.platform == 'win32':
        lemon_lib_name = 'lemon'
    elif sys.platform == 'linux' and not IS_CENTOS: # ubuntu 16.04
        lemon_lib_name = 'lemon'
    else:
        lemon_lib_name = 'emon'

    if os.environ.get('VCPKG_ROOT'):
        root_dir = os.environ['VCPKG_ROOT']
        triplet = os.environ.get('VCPKG_DEFAULT_TRIPLET', 'x64-windows')
        include_dir = os.path.join(root_dir, 'installed', triplet, 'include')
        if os.path.exists(include_dir):
            extra_include_path.append(include_dir)
        lib_dir = os.path.join(root_dir, 'installed', triplet, 'lib')
        if os.path.exists(lib_dir):
            extra_lib_dir.append(lib_dir)
    # collect library
    sourcefiles = ['pspartition.pyx']
    sourcefiles.extend(find_all_cpp(os.path.join(os.getcwd(), 'psp', 'psp')))
    set_file = os.path.join(os.getcwd(), 'psp', 'psp', 'set', 'set_stl.cpp')
    add_source_file(sourcefiles, set_file)
    thread_file = os.path.join(os.getcwd(), 'psp', 'psp',
                               'preflow', 'InterruptibleThread', 'InterruptibleThread.cpp')
    add_source_file(sourcefiles, thread_file)
    extra_compile_flags_list = []
    extra_link_flags_list = []
    if sys.platform != 'win32':
        extra_compile_flags_list.append('-std=c++14')
        extra_link_flags_list.append('-pthread')
    extensions = [
        Extension('pspartition', sourcefiles,
                  include_dirs=extra_include_path,
                  library_dirs=extra_lib_dir,
                  extra_compile_args=extra_compile_flags_list,
                  extra_link_args=extra_link_flags_list,
                  libraries=[lemon_lib_name]
                 )
    ]
    return cythonize(extensions)

EXT_MODULE_CLASS = set_up_cython_extension()

setup(
    name='pspartition',
    version='0.7.post2', # different with C++ lib version
    ext_modules=EXT_MODULE_CLASS,
    author="zhaofeng-shu33",
    author_email="616545598@qq.com",
    description="a hierachical clustering algorithm based on information theory",
    url="https://github.com/zhaofeng-shu33/principal_sequence_of_partition",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    license="Apache License Version 2.0",
)
