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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carritos`
--

LOCK TABLES `carritos` WRITE;
/*!40000 ALTER TABLE `carritos` DISABLE KEYS */;
INSERT INTO `carritos` VALUES (1,10);
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
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
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
  `formato_soportado` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `material` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `refrigeracion_incluye` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `certificacion_80plus` enum('Bronze','Silver','Gold','Platinum','Titanium') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modularidad` enum('No modular','Semi-modular','Full modular') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_formato` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `voltaje_12v_a` decimal(6,2) DEFAULT NULL,
  `num_sata` int DEFAULT '0',
  `protecciones_ip` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `tipo_ram` enum('DDR3','DDR4','DDR5') COLLATE utf8mb4_general_ci NOT NULL,
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
  `socket` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `chipset` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `formato` enum('ATX','Micro-ATX','Mini-ITX','E-ATX') COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `audio_chipset` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `gpu_integrado` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `tipo_refrigeracion` enum('Aire','Líquida') COLLATE utf8mb4_general_ci NOT NULL,
  `altura_mm` int DEFAULT NULL,
  `flujo_aire_cfm` decimal(6,2) DEFAULT NULL,
  `nivel_ruido_db` decimal(5,2) DEFAULT NULL,
  `socket_compatibles` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `radiador_mm` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bombas_rpm` int DEFAULT NULL,
  `conductos_material` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `tipo_memoria` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
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
INSERT INTO `detalles_tarjetas_graficas` VALUES (54,6,'GDDR6',96,NULL,-11492.00,70,2304,189,0),(55,12,'GDDR6',192,NULL,1777.00,NULL,3584,242,0),(56,8,'GDDR6',128,NULL,2355.00,550,2048,110,0);
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
  `estado` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
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
  `nombre_archivo` varchar(255) NOT NULL,
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
INSERT INTO `items_carrito` VALUES (1,42,1);
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
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
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
  `fecha_pedido` date NOT NULL,
  `fecha_entrega` date NOT NULL,
  `valor_total` decimal(10,2) NOT NULL,
  `id_estado` int NOT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `id_usuario` (`id_usuario`),
  KEY `fk_estado_id` (`id_estado`),
  CONSTRAINT `fk_estado_id` FOREIGN KEY (`id_estado`) REFERENCES `estados` (`id_estado`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
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
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `id_categoria` int NOT NULL,
  `id_marca` int NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
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
INSERT INTO `productos` VALUES (42,'Kingston Fury Beast RGB DDR5 6000mhz',260000.00,15,2,4,NULL),(43,'Kingston Fury Impact 16gb DDR4 3200MHZ',172000.00,30,2,4,NULL),(45,'Puskill Killblade 16 GB Cl22 PSK-D4D22M3200B-16G',141000.00,15,2,24,NULL),(46,'Samsung DDR3 8GB 1600mhz M471B1G73EB0-YK0',30000.00,10,2,25,NULL),(54,'Tarjeta Grafica Msi Geforce RTX 3050 Ventus 2x 6g Oc',970000.00,5,3,9,NULL),(55,'Nvidia Zotac GeForce Series RTX 3060 ZT-A30600E-10M 12GB',1795000.00,10,3,11,NULL),(56,'Gigabyte Amd Radeon Rx 7600 Gaming Oc 8g Gddr6',175000.00,21,3,10,NULL),(58,'Procesador Intel Core i5-12400F   6 núcleos y 4.4GHz ',600000.00,21,1,1,NULL);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_pedidos`
--

LOCK TABLES `productos_pedidos` WRITE;
/*!40000 ALTER TABLE `productos_pedidos` DISABLE KEYS */;
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
  `comentario` text COLLATE utf8mb4_general_ci,
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
  `rol` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
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
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `direccion` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `id_rol` int DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (7,'Admin2','De Prueba','jose@example.com','Calle Falsa 123','123456789','scrypt:32768:8:1$ADa3l6daHgE8FXK0$c3e38a7412ac5d92ddfb0fae7b5e56975386d6380a853415ff94bf089ac032f17d653e08d37be99ce5623b3a24c1e670c743b3fdbd71661bd99598343fc208d2',3),(8,'Sarten Imusa','De Prueba Epica','example@email.com','un ejemplo de direccion#14','123456888','scrypt:32768:8:1$2lPSKEeovTSiWcnu$0f6376050d32f836b9596e56f3c2fbdcb0ef3fc5e5f47be4d605456b4630757699bd33e64617314611476eaa18e4c45ffb56f5c5be9a8c03a7432645335baa2b',1),(9,'Json','Jddd','je@example.com','CARRERA 18 #4A 46 APTO 401','300****303','scrypt:32768:8:1$RzSbVNtWgoj4QBon$7d770595c291d7abdcbebb21734da602895c465f09fe20a4c4557d9b7d102ab3884154bb8f870a3c524283792588164ecaf468e380afb3aa8f06b6f1f50b0899',1),(10,'David','Jitomate','ccairon29@gmail.com','CARRERA 18 #4A 46 APTO 401','3160429080','scrypt:32768:8:1$tg86xCm06vKeknyA$b09174f011b96c2147cb524da47d802302d0db748998cce5a7cb564edcb09d6b96970c59463a79e3de3212bd7abe781e343413f0c86f7327ae5abd1af0ee81be',1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'buildify'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-15 17:23:25
