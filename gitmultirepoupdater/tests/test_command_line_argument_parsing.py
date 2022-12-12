from unittest import TestCase
import logging

from gitmultirepoupdater.cli import parse_command_line_arguments


class CommandLineArgumentParsingTests(TestCase):
    def test_repositories_parsing(self):
        args = parse_command_line_arguments(["-r", "foo"])
        self.assertEqual(args.repos, ["foo"])

        args = parse_command_line_arguments(["-r", "foo", "-r", "bar", "-r", "spam"])
        self.assertEqual(args.repos, ["foo", "bar", "spam"])

        args = parse_command_line_arguments(["--repo", "foo", "--repos", "bar", "-r", "spam"])
        self.assertEqual(args.repos, ["foo", "bar", "spam"])

        args = parse_command_line_arguments(["--repos", "foo", "bar"])
        self.assertEqual(args.repos, ["foo"])

        args = parse_command_line_arguments([])
        self.assertEqual(args.repos, [])

    def test_clone_to_parsing(self):
        args = parse_command_line_arguments(["-r", "foo"])  # Default value
        self.assertEqual(args.clone_to, "/tmp/")

        args = parse_command_line_arguments(["-r", "foo", "-c", "my_dir"])
        self.assertEqual(args.clone_to, "my_dir")

        args = parse_command_line_arguments(["-r", "foo", "--clone-to", "my_another_dir"])
        self.assertEqual(args.clone_to, "my_another_dir")

    def test_verbose_parsing(self):
        args = parse_command_line_arguments([])
        self.assertFalse(args.verbose)
        self.assertEqual(logging.getLogger().level, logging.WARNING)

        args = parse_command_line_arguments(["-v"])
        self.assertTrue(args.verbose)
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

        args = parse_command_line_arguments(["--verbose"])
        self.assertTrue(args.verbose)
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

    def test_commands_parsing(self):
        args = parse_command_line_arguments(["ls"])
        self.assertEqual(args.commands, ["ls"])

        args = parse_command_line_arguments(["ls", "pwd"])
        self.assertEqual(args.commands, ["ls", "pwd"])

        args = parse_command_line_arguments(["-r", "repos.txt", "ls", "pwd"])
        self.assertEqual(args.commands, ["ls", "pwd"])
