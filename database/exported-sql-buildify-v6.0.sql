-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: buildify
-- ------------------------------------------------------
-- Server version	8.4.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `carritos`
--

DROP TABLE IF EXISTS `carritos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carritos` (
  `id_carrito` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_carrito`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `carritos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carritos`
--

LOCK TABLES `carritos` WRITE;
/*!40000 ALTER TABLE `carritos` DISABLE KEYS */;
INSERT INTO `carritos` VALUES (2,7),(1,10);
/*!40000 ALTER TABLE `carritos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (4,'chasises'),(6,'fuente de poder'),(2,'memorias ram'),(7,'placas base'),(1,'procesadores'),(5,'refrigeraciones'),(3,'tarjetas graficas');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_chasises`
--

DROP TABLE IF EXISTS `detalles_chasises`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_chasises` (
  `id_producto` int NOT NULL,
  `formato_soportado` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `material` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `alto_mm` int DEFAULT NULL,
  `ancho_mm` int DEFAULT NULL,
  `profundidad_mm` int DEFAULT NULL,
  `peso_kg` decimal(5,2) DEFAULT NULL,
  `bahias_5_25` int DEFAULT '0',
  `bahias_3_5` int DEFAULT '0',
  `slots_expansion` int DEFAULT '0',
  `puertos_usb2` int DEFAULT '0',
  `puertos_usb3` int DEFAULT '0',
  `puerto_usb_c` int DEFAULT '0',
  `ventana_lateral` tinyint(1) DEFAULT '0',
  `refrigeracion_incluye` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rgb` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_chasises_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_chasises`
--

LOCK TABLES `detalles_chasises` WRITE;
/*!40000 ALTER TABLE `detalles_chasises` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalles_chasises` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_fuentes_poder`
--

DROP TABLE IF EXISTS `detalles_fuentes_poder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_fuentes_poder` (
  `id_producto` int NOT NULL,
  `potencia_w` int NOT NULL,
  `certificacion_80plus` enum('Bronze','Silver','Gold','Platinum','Titanium') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modularidad` enum('No modular','Semi-modular','Full modular') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_formato` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `voltaje_12v_a` decimal(6,2) DEFAULT NULL,
  `num_sata` int DEFAULT '0',
  `protecciones_ip` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ventilador_mm` int DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_fuentes_poder_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_fuentes_poder`
--

LOCK TABLES `detalles_fuentes_poder` WRITE;
/*!40000 ALTER TABLE `detalles_fuentes_poder` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalles_fuentes_poder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_memorias_ram`
--

DROP TABLE IF EXISTS `detalles_memorias_ram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_memorias_ram` (
  `id_producto` int NOT NULL,
  `capacidad_gb` int NOT NULL,
  `tipo_ram` enum('DDR3','DDR4','DDR5') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `velocidad_mhz` int NOT NULL,
  `voltaje_v` decimal(3,2) DEFAULT NULL,
  `rgb` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_memorias_ram_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_memorias_ram`
--

LOCK TABLES `detalles_memorias_ram` WRITE;
/*!40000 ALTER TABLE `detalles_memorias_ram` DISABLE KEYS */;
INSERT INTO `detalles_memorias_ram` VALUES (42,16,'DDR5',6000,2.00,1),(43,16,'DDR4',3200,1.00,0),(45,16,'DDR4',3200,1.00,0),(46,8,'DDR3',1600,1.00,0);
/*!40000 ALTER TABLE `detalles_memorias_ram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_placas_base`
--

DROP TABLE IF EXISTS `detalles_placas_base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_placas_base` (
  `id_producto` int NOT NULL,
  `socket` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `chipset` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `formato` enum('ATX','Micro-ATX','Mini-ITX','E-ATX') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `num_slots_ram` int NOT NULL,
  `max_ram_gb` int NOT NULL,
  `pcie_x16_slots` int DEFAULT '0',
  `pcie_x8_slots` int DEFAULT '0',
  `pcie_x4_slots` int DEFAULT '0',
  `num_m2_slots` int DEFAULT '0',
  `num_sata_ports` int DEFAULT '0',
  `usb2_0_traseros` int DEFAULT '0',
  `usb3_0_traseros` int DEFAULT '0',
  `usb3_1_typeC_traseros` int DEFAULT '0',
  `lan_gbps` decimal(3,1) DEFAULT NULL,
  `wifi_integrado` tinyint(1) DEFAULT '0',
  `bluetooth_integrado` tinyint(1) DEFAULT '0',
  `fases_vrm` int DEFAULT NULL,
  `audio_chipset` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rgb` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_placas_base_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_placas_base`
--

LOCK TABLES `detalles_placas_base` WRITE;
/*!40000 ALTER TABLE `detalles_placas_base` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalles_placas_base` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_procesadores`
--

DROP TABLE IF EXISTS `detalles_procesadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_procesadores` (
  `id_producto` int NOT NULL,
  `reloj_base_ghz` decimal(4,2) NOT NULL,
  `reloj_boost_ghz` decimal(4,2) DEFAULT NULL,
  `num_nucleos` int NOT NULL,
  `num_hilos` int NOT NULL,
  `tdp_w` int DEFAULT NULL,
  `cache_l2_mb` decimal(5,2) DEFAULT NULL,
  `cache_l3_mb` decimal(6,2) DEFAULT NULL,
  `gpu_integrado` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_procesadores_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_procesadores`
--

LOCK TABLES `detalles_procesadores` WRITE;
/*!40000 ALTER TABLE `detalles_procesadores` DISABLE KEYS */;
INSERT INTO `detalles_procesadores` VALUES (58,2.50,4.40,6,12,65,7.50,18.00,'NO');
/*!40000 ALTER TABLE `detalles_procesadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_refrigeraciones`
--

DROP TABLE IF EXISTS `detalles_refrigeraciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_refrigeraciones` (
  `id_producto` int NOT NULL,
  `tipo_refrigeracion` enum('Aire','Líquida') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `altura_mm` int DEFAULT NULL,
  `flujo_aire_cfm` decimal(6,2) DEFAULT NULL,
  `nivel_ruido_db` decimal(5,2) DEFAULT NULL,
  `socket_compatibles` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `radiador_mm` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bombas_rpm` int DEFAULT NULL,
  `conductos_material` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rgb` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_refrigeraciones_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_refrigeraciones`
--

LOCK TABLES `detalles_refrigeraciones` WRITE;
/*!40000 ALTER TABLE `detalles_refrigeraciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalles_refrigeraciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_tarjetas_graficas`
--

DROP TABLE IF EXISTS `detalles_tarjetas_graficas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_tarjetas_graficas` (
  `id_producto` int NOT NULL,
  `memoria_gb` int NOT NULL,
  `tipo_memoria` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bus_memoria_bits` int DEFAULT NULL,
  `reloj_base_ghz` decimal(7,2) DEFAULT NULL,
  `reloj_boost_ghz` decimal(7,2) DEFAULT NULL,
  `tdp_w` int DEFAULT NULL,
  `cuda_cores` int DEFAULT NULL,
  `longitud_mm` int DEFAULT NULL,
  `rgb` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_tarjetas_graficas_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_tarjetas_graficas`
--

LOCK TABLES `detalles_tarjetas_graficas` WRITE;
/*!40000 ALTER TABLE `detalles_tarjetas_graficas` DISABLE KEYS */;
INSERT INTO `detalles_tarjetas_graficas` VALUES (54,6,'GDDR6',96,0.00,-11492.00,70,2304,189,0),(55,12,'GDDR6',192,NULL,1777.00,NULL,3584,242,0),(56,8,'GDDR6',128,NULL,2355.00,550,2048,110,0);
/*!40000 ALTER TABLE `detalles_tarjetas_graficas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados`
--

DROP TABLE IF EXISTS `estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados` (
  `id_estado` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_estado`),
  UNIQUE KEY `estado` (`estado`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados`
--

LOCK TABLES `estados` WRITE;
/*!40000 ALTER TABLE `estados` DISABLE KEYS */;
INSERT INTO `estados` VALUES (6,'Cancelado'),(5,'Entregado'),(4,'Enviado'),(2,'Pendiente de envio'),(1,'Pendiente de pago'),(3,'Procesado');
/*!40000 ALTER TABLE `estados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facturas`
--

DROP TABLE IF EXISTS `facturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facturas` (
  `id_factura` varchar(255) NOT NULL,
  `id_pedido` int DEFAULT NULL,
  `numero_factura` varchar(100) NOT NULL,
  `factura_url_invoice_stripe` varchar(2083) NOT NULL,
  `factura_url_pdf_stripe` varchar(2083) DEFAULT NULL,
  `factura_url_pdf_cloud` varchar(2083) DEFAULT NULL,
  `total` bigint unsigned NOT NULL,
  `moneda` char(3) NOT NULL,
  PRIMARY KEY (`id_factura`),
  UNIQUE KEY `numero_factura` (`numero_factura`),
  KEY `id_pedido` (`id_pedido`),
  CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facturas`
--

LOCK TABLES `facturas` WRITE;
/*!40000 ALTER TABLE `facturas` DISABLE KEYS */;
INSERT INTO `facturas` VALUES ('in_1RxGEQPGZpDH0PL7KGsIm6NG',17,'QLKXK8WF-0005','https://invoice.stripe.com/i/acct_1RmkbLPGZpDH0PL7/test_YWNjdF8xUm1rYkxQR1pwREgwUEw3LF9TdDJKdnp0aGRoaTUwUjJjUlI2MG4wOWdNMTRJbUZ5LDE0NjAxNTAwNg0200dtdOhOgT?s=ap','https://pay.stripe.com/invoice/acct_1RmkbLPGZpDH0PL7/test_YWNjdF8xUm1rYkxQR1pwREgwUEw3LF9TdDJKdnp0aGRoaTUwUjJjUlI2MG4wOWdNMTRJbUZ5LDE0NjAxNTAwNg0200dtdOhOgT/pdf?s=ap',NULL,6000000,'cop'),('in_1RxUTmPGZpDH0PL7fghcCPsL',20,'QLKXK8WF-0008','https://invoice.stripe.com/i/acct_1RmkbLPGZpDH0PL7/test_YWNjdF8xUm1rYkxQR1pwREgwUEw3LF9TdEgxM3lmVklWcVo1U1dHbERzbkR4blo4eVhQVGQyLDE0NjA2OTc3Mg0200q41ccIWO?s=ap','https://pay.stripe.com/invoice/acct_1RmkbLPGZpDH0PL7/test_YWNjdF8xUm1rYkxQR1pwREgwUEw3LF9TdEgxM3lmVklWcVo1U1dHbERzbkR4blo4eVhQVGQyLDE0NjA2OTc3Mg0200q41ccIWO/pdf?s=ap','https://teufphonqxnnqckmkrfk.supabase.co/storage/v1/object/facturas/10/factura_in_1RxUTmPGZpDH0PL7fghcCPsL.pdf',6000000,'cop');
/*!40000 ALTER TABLE `facturas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favoritos`
--

DROP TABLE IF EXISTS `favoritos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favoritos` (
  `id_favorito` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_producto` int NOT NULL,
  PRIMARY KEY (`id_favorito`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `favoritos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `favoritos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favoritos`
--

LOCK TABLES `favoritos` WRITE;
/*!40000 ALTER TABLE `favoritos` DISABLE KEYS */;
/*!40000 ALTER TABLE `favoritos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagenes_producto`
--

DROP TABLE IF EXISTS `imagenes_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagenes_producto` (
  `id_imagen_producto` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `nombre_archivo` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `es_principal` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_imagen_producto`),
  KEY `imagenes_producto_ibfk_1` (`id_producto`),
  CONSTRAINT `imagenes_producto_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagenes_producto`
--

LOCK TABLES `imagenes_producto` WRITE;
/*!40000 ALTER TABLE `imagenes_producto` DISABLE KEYS */;
INSERT INTO `imagenes_producto` VALUES (7,42,'images/memorias ram/producto_42/Kingston_Fury_Beast_RGB.jpg',1),(8,42,'images/memorias ram/producto_42/Kingston_Fury_Beast_RGB-add.jpg',0),(9,43,'images/memorias ram/producto_43/Memoria_Ram_Kingston_Fury_Impact_DDR4_Modelo_KF432S20IB.webp',1),(10,43,'images/memorias ram/producto_43/Memoria_Ram_Kingston_Fury_Impact_DDR4_Modelo_KF432S20IB-add.webp',0),(12,45,'images/memorias ram/producto_45/Memoria_Ram_Puskill_Killblade_16GB_Cl22_PSK-D4D22M3200B-16G.webp',1),(13,45,'images/memorias ram/producto_45/Memoria_Ram_Puskill_Killblade_16GB_Cl22_PSK-D4D22M3200B-16G-add.webp',0),(14,46,'images/memorias ram/producto_46/Memoria_RAM_DDR3_8GB_Samsung_M471B1G73EB0-YK0.webp',0),(15,46,'images/memorias ram/producto_46/Memoria_RAM_DDR3_8GB_Samsung_M471B1G73EB0-YK0-2.webp',1),(20,54,'images/tarjetas graficas/producto_54/MSI_geforce_RTX_3050_Ventus_2x_6gb_DDR6.webp',1),(21,54,'images/tarjetas graficas/producto_54/MSI_geforce_RTX_3050_Ventus_2x_6gb_DDR6-2.webp',0),(22,55,'images/tarjetas graficas/producto_55/Nvidia_Zotac_Gaming_GeForce_RTX_30_Series_RTX_3060_ZT-A30600E-10M_12GB.webp',1),(23,55,'images/tarjetas graficas/producto_55/Nvidia_Zotac_Gaming_GeForce_RTX_30_Series_RTX_3060_ZT-A30600E-10M_12GB2.webp',0),(24,56,'images/tarjetas graficas/producto_56/Gigabyte_AMD_Radeon_Rx_7600_gAMING_oC_8gb_GDDR6.webp',1),(25,56,'images/tarjetas graficas/producto_56/Gigabyte_AMD_Radeon_Rx_7600_gAMING_oC_8gb_GDDR6-2.webp',0),(28,58,'images/procesadores/producto_58/Intel_Core_i5-12400F-1.webp',1),(29,58,'images/procesadores/producto_58/Intel_Core_i5-12400F-2.webp',0);
/*!40000 ALTER TABLE `imagenes_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items_carrito`
--

DROP TABLE IF EXISTS `items_carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items_carrito` (
  `id_carrito` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int NOT NULL,
  PRIMARY KEY (`id_carrito`,`id_producto`),
  KEY `items_carrito_ibfk_2` (`id_producto`),
  CONSTRAINT `items_carrito_ibfk_1` FOREIGN KEY (`id_carrito`) REFERENCES `carritos` (`id_carrito`),
  CONSTRAINT `items_carrito_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items_carrito`
--

LOCK TABLES `items_carrito` WRITE;
/*!40000 ALTER TABLE `items_carrito` DISABLE KEYS */;
INSERT INTO `items_carrito` VALUES (2,46,2);
/*!40000 ALTER TABLE `items_carrito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marcas`
--

DROP TABLE IF EXISTS `marcas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marcas` (
  `id_marca` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_marca`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marcas`
--

LOCK TABLES `marcas` WRITE;
/*!40000 ALTER TABLE `marcas` DISABLE KEYS */;
INSERT INTO `marcas` VALUES (2,'AMD'),(19,'Arctic'),(22,'ASRock'),(18,'be quiet!'),(14,'Cooler Master'),(3,'Corsair'),(6,'Crucial'),(20,'DeepCool'),(12,'EVGA'),(5,'G.Skill'),(10,'Gigabyte'),(1,'Intel'),(4,'Kingston'),(16,'Lian Li'),(9,'MSI'),(17,'Noctua'),(7,'Nvidia'),(13,'NZXT'),(24,'PUSKILL'),(25,'Samsung'),(21,'Seasonic'),(15,'Thermaltake'),(23,'XPG'),(11,'Zotac');
/*!40000 ALTER TABLE `marcas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marcas_categorias`
--

DROP TABLE IF EXISTS `marcas_categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marcas_categorias` (
  `id_marca_categoria` int NOT NULL AUTO_INCREMENT,
  `id_marca` int NOT NULL,
  `id_categoria` int NOT NULL,
  PRIMARY KEY (`id_marca_categoria`),
  KEY `id_marca` (`id_marca`),
  KEY `id_categoria` (`id_categoria`),
  CONSTRAINT `marcas_categorias_ibfk_1` FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id_marca`),
  CONSTRAINT `marcas_categorias_ibfk_2` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marcas_categorias`
--

LOCK TABLES `marcas_categorias` WRITE;
/*!40000 ALTER TABLE `marcas_categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `marcas_categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `fecha_pedido` timestamp NOT NULL,
  `fecha_entrega` timestamp NULL DEFAULT NULL,
  `valor_total` decimal(10,2) NOT NULL,
  `id_estado` int NOT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `id_usuario` (`id_usuario`),
  KEY `fk_estado_id` (`id_estado`),
  CONSTRAINT `fk_estado_id` FOREIGN KEY (`id_estado`) REFERENCES `estados` (`id_estado`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (2,10,'2025-07-23 05:00:00','2025-07-23 05:00:00',282000.00,1),(3,7,'2025-07-23 05:00:00','2025-07-23 05:00:00',60000.00,1),(4,10,'2025-07-25 05:00:00','2025-07-25 05:00:00',457000.00,1),(5,10,'2025-07-25 05:00:00','2025-07-25 05:00:00',1460000.00,1),(6,10,'2025-08-01 05:00:00','2025-08-01 05:00:00',600000.00,1),(7,10,'2025-08-01 05:00:00','2025-08-01 05:00:00',260000.00,1),(8,10,'2025-08-01 05:00:00','2025-08-01 05:00:00',175000.00,1),(9,10,'2025-08-02 12:29:53','2025-08-02 12:29:53',260000.00,1),(10,10,'2025-08-13 20:18:42','2025-08-13 20:18:42',3060000.00,1),(11,10,'2025-08-13 20:20:56','2025-08-13 20:20:56',344000.00,1),(12,10,'2025-08-13 20:23:15','2025-08-13 20:23:15',1795000.00,1),(13,10,'2025-08-16 19:09:35','2025-08-16 19:09:35',1940000.00,1),(14,10,'2025-08-16 21:26:06','2025-08-16 21:26:06',1260000.00,1),(15,10,'2025-08-16 21:35:05','2025-08-16 21:35:05',775000.00,1),(16,10,'2025-08-16 21:45:56','2025-08-16 21:45:56',60000.00,1),(17,10,'2025-08-17 23:43:00','2025-08-17 23:43:00',60000.00,1),(18,10,'2025-08-18 14:45:11','2025-08-18 14:45:11',60000.00,1),(19,10,'2025-08-18 14:50:00','2025-08-18 14:50:00',260000.00,1),(20,10,'2025-08-18 14:56:02','2025-08-18 14:56:02',60000.00,1);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `id_categoria` int NOT NULL,
  `id_marca` int NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id_producto`),
  KEY `fk_categoria` (`id_categoria`),
  KEY `fk_marca` (`id_marca`),
  CONSTRAINT `fk_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`),
  CONSTRAINT `fk_marca` FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id_marca`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (42,'Kingston Fury Beast RGB DDR5 6000mhz',260000.00,9,2,4,NULL),(43,'Kingston Fury Impact 16gb DDR4 3200MHZ',172000.00,28,2,4,NULL),(45,'Puskill Killblade 16 GB Cl22 PSK-D4D22M3200B-16G',141000.00,11,2,24,NULL),(46,'Samsung DDR3 8GB 1600mhz M471B1G73EB0-YK0',30000.00,18,2,25,NULL),(54,'Tarjeta Grafica Msi Geforce RTX 3050 Ventus 2x 6g Oc',970000.00,20,3,9,NULL),(55,'Nvidia Zotac GeForce Series RTX 3060 ZT-A30600E-10M 12GB',1795000.00,9,3,11,NULL),(56,'Gigabyte Amd Radeon Rx 7600 Gaming Oc 8g Gddr6',175000.00,18,3,10,NULL),(58,'Procesador Intel Core i5-12400F   6 núcleos y 4.4GHz ',600000.00,14,1,1,NULL);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_pedidos`
--

DROP TABLE IF EXISTS `productos_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_pedidos` (
  `id_producto_pedido` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int NOT NULL,
  PRIMARY KEY (`id_producto_pedido`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `productos_pedidos_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  CONSTRAINT `productos_pedidos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_pedidos`
--

LOCK TABLES `productos_pedidos` WRITE;
/*!40000 ALTER TABLE `productos_pedidos` DISABLE KEYS */;
INSERT INTO `productos_pedidos` VALUES (2,2,45,2),(3,3,46,2),(4,4,45,2),(5,4,56,1),(6,5,42,1),(7,5,58,2),(8,6,58,1),(9,7,42,1),(10,8,56,1),(11,9,42,1),(12,10,42,2),(13,10,54,2),(14,10,58,1),(15,11,43,2),(16,12,55,1),(17,13,54,2),(18,14,46,2),(19,14,58,2),(20,15,56,1),(21,15,58,1),(22,16,46,2),(23,17,46,2),(24,18,46,2),(25,19,42,1),(26,20,46,2);
/*!40000 ALTER TABLE `productos_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id_review` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `id_usuario` int NOT NULL,
  `estrellas` int NOT NULL,
  `comentario` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id_review`),
  KEY `id_producto` (`id_producto`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `reviews_chk_1` CHECK (((`estrellas` >= 1) and (`estrellas` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `rol` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'usuario'),(2,'moderador'),(3,'administrador');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `apellido` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `direccion` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `id_rol` int DEFAULT NULL,
  `stripe_customer_id` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `stripe_customer_id` (`stripe_customer_id`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (7,'Admin2','De Prueba','jose@example.com','Calle Falsa 123','123456789','scrypt:32768:8:1$ADa3l6daHgE8FXK0$c3e38a7412ac5d92ddfb0fae7b5e56975386d6380a853415ff94bf089ac032f17d653e08d37be99ce5623b3a24c1e670c743b3fdbd71661bd99598343fc208d2',3,NULL),(8,'Sarten Imusa','De Prueba Epica','example@email.com','un ejemplo de direccion#14','123456888','scrypt:32768:8:1$2lPSKEeovTSiWcnu$0f6376050d32f836b9596e56f3c2fbdcb0ef3fc5e5f47be4d605456b4630757699bd33e64617314611476eaa18e4c45ffb56f5c5be9a8c03a7432645335baa2b',1,NULL),(9,'Json','Jddd','je@example.com','CARRERA 18 #4A 46 APTO 401','300****303','scrypt:32768:8:1$RzSbVNtWgoj4QBon$7d770595c291d7abdcbebb21734da602895c465f09fe20a4c4557d9b7d102ab3884154bb8f870a3c524283792588164ecaf468e380afb3aa8f06b6f1f50b0899',1,NULL),(10,'David','Jitomate','ccairon29@gmail.com','CARRERA 18 #4A 46 APTO 401','3160429080','scrypt:32768:8:1$tg86xCm06vKeknyA$b09174f011b96c2147cb524da47d802302d0db748998cce5a7cb564edcb09d6b96970c59463a79e3de3212bd7abe781e343413f0c86f7327ae5abd1af0ee81be',1,'cus_SsafZLRXSqE3Lm'),(11,'Johan David','Acero','johanacero8@gmail.com','jsakdnaskj','3160429081','scrypt:32768:8:1$VSUgvcMPJMarPLja$537dbe58394c5cb334b648bd7e5a586a852da4310304123213cd098f1186c8d54197d0333953dfdf03deddb92f1ef34dc422f8758b40a8c95f8daac131a3baa5',1,NULL),(12,'Camila Andrea Olaya','Olaya Guevara','camilaolaya@gmail.com','Cra. 86f #49a Sur-1 a 49a Sur-55','3177744368','123456789',3,'cus_Ssa3ky7YvXWlAh');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-18 11:12:04
