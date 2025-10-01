import logging

from autogit.cli import parse_command_line_arguments


def test_repositories_parsing() -> None:
    args = parse_command_line_arguments(['-r', 'foo'])
    assert args.repos == ['foo']

    args = parse_command_line_arguments(['-r', 'foo', '-r', 'bar', '-r', 'spam'])
    assert args.repos == ['foo', 'bar', 'spam']

    args = parse_command_line_arguments(['--repo', 'foo', '--repos', 'bar', '-r', 'spam'])
    assert args.repos == ['foo', 'bar', 'spam']

    args = parse_command_line_arguments(['--repos', 'foo', 'bar'])
    assert args.repos == ['foo']

    args = parse_command_line_arguments([])
    assert args.repos == []


def test_clone_to_parsing() -> None:
    args = parse_command_line_arguments(['-r', 'foo'])  # Default value
    assert args.clone_to == '/tmp/'

    args = parse_command_line_arguments(['-r', 'foo', '-c', 'my_dir'])
    assert args.clone_to == 'my_dir'

    args = parse_command_line_arguments(['-r', 'foo', '--clone-to', 'my_another_dir'])
    assert args.clone_to == 'my_another_dir'


def test_verbose_parsing() -> None:
    args = parse_command_line_arguments([])
    assert not args.verbose
    assert logging.getLogger().level == logging.WARNING

    args = parse_command_line_arguments(['-v'])
    assert args.verbose
    assert logging.getLogger().level == logging.DEBUG

    args = parse_command_line_arguments(['--verbose'])
    assert args.verbose
    assert logging.getLogger().level == logging.DEBUG


def test_commands_parsing() -> None:
    args = parse_command_line_arguments(['ls'])
    assert args.commands == ['ls']

    args = parse_command_line_arguments(['ls', 'pwd'])
    assert args.commands == ['ls', 'pwd']

    args = parse_command_line_arguments(['-r', 'repos.txt', 'ls', 'pwd'])
    assert args.commands == ['ls', 'pwd']
