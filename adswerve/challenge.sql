-- pounds to kilograms: 1lb = 0.453592kg
with annual_avgs as (
    select
        year,
        avg(weight_pounds) * 0.453592 as avg_weight_kg
    from `bigquery-public-data.samples.natality`
    group by year
),

recent_avgs as (
    select * from annual_avgs
    where year between 1988 and 2008
)

select
    recent.year,
    recent.avg_weight_kg,
    recent.avg_weight_kg - prev.avg_weight_kg as delta_20_yrs_prior
from recent_avgs as recent
left join annual_avgs as prev
    on recent.year = (prev.year + 20)
order by recent.year;


select
    month,
    count(*) as n_births
from `bigquery-public-data.samples.natality`
group by month
order by month;
/*
Births peak in August at 12.3M (total) and are lowest in February at 10.5M.
July through October have the most births, suggesting that conception is more common during the period 9-10 months prior: fall and early winter.
Conception must also be less common 9-10 months prior to Feb: April/May.
*/


select
    wday,
    count(*) as n_births
from `bigquery-public-data.samples.natality`
group by wday
order by wday;
/*
Births are much less common on weekends than weekdays.
9.3M total births occurred on a Saturday and 8.4M total occurred on a Sunday, whereas 12-13M births occurred on each weekday.
This suggests that induced births, which would presumably be scheduled for a weekday, account for a fair portion of total births.
*/


select
    year,
    wday,
    count(*) as n_births
from `bigquery-public-data.samples.natality`
where year >= 1989
group by year, wday
order by year, wday;
/*
Weekday of birth was not recorded in the dataset until 1989.
The difference in proportion of births on weekends vs weekdays has increased over time.
This adds evidence to the scheduled inducement hypothesis, assuming that access to inducement has also increased over time.
*/


select
    state,
    countif(state <> mother_residence_state) / count(*) as prop_out_of_state
from `bigquery-public-data.samples.natality`
group by state
order by prop_out_of_state desc;
/*
The majority of DC births are to non-residents, suggesting that many mothers travel to DC from surrounding areas to give birth.
Other states with high proportions of non-resident births include ND, WV, and small northeastern states like NH, DE, and RI.
Interestingly, the only island-state of Hawaii ranks above three other states in non-resident births (MI, CA, AK).
*/


CREATE OR REPLACE MODEL `exalted-entry-451621-h3.natality.cont2`
  OPTIONS(
    MODEL_TYPE = 'CONTRIBUTION_ANALYSIS',
    CONTRIBUTION_METRIC = 'SUM(weight_pounds)',
    DIMENSION_ID_COLS = ['mother_age', 'father_age'],
    IS_TEST_COL = 'is_test'
) AS
SELECT
  weight_pounds,
  mother_age, 
  father_age, 
  year = 2008 as is_test
FROM `natality.all`;

SELECT
  *
FROM
  ML.GET_INSIGHTS(
    MODEL `exalted-entry-451621-h3.natality.cont2`)
ORDER BY unexpected_difference DESC;
