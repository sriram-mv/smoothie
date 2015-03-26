import unittest

from smoothie.exc import CallableCallbackException
from smoothie.king import Dispenser


class SmoothieKingTest(unittest.TestCase):

    def test_smoothie_single_func_exception(self):

        self.was_called = False

        def err_callback(*args, **kwargs):
            self.was_called = True
            return "Error Handled"

        juice = Dispenser()
        @juice.attach(exception=IndexError,
                      callback=err_callback)
        def func_with_error():
            drinks = ['Tea','Coffee', 'Water']
            return drinks[4]

        self.assertEqual(func_with_error(), "Error Handled")
        self.assertTrue(self.was_called)

    def test_smoothie_multiple_func_exception(self):

        self.first_was_called = False

        def first_err_callback(*args, **kwargs):
            self.first_was_called = True
            return "First Error Handled"

        self.second_was_called = False

        def second_err_callback(*args, **kwargs):
            self.second_was_called = True
            return "Second Error Handled"

        juice = Dispenser()
        @juice.attach(exception=RuntimeError,
                      callback=first_err_callback)
        @juice.attach(exception=TypeError,
                      callback=second_err_callback)
        def func_with_error(error_case):
            if error_case % 2 == 0:
                raise RuntimeError
            else:
                raise TypeError

        self.assertEqual(func_with_error(2), "First Error Handled")
        self.assertTrue(self.first_was_called)
        self.assertEqual(func_with_error(3), "Second Error Handled")
        self.assertTrue(self.second_was_called)

    def test_smoothie_stores_original(self):

        self.was_called = False

        def err_callback(*args, **kwargs):
            self.was_called = True
            return "Error Handled"

        juice = Dispenser()
        @juice.attach(exception=IndexError,
                      callback=err_callback)
        def func_with_error():
            sauce = ['Mustard', 'Ketchup']
            return sauce[3]

        func_not_captured_exception = juice.original(func_with_error.__name__)

        with self.assertRaises(IndexError):
            func_not_captured_exception()


    def test_smoothie_class_function(self):

        self.was_called = False

        def err_callback(*args, **kwargs):
            self.was_called = True
            return kwargs

        juice = Dispenser()

        class Drinks(object):
            def __init__(self):
                self.drinks = []
                pass

            @juice.attach(exception=IndexError,
                          callback=err_callback)
            def drink_error_args(self, new_drink):
                self.was_called = False
                self.new_drink = new_drink
                self.drinks.append(self.new_drink)
                return self.drinks[4]

        drinks_obj = Drinks()
        returns = drinks_obj.drink_error_args('Water')
        raised_exception = returns['ex']

        self.assertTrue('exc_info' in returns)
        self.assertEqual(raised_exception.__class__,
                         IndexError)

        with self.assertRaises(IndexError):
            orig_drink_error_args = juice.original('drink_error_args')
            # NOTE(TheSriram): The first argument needs to be self,
            # since the original function was a member function of a
            # class. It can also be any object that closely matches
            # the spec of `self`
            orig_drink_error_args(drinks_obj, 'Coffee')

    def test_smoothie_bad_callback(self):

        my_bad_callback = ("A Tuple?, Really?")
        self.was_called = False

        juice = Dispenser()

        @juice.attach(exception=IndexError,
                      callback=my_bad_callback)
        def my_bad_function():
            raise IndexError

        with self.assertRaises(CallableCallbackException):
            my_bad_function()
