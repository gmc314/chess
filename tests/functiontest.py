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
    
    def testNoneInput(self):
        sqr = None
        result = isSquareValid(sqr)
        self.assertEqual(result, False)

    def testWrongTupleLength(self):
        sqr = (3, 7, 6)
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

    def testNone(self):
        param = None
        result = getBoardIndexFromRankAndFile(param)
        self.assertEqual(result, "Invalid")

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

    def testTuple(self):
        lst = (5,5)
        result = filterListForSquares(lst)
        self.assertEqual(result, [])

    def testNonIterable(self):
        lst = "1"
        result = filterListForSquares(lst)
        self.assertEqual(result, [])

    def testNonIterable2(self):
        lst = 1
        result = filterListForSquares(lst)
        self.assertEqual(result, [])

        
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

class TestStringifyRankFile(unittest.TestCase):
    def testInvalidInput(self):
        param = 5
        result = stringifyRankFile(param)
        self.assertEqual(result, False)

    def testValidInput(self):
        param = ("e", 8)
        result = stringifyRankFile(param)
        self.assertEqual(result, "E8")


class TestGetPieceFromLocation(unittest.TestCase):
    def testNone(self):
        param = None
        result = getPieceFromLocation(param)
        self.assertEqual(result, "Invalid")
    
    def testList(self):
        param = []
        result = getPieceFromLocation(param)
        self.assertEqual(result, "Invalid")
    
    def testValidInputOnEmptyBoard(self):
        param = ("a", 6)
        result = getPieceFromLocation(param)
        self.assertEqual(result, emptySquare)


unittest.main()
