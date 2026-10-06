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
-- Original statement 2: Creación de la Base de Datos
-- DDLs
-- 1. SCHEMA CREATION
-- =============================================================================
-- Safely drop schema
DROP SCHEMA IF EXISTS maibd_bigdata_sys;

-- Create target schema with full UTF8 encoding support (only for MYSQL/MariaDB)
CREATE SCHEMA IF NOT EXISTS maibd_bigdata_sys 
  DEFAULT CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE maibd_bigdata_sys;

-- =============================================================================
-- Original statement 2: Crea una tabla llamada 'books', a.1, a.2, a.3
-- DDLs
-- 2. TABLE CREATION
-- =============================================================================
-- Safely drop table if re-running the script
DROP TABLE IF EXISTS ra_1_5_books;

-- Create main books catalog table with ra_1_5_ prefix
CREATE TABLE ra_1_5_books (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(128) NOT NULL,
  price DECIMAL(10, 2) NOT NULL
) ENGINE = InnoDB;

-- Index on title: Optimizes searches, filtering, and text lookups
CREATE INDEX idx_ra_1_5_books_title ON ra_1_5_books(title);
-- Explicit index on price column to optimize analytical queries
CREATE INDEX idx_ra_1_5_books_price ON ra_1_5_books(price);

-- =============================================================================
-- Original statement 3: Inserción de Datos, a
-- DML
-- DATA INSERTION
-- =============================================================================
-- Populate table with the full 20-book dataset retrieved from web scraper
INSERT INTO ra_1_5_books (title, price) VALUES
('A Light in the Attic', 51.77),
('Tipping the Velvet', 53.74),
('Soumission', 50.10),
('Sharp Objects', 47.82),
('Sapiens: A Brief History of Humankind', 54.23),
('The Requiem Red', 22.65),
('The Dirty Little Secrets of Getting Your Dream Job', 33.34),
('The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull', 17.93),
('The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics', 22.60),
('The Black Maria', 52.15),
('Starving Hearts (Triangular Trade Trilogy, #1)', 13.99),
('Shakespeare''s Sonnets', 20.66),
('Set Me Free', 17.46),
('Scott Pilgrim''s Precious Little Life (Scott Pilgrim #1)', 52.29),
('Rip it Up and Start Again', 35.02),
('Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991', 57.25),
('Olio', 23.88),
('Mesaerion: The Best Science Fiction Stories 1800-1849', 37.59),
('Libertarianism for Beginners', 51.33),
('It''s Only the Himalayas', 45.17);

-- =============================================================================
-- Original statement 5: Consultas SQL
-- DQL - ANALYTICAL QUERIES
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
-- ADVANCED CONSULTATION
-- =============================================================================
-- Query 5: Categorize each book as 'Expensive' or 'Cheap' relative to the average price
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