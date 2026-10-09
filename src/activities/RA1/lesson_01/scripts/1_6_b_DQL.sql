-- =============================================================================
-- @version     1.0.0
-- @author      dcueli 
-- @date        2026-10-06
-- @engine      MySQL
-- @dialect     ANSI SQL
-- @brief       
-- Master AI & Big Data
-- 26-27_1_1_M-IA_5074_Sistemas de Big Data
-- RA1/1/06
-- Database schema creation and analytical queries for books dataset.
-- Original statement for the exercise:
-- -----------------------------------------------------------------------------
-- 1.	Acceso al Compilador SQL en línea:
--    - Visita https://www.programiz.com/sql/online-compiler/
-- 2.	Creación de la Base de Datos:
--    a. Crea una tabla llamada 'books' con las siguientes columnas:
--       a.1 id (INTEGER, clave primaria, autoincremento)
--       a.2 title (TEXT)
--       a.3 price (DECIMAL(10,2))
-- 3.	Inserción de Datos:
--    a. Inserta al menos 10 libros en la tabla 'books' utilizando los datos 
--       obtenidos del web scraping, si no lo has conseguido puedes poner propios
-- 4.	Consultas SQL:
--    Realiza las siguientes consultas:
--      a. Selecciona todos los libros y muéstralos ordenados por precio de 
--         forma descendente
--      b. Calcula el precio promedio de todos los libros.
--      c. Encuentra el libro más caro y el más barato.
--      d. Cuenta cuántos libros tienen un precio superior a $50.
--      e. Selecciona los títulos de los 5 libros más baratos.
--      f. Calcula el precio total de todos los libros en la base de datos.
-- 5.	Consulta Avanzada:
--    a. Crea una consulta que muestre el título del libro, su precio, y una 
--       columna adicional que indique si el libro es "Barato" (menor al 
--       promedio) o "Caro" (mayor o igual al promedio).
-- -----------------------------------------------------------------------------
--
-- @Changelog
-- Date         Author      Description
-- ----------   ----------  ----------------------------------------------------
-- 2026-10-06   dcueli      Initial creation of the SQL script for RA1/1/6
-- =============================================================================
-- Original statement 4: Consultas SQL
-- DQLs
-- 1. ANALYTICAL QUERIES
-- =============================================================================
-- 5.a. Selecciona todos los libros y muéstralos ordenados por precio de forma 
--      descendente
SELECT id,
  title,
  price
FROM ra_1_5_books
ORDER BY price DESC;

-- 5.b. Calcula el precio promedio de todos los libros.
SELECT ROUND(AVG(price), 2) AS average_price
FROM ra_1_5_books;

-- 5.c. Encuentra el libro más caro y el más barato.
SELECT 'Most Expensive' AS category, id, title, price
FROM ra_1_5_books
WHERE price = (
    SELECT MAX(price)
    FROM ra_1_5_books
  )
UNION ALL
SELECT 'Cheapest' AS category, id, title, price
FROM ra_1_5_books
WHERE price = (
    SELECT MIN(price)
    FROM ra_1_5_books
  );

-- 5.d. Cuenta cuántos libros tienen un precio superior a $50.
SELECT COUNT(*) AS total_books_over_50
FROM ra_1_5_books
WHERE price > 50.00;

-- 5.e. Selecciona los títulos de los 5 libros más baratos
SELECT title,
  price
FROM ra_1_5_books
ORDER BY price ASC
LIMIT 5;

-- 5.f. Calcula el precio total de todos los libros en la base de datos
SELECT ROUND(SUM(price), 2) AS total_catalog_price
FROM ra_1_5_books;

-- =============================================================================
-- DQLs
-- Original statement 5: Consulta Avanzada
-- Crea una consulta que muestre el título del libro, su precio, y una columna
-- adicional que indique si el libro es "Barato" (menor al promedio) o "Caro" 
-- (mayor o igual al promedio).
-- ADVANCED QUERY
-- =============================================================================
SELECT title, price,
  CASE
    WHEN price >= (
      SELECT AVG(price)
      FROM ra_1_5_books
    ) THEN 'Expensive'
    ELSE 'Cheap'
  END AS price_category
FROM ra_1_5_books
ORDER BY price DESC;

-- My version of the advanced query with a Common Table Expression (CTE, ANSI SQL)
-- 
-- To add more value, we can also include the average price in the result set 
-- and categorize each book as "Barato" or "Caro" based on its price relative
-- to the average.
-- This provides a clearer context for the pricing of each book.
-- [OPTIONAL] EXPLAIN ANALYZE 
WITH book_stats AS (
  SELECT ROUND(AVG(price), 2) AS avg_price
  FROM ra_1_5_books
)
SELECT title,  price,  price_category
FROM (
  SELECT '' AS title,
    s.avg_price AS price,
    'Precio medio' AS price_category,
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