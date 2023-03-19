import os
import shutil
from pathlib import Path
from pyshell.core.pyshell import PyShell
from pyshell.modules.docker import Docker
from typing import Any

def test_build_image(tmp_path: Any):
    # Copy files to a temporary directory
    source_dockerfile = Path(__file__).parent / "test-basic.dockerfile"
    dest_dockerfile = tmp_path / "test-basic.dockerfile"
    shutil.copyfile(source_dockerfile, dest_dockerfile)

    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    pyshell = PyShell()
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    # Build the image
    tag = "foobar:build-image"
    build_result = Docker.build(
        tag=tag,
        dockerfile=str(dest_dockerfile),
        context=str(tmp_path),
        use_sudo=use_sudo,
        pyshell=pyshell
    )

    # Clean up after the test before checking results
    rmi_result = Docker.rmi(tag=tag, use_sudo=use_sudo, pyshell=pyshell)

    # Check the results
    assert build_result.success
    assert rmi_result.success


def test_build_with_args(tmp_path: Any):
    # Copy files to a temporary directory
    source_dockerfile = Path(__file__).parent / "test-args.dockerfile"
    dest_dockerfile = tmp_path / "test-args.dockerfile"
    shutil.copyfile(source_dockerfile, dest_dockerfile)

    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    pyshell = PyShell()
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    # Build the image
    tag = "foobar:build-args"
    foo_arg = "foo1"
    bar_arg = "bar2"
    build_result = Docker.build(
        tag=tag,
        dockerfile=str(dest_dockerfile),
        context=str(tmp_path),
        use_sudo=use_sudo,
        pyshell=pyshell,
        FOO=foo_arg,
        BAR=bar_arg
    )

    # Start a container using the image and print the arguments
    run_result = Docker.run(
        tag,
        "/bin/ash",
        args = ["-c", "echo $FOO $BAR"],
        remove_after=True,
        use_sudo=use_sudo,
        pyshell=pyshell
    )

    # Clean up after the test before checking results
    rmi_result = Docker.rmi(tag=tag, use_sudo=use_sudo, pyshell=pyshell)

    # Check the results
    assert build_result.success
    assert run_result.success
    assert rmi_result.success
    assert f"{foo_arg} {bar_arg}" in run_result.output


def test_build_with_custom_context_path(tmp_path: Any):
    # Copy files to a temporary directory
    source_dockerfile = Path(__file__).parent / "test-context.dockerfile"
    dest_dockerfile = tmp_path / "test-context.dockerfile"
    shutil.copyfile(source_dockerfile, dest_dockerfile)

    # Create the file that will be copied into the image
    foo_file = tmp_path / "foo.txt"
    foo_contents = "foo bar baz"
    foo_file.write_text(foo_contents)

    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    pyshell = PyShell()
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    # Build the image
    tag = "foobar:build-context"
    build_result = Docker.build(
        tag=tag,
        dockerfile=str(dest_dockerfile),
        context=str(tmp_path),
        use_sudo=use_sudo,
        pyshell=pyshell
    )

    # Start a container using the image and print the arguments
    # This path is defined in the Dockerfile
    foo_dest_path = "/home/foo.txt"
    run_result = Docker.run(
        tag,
        "/bin/ash",
        args = ["-c", f"cat {foo_dest_path}"],
        remove_after=True,
        use_sudo=use_sudo,
        pyshell=pyshell
    )

    # Clean up after the test before checking results
    rmi_result = Docker.rmi(tag=tag, use_sudo=use_sudo, pyshell=pyshell)

    # Check the results
    assert build_result.success
    assert run_result.success
    assert rmi_result.success

    assert foo_contents in run_result.output
