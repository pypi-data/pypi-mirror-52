import codecs
import os
import re
from pathlib import Path

from setuptools import setup

with open("README.md") as f:
    readme_text = f.read()

with open("CHANGELOG.md") as f:
    changelog_text = f.read()

long_description = f"{readme_text}\n\n{changelog_text}"

package_dir = "src"
package = "pupil_pthreads_win"

package_data = [
    str(match.resolve())
    for match in (Path() / package_dir / package / "data").rglob("*")
    if match.is_file()
]

here = Path(__file__).parent


def read_version():
    path = here / "src" / "pupil_pthreads_win" / "__init__.py"
    with codecs.open(path, "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="pupil-pthreads-win",
    description="A precompiled version of pthreads-win.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=read_version(),
    url="https://github.com/pupil-labs/pupil-pthreads-win",
    license="MIT License",
    author="Pupil Labs GmbH",
    author_email="pypi@pupil-labs.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[package],
    package_dir={"": package_dir},
    package_data={package: package_data},
)
