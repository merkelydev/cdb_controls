from errors import ChangeError
from fingerprinters import DockerFingerprinter
from pytest import raises

DOCKER_PROTOCOL = "docker://"


def X_test_real_example():
    # Requires docker socket to be mounted. No good for Windows.
    # TODO: Stub the docker call
    fingerprinter = DockerFingerprinter()
    image_name = 'python:3.7-alpine'  # The base image of merkely/change
    expected = '13032d90afaaa111e92920eea2b1abb0a6b6eafa6863ad7a4bd082a9c8574240'
    assert fingerprinter.sha(f"{DOCKER_PROTOCOL}{image_name}") == expected


def X_test_getting_sha_of_bad_image_name_raises():
    # Requires docker socket to be mounted. No good for Windows.
    # TODO: Stub the docker call
    fingerprinter = DockerFingerprinter()
    bad_image_name = 'python:3.7-alpine-does-not-exist'
    with raises(ChangeError) as exc:
        fingerprinter.sha(f"docker://{bad_image_name}")
    start = f"Cannot determine digest for image: {bad_image_name}"
    diagnostic = str(exc.value)
    assert diagnostic.startswith(start), diagnostic


def test_handles_only_its_own_protocol():
    fingerprinter = DockerFingerprinter()
    assert fingerprinter.handles_protocol(DOCKER_PROTOCOL)
    assert not fingerprinter.handles_protocol('X'+DOCKER_PROTOCOL)


def test_non_empty_image_name_properties():
    fingerprinter = DockerFingerprinter()
    image_name = "acme/road-runner:4.8"
    string = DOCKER_PROTOCOL + image_name
    assert fingerprinter.artifact_name(string) == image_name
    assert fingerprinter.artifact_basename(string) == image_name


def test_notes_and_example_docs_are_set():
    fingerprinter = DockerFingerprinter()
    assert len(fingerprinter.notes) > 0
    assert len(fingerprinter.example) > 0


def test_empty_image_name_raises():
    fingerprinter = DockerFingerprinter()
    image_name = ""
    string = DOCKER_PROTOCOL + image_name

    def assert_raises_empty_image(method_name):
        with raises(ChangeError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {DOCKER_PROTOCOL} fingerprint"

    assert_raises_empty_image('artifact_name')
    assert_raises_empty_image('artifact_basename')
    assert_raises_empty_image('sha')


def test_trailing_whitespace_is_stripped_from_image_name():
    fingerprinter = DockerFingerprinter()
    image_name = " " * 4
    string = DOCKER_PROTOCOL + image_name

    def assert_raises_empty_image(method_name):
        with raises(ChangeError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {DOCKER_PROTOCOL} fingerprint"

    assert_raises_empty_image('sha')