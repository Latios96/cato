import unittest
from pinject import bindings as bindings, errors as errors, support as support

class VerifyTypeTest(unittest.TestCase):
    def test_verifies_correct_type_ok(self) -> None: ...
    def test_raises_exception_if_incorrect_type(self) -> None: ...

class VerifyTypesTest(unittest.TestCase):
    def test_verifies_empty_sequence_ok(self): ...
    def test_verifies_correct_type_ok(self) -> None: ...
    def test_raises_exception_if_not_sequence(self) -> None: ...
    def test_raises_exception_if_element_is_incorrect_type(self) -> None: ...

class VerifySubclassesTest(unittest.TestCase):
    def test_verifies_empty_sequence_ok(self) -> None: ...
    def test_verifies_correct_type_ok(self) -> None: ...
    def test_raises_exception_if_not_sequence(self) -> None: ...
    def test_raises_exception_if_element_is_not_subclass(self) -> None: ...

class VerifyCallableTest(unittest.TestCase):
    def test_verifies_callable_ok(self) -> None: ...
    def test_raises_exception_if_not_callable(self) -> None: ...

class VerifyModuleTypesTest(unittest.TestCase):
    def test_verifies_module_types_ok(self) -> None: ...
    def test_raises_exception_if_not_module_types(self) -> None: ...

class VerifyClassTypesTest(unittest.TestCase):
    def test_verifies_module_types_ok(self) -> None: ...
    def test_raises_exception_if_not_class_types(self) -> None: ...

class IsSequenceTest(unittest.TestCase):
    def test_argument_identified_as_sequence_instance(self) -> None: ...
    def test_argument_identified_as_not_sequence_instance(self) -> None: ...

class IsStringTest(unittest.TestCase):
    def test_argument_identified_as_string_instance(self) -> None: ...
    def test_argument_identified_as_not_string_instance(self) -> None: ...

class IsConstructorDefinedTest(unittest.TestCase):
    def test_constructor_present_detection(self) -> None: ...
    def test_constructor_not_present_detection(self) -> None: ...
