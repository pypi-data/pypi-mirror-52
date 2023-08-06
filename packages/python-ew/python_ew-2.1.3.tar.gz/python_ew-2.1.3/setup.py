import os
import subprocess
import sys

from setuptools import setup, Extension
from distutils.command.build import build


min_version = (3, 6)

if sys.version_info < min_version:
    error = """
Python-EW requires Python version {0} or above.
This may be due to an out of date pip.
Make sure you have pip >= 9.0.1.
""".format('.'.join(str(n) for n in min_version)),
    sys.exit(error)

EW_HOME = os.environ.get('EW_HOME', None)
if EW_HOME:
    EW_LIBS = os.path.join(EW_HOME, 'lib')
    if not os.path.exists(EW_LIBS):
        test_dir = os.path.join(EW_HOME, 'earthworm_7.9', 'lib')
        if os.path.exists(test_dir):
            EW_LIBS = test_dir
        else:
            EW_LIBS = None
    EW_INCLUDES = os.path.join(EW_HOME, 'include')
    if not os.path.exists(EW_INCLUDES):
        test_dir = os.path.join(EW_HOME, 'earthworm_7.9', 'include')
        if os.path.exists(test_dir):
            EW_INCLUDES = test_dir
        else:
            EW_INCLUDES = None
else:
    EW_LIBS = None
    EW_INCLUDES = None

setup_py_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
RING_ACCESS_DIR = os.path.join(setup_py_dir, 'ring_access')


class CustomBuild(build):

    def check(self):
        """
        Ensure our build environment is set up properly before beginning.
        """
        if not EW_HOME:
            error = """
The Python-EW build process requires the EW_HOME environment
variable to be properly set.  This variable is not in your
environment.
"""
            sys.exit(error)

        if not EW_LIBS:
            error = """
The EW_HOME environment variable is set to {0} but we could not find a "lib" subfolder.  We tried: {}. We need the .o
files from the Earthworm build so that we can properly link our C extensions.
""".format(EW_HOME, ", ".join(os.path.join(EW_HOME, 'lib'), os.path.join(EW_HOME, 'earthworm_7.9', 'lib')))
            sys.exit(error)

        if not EW_INCLUDES:
            error = """
The EW_HOME environment variable is set to {0} but we could not find a "include" subfolder.  We tried: {}. We need
the .h files from the Earthworm build so that we can properly compile our C extensions.
""".format(EW_HOME, ", ".join(os.path.join(EW_HOME, 'include'), os.path.join(EW_HOME, 'earthworm_7.9', 'include')))
            sys.exit(error)

    def run(self):
        self.check()
        print("Building the ring_access interface code ...")
        try:
            subprocess.run(
                "make build EW_INCLUDE={} EW_LIB={}".format(EW_INCLUDES, EW_LIBS),
                shell=True,
                cwd=RING_ACCESS_DIR,
                check=True
            )
        except subprocess.CalledProcessError as err:
            print("\n\nring_access build failed:")
            print("-" * 40)
            print(err.stdout)
            print(err.stderr)
            sys.exit(err.returncode)
        super().run()


tracebuf2_module = Extension(
    name='python_ew.tracebuf2.tracebuf2module',
    sources=['python_ew/tracebuf2/tracebuf2module.c'],
    include_dirs=[EW_INCLUDES, RING_ACCESS_DIR],
    library_dirs=[EW_LIBS, RING_ACCESS_DIR],
    extra_objects=[
        '%s/ringwriter.o' % RING_ACCESS_DIR,
        '%s/ringreader.o' % RING_ACCESS_DIR,
        '%s/transport.o' % EW_LIBS,
        '%s/getutil.o' % EW_LIBS,
        '%s/kom.o' % EW_LIBS,
        '%s/sleep_ew.o' % EW_LIBS,
        '%s/logit.o' % EW_LIBS,
        '%s/time_ew.o' % EW_LIBS,
        '%s/swap.o' % EW_LIBS
    ],
    extra_compile_args=[
        '-fPIC',
        '-m64',
        '-Dlinux',
        '-D_LINUX',
        '-D_INTEL',
        '-D_USE_SCHED',
        '-D_USE_PTHREADS',
        '-D_USE_TERMIOS'
    ],
    extra_link_args=[
        '-lm',
        '-lpthread'
    ]
)


status_module = Extension(
    name='python_ew.status.statusmodule',
    sources=['python_ew/status/statusmodule.c'],
    include_dirs=[EW_INCLUDES, RING_ACCESS_DIR],
    library_dirs=[EW_LIBS, RING_ACCESS_DIR],
    extra_objects=[
        '%s/ringwriter.o' % RING_ACCESS_DIR,
        '%s/ringreader.o' % RING_ACCESS_DIR,
        '%s/transport.o' % EW_LIBS,
        '%s/getutil.o' % EW_LIBS,
        '%s/kom.o' % EW_LIBS,
        '%s/sleep_ew.o' % EW_LIBS,
        '%s/logit.o' % EW_LIBS,
        '%s/time_ew.o' % EW_LIBS,
        '%s/swap.o' % EW_LIBS
    ],
    extra_compile_args=[
        '-fPIC',
        '-m64',
        '-Dlinux',
        '-D_LINUX',
        '-D_INTEL',
        '-D_USE_SCHED',
        '-D_USE_PTHREADS',
        '-D_USE_TERMIOS'
    ],
    extra_link_args=[
        '-lm',
        '-lpthread'
    ]
)


heartbeat_module = Extension(
    name='python_ew.heartbeat.heartbeatmodule',
    sources=['python_ew/heartbeat/heartbeatmodule.c'],
    include_dirs=[EW_INCLUDES, RING_ACCESS_DIR],
    library_dirs=[EW_LIBS, RING_ACCESS_DIR],
    extra_objects=[
        '%s/ringwriter.o' % RING_ACCESS_DIR,
        '%s/ringreader.o' % RING_ACCESS_DIR,
        '%s/transport.o' % EW_LIBS,
        '%s/getutil.o' % EW_LIBS,
        '%s/kom.o' % EW_LIBS,
        '%s/sleep_ew.o' % EW_LIBS,
        '%s/logit.o' % EW_LIBS,
        '%s/time_ew.o' % EW_LIBS,
        '%s/swap.o' % EW_LIBS
    ],
    extra_compile_args=[
        '-fPIC',
        '-m64',
        '-Dlinux',
        '-D_LINUX',
        '-D_INTEL',
        '-D_USE_SCHED',
        '-D_USE_PTHREADS',
        '-D_USE_TERMIOS'
    ],
    extra_link_args=[
        '-lm',
        '-lpthread'
    ]
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python_ew',
    version='2.1.3',
    author_email='imss-ads-staff@caltech.edu',
    author="Caltech IMSS ADS",
    url='https://github.com/caltechads/python-ew',
    description='Allow reading from and writing to Earthworm shared memory ring buffers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['python_ew', 'python_ew.heartbeat', 'python_ew.status', 'python_ew.tracebuf2'],
    project_urls={
        'Home Page': 'https://github.com/caltechads/python-ew',
        'Bug Tracker': 'https://github.com/caltechads/python-ew/issues',
        'Documentation': 'https://github.com/caltechads/python-ew',
    },
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    ext_modules=[
        tracebuf2_module,
        status_module,
        heartbeat_module
    ],
    cmdclass={
        'build': CustomBuild
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
)
