# G2 golden set. Questions 1-6 are from PDF Appendix A (the SQL is ours). Add your own below.
GOLD_SQL = [
 {"q": "Top 5 issues for Credit card complaints received in June 2026. Return issue and count n.",
  "gold_sql": """SELECT issue, COUNT(*) AS n FROM v_complaints
                 WHERE product = 'Credit card' AND date_received >= DATE '2026-06-01'
                 GROUP BY issue ORDER BY n DESC LIMIT 5"""},
 {"q": "Month-over-month change in Checking or savings account complaints tagged Older American, Jan-Jun 2026. Return month (first day of month), n, and change versus the previous month.",
  "gold_sql": """WITH m AS (SELECT date_trunc('month', date_received) AS month, COUNT(*) AS n
                   FROM v_complaints
                   WHERE product = 'Checking or savings account' AND tags ILIKE '%Older American%'
                   GROUP BY 1)
                 SELECT month, n, n - LAG(n) OVER (ORDER BY month) AS change FROM m ORDER BY month"""},
 {"q": "Among companies with at least 200 complaints in the window, which 5 have the lowest share of timely responses? Return company and timely_pct (percent of complaints with timely = 'Yes', 2 decimals).",
  "gold_sql": """SELECT company, ROUND(100.0 * SUM(CASE WHEN timely = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS timely_pct
                 FROM v_complaints GROUP BY company HAVING COUNT(*) >= 200
                 ORDER BY timely_pct ASC LIMIT 5"""},
 {"q": "Share of complaints closed with monetary relief, by product. Return product and pct (percent, 2 decimals).",
  "gold_sql": """SELECT product, ROUND(100.0 * SUM(CASE WHEN company_response = 'Closed with monetary relief' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct
                 FROM v_complaints GROUP BY product"""},
 {"q": "Which subissue under the issue 'Problem with a purchase shown on your statement' had the largest increase in complaint count from Q1 (Jan-Mar) to Q2 (Apr-Jun) 2026? Return only subissue.",
  "gold_sql": """SELECT subissue FROM (
                   SELECT subissue,
                          SUM(CASE WHEN date_received <  DATE '2026-04-01' THEN 1 ELSE 0 END) AS q1,
                          SUM(CASE WHEN date_received >= DATE '2026-04-01' THEN 1 ELSE 0 END) AS q2
                   FROM v_complaints WHERE issue = 'Problem with a purchase shown on your statement'
                   GROUP BY subissue) AS t
                 ORDER BY q2 - q1 DESC LIMIT 1"""},
]
UNANSWERABLE = [
 "Complaints per 100,000 residents by state.",   # Appendix A item 6: no population data in the view
]
