WITH book_stats AS (
  SELECT ROUND(AVG(price), 2) AS avg_price
  FROM ra_1_5_books
)
SELECT '---' AS title,
  s.avg_price AS price,
  'Precio medio' AS price_category
FROM book_stats AS s
UNION
SELECT b.title,
  b.price,
  CASE
    WHEN b.price = s.avg_price THEN 'Precio medio'
    WHEN b.price > s.avg_price THEN 'Caro (+' || ROUND((b.price - s.avg_price) / s.avg_price * 100, 2) || '%)'
    ELSE 'Barato (-' || ROUND((s.avg_price - b.price) / s.avg_price * 100, 2) || '%)'
  END AS price_category
FROM ra_1_5_books AS b
  CROSS JOIN book_stats AS s
ORDER BY title ASC;
--

WITH book_stats AS (
  SELECT AVG(price) AS avg_price
  FROM ra_1_5_books
)
SELECT title,  price,  price_category
FROM (
  SELECT 'Precio medio' AS title,
    s.avg_price AS price,
    '' AS price_category,
    0 AS sort_order
  FROM book_stats AS s
  UNION ALL
  SELECT b.title,
    b.price,
    CASE
      WHEN b.price = s.avg_price THEN 'Precio medio'
      WHEN b.price > s.avg_price THEN 'Caro (+' || CAST(
        ROUND((b.price - s.avg_price) / s.avg_price * 100, 2) AS CHAR(20)
      ) || '%)'
      ELSE 'Barato (-' || CAST(
        ROUND((s.avg_price - b.price) / s.avg_price * 100, 2) AS CHAR(20)
      ) || '%)'
    END AS price_category,
    1 AS sort_order
  FROM ra_1_5_books AS b
    CROSS JOIN book_stats AS s
) AS result
ORDER BY sort_order,
price DESC;