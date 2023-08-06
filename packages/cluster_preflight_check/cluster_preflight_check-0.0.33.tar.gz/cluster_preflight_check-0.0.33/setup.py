import setuptools

setuptools.setup(
    name="cluster_preflight_check",
    version="0.0.33",
    author="Xin Liang",
    author_email="XLiang@suse.com",
    url="https://github.com/liangxin1300/cluster_preflight_check.git",
    license="BSD",
    packages=setuptools.find_packages(),
    description="Tool for Standardize Testing of Basic Cluster Functionality",
    entry_points={
        'console_scripts': ['ha-cluster-preflight-check=cluster_preflight_check.main:main'],
    },
    classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: BSD License",
          "Operating System :: POSIX",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.1",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: System :: Clustering",
          "Topic :: System :: Networking",
          "Topic :: System :: Systems Administration",
      ]
)
