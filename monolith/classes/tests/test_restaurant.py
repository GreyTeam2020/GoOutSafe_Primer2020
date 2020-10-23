import unittest
from monolith.classes.restaurant import Restaurant


class TestRestaurant(unittest.TestCase):

    def test_rest_init(self):
        rest = Restaurant('./monolith/classes/tests/rest0.txt')
        name = rest.name
        tables = rest.tables

        self.assertEqual(name, 'ASEPizza')
        self.assertEqual(len(tables), 3)
        self.assertEqual(tables[0].name, 'red')
        self.assertEqual(tables[0].capacity, 10)
        self.assertEqual(tables[1].name, 'yellow')
        self.assertEqual(tables[1].capacity, 2)
        self.assertEqual(tables[2].name, 'pink')
        self.assertEqual(tables[2].capacity, 3)


if __name__ == '__main__':
    unittest.main()
