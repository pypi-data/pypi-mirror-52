import json
from dataclasses import dataclass
from unittest import TestCase

from json_dataclass_io_hooks import dataclass_object_load, dataclass_object_dump


@dataclass
class DataclassObject:
    number: int
    text: str


class TestJsonDataclassHooks(TestCase):
    def test_produce_json(self):
        obj = DataclassObject(number=42, text="hello_world")
        json_text = json.dumps(obj, default=dataclass_object_dump)
        expected = """{"number": 42, "text": "hello_world", "__dataclass__": "json_dataclass_io_hooks.tests.test_json_dataclass_io_hooks.DataclassObject"}"""
        self.assertEqual(json_text, expected)

    def test_produce_object(self):
        json_text = """{"number": 42, "text": "hello_world", "__dataclass__": "json_dataclass_io_hooks.tests.test_json_dataclass_io_hooks.DataclassObject"}"""
        obj = json.loads(json_text, object_hook=dataclass_object_load)
        self.assertEqual(obj, DataclassObject(number=42, text="hello_world"))

    def test_produce_json_illegal_dataclass(self):
        obj = "no dataclass object"
        self.assertRaises(TypeError, lambda x: json.dumps(obj, default=dataclass_object_dump))
