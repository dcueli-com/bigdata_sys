SELECT 'Precio medio' AS title, s.avg_price AS price, NULL AS price_category
UNION
WITH book_stats AS (
  SELECT AVG(price) AS avg_price
  FROM ra_1_5_books
)
SELECT title, price,
  CASE
    WHEN price = s.avg_price THEN 'Precio medio'
    WHEN price > s.avg_price THEN CONCAT(
      'Caro (+',
      ROUND((price - s.avg_price) / s.avg_price * 100, 2),
      '%)'
    )
    ELSE CONCAT(
      'Barato (-',
      ROUND((s.avg_price - price) / s.avg_price * 100, 2),
      '%)'
    )
  END AS price_category
FROM ra_1_5_books
  JOIN book_stats s
ORDER BY price DESC;

SELECT title,
  price,
  CASE
    WHEN price = s.avg_price THEN 'Precio medio'
    WHEN price > s.avg_price THEN CONCAT(
      'Caro (+',
      ROUND((price - s.avg_price) / s.avg_price * 100, 2),
      '%)'
    )
    ELSE CONCAT(
      'Barato (-',
      ROUND((s.avg_price - price) / s.avg_price * 100, 2),
      '%)'
    )
  END AS price_category
FROM ra_1_5_books
  JOIN (
    SELECT AVG(price) AS avg_price
    FROM ra_1_5_books
  ) AS s
ORDER BY price DESC;