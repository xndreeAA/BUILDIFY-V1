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
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `formato_soportado` varchar(50) DEFAULT NULL,
  `material` varchar(50) DEFAULT NULL,
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
  `refrigeracion_incluye` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_chasises_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_chasises`
--

LOCK TABLES `detalles_chasises` WRITE;
/*!40000 ALTER TABLE `detalles_chasises` DISABLE KEYS */;
INSERT INTO `detalles_chasises` VALUES (17,'ATX/Micro-ATX','Acero',478,209,473,7.20,2,2,7,0,2,0,0,'—'),(18,'Open Frame ATX','Acero/Templado',589,343,450,13.30,2,2,8,0,2,0,1,'No fans'),(19,'ATX','Acero/Templado',453,230,466,8.60,2,3,7,0,2,1,1,'2×120mm fans');
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
  `certificacion_80plus` enum('Bronze','Silver','Gold','Platinum','Titanium') DEFAULT NULL,
  `modularidad` enum('No modular','Semi-modular','Full modular') DEFAULT NULL,
  `tipo_formato` varchar(20) DEFAULT NULL,
  `voltaje_12v_a` decimal(6,2) DEFAULT NULL,
  `num_conectores_24pin` int DEFAULT '1',
  `num_conectores_8pin` int DEFAULT '0',
  `num_sata` int DEFAULT '0',
  `num_molex` int DEFAULT '0',
  `protecciones_ip` varchar(100) DEFAULT NULL,
  `ventilador_mm` int DEFAULT NULL,
  `ruido_max_db` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_fuentes_poder_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_fuentes_poder`
--

LOCK TABLES `detalles_fuentes_poder` WRITE;
/*!40000 ALTER TABLE `detalles_fuentes_poder` DISABLE KEYS */;
INSERT INTO `detalles_fuentes_poder` VALUES (25,650,'Gold','Full modular','ATX',54.00,1,2,6,2,'OVP,UVP,OPP,SCP',120,20.00),(26,750,'Gold','Full modular','ATX',62.00,1,2,8,2,'OVP,UVP,OPP,SCP,OTP',135,18.50),(27,600,'Bronze','No modular','ATX',48.00,1,1,4,2,'OVP,UVP,OPP,SCP',120,22.00),(28,850,'Gold','Full modular','ATX',70.00,1,2,8,2,'OVP,UVP,OPP,SCP,OTP',140,19.00),(29,650,'Gold','Semi-modular','ATX',54.00,1,1,6,2,'OVP,UVP,OPP,SCP',120,21.00);
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
  `tipo_ram` enum('DDR3','DDR4','DDR5') NOT NULL,
  `velocidad_mhz` int NOT NULL,
  `num_modulos` int NOT NULL,
  `voltaje_v` decimal(3,2) DEFAULT NULL,
  `cl_latencia` varchar(10) DEFAULT NULL,
  `ecc` tinyint(1) DEFAULT '0',
  `perfil_xmp` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_memorias_ram_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_memorias_ram`
--

LOCK TABLES `detalles_memorias_ram` WRITE;
/*!40000 ALTER TABLE `detalles_memorias_ram` DISABLE KEYS */;
INSERT INTO `detalles_memorias_ram` VALUES (6,16,'DDR4',3200,2,1.35,'CL16',0,1),(7,16,'DDR4',3600,2,1.35,'CL18',0,1),(8,16,'DDR4',2400,2,1.20,'CL15',0,0),(9,32,'DDR4',3200,2,1.35,'CL16',0,1),(10,32,'DDR5',5200,2,1.25,'CL38',0,1);
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
  `socket` varchar(20) NOT NULL,
  `chipset` varchar(50) NOT NULL,
  `formato` enum('ATX','Micro-ATX','Mini-ITX','E-ATX') DEFAULT NULL,
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
  `audio_chipset` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_placas_base_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_placas_base`
--

LOCK TABLES `detalles_placas_base` WRITE;
/*!40000 ALTER TABLE `detalles_placas_base` DISABLE KEYS */;
INSERT INTO `detalles_placas_base` VALUES (30,'LGA1700','Z690','ATX',4,128,2,0,1,3,6,2,4,1,2.5,1,1,16,'SupremeFX'),(31,'AM4','B550','ATX',4,128,2,0,1,2,6,2,2,1,2.5,0,0,12,'Realtek ALC892'),(32,'AM4','X570','ATX',4,128,3,0,1,2,6,2,2,1,2.5,0,0,14,'Realtek ALC1220'),(33,'LGA1700','B660','Micro-ATX',4,128,1,0,1,1,6,2,2,1,1.0,0,0,10,'Realtek ALC887'),(34,'LGA1700','Z690','E-ATX',4,128,3,0,2,4,8,2,6,2,2.5,1,1,20,'Realtek ALC4080');
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
  `socket` varchar(20) DEFAULT NULL,
  `litografia_nm` int DEFAULT NULL,
  `cache_l2_mb` decimal(5,2) DEFAULT NULL,
  `cache_l3_mb` decimal(6,2) DEFAULT NULL,
  `gpu_integrado` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_procesadores_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_procesadores`
--

LOCK TABLES `detalles_procesadores` WRITE;
/*!40000 ALTER TABLE `detalles_procesadores` DISABLE KEYS */;
INSERT INTO `detalles_procesadores` VALUES (1,3.70,4.90,10,16,125,'LGA1700',10,9.50,20.00,'Intel UHD 770');
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
  `tipo_refrigeracion` enum('Aire','Líquida') NOT NULL,
  `altura_mm` int DEFAULT NULL,
  `ventilador_mm` int DEFAULT NULL,
  `flujo_aire_cfm` decimal(6,2) DEFAULT NULL,
  `nivel_ruido_db` decimal(5,2) DEFAULT NULL,
  `socket_compatibles` varchar(100) DEFAULT NULL,
  `radiador_mm` varchar(20) DEFAULT NULL,
  `bombas_rpm` int DEFAULT NULL,
  `conductos_material` varchar(50) DEFAULT NULL,
  `peso_kg` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_refrigeraciones_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_refrigeraciones`
--

LOCK TABLES `detalles_refrigeraciones` WRITE;
/*!40000 ALTER TABLE `detalles_refrigeraciones` DISABLE KEYS */;
INSERT INTO `detalles_refrigeraciones` VALUES (20,'Aire',165,140,82.50,24.60,'AM4,LGA1151,LGA1200',NULL,NULL,'Cobre',1.32),(21,'Líquida',NULL,120,75.00,36.00,'AM4,LGA1200','240x120',3000,'Cobre',1.22),(22,'Líquida',NULL,140,73.11,21.00,'AM4,LGA1700','280x140',2200,'Aluminio',1.54),(23,'Aire',163,120,82.80,24.30,'LGA1151,LGA1200,AM4',NULL,NULL,'Cobre',1.10),(24,'Aire',155,120,63.50,27.80,'LGA1151,LGA1200,AM4',NULL,NULL,'Aluminio',0.70);
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
  `chipset` varchar(50) NOT NULL,
  `memoria_gb` int NOT NULL,
  `tipo_memoria` varchar(20) DEFAULT NULL,
  `bus_memoria_bits` int DEFAULT NULL,
  `reloj_base_ghz` decimal(5,2) DEFAULT NULL,
  `reloj_boost_ghz` decimal(5,2) DEFAULT NULL,
  `tdp_w` int DEFAULT NULL,
  `pcie_version` varchar(10) DEFAULT NULL,
  `cuda_cores` int DEFAULT NULL,
  `long_mm` int DEFAULT NULL,
  `altura_mm` int DEFAULT NULL,
  `espesor_slots` decimal(3,1) DEFAULT NULL,
  `conector_6pin` int DEFAULT '0',
  `conector_8pin` int DEFAULT '0',
  `sli_xfire_soporte` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `detalles_tarjetas_graficas_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_tarjetas_graficas`
--

LOCK TABLES `detalles_tarjetas_graficas` WRITE;
/*!40000 ALTER TABLE `detalles_tarjetas_graficas` DISABLE KEYS */;
INSERT INTO `detalles_tarjetas_graficas` VALUES (11,'GA106',12,'GDDR6',192,1.32,1.78,170,'PCIe 4.0',3584,242,112,2.0,0,1,0),(12,'Navi 22',12,'GDDR6',192,2.32,2.58,230,'PCIe 4.0',NULL,267,120,2.5,0,1,0),(13,'GA102',10,'GDDR6X',320,1.44,1.71,320,'PCIe 4.0',8704,318,137,2.7,0,2,0),(14,'GA104',8,'GDDR6',256,1.50,1.73,220,'PCIe 4.0',5888,242,112,2.0,0,2,0),(15,'Navi 21',16,'GDDR6',256,1.70,2.10,250,'PCIe 4.0',NULL,300,125,2.8,0,2,0);
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
  `estado` varchar(100) NOT NULL,
  PRIMARY KEY (`id_estado`),
  UNIQUE KEY `estado` (`estado`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  CONSTRAINT `favoritos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favoritos`
--

LOCK TABLES `favoritos` WRITE;
/*!40000 ALTER TABLE `favoritos` DISABLE KEYS */;
/*!40000 ALTER TABLE `favoritos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marcas`
--

DROP TABLE IF EXISTS `marcas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marcas` (
  `id_marca` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id_marca`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marcas`
--

LOCK TABLES `marcas` WRITE;
/*!40000 ALTER TABLE `marcas` DISABLE KEYS */;
INSERT INTO `marcas` VALUES (2,'AMD'),(19,'Arctic'),(22,'ASRock'),(8,'ASUS'),(18,'be quiet!'),(14,'Cooler Master'),(3,'Corsair'),(6,'Crucial'),(20,'DeepCool'),(12,'EVGA'),(5,'G.Skill'),(10,'Gigabyte'),(1,'Intel'),(4,'Kingston'),(16,'Lian Li'),(9,'MSI'),(17,'Noctua'),(7,'Nvidia'),(13,'NZXT'),(21,'Seasonic'),(15,'Thermaltake'),(11,'Zotac');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `id_categoria` int NOT NULL,
  `id_marca` int NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `fk_categoria` (`id_categoria`),
  KEY `fk_marca` (`id_marca`),
  CONSTRAINT `fk_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`),
  CONSTRAINT `fk_marca` FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id_marca`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Intel Core i5-12600K',289.99,50,1,1,'i5-12600K.jpg'),(2,'Intel Core i7-12700K',409.99,30,1,1,'i7-12700K.jpg'),(3,'AMD Ryzen 5 5600X',199.99,60,1,2,'ryzen5-5600x.jpg'),(4,'AMD Ryzen 7 5800X',329.99,40,1,2,'ryzen7-5800x.jpg'),(5,'Intel Core i9-12900K',589.99,25,1,1,'i9-12900K.jpg'),(6,'Corsair Vengeance LPX 16GB (2x8) DDR4-3200',79.99,100,2,3,'vengeance-16gb-3200.jpg'),(7,'G.Skill Trident Z RGB 16GB (2x8) DDR4-3600',109.99,80,2,5,'tridentz-16gb-3600.jpg'),(8,'Kingston HyperX Fury 16GB (2x8) DDR4-2400',69.99,120,2,4,'hx-fury-16gb-2400.jpg'),(9,'Crucial Ballistix 32GB (2x16) DDR4-3200',159.99,70,2,6,'ballistix-32gb-3200.jpg'),(10,'Corsair Dominator Platinum RGB 32GB (2x16) DDR5-5200',299.99,40,2,3,'dominator-32gb-ddr5.jpg'),(11,'Nvidia GeForce RTX 3060',329.99,60,3,7,'rtx3060.jpg'),(12,'AMD Radeon RX 6700 XT',479.99,45,3,2,'rx6700xt.jpg'),(13,'ASUS ROG Strix RTX 3080',699.99,30,3,8,'strix-3080.jpg'),(14,'MSI Ventus RTX 3070',499.99,35,3,9,'ventus-3070.jpg'),(15,'Gigabyte AORUS RX 6800',579.99,25,3,10,'aorus-rx6800.jpg'),(16,'NZXT H510',69.99,80,4,13,'h510.jpg'),(17,'Cooler Master MasterBox NR600',79.99,60,4,14,'nr600.jpg'),(18,'Thermaltake Core P3',129.99,40,4,15,'core-p3.jpg'),(19,'Corsair 4000D Airflow',94.99,70,4,3,'4000d.jpg'),(20,'Noctua NH-D15',89.99,50,5,17,'nh-d15.jpg'),(21,'Corsair H100i RGB Platinum',159.99,40,5,3,'h100i.jpg'),(22,'NZXT Kraken X63',159.99,45,5,13,'kraken-x63.jpg'),(23,'be quiet! Dark Rock Pro 4',89.99,35,5,18,'darkrock-pro4.jpg'),(24,'DeepCool Gammaxx 400',29.99,70,5,20,'gammaxx-400.jpg'),(25,'Seasonic Focus GX-650',119.99,60,6,21,'focus-gx-650.jpg'),(26,'Corsair RM750x',129.99,50,6,3,'rm750x.jpg'),(27,'EVGA 600 BR',59.99,80,6,12,'600-br.jpg'),(28,'Thermaltake Toughpower GF1 850W',139.99,40,6,15,'toughpower-850w.jpg'),(29,'Cooler Master MWE Gold 650',89.99,70,6,14,'mwe-gold-650.jpg'),(30,'ASUS ROG Strix Z690-E',379.99,30,7,8,'strix-z690e.jpg'),(31,'MSI MAG B550 Tomahawk',179.99,45,7,9,'b550-tomahawk.jpg'),(32,'Gigabyte X570 AORUS Elite',199.99,40,7,10,'x570-aorus.jpg'),(33,'ASRock B660M Pro RS',129.99,50,7,22,'b660m-pro.jpg'),(34,'MSI MEG Z690 Unify',409.99,20,7,9,'meg-z690-unify.jpg');
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
  CONSTRAINT `productos_pedidos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `comentario` text,
  PRIMARY KEY (`id_review`),
  KEY `id_producto` (`id_producto`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `reviews_chk_1` CHECK (((`estrellas` >= 1) and (`estrellas` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `rol` varchar(100) NOT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `password` varchar(100) NOT NULL,
  `id_rol` int DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Jose David','Junco Navarro','josewjjunco@gmail.com','Carrera 18# 4A-46','3160429080','123456789',3),(2,'Camila Andrea','Olaya Guevara','camilaolayaguevara@gmail.com','Cra. 86f #49a Sur-1 a 49a Sur-55','3177744368','123456789',3),(3,'Dayana Andrea','Zuñiga Tumba','andreazutum@gmail.com','Cl. 52F Sur #24-20','3202562695','123456789',3),(4,'Jeison Alejandro','Gutierrez Barajas','jeisonalejandrogutierrezbaraja@gmail.com','Calle 18 # 4-46','3219026083','123456789',3),(5,'John Doe','Doe','johndoe@gmail','Calle 1 # 1-1','3000000000','123456789',1),(6,'Jane Doe','Doe Second','janedoe@gmail','Calle 2 # 2-2','3000000001','123456789',2);
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

-- Dump completed on 2025-05-25 22:27:53
