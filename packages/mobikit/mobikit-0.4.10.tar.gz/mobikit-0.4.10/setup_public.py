from setuptools import setup, find_packages
from setup_base import base_kwargs

setup(
    **base_kwargs,
    packages=find_packages(
        include=["mobikit", "mobikit.config", "mobikit.feeds", "mobikit.feeds.*"]
    ),
    zip_safe=False,
    include_package_data=True,
    install_requires=["pandas>=0.24.2", "requests>=2.21.0", "mobikit-utils~=0.1.0"],
)
