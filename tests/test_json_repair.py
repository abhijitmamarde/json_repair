from src.json_repair.json_repair import repair_json


def test_repair_json():
    # Test with valid JSON strings
    assert repair_json("[]") == "[]"
    assert repair_json("{}") == "{}"
    assert (
        repair_json('{"name": "John", "age": 30, "city": "New York"}')
        == '{"name": "John", "age": 30, "city": "New York"}'
    )
    assert repair_json("[1, 2, 3, 4]") == "[1, 2, 3, 4]"
    assert (
        repair_json('{"employees":["John", "Anna", "Peter"]} ')
        == '{"employees": ["John", "Anna", "Peter"]}'
    )

    # Test with invalid JSON strings
    assert (
        repair_json('{"name": "John", "age": 30, "city": "New York')
        == '{"name": "John", "age": 30, "city": "New York"}'
    )
    assert (
        repair_json('{"name": "John", "age": 30, city: "New York"}')
        == '{"name": "John", "age": 30, "city": "New York"}'
    )
    assert (
        repair_json('{"name": "John", "age": 30, "city": New York}')
        == '{"name": "John", "age": 30, "city": "New York"}'
    )
    assert (
        repair_json('{"name": John, "age": 30, "city": "New York"}')
        == '{"name": "John", "age": 30, "city": "New York"}'
    )
    assert repair_json("[1, 2, 3,") == "[1, 2, 3]"
    assert (
        repair_json('{"employees":["John", "Anna",')
        == '{"employees": ["John", "Anna"]}'
    )

    # Test with edge cases
    assert repair_json(" ") == '""'
    assert repair_json("[") == "[]"
    assert repair_json("[[1\n\n]") == "[[1]]"
    assert repair_json("{") == "{}"
    assert repair_json('{"key": "value:value"}') == '{"key": "value:value"}'
    assert (
        repair_json('{"name": "John", "age": 30, "city": "New')
        == '{"name": "John", "age": 30, "city": "New"}'
    )
    assert (
        repair_json('{"employees":["John", "Anna", "Peter')
        == '{"employees": ["John", "Anna", "Peter"]}'
    )
    assert (
        repair_json('{"employees":["John", "Anna", "Peter"]}')
        == '{"employees": ["John", "Anna", "Peter"]}'
    )
    assert (
        repair_json('{"text": "The quick brown fox,"}')
        == '{"text": "The quick brown fox,"}'
    )


def test_repair_json_with_objects():
    # Test with valid JSON strings
    assert repair_json("[]", True) == []
    assert repair_json("{}", True) == {}
    assert repair_json('{"name": "John", "age": 30, "city": "New York"}', True) == {
        "name": "John",
        "age": 30,
        "city": "New York",
    }
    assert repair_json("[1, 2, 3, 4]", True) == [1, 2, 3, 4]
    assert repair_json('{"employees":["John", "Anna", "Peter"]} ', True) == {
        "employees": ["John", "Anna", "Peter"]
    }

    # Test with invalid JSON strings
    assert repair_json('{"name": "John", "age": 30, "city": "New York', True) == {
        "name": "John",
        "age": 30,
        "city": "New York",
    }
    assert repair_json('{"name": "John", "age": 30, city: "New York"}', True) == {
        "name": "John",
        "age": 30,
        "city": "New York",
    }
    assert repair_json('{"name": "John", "age": 30, "city": New York}', True) == {
        "name": "John",
        "age": 30,
        "city": "New York",
    }
    assert repair_json("[1, 2, 3,", True) == [1, 2, 3]
    assert repair_json('{"employees":["John", "Anna",', True) == {
        "employees": ["John", "Anna"]
    }

    # Test with edge cases
    assert repair_json(" ", True) == ""
    assert repair_json("[", True) == []
    assert repair_json("{", True) == {}
    assert repair_json('{"key": "value:value"}', True) == {"key": "value:value"}
    assert repair_json('{"name": "John", "age": 30, "city": "New', True) == {
        "name": "John",
        "age": 30,
        "city": "New",
    }
    assert repair_json('{"employees":["John", "Anna", "Peter', True) == {
        "employees": ["John", "Anna", "Peter"]
    }


def test_repair_json_corner_cases_generate_by_gpt():
    # Test with nested JSON
    assert (
        repair_json('{"key1": {"key2": [1, 2, 3]}}') == '{"key1": {"key2": [1, 2, 3]}}'
    )
    assert repair_json('{"key1": {"key2": [1, 2, 3') == '{"key1": {"key2": [1, 2, 3]}}'

    # Test with empty keys
    assert repair_json('{"": "value"}') == '{"": "value"}'

    # Test with Unicode characters
    assert repair_json('{"key": "value\u263A"}') == '{"key": "value\\u263a"}'

    # Test with special characters
    assert repair_json('{"key": "value\\nvalue"}') == '{"key": "value\\nvalue"}'

    # Test with large numbers
    assert (
        repair_json('{"key": 12345678901234567890}') == '{"key": 12345678901234567890}'
    )

    # Test with whitespace
    assert repair_json(' { "key" : "value" } ') == '{"key": "value"}'

    # Test with null values
    assert repair_json('{"key": null}') == '{"key": null}'


def test_repair_json_corner_cases_generate_by_gpt_with_objects():
    # Test with nested JSON
    assert repair_json('{"key1": {"key2": [1, 2, 3]}}', True) == {
        "key1": {"key2": [1, 2, 3]}
    }
    assert repair_json('{"key1": {"key2": [1, 2, 3', True) == {
        "key1": {"key2": [1, 2, 3]}
    }

    # Test with empty keys
    assert repair_json('{"": "value"}', True) == {"": "value"}

    # Test with Unicode characters
    assert repair_json('{"key": "value\u263A"}', True) == {"key": "value☺"}

    # Test with special characters
    assert repair_json('{"key": "value\\nvalue"}', True) == {"key": "value\nvalue"}

    # Test with large numbers
    assert repair_json('{"key": 12345678901234567890}', True) == {
        "key": 12345678901234567890
    }

    # Test with whitespace
    assert repair_json(' { "key" : "value" } ', True) == {"key": "value"}

    # Test with null values
    assert repair_json('{"key": null}', True) == {"key": None}
