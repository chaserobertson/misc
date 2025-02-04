import unittest
from review import ReviewCollection, Review
from scrape import (digest_subratings_element,
                    digest_employees_element,
                    digest_review_element,
                    populateReviews)
from main import create_request, main


TESTARGS = [
    {
        'rating': 1,
        'content': 'this is a test review body',
        'subratings': {'testsub': 2},
        'employee_ratings': [3]
    },
    {
        'rating': 2,
        'content': 'test2',
        'subratings': {'testsub2': 3, 'testsub3': 4},
        'employee_ratings': [4, 4, 4]
    }
]


class Test(unittest.TestCase):

    def testReviewCalcPositivityScore(self):
        review = Review(**TESTARGS[0])
        review.calcPositivityScore(6, 1)
        self.assertEqual(review.getPositivityScore(), 46)

    def testReviewCollectionAddReview(self):
        collection = ReviewCollection()
        collection.addReview(**TESTARGS[0])
        self.assertEqual(str(collection.getReviews()[
                         0]), str(Review(**TESTARGS[0])))

    def testReviewCollectionIdentifyPositive(self):
        collection = ReviewCollection()
        for args in TESTARGS:
            collection.addReview(**args)
        pre = collection.getReviews()
        collection.identifyPositive()
        post = collection.getReviews()
        post.reverse()
        self.assertListEqual(pre, post)


if __name__ == '__main__':
    unittest.main()
