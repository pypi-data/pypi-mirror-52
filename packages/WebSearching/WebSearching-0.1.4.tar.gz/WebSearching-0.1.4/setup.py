# WebSearcher - Tools for conducting, collecting, and parsing web search
# Copyright (C) 2017-2019 Ronald E. Robertson <rer@ronalderobertson.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import setuptools

def get_readme_title(fp='README.md', delim='# ', stop_at=1):
    with open(fp, 'r') as infile:
        readme = [l.strip() for l in infile.read().split('\n')]
    selected = [l.replace('#', '') for l in readme if l.startswith(delim)][0]
    return selected

def get_readme_abstract(fp='README.md', delim='#', stop_at=1):
    with open(fp, 'r') as infile:
        readme = [l.strip() for l in infile.read().split('\n')]
    selected = [l.replace('#', '') for l in readme 
                if l.startswith(delim)][:stop_at]
    start, stop = selected[0], selected[-1]
    abstract = selected[start:stop]
    return ' '.join(abstract)

setuptools.setup(
    name='WebSearching',
    version='0.1.4',
    url='http://github.com/gitronald/WebSearcher',
    author='Ronald E. Robertson',
    author_email='rer@ccs.neu.edu',
    license='BSD-3-Clause',
    description=get_readme_title(),
    packages=setuptools.find_packages(),
    install_requires=['requests','lxml','bs4','brotli',
                      'tldextract','emoji','pandas'],
    python_requires='>=3.6'
)
