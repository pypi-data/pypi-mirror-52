#!/usr/bin/env python3

# Copyright (c) 2019 Kai Hoewelmeyer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
from check_copyright.filter_files import matching_files
from configparser import ConfigParser

CONFIG_FILE = ".copyright.cfg"
WHITESPACE_TRANSLATION = {
        ord('#'): None,
        ord('/'): None,
        ord('*'): None,
}


def contains_license(license_text, source_code):
    """
    Check if license_text is contained in source_code.
    The comparison ignores linebreaks and source code comment characters.
    """
    stripped_license = canonicalize_whitespace(license_text)
    stripped_source = canonicalize_whitespace(source_code)
    return stripped_license in stripped_source

def canonicalize_whitespace(text):
    """
    Remove comment markers and superfluous whitespace.
    E.g., 'test   test # test' -> 'test test test'
    """
    no_comment_markers = text.translate(WHITESPACE_TRANSLATION)
    collapse_whitespace = ' '.join(no_comment_markers.split())
    return collapse_whitespace

def check_copyright(filename, license):
    with open(filename) as f:
        head_file = f.read(len(license) + 100)
        if not contains_license(license, head_file):
            print("%s is missing copyright header" % filename, file=sys.stderr)
            return False
        return True


def read_license(license_file):
    if not os.path.exists(license_file):
        print("Cannot find {}".format(license_file), file=sys.stderr)
        sys.exit(1)

    license = open(license_file).read()
    return license


def get_config_files():
    if not os.path.exists(CONFIG_FILE):
        return []

    return [CONFIG_FILE]


def read_config(config_files):
    """ Read config from provided files, use default values if not there. """

    config = ConfigParser()
    config['check-copyright'] = {
             'patterns': '*.cpp, *.h, *.py, *.sh',
             'exclude': '',
             'license_file': 'LICENSE'}
    config.read(config_files)

    section = config['check-copyright']
    check_extensions = [x.strip() for x in section['patterns'].split(',')]
    if section['exclude'] != '':
        exclude_patterns = [x.strip() for x in section['exclude'].split(',')]
    else:
        exclude_patterns = []
    license_file = section['license_file']

    return {'extensions': check_extensions,
            'exclude_patterns': exclude_patterns,
            'license_file': license_file}


def check_all_files():
    config = read_config(CONFIG_FILE)
    license = read_license(config['license_file'])
    files = matching_files(".", config['extensions'], config['exclude_patterns'])
    if not all([check_copyright(f, license) for f in files]):
        print("Not all files have correct copyrights", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    check_all_files()

