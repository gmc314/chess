from script import *
import unittest

class TestMiscFunctions(unittest.TestCase):
    def testClearBoard(self):
        result = clearBoard()
        self.assertEqual(result, "Board Cleared")
        

    def testGetRankAndFile(self):
        testIndices = (1,1)
        row, col = testIndices
        result = getRankAndFileFromBoardIndex(row, col)
        self.assertEqual(result, ("b", 7))

class TestChessPieces(unittest.TestCase):
    def testPlacePiece(self):
        testPiece = Pawn("Black", "5", ("a", 7))
        resultString = placePiece(testPiece)
        self.assertEqual(resultString, "BP placed")

unittest.main()





