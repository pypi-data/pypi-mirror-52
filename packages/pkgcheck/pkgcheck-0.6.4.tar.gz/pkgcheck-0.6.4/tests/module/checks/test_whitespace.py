from pkgcheck.checks import whitespace

from .. import misc


class WhitespaceCheckTest(misc.ReportTestCase):
    """Various whitespace related test support."""

    check_kls = whitespace.WhitespaceCheck
    check = whitespace.WhitespaceCheck(None, None)


class TestWhitespaceFound(WhitespaceCheckTest):

    def test_leading(self):
        fake_pkg = misc.FakePkg("dev-util/diffball-0.5")
        fake_src = [
            "# This is our first fake ebuild\n",
            " # This line contains a leading whitespace\n",
            "# That's it for now\n",
        ]

        r = self.assertReport(self.check, [fake_pkg, fake_src])
        assert isinstance(r, whitespace.WhitespaceFound)
        assert r.lines == (2,)
        assert 'leading whitespace' in str(r)

    def test_trailing(self):
        fake_pkg = misc.FakePkg("dev-util/diffball-0.5")
        fake_src = [
            "# This is our first fake ebuild\n",
            "# This line contains a trailing whitespace \n",
            "# That's it for now\n",
        ]

        r = self.assertReport(self.check, [fake_pkg, fake_src])
        assert isinstance(r, whitespace.WhitespaceFound)
        assert r.lines == (2,)
        assert 'trailing whitespace' in str(r)


class TestWrongIndentFound(WhitespaceCheckTest):

    def test_it(self):
        fake_pkg = misc.FakePkg("dev-util/diffball-0.5")
        fake_src = [
            "# This is our first fake ebuild\n",
            "\t \tBad indentation\n",
            "# That's it for now\n",
        ]

        r = self.assertReport(self.check, [fake_pkg, fake_src])
        assert isinstance(r, whitespace.WrongIndentFound)
        assert r.lines == (2,)
        assert 'whitespace in indentation' in str(r)


class TestDoubleEmptyLine(WhitespaceCheckTest):

    def test_it(self):
        fake_pkg = misc.FakePkg("dev-util/diffball-0.5")
        fake_src = [
            "# This is our first fake ebuild\n",
            "\n",
            "\n",
            "# That's it for now\n",
        ]

        r = self.assertReport(self.check, [fake_pkg, fake_src])
        assert isinstance(r, whitespace.DoubleEmptyLine)
        assert r.lines == (3,)
        assert 'unneeded empty line' in str(r)


class TestNoNewLineOnEnd(WhitespaceCheckTest):

    def test_it(self):
        fake_pkg = misc.FakePkg("dev-util/diffball-0.5")
        fake_src = [
            "# This is our first fake ebuild\n",
            "# That's it for now",
        ]

        r = self.assertReport(self.check, [fake_pkg, fake_src])
        assert isinstance(r, whitespace.NoFinalNewline)
        assert 'lacks an ending newline' in str(r)


class TestTrailingNewLineOnEnd(WhitespaceCheckTest):

    def test_it(self):
        fake_pkg = misc.FakePkg("dev-util/diffball-0.5")
        fake_src = [
            "# This is our first fake ebuild\n",
            "# That's it for now\n",
            "\n",
        ]

        r = self.assertReport(self.check, [fake_pkg, fake_src])
        assert isinstance(r, whitespace.TrailingEmptyLine)
        assert 'trailing blank line(s)' in str(r)


class TestMultiReport(WhitespaceCheckTest):

    def test_it(self):
        fake_pkg = misc.FakePkg("dev-util/diffball-0.5")
        fake_src = [
            "# This is our first fake ebuild\n",
            " # This line contains a leading whitespace\n",
            "# This line contains a trailing whitespace \n",
            "# This line contains a trailing tab\t\n",
            "\t \t#The first whitey is bad...\n",
            "\t\t #... the second one is fine\n",
            "\n",
            "\n",
            "# That's it for now\n",
        ]

        reports = self.assertReports(self.check, [fake_pkg, fake_src])
        assert len(reports) == 4
