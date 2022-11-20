from unittest import TestCase

from gitmultirepoupdater.cli import parse_cli_arguments


class CommandLineArgumentParsingTests(TestCase):
    def test_repositories_parsing(self):
        args = parse_cli_arguments(["-r", "foo"])
        self.assertEqual(args.repos, ["foo"])

        args = parse_cli_arguments(["-r", "foo", "-r", "bar", "-r", "spam"])
        self.assertEqual(args.repos, ["foo", "bar", "spam"])

        args = parse_cli_arguments(["--repo", "foo", "--repos", "bar", "-r", "spam"])
        self.assertEqual(args.repos, ["foo", "bar", "spam"])
