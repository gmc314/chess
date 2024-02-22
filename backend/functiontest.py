import unittest
from script import *

class TestClearBoard(unittest.TestCase):
    def testClearBoard(self):
        result = clearBoard()
        self.assertEqual(result, "Board Cleared")


class TestIsSquareValid(unittest.TestCase):
    def testInvalidInput(self):
        sqr = "f"
        result = isSquareValid(sqr)
        self.assertEqual(result, False)
    
    def testInvalidFile(self):
        sqr = ("z", 6)
        result = isSquareValid(sqr)
        self.assertEqual(result, False)
    
    def testInvalidRank(self):
        sqr = ("a", 9)
        result = isSquareValid(sqr)
        self.assertEqual(result, False)

    def testValidSquare(self):
        sqr = ("g", 6)
        result = isSquareValid(sqr)
        self.assertEqual(result, True)


class TestGetBoardIndices(unittest.TestCase):
    def testGetIndicesRegular(self):
        testCoords = ("b", 5)
        result = getBoardIndexFromRankAndFile(testCoords)
        self.assertEqual(result, (3, 1))      

    def testGetIndicesKeyError(self):
        testCoords = ("z", 5)
        result = getBoardIndexFromRankAndFile(testCoords)
        self.assertEqual(result, "Invalid")

    def testGetIndicesNumError(self):
        testCoords = ("a", 9)
        result = getBoardIndexFromRankAndFile(testCoords)
        self.assertEqual(result, "Invalid")

    def testGetIndicesNumEdgeCase1(self):
        testCoords = ("a", 8)
        result = getBoardIndexFromRankAndFile(testCoords)
        self.assertEqual(result, (0, 0))
        
    def testGetIndicesNumEdgeCase2(self):
        testCoords = ("a", 1)
        result = getBoardIndexFromRankAndFile(testCoords)
        self.assertEqual(result, (7, 0))


class TestFilterListForSquares(unittest.TestCase):
    def testEmptyList(self):
        lst = []
        result = filterListForSquares(lst)
        self.assertEqual(result, lst)

    def testSingleElement(self):
        lst = [("a", 6)]
        result = filterListForSquares(lst)
        self.assertEqual(result, lst)

    def testSingleElementFalse(self):
        lst = [False]
        result = filterListForSquares(lst)
        self.assertEqual(result, [])    
        
    def testTwoElement(self):
        lst = [False, ("a", 6)]
        result = filterListForSquares(lst)
        self.assertEqual(result, [("a", 6)])


class TestGetRankAndFileFromBoardIndex(unittest.TestCase):
    def testInvalidInputs(self):
        params = ("a", 9)
        result = getRankAndFileFromBoardIndex(*params)
        self.assertEqual(result, "Invalid")

    def testInvalidInputs2(self):
        params = (-2, "h")
        result = getRankAndFileFromBoardIndex(*params)
        self.assertEqual(result, "Invalid")

    def testValidInput(self):
        params = (4, 4)
        result = getRankAndFileFromBoardIndex(*params)
        self.assertEqual(result, ("e", 4))



unittest.main()