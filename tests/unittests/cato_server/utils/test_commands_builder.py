from cato_server.utils.commands_builder import CommandsBuilder


def test_push_command_should_append_to_current_command():
    commands_builder = CommandsBuilder("base_command", 80)

    commands_builder.push(" part")
    commands = commands_builder.finalize()

    assert commands == ["base_command part"]


def test_push_command_should_create_new_command():
    commands_builder = CommandsBuilder("base_command", 20)

    commands_builder.push(" part")
    commands_builder.push(" part")
    commands = commands_builder.finalize()

    assert commands == ["base_command part", "base_command part"]
