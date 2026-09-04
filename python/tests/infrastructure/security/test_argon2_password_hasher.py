from payment_transfer.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)


def test_should_hash_password():
    hasher = Argon2PasswordHasher()

    password = "MySecurePassword123!"
    password_hash = hasher.hash(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2")


def test_should_verify_correct_password():
    hasher = Argon2PasswordHasher()

    password = "MySecurePassword123!"
    password_hash = hasher.hash(password)

    assert hasher.verify(password, password_hash)


def test_should_reject_incorrect_password():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash("MySecurePassword123!")

    assert not hasher.verify(
        "WrongPassword",
        password_hash,
    )


def test_should_generate_different_hashes_for_same_password():
    hasher = Argon2PasswordHasher()

    password = "MySecurePassword123!"

    first_hash = hasher.hash(password)
    second_hash = hasher.hash(password)

    assert first_hash != second_hash
