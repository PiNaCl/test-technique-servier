SELECT  transaction.client_id, 
        SUM(
            CASE WHEN product_type = 'MEUBLE' THEN transaction.prod_price * transaction.prod_qty ELSE 0 END
        ) AS ventes_meuble,
        SUM(
            CASE WHEN product_type = 'DECO' THEN transaction.prod_price * transaction.prod_qty ELSE 0 END
        ) AS ventes_deco
FROM transaction
LEFT JOIN product_nomenclature ON (transaction.prop_id = product_nomenclature.product_id)

WHERE
    date >= '2019-01-01'
    AND date <= '2019-12-31' 
    AND product_nomenclature.product_type IN ('MEUBLE', 'DECO')

GROUP BY transaction.client_id
