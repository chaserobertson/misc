from review import ReviewCollection


def digest_subratings_element(e):
    subratings = dict()
    ratings = e.find('.review-ratings-all')[0].find('.tr')
    for rating in ratings:
        # get text name of this subrating
        text = rating.find('.td')[0].text

        # get numerical or boolean score of this subrating
        score = rating.search(' rating-{} ')
        if score == None:
            # text score of 'Yes' becomes boolean value True
            score = rating.find('.small-text.boldest')[0].text == 'Yes'
        else:
            # numerical score shifted from 50 to 5.0
            score = int(score[0]) / 10

        # add this subrating to dict
        subratings.setdefault(text, score)
    return subratings


def digest_employees_element(e):
    employees = []
    emp_ratings = e.find('.review-employee')
    for er in emp_ratings:
        # find numerical employee rating
        rating_found = er.search(' rating-{} ')

        # only add to ratings list if numerical value exists
        if rating_found != None:
            employees.append(int(rating_found[0]) / 10)
    return employees


def digest_review_element(e):
    rating = int(e.search(' rating-{} ')[0]) / 10
    content = e.find('.review-content')[0].text
    subratings = digest_subratings_element(e)
    employees = digest_employees_element(e)

    # create kwargs struct from processed review element
    return {
        'rating': rating,
        'content': content,
        'subratings': subratings,
        'employee_ratings': employees
    }


def populateReviews(html_tree):
    review_collection = ReviewCollection()

    for result in html_tree:
        # get all review elements in current page
        review_elements = result.html.find('.review-entry')

        for re in review_elements:
            # digest html of review element
            review = digest_review_element(re)

            # add review to collection
            review_collection.addReview(**review)

    return review_collection
