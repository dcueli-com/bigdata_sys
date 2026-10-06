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
SELECT 'Most Expensive' AS category,
  title,
  price
FROM ra_1_5_books
WHERE price = (
    SELECT MAX(price)
    FROM ra_1_5_books
  )
UNION ALL
SELECT 'Cheapest' AS category,
  title,
  price
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
-- Original statement 5: Consulta Avanzada
-- DQLs
-- ADVANCED QUERY
-- =============================================================================
-- Crea una consulta que muestre el título del libro, su precio, y una columna
-- adicional que indique si el libro es "Barato" (menor al promedio) o "Caro" 
-- (mayor o igual al promedio).
SELECT title,
  price,
  CASE
    WHEN price >= (
      SELECT AVG(price)
      FROM ra_1_5_books
    ) THEN 'Expensive'
    ELSE 'Cheap'
  END AS price_category
FROM ra_1_5_books
ORDER BY price DESC;