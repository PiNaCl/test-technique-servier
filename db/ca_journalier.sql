SELECT date, SUM(prod_price * prod_qty) as ventes FROM transaction 

WHERE date >= '2019-01-01' AND date <= '2019-12-31'

GROUP BY date