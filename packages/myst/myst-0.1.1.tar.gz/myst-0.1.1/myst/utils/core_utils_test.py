import datetime
import os
import shutil
import tempfile
import unittest
from collections import OrderedDict

import mock
import pytz

from myst.utils.core_utils import build_resource_url
from myst.utils.core_utils import encode_url
from myst.utils.core_utils import format_repr
from myst.utils.core_utils import format_timestamp
from myst.utils.core_utils import get_package_version
from myst.utils.core_utils import get_pkg_resource_path
from myst.utils.core_utils import get_user_agent
from myst.utils.core_utils import make_directory


class CoreUtilsTest(unittest.TestCase):
    def test_get_package_version(self):
        # Note that you'll need to bump this version before you release a new version of this package!
        self.assertEqual(get_package_version(), "0.1.1")

    @mock.patch("myst.utils.core_utils.get_package_version")
    def test_get_user_agent(self, get_package_version_patch):
        # Test with different package and api versions to make sure we are constructing the `User-Agent` string
        # properly.
        for myst_api_version, myst_package_version, expected_user_agent_string in [
            ("v1alpha1", "0.1.1", "Myst/v1alpha1 PythonBindings/0.1.1"),
            ("v1", "0.2.0", "Myst/v1 PythonBindings/0.2.0"),
        ]:
            get_package_version_patch.return_value = myst_package_version
            with mock.patch("myst.api_version", myst_api_version):
                self.assertEqual(get_user_agent(), expected_user_agent_string)

    def test_get_pkg_resource_path(self):
        # We're using these tests to not only test that `get_pkg_resource_path` works but also to make sure that the
        # expected package resources exist. Any time a package resource is added, add a corresponding test here to
        # test that we can locate it.
        self.assertTrue(os.path.exists(get_pkg_resource_path()))
        self.assertTrue(os.path.exists(get_pkg_resource_path("google_oauth_client_not_so_secret.json")))

    def test_build_resource_url(self):
        self.assertEqual(build_resource_url(resource_name="resource"), "https://api.myst.ai/v1alpha1/resource")
        self.assertEqual(
            build_resource_url(resource_name="resource", resource_uuid="4b84d6c0-b7c0-450c-b836-9f0402ad681c"),
            "https://api.myst.ai/v1alpha1/resource/4b84d6c0-b7c0-450c-b836-9f0402ad681c",
        )

    def test_encode_url(self):
        self.assertEqual(
            encode_url(base_url="myst.ai", params=[("key_1", "value_1"), ("key_2", "value_2")]),
            "myst.ai?key_1=value_1&key_2=value_2",
        )

    def test_format_timestamp(self):
        utc_timezone = pytz.timezone("UTC")
        denver_timezone = pytz.timezone("America/Denver")

        # Test that by default, we assume timezone-naive timestamps are in UTC.
        self.assertEqual(format_timestamp(timestamp=datetime.datetime(2018, 1, 1, 12, 42, 12)), "2018-01-01T12:42:12Z")

        # Test that we format timezone-aware timestamps according to their timezones.
        self.assertEqual(
            format_timestamp(timestamp=utc_timezone.localize(datetime.datetime(2018, 1, 1, 12, 42, 12))),
            "2018-01-01T12:42:12Z",
        )
        self.assertEqual(
            format_timestamp(timestamp=denver_timezone.localize(datetime.datetime(2018, 1, 1, 12, 42, 12))),
            "2018-01-01T12:42:12-07:00",
        )

    def test_make_directory(self):
        # Test that we can make directory.
        temp_dir = tempfile.mktemp()
        make_directory(temp_dir)

        self.assertTrue(os.path.exists(temp_dir))
        self.assertTrue(os.path.isdir(temp_dir))

        # Clean up.
        shutil.rmtree(temp_dir)

        # Test that we can make nested directories.
        temp_nested_dir = tempfile.mktemp(dir="/tmp/nested")
        make_directory(temp_nested_dir)

        self.assertTrue(os.path.exists(temp_nested_dir))
        self.assertTrue(os.path.isdir(temp_nested_dir))

        # Clean up.
        shutil.rmtree(temp_nested_dir)

    def test_format_repr(self):
        self.assertEqual(format_repr(class_name="class_name"), "<class_name>")
        self.assertEqual(
            format_repr(
                class_name="class_name",
                class_properties=OrderedDict([("property_1", "value_1"), ("property_2", "value_2")]),
            ),
            "<class_name: property_1=value_1, property_2=value_2>",
        )
