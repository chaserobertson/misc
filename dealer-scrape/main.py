#!/usr/bin/env/python3
from requests_html import AsyncHTMLSession
from scrape import populateReviews
from time import sleep

NUM_REVIEWS_TO_DISPLAY = 3
NUM_PAGES_TO_SCRAPE = 5
URL = 'https://www.dealerrater.com/dealer'
DEALER = '/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685'
PAGE = '/page'
asession = AsyncHTMLSession()


def create_request(dealer, page_num):
    # define new request with different page num
    async def get_reviews_page():
        request_url = URL + dealer + PAGE + str(page_num)
        r = await asession.get(request_url)
        return r
    return get_reviews_page


def main():
    # Step 1: scrape the first 5 pages of reviews
    print('Scraping review pages...')
    get_review_pages = [create_request(DEALER, i)
                        for i in range(1, NUM_PAGES_TO_SCRAPE + 1)]
    results = asession.run(*get_review_pages)
    reviews = populateReviews(results)

    # Step 2: identify the top three most overly positive endorsements
    print('Identifying most overly positive reviews...')
    sleep(2)
    top_reviews = reviews.identifyPositive()

    # Step 3: output top three reviews to the console in order of severity
    for i in range(0, NUM_REVIEWS_TO_DISPLAY):
        review = top_reviews[i]
        print('--------#%d OVERLY POSITIVE REVIEW----------' % int(i+1))
        print(review)

    print('Done.')
    return 0


if __name__ == '__main__':
    main()
