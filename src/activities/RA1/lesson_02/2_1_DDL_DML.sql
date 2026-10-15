-- =============================================================================
-- @version     1.0.0
-- @author      dcueli 
-- @date        2026-10-06
-- @engine      MySQL
-- @dialect     ANSI SQL
-- @brief       
-- Master AI & Big Data
-- 26-27_1_1_M-IA_5074_Sistemas de Big Data
-- RA1/2/1
-- Original statement for the exercise:
-- -----------------------------------------------------------------------------
-- Una tienda online quiere mejorar su sistema de gestión de inventario y 
-- pedidos. Para ello se pide el diseño de un modelo conceptual que incluya 
-- las entidades principales (por ejemplo, Producto, Cliente, Pedido).
-- Basándote en el modelo conceptual, crea un modelo lógico detallando atributos 
-- y relaciones.
-- Finalmente, desarrolla un modelo físico para una base de datos relacional, 
-- especificando tipos de datos y claves.
-- -----------------------------------------------------------------------------
--
-- @Changelog
-- Date         Author      Description
-- ----------   ----------  ----------------------------------------------------
-- 2026-10-15   dcueli      Physical model DDL creation for RA1/2/1
-- -----------------------------------------------------------------------------
-- DDLs
-- 1. SCHEMA CREATION
-- =============================================================================
-- Safely drop schema
DROP SCHEMA IF EXISTS maibd_bigdata_sys_2_1;

-- Create target schema with full UTF8 encoding support (only for MYSQL/MariaDB)
CREATE SCHEMA IF NOT EXISTS maibd_bigdata_sys_2_1 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE maibd_bigdata_sys_2_1;

-- =====================================================================
-- 1. CATALOG & CLASSIFICATION SUBSYSTEM
-- =====================================================================
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  slug VARCHAR(32) UNIQUE NOT NULL,
  description TEXT NULL
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  sku VARCHAR(32) UNIQUE NOT NULL,
  name VARCHAR(128) NOT NULL,
  description TEXT NULL,
  base_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE product_categories (
  product_id INT NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (product_id, category_id),
  CONSTRAINT fk_pc_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  CONSTRAINT fk_pc_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- =====================================================================
-- 2. SUPPLIERS & PROCUREMENT SUBSYSTEM
-- =====================================================================
CREATE TABLE suppliers (
  id SERIAL PRIMARY KEY,
  fiscal_name VARCHAR(128) NOT NULL,
  tax_id VARCHAR(32) UNIQUE NOT NULL,
  contact_name VARCHAR(64) NULL,
  email VARCHAR(64) NULL
);

-- =====================================================================
-- 3. COMMERCIAL & CUSTOMER SUBSYSTEM
-- =====================================================================
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(64) NOT NULL,
  last_name VARCHAR(64) NOT NULL,
  email VARCHAR(64) UNIQUE NOT NULL,
  phone VARCHAR(32) NULL
);

CREATE TABLE sales (
  id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(32) NOT NULL,
  -- e.g., 'PAID', 'SHIPPED', 'COMPLETED'
  CONSTRAINT fk_sale_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- =====================================================================
-- 4. LOGISTICS SUBSYSTEM (WAREHOUSES, TRANSFERS & AUDITS)
-- =====================================================================
CREATE TABLE warehouses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  location VARCHAR(128) NOT NULL
);

CREATE TABLE purchases (
  id SERIAL PRIMARY KEY,
  supplier_id INT NOT NULL,
  warehouse_id INT NOT NULL,
  purchase_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(32) NOT NULL,
  -- e.g., 'PENDING', 'RECEIVED', 'CANCELLED'
  CONSTRAINT fk_purchase_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
  CONSTRAINT fk_purchase_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

CREATE TABLE transfers (
  id SERIAL PRIMARY KEY,
  warehouse_out_id INT NOT NULL,
  warehouse_in_id INT NOT NULL,
  transfer_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_transfer_warehouse_out FOREIGN KEY (warehouse_out_id) REFERENCES warehouses(id),
  CONSTRAINT fk_transfer_warehouse_in FOREIGN KEY (warehouse_in_id) REFERENCES warehouses(id)
);

CREATE TABLE inventories (
  id SERIAL PRIMARY KEY,
  warehouse_id INT NOT NULL,
  audit_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  notes TEXT NULL,
  CONSTRAINT fk_inventory_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- =====================================================================
-- 5. CORE LEDGER: stock_moves (MOVEMENT LEDGER)
-- =====================================================================
CREATE TABLE stock_moves (
  id SERIAL PRIMARY KEY,
  warehouse_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  -- Positive for inflows, negative for outflows
  movement_type VARCHAR(32) NOT NULL,
  -- 'SALE', 'PURCHASE', 'TRANSFER_OUT', 'TRANSFER_IN', 'INVENTORY_ADJUSTMENT'
  sale_id INT NULL,
  purchase_id INT NULL,
  transfer_id INT NULL,
  movement_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_stock_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
  CONSTRAINT fk_stock_product FOREIGN KEY (product_id) REFERENCES products(id),
  CONSTRAINT fk_stock_sale FOREIGN KEY (sale_id) REFERENCES sales(id),
  CONSTRAINT fk_stock_purchase FOREIGN KEY (purchase_id) REFERENCES purchases(id),
  CONSTRAINT fk_stock_transfer FOREIGN KEY (transfer_id) REFERENCES transfers(id)
);