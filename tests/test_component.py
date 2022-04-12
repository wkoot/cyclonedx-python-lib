# encoding: utf-8

# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

from os.path import dirname, join
from unittest import TestCase

from data import (
    get_component_setuptools_simple,
    get_component_setuptools_simple_no_version,
    get_component_toml_with_hashes_with_references,
)

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component

FIXTURES_DIRECTORY = 'fixtures/xml/1.4'


class TestComponent(TestCase):

    def test_purl_correct(self) -> None:
        self.assertEqual(
            PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ),
            get_component_setuptools_simple().purl
        )

    def test_purl_incorrect_version(self) -> None:
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.1'
        )
        self.assertNotEqual(
            str(purl),
            str(get_component_setuptools_simple().purl)
        )
        self.assertEqual(purl.type, 'pypi')
        self.assertEqual(purl.name, 'setuptools')
        self.assertEqual(purl.version, '50.3.1')

    def test_purl_incorrect_name(self) -> None:
        purl = PackageURL(
            type='pypi', name='setuptoolz', version='50.3.2', qualifiers='extension=tar.gz'
        )
        self.assertNotEqual(
            str(purl),
            str(get_component_setuptools_simple().purl)
        )
        self.assertEqual(purl.type, 'pypi')
        self.assertEqual(purl.name, 'setuptoolz')
        self.assertEqual(purl.version, '50.3.2')
        self.assertEqual(purl.qualifiers, {'extension': 'tar.gz'})

    def test_from_file_with_path_for_bom(self) -> None:
        test_file = join(dirname(__file__), FIXTURES_DIRECTORY, 'bom_setuptools.xml')
        c = Component.for_file(absolute_file_path=test_file, path_for_bom='fixtures/bom_setuptools.xml')
        self.assertEqual(c.name, 'fixtures/bom_setuptools.xml')
        self.assertEqual(c.version, '0.0.0-38165abddb68')
        purl = PackageURL(
            type='generic', name='fixtures/bom_setuptools.xml', version='0.0.0-38165abddb68'
        )
        self.assertEqual(c.purl, purl)
        self.assertEqual(len(c.hashes), 1)

    def test_has_component_1(self) -> None:
        bom = Bom()
        bom.components.update([get_component_setuptools_simple(), get_component_setuptools_simple_no_version()])
        self.assertEqual(len(bom.components), 2)
        self.assertTrue(bom.has_component(component=get_component_setuptools_simple_no_version()))
        self.assertIsNot(get_component_setuptools_simple(), get_component_setuptools_simple_no_version())
