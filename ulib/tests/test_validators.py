import socket
import json

from .. import tools
import ulib.tools.tests # pylint: disable=W0611
import ulib.tools.pep8

from .. import validators
import ulib.validators.fs
import ulib.validators.unix
import ulib.validators.common
import ulib.validators.extra
import ulib.validators.network
import ulib.validators.python


##### Public classes #####
class TestValidatorsUnix(tools.tests.TestValidatorsCase) :
    def test_valid_user_name(self) :
        self.checkValidator(
            validators.unix.validUserName,
            (
                ("glados",    "glados"),
                ("test",      "test"),
                ("_",         "_"),
                ("_foo_bar_", "_foo_bar_"),
            ),
            ("-molestia", "te~st", "-", "-foo_bar", "", None),
        )

    def test_valid_group_name(self) :
        self.checkValidator(
            validators.unix.validGroupName,
            (
                ("glados",    "glados"),
                ("test",      "test"),
                ("_",         "_"),
                ("_foo_bar_", "_foo_bar_"),
            ),
            ("-molestia", "te~st", "-", "-foo_bar", "", None),
        )

class TestValidatorsFs(tools.tests.TestValidatorsCase) :
    def test_valid_accessible_path(self) :
        self.checkValidator(
            validators.fs.validAccessiblePath,
            (
                ("/root", "/root"),
                (".", "."),
            ),
            ("/C:", "", None),
        )

    def test_valid_file_name(self) :
        self.checkValidator(
            validators.fs.validFileName,
            (
                ("test",       "test"),
                ("test test [test] #test$", "test test [test] #test$"),
                (".test",      ".test"),
                ("..test",     "..test"),
                ("..тест..",   "..тест.."),
                ("..те\\ст..", "..те\\ст.."),
                (".....",      "....."),
                (".....txt",   ".....txt"),
                ("test/",      "test"),
            ),
            (".", "..", "/test", "../test", "./.", "../.", "./..", "../.."),
        )

class TestValidatorsCommon(tools.tests.TestValidatorsCase) :
    def test_valid_bool(self) :
        self.checkValidator(
            validators.common.validBool,
            (
                ("1",     True),
                ("true",  True),
                ("yes",   True),
                (1,       True),
                (True,    True),
                ("0",     False),
                ("false", False),
                ("no",    False),
                (0,       False),
                (False,   False),
            ),
            ("x", "", None, -1),
        )

    def test_valid_number(self) :
        self.checkValidator(
            validators.common.validNumber,
            (
                ("1",    1),
                ("-1",   -1),
                (1,      1),
                (-1,     -1),
                (0,      0),
                (100500, 100500),
            ),
            ("1x", "", None, 100500.0), # By default - int
        )

    def test_valid_number_min_max(self) :
        self.checkValidator(
            lambda arg : validators.common.validNumber(arg, -5, 5),
            (
                (-5,   -5),
                (0,    0),
                (5,    5),
                ("-5", -5),
                ("0",  0),
                ("5",  5),
            ),
            (-6, 6, "-6", "6"),
        )

    def test_valid_range(self) :
        self.checkValidator(
            lambda arg : validators.common.validRange(arg, (1, 3, "5")),
            (
                (1,   1),
                (3,   3),
                ("5", "5"),
            ),
            ("1", "3", 5, ""),
        )

    def test_valid_string_list(self) :
        self.assertValidatorError(validators.common.validStringList, None)
        test_list = list(map(str, list(range(10))))
        self.assertEqual(validators.common.validStringList(", \t".join(test_list)), test_list)
        self.assertEqual(validators.common.validStringList(test_list), test_list)

    def test_valid_empty(self) :
        self.assertEqual(validators.common.validEmpty(""), None)
        self.assertEqual(validators.common.validEmpty(None), None)
        self.assertNotEqual(validators.common.validEmpty("x"), None)

    # def test_valid_maybe_empty(self) : pass

class TestValidatorsExtra(tools.tests.TestValidatorsCase) :
    def test_valid_json(self) :
        valid_json = """{"1": 1, "3": ["a", "b", "c"], "2": 2}"""
        self.assertEqual(json.loads(validators.extra.validJson(valid_json)), json.loads(valid_json))
        self.assertValidatorError(validators.extra.validJson, "{1:1}")

    def test_valid_hex_string(self) :
        valid_hex_string1 = "d41d8cd98f00b204e9800998ecf8427e"
        valid_hex_string2 = valid_hex_string1.upper()
        invalid_hex_string = "d41d8cd98f00b204e9800998ecf8427ex"
        self.checkValidator(
            validators.extra.validHexString,
            (
                (valid_hex_string1, valid_hex_string1),
                (valid_hex_string2, valid_hex_string2),
            ),
            (invalid_hex_string, "", None),
        )

    def test_valid_uuid(self) :
        valid_uuid1 = "550e8400-e29b-41d4-a716-446655440000"
        valid_uuid2 = "00000000-0000-0000-C000-000000000046"
        invalid_uuid1 = "550e8400-e29b-41d4-a716-44665544"
        invalid_uuid2 = "ffffuuuu-0000-0000-C000-000000000046"
        self.checkValidator(
            validators.extra.validUuid,
            (
                (valid_uuid1, valid_uuid1),
                (valid_uuid2, valid_uuid2),
            ),
            (invalid_uuid1, invalid_uuid2, "", None),
        )

class TestValidatorsNetwork(tools.tests.TestValidatorsCase) :
    def test_valid_rfc_host(self) :
        self.checkValidator(
            validators.network.validRfcHost,
            (
                ("yandex.ru",  "yandex.ru"),
                ("foobar",     "foobar"),
                ("foo-bar.ru", "foo-bar.ru"),
                ("z0r.de",     "z0r.de"),
                ("11.ru",      "11.ru"),
            ),
            ("foo_bar.ru", "", None),
        )

    def test_valid_ip_address(self) :
        self.checkValidator(
            validators.network.validIpAddress,
            (
                ("127.0.0.1",      ("127.0.0.1",      socket.AF_INET)),
                ("8.8.8.8",        ("8.8.8.8",        socket.AF_INET)),
                ("::1",            ("::1",            socket.AF_INET6)),
                ("2001:500:2f::f", ("2001:500:2f::f", socket.AF_INET6)),
            ),
            ("1", "1.1.1.", ":", "", None),
        )

    def test_valid_ip_or_host(self) :
        self.checkValidator(
            validators.network.validIpOrHost,
            (
                ("yandex.ru",      ("yandex.ru",      None)),
                ("foobar",         ("foobar",         None)),
                ("foo-bar.ru",     ("foo-bar.ru",     None)),
                ("127.0.0.1",      ("127.0.0.1",      socket.AF_INET)),
                ("8.8.8.8",        ("8.8.8.8",        socket.AF_INET)),
                ("::1",            ("::1",            socket.AF_INET6)),
                ("2001:500:2f::f", ("2001:500:2f::f", socket.AF_INET6)),
            ),
            ("foo_bar.ru", "1.1.1.", ":", "", None),
        )

    def test_valid_port(self) :
        self.checkValidator(
            validators.network.validPort,
            (
                ("0",   0),
                (0,     0),
                (22,    22),
                (443,   443),
                (65535, 65535),
            ),
            ("x", 65536, "", None),
        )

    def test_valid_bsd_address(self) :
        self.checkValidator(
            validators.network.validBsdAddress,
            (
                ("yandex.ru.80",    ("yandex.ru.80",    ("yandex.ru",    80))),
                ("canterlot.eq.80", ("canterlot.eq.80", ("canterlot.eq", 80))),
            ),
            ("yandex.ru.65536", "", None),
        )

class TestValidatorsPython(tools.tests.TestValidatorsCase) :
    def test_valid_object_name(self) :
        self.checkValidator(
            validators.python.validObjectName,
            (
                ("__test",         "__test"),
                ("__test__",       "__test__"),
                ("Object_Name",    "Object_Name"),
                ("objectName123",  "objectName123"),
                ("_",              "_"),
            ),
            (".object", "123object", "/object"),
        )


##### PEP8 #####
tools.pep8.setupAliases()

