
class Review:
    def __init__(self, rating, content, subratings, employee_ratings):
        self.rating = rating
        self.content = content
        self.subratings = subratings
        self.employee_ratings = employee_ratings
        self.positivityScore = 0

    def __str__(self):
        output = '\n'
        output += 'POSITIVITY SCORE: ' + \
            str(int(self.positivityScore)) + '/100' + '\n'
        output += 'Overall Rating: ' + str(self.rating) + '\n'
        output += self.content + '\n'
        for rating in self.subratings.keys():
            output += str(rating) + ': ' + str(self.subratings[rating]) + '\n'
        for rating in self.employee_ratings:
            output += 'Employee Rating: ' + str(rating) + '\n'
        return output

    def getPositivityScore(self):
        return self.positivityScore

    def calcSubratingsSubscore(self):
        # sum all subratings
        subscore = sum(self.subratings.values())
        if 'Recommend Dealer' in self.subratings.keys() and self.subratings['Recommend Dealer'] == True:
            # correct for extra boolean 1 in subratings if present
            subscore -= 1
        else:
            # if not present divide subscore by 2
            subscore /= 2
        return subscore

    def calcBodySubscore(self, body_max):
        # number of words in the review body, relative to maximum, scaled to 25
        body_score = (len(self.content.split(' ')) / body_max) * 25
        return body_score

    def calcEmpReviewsSubscore(self, num_emp_max):
        # number of employee ratings relative to max, scaled to 25, multiplied by avg rating out of 5
        num_emp = len(self.employee_ratings)
        if num_emp == 0:
            emp_subscore = 0
        else:
            avg_rating = sum(self.employee_ratings) / num_emp
            emp_subscore = (25 * num_emp / num_emp_max) * (avg_rating / 5)
        return emp_subscore

    def calcPositivityScore(self, body_max, num_emp_max):
        # start with review rating multiplied by 5
        subscores = [self.rating * 5]
        subscores.append(self.calcSubratingsSubscore())
        subscores.append(self.calcEmpReviewsSubscore(num_emp_max))
        subscores.append(self.calcBodySubscore(body_max))

        self.positivityScore = sum(subscores)


class ReviewCollection:
    def __init__(self):
        self.reviews = []
        self.body_max = 0.1
        self.num_emp_max = 0.1

    def __str__(self):
        output = ''
        for review in self.reviews:
            output += str(review)
        return output

    def addReview(self, **kwargs):
        # update max review body size
        if 'content' in kwargs.keys():
            body_size = len(kwargs['content'].split(' '))
            if body_size > self.body_max:
                self.body_max = body_size

        # update max number of employee reviews
        if 'employee_ratings' in kwargs.keys():
            num_emp = len(kwargs['employee_ratings'])
            if num_emp > self.num_emp_max:
                self.num_emp_max = num_emp

        # add the review
        self.reviews.append(Review(**kwargs))

    def getReviews(self):
        return self.reviews

    def numReviews(self):
        return len(self.reviews)

    def identifyPositive(self):
        # calculate score of each review
        for review in self.reviews:
            review.calcPositivityScore(self.body_max, self.num_emp_max)

        # sort by positivity score, descending
        self.reviews.sort(key=Review.getPositivityScore, reverse=True)
        return self.reviews
