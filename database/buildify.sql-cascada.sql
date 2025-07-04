-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-07-2025 a las 07:52:48
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `buildify`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre`) VALUES
(4, 'chasises'),
(6, 'fuente de poder'),
(2, 'memorias ram'),
(7, 'placas base'),
(1, 'procesadores'),
(5, 'refrigeraciones'),
(3, 'tarjetas graficas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_chasises`
--

CREATE TABLE `detalles_chasises` (
  `id_producto` int(11) NOT NULL,
  `formato_soportado` varchar(50) DEFAULT NULL,
  `material` varchar(50) DEFAULT NULL,
  `alto_mm` int(11) DEFAULT NULL,
  `ancho_mm` int(11) DEFAULT NULL,
  `profundidad_mm` int(11) DEFAULT NULL,
  `peso_kg` decimal(5,2) DEFAULT NULL,
  `bahias_5_25` int(11) DEFAULT 0,
  `bahias_3_5` int(11) DEFAULT 0,
  `slots_expansion` int(11) DEFAULT 0,
  `puertos_usb2` int(11) DEFAULT 0,
  `puertos_usb3` int(11) DEFAULT 0,
  `puerto_usb_c` int(11) DEFAULT 0,
  `ventana_lateral` tinyint(1) DEFAULT 0,
  `refrigeracion_incluye` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_chasises`
--

INSERT INTO `detalles_chasises` (`id_producto`, `formato_soportado`, `material`, `alto_mm`, `ancho_mm`, `profundidad_mm`, `peso_kg`, `bahias_5_25`, `bahias_3_5`, `slots_expansion`, `puertos_usb2`, `puertos_usb3`, `puerto_usb_c`, `ventana_lateral`, `refrigeracion_incluye`) VALUES
(17, 'ATX/Micro-ATX', 'Acero', 478, 209, 473, 7.20, 2, 2, 7, 0, 2, 0, 0, '—'),
(18, 'Open Frame ATX', 'Acero/Templado', 589, 343, 450, 13.30, 2, 2, 8, 0, 2, 0, 1, 'No fans'),
(19, 'ATX', 'Acero/Templado', 453, 230, 466, 8.60, 2, 3, 7, 0, 2, 1, 1, '2×120mm fans');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_fuentes_poder`
--

CREATE TABLE `detalles_fuentes_poder` (
  `id_producto` int(11) NOT NULL,
  `potencia_w` int(11) NOT NULL,
  `certificacion_80plus` enum('Bronze','Silver','Gold','Platinum','Titanium') DEFAULT NULL,
  `modularidad` enum('No modular','Semi-modular','Full modular') DEFAULT NULL,
  `tipo_formato` varchar(20) DEFAULT NULL,
  `voltaje_12v_a` decimal(6,2) DEFAULT NULL,
  `num_conectores_24pin` int(11) DEFAULT 1,
  `num_conectores_8pin` int(11) DEFAULT 0,
  `num_sata` int(11) DEFAULT 0,
  `num_molex` int(11) DEFAULT 0,
  `protecciones_ip` varchar(100) DEFAULT NULL,
  `ventilador_mm` int(11) DEFAULT NULL,
  `ruido_max_db` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_fuentes_poder`
--

INSERT INTO `detalles_fuentes_poder` (`id_producto`, `potencia_w`, `certificacion_80plus`, `modularidad`, `tipo_formato`, `voltaje_12v_a`, `num_conectores_24pin`, `num_conectores_8pin`, `num_sata`, `num_molex`, `protecciones_ip`, `ventilador_mm`, `ruido_max_db`) VALUES
(25, 650, 'Gold', 'Full modular', 'ATX', 54.00, 1, 2, 6, 2, 'OVP,UVP,OPP,SCP', 120, 20.00),
(26, 750, 'Gold', 'Full modular', 'ATX', 62.00, 1, 2, 8, 2, 'OVP,UVP,OPP,SCP,OTP', 135, 18.50),
(27, 600, 'Bronze', 'No modular', 'ATX', 48.00, 1, 1, 4, 2, 'OVP,UVP,OPP,SCP', 120, 22.00),
(28, 850, 'Gold', 'Full modular', 'ATX', 70.00, 1, 2, 8, 2, 'OVP,UVP,OPP,SCP,OTP', 140, 19.00),
(29, 650, 'Gold', 'Semi-modular', 'ATX', 54.00, 1, 1, 6, 2, 'OVP,UVP,OPP,SCP', 120, 21.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_memorias_ram`
--

CREATE TABLE `detalles_memorias_ram` (
  `id_producto` int(11) NOT NULL,
  `capacidad_gb` int(11) NOT NULL,
  `tipo_ram` enum('DDR3','DDR4','DDR5') NOT NULL,
  `velocidad_mhz` int(11) NOT NULL,
  `num_modulos` int(11) NOT NULL,
  `voltaje_v` decimal(3,2) DEFAULT NULL,
  `cl_latencia` varchar(10) DEFAULT NULL,
  `ecc` tinyint(1) DEFAULT 0,
  `perfil_xmp` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_memorias_ram`
--

INSERT INTO `detalles_memorias_ram` (`id_producto`, `capacidad_gb`, `tipo_ram`, `velocidad_mhz`, `num_modulos`, `voltaje_v`, `cl_latencia`, `ecc`, `perfil_xmp`) VALUES
(10, 32, 'DDR5', 5200, 2, 1.25, 'CL38', 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_placas_base`
--

CREATE TABLE `detalles_placas_base` (
  `id_producto` int(11) NOT NULL,
  `socket` varchar(20) NOT NULL,
  `chipset` varchar(50) NOT NULL,
  `formato` enum('ATX','Micro-ATX','Mini-ITX','E-ATX') DEFAULT NULL,
  `num_slots_ram` int(11) NOT NULL,
  `max_ram_gb` int(11) NOT NULL,
  `pcie_x16_slots` int(11) DEFAULT 0,
  `pcie_x8_slots` int(11) DEFAULT 0,
  `pcie_x4_slots` int(11) DEFAULT 0,
  `num_m2_slots` int(11) DEFAULT 0,
  `num_sata_ports` int(11) DEFAULT 0,
  `usb2_0_traseros` int(11) DEFAULT 0,
  `usb3_0_traseros` int(11) DEFAULT 0,
  `usb3_1_typeC_traseros` int(11) DEFAULT 0,
  `lan_gbps` decimal(3,1) DEFAULT NULL,
  `wifi_integrado` tinyint(1) DEFAULT 0,
  `bluetooth_integrado` tinyint(1) DEFAULT 0,
  `fases_vrm` int(11) DEFAULT NULL,
  `audio_chipset` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_placas_base`
--

INSERT INTO `detalles_placas_base` (`id_producto`, `socket`, `chipset`, `formato`, `num_slots_ram`, `max_ram_gb`, `pcie_x16_slots`, `pcie_x8_slots`, `pcie_x4_slots`, `num_m2_slots`, `num_sata_ports`, `usb2_0_traseros`, `usb3_0_traseros`, `usb3_1_typeC_traseros`, `lan_gbps`, `wifi_integrado`, `bluetooth_integrado`, `fases_vrm`, `audio_chipset`) VALUES
(30, 'LGA1700', 'Z690', 'ATX', 4, 128, 2, 0, 1, 3, 6, 2, 4, 1, 2.5, 1, 1, 16, 'SupremeFX'),
(31, 'AM4', 'B550', 'ATX', 4, 128, 2, 0, 1, 2, 6, 2, 2, 1, 2.5, 0, 0, 12, 'Realtek ALC892'),
(32, 'AM4', 'X570', 'ATX', 4, 128, 3, 0, 1, 2, 6, 2, 2, 1, 2.5, 0, 0, 14, 'Realtek ALC1220'),
(33, 'LGA1700', 'B660', 'Micro-ATX', 4, 128, 1, 0, 1, 1, 6, 2, 2, 1, 1.0, 0, 0, 10, 'Realtek ALC887'),
(34, 'LGA1700', 'Z690', 'E-ATX', 4, 128, 3, 0, 2, 4, 8, 2, 6, 2, 2.5, 1, 1, 20, 'Realtek ALC4080');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_procesadores`
--

CREATE TABLE `detalles_procesadores` (
  `id_producto` int(11) NOT NULL,
  `reloj_base_ghz` decimal(4,2) NOT NULL,
  `reloj_boost_ghz` decimal(4,2) DEFAULT NULL,
  `num_nucleos` int(11) NOT NULL,
  `num_hilos` int(11) NOT NULL,
  `tdp_w` int(11) DEFAULT NULL,
  `socket` varchar(20) DEFAULT NULL,
  `litografia_nm` int(11) DEFAULT NULL,
  `cache_l2_mb` decimal(5,2) DEFAULT NULL,
  `cache_l3_mb` decimal(6,2) DEFAULT NULL,
  `gpu_integrado` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_refrigeraciones`
--

CREATE TABLE `detalles_refrigeraciones` (
  `id_producto` int(11) NOT NULL,
  `tipo_refrigeracion` enum('Aire','Líquida') NOT NULL,
  `altura_mm` int(11) DEFAULT NULL,
  `ventilador_mm` int(11) DEFAULT NULL,
  `flujo_aire_cfm` decimal(6,2) DEFAULT NULL,
  `nivel_ruido_db` decimal(5,2) DEFAULT NULL,
  `socket_compatibles` varchar(100) DEFAULT NULL,
  `radiador_mm` varchar(20) DEFAULT NULL,
  `bombas_rpm` int(11) DEFAULT NULL,
  `conductos_material` varchar(50) DEFAULT NULL,
  `peso_kg` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_refrigeraciones`
--

INSERT INTO `detalles_refrigeraciones` (`id_producto`, `tipo_refrigeracion`, `altura_mm`, `ventilador_mm`, `flujo_aire_cfm`, `nivel_ruido_db`, `socket_compatibles`, `radiador_mm`, `bombas_rpm`, `conductos_material`, `peso_kg`) VALUES
(20, 'Aire', 165, 140, 82.50, 24.60, 'AM4,LGA1151,LGA1200', NULL, NULL, 'Cobre', 1.32),
(21, 'Líquida', NULL, 120, 75.00, 36.00, 'AM4,LGA1200', '240x120', 3000, 'Cobre', 1.22),
(22, 'Líquida', NULL, 140, 73.11, 21.00, 'AM4,LGA1700', '280x140', 2200, 'Aluminio', 1.54),
(23, 'Aire', 163, 120, 82.80, 24.30, 'LGA1151,LGA1200,AM4', NULL, NULL, 'Cobre', 1.10),
(24, 'Aire', 155, 120, 63.50, 27.80, 'LGA1151,LGA1200,AM4', NULL, NULL, 'Aluminio', 0.70);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_tarjetas_graficas`
--

CREATE TABLE `detalles_tarjetas_graficas` (
  `id_producto` int(11) NOT NULL,
  `chipset` varchar(50) NOT NULL,
  `memoria_gb` int(11) NOT NULL,
  `tipo_memoria` varchar(20) DEFAULT NULL,
  `bus_memoria_bits` int(11) DEFAULT NULL,
  `reloj_base_ghz` decimal(5,2) DEFAULT NULL,
  `reloj_boost_ghz` decimal(5,2) DEFAULT NULL,
  `tdp_w` int(11) DEFAULT NULL,
  `pcie_version` varchar(10) DEFAULT NULL,
  `cuda_cores` int(11) DEFAULT NULL,
  `long_mm` int(11) DEFAULT NULL,
  `altura_mm` int(11) DEFAULT NULL,
  `espesor_slots` decimal(3,1) DEFAULT NULL,
  `conector_6pin` int(11) DEFAULT 0,
  `conector_8pin` int(11) DEFAULT 0,
  `sli_xfire_soporte` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_tarjetas_graficas`
--

INSERT INTO `detalles_tarjetas_graficas` (`id_producto`, `chipset`, `memoria_gb`, `tipo_memoria`, `bus_memoria_bits`, `reloj_base_ghz`, `reloj_boost_ghz`, `tdp_w`, `pcie_version`, `cuda_cores`, `long_mm`, `altura_mm`, `espesor_slots`, `conector_6pin`, `conector_8pin`, `sli_xfire_soporte`) VALUES
(11, 'GA106', 12, 'GDDR6', 192, 1.32, 1.78, 170, 'PCIe 4.0', 3584, 242, 112, 2.0, 0, 1, 0),
(13, 'GA102', 10, 'GDDR6X', 320, 1.44, 1.71, 320, 'PCIe 4.0', 8704, 318, 137, 2.7, 0, 2, 0),
(14, 'GA104', 8, 'GDDR6', 256, 1.50, 1.73, 220, 'PCIe 4.0', 5888, 242, 112, 2.0, 0, 2, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estados`
--

CREATE TABLE `estados` (
  `id_estado` int(11) NOT NULL,
  `estado` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estados`
--

INSERT INTO `estados` (`id_estado`, `estado`) VALUES
(6, 'Cancelado'),
(5, 'Entregado'),
(4, 'Enviado'),
(2, 'Pendiente de envio'),
(1, 'Pendiente de pago'),
(3, 'Procesado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `favoritos`
--

CREATE TABLE `favoritos` (
  `id_favorito` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marcas`
--

CREATE TABLE `marcas` (
  `id_marca` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marcas`
--

INSERT INTO `marcas` (`id_marca`, `nombre`) VALUES
(2, 'AMD'),
(19, 'Arctic'),
(22, 'ASRock'),
(8, 'ASUS'),
(18, 'be quiet!'),
(14, 'Cooler Master'),
(3, 'Corsair'),
(6, 'Crucial'),
(20, 'DeepCool'),
(12, 'EVGA'),
(5, 'G.Skill'),
(10, 'Gigabyte'),
(1, 'Intel'),
(4, 'Kingston'),
(16, 'Lian Li'),
(9, 'MSI'),
(17, 'Noctua'),
(7, 'Nvidia'),
(13, 'NZXT'),
(21, 'Seasonic'),
(15, 'Thermaltake'),
(11, 'Zotac');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marcas_categorias`
--

CREATE TABLE `marcas_categorias` (
  `id_marca_categoria` int(11) NOT NULL,
  `id_marca` int(11) NOT NULL,
  `id_categoria` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_pedido` date NOT NULL,
  `fecha_entrega` date NOT NULL,
  `valor_total` decimal(10,2) NOT NULL,
  `id_estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `id_marca` int(11) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `precio`, `stock`, `id_categoria`, `id_marca`, `imagen`) VALUES
(4, 'AMD Ryzen 7 5800X je', 329.99, 69, 1, 2, 'ryzen7-5800x.jpg'),
(10, 'Corsair Dominator Platinum RGB 32GB (2x16) DDR5-5200', 299.99, 40, 2, 3, 'dominator-32gb-ddr5.jpg'),
(11, 'Nvidia GeForce RTX 3060', 329.99, 60, 3, 7, 'rtx3060.jpg'),
(13, 'ASUS ROG Strix RTX 3080', 699.99, 30, 3, 8, 'strix-3080.jpg'),
(14, 'MSI Ventus RTX 3070', 499.99, 35, 3, 9, 'ventus-3070.jpg'),
(16, 'NZXT H510', 69.99, 80, 4, 13, 'h510.jpg'),
(17, 'Cooler Master MasterBox NR600', 79.99, 60, 4, 14, 'nr600.jpg'),
(18, 'Thermaltake Core P3', 129.99, 40, 4, 15, 'core-p3.jpg'),
(19, 'Corsair 4000D Airflow', 94.99, 70, 4, 3, '4000d.jpg'),
(20, 'Noctua NH-D15', 89.99, 50, 5, 17, 'nh-d15.jpg'),
(21, 'Corsair H100i RGB Platinum', 159.99, 40, 5, 3, 'h100i.jpg'),
(22, 'NZXT Kraken X63', 159.99, 45, 5, 13, 'kraken-x63.jpg'),
(23, 'be quiet! Dark Rock Pro 4', 89.99, 35, 5, 18, 'darkrock-pro4.jpg'),
(24, 'DeepCool Gammaxx 400', 29.99, 70, 5, 20, 'gammaxx-400.jpg'),
(25, 'Seasonic Focus GX-650', 119.99, 60, 6, 21, 'focus-gx-650.jpg'),
(26, 'Corsair RM750x', 129.99, 50, 6, 3, 'rm750x.jpg'),
(27, 'EVGA 600 BR', 59.99, 80, 6, 12, '600-br.jpg'),
(28, 'Thermaltake Toughpower GF1 850W', 139.99, 40, 6, 15, 'toughpower-850w.jpg'),
(29, 'Cooler Master MWE Gold 650', 89.99, 70, 6, 14, 'mwe-gold-650.jpg'),
(30, 'ASUS ROG Strix Z690-E', 379.99, 30, 7, 8, 'strix-z690e.jpg'),
(31, 'MSI MAG B550 Tomahawk', 179.99, 45, 7, 9, 'b550-tomahawk.jpg'),
(32, 'Gigabyte X570 AORUS Elite', 199.99, 40, 7, 10, 'x570-aorus.jpg'),
(33, 'ASRock B660M Pro RS', 129.99, 50, 7, 22, 'b660m-pro.jpg'),
(34, 'MSI MEG Z690 Unify', 409.99, 20, 7, 9, 'meg-z690-unify.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos_pedidos`
--

CREATE TABLE `productos_pedidos` (
  `id_producto_pedido` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reviews`
--

CREATE TABLE `reviews` (
  `id_review` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `estrellas` int(11) NOT NULL,
  `comentario` text DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `rol` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `rol`) VALUES
(1, 'usuario'),
(2, 'moderador'),
(3, 'administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `password` varchar(256) NOT NULL,
  `id_rol` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `apellido`, `email`, `direccion`, `telefono`, `password`, `id_rol`) VALUES
(7, 'Admin2', 'De Prueba', 'admin2@example.com', 'Calle Falsa 123', '123456789', 'scrypt:32768:8:1$tuPR5rDHuRrJKqUH$7ba1fb9b67d0e64788e012e12d41c96d21039c1eadf325db1bd7c5f3ccda19a0ecd1584927a4be722ee7bb969d11730cd20ebe69b56128d17145b94296df4446', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `detalles_chasises`
--
ALTER TABLE `detalles_chasises`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `detalles_fuentes_poder`
--
ALTER TABLE `detalles_fuentes_poder`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `detalles_memorias_ram`
--
ALTER TABLE `detalles_memorias_ram`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `detalles_placas_base`
--
ALTER TABLE `detalles_placas_base`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `detalles_procesadores`
--
ALTER TABLE `detalles_procesadores`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `detalles_refrigeraciones`
--
ALTER TABLE `detalles_refrigeraciones`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `detalles_tarjetas_graficas`
--
ALTER TABLE `detalles_tarjetas_graficas`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `estados`
--
ALTER TABLE `estados`
  ADD PRIMARY KEY (`id_estado`),
  ADD UNIQUE KEY `estado` (`estado`);

--
-- Indices de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`id_favorito`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `marcas`
--
ALTER TABLE `marcas`
  ADD PRIMARY KEY (`id_marca`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `marcas_categorias`
--
ALTER TABLE `marcas_categorias`
  ADD PRIMARY KEY (`id_marca_categoria`),
  ADD KEY `id_marca` (`id_marca`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_estado_id` (`id_estado`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `fk_categoria` (`id_categoria`),
  ADD KEY `fk_marca` (`id_marca`);

--
-- Indices de la tabla `productos_pedidos`
--
ALTER TABLE `productos_pedidos`
  ADD PRIMARY KEY (`id_producto_pedido`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id_review`),
  ADD KEY `id_producto` (`id_producto`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `estados`
--
ALTER TABLE `estados`
  MODIFY `id_estado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id_favorito` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `marcas`
--
ALTER TABLE `marcas`
  MODIFY `id_marca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `marcas_categorias`
--
ALTER TABLE `marcas_categorias`
  MODIFY `id_marca_categoria` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `productos_pedidos`
--
ALTER TABLE `productos_pedidos`
  MODIFY `id_producto_pedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id_review` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalles_chasises`
--
ALTER TABLE `detalles_chasises`
  ADD CONSTRAINT `detalles_chasises_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalles_fuentes_poder`
--
ALTER TABLE `detalles_fuentes_poder`
  ADD CONSTRAINT `detalles_fuentes_poder_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalles_memorias_ram`
--
ALTER TABLE `detalles_memorias_ram`
  ADD CONSTRAINT `detalles_memorias_ram_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalles_placas_base`
--
ALTER TABLE `detalles_placas_base`
  ADD CONSTRAINT `detalles_placas_base_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalles_procesadores`
--
ALTER TABLE `detalles_procesadores`
  ADD CONSTRAINT `detalles_procesadores_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalles_refrigeraciones`
--
ALTER TABLE `detalles_refrigeraciones`
  ADD CONSTRAINT `detalles_refrigeraciones_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalles_tarjetas_graficas`
--
ALTER TABLE `detalles_tarjetas_graficas`
  ADD CONSTRAINT `detalles_tarjetas_graficas_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `favoritos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `favoritos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `marcas_categorias`
--
ALTER TABLE `marcas_categorias`
  ADD CONSTRAINT `marcas_categorias_ibfk_1` FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id_marca`),
  ADD CONSTRAINT `marcas_categorias_ibfk_2` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `fk_estado_id` FOREIGN KEY (`id_estado`) REFERENCES `estados` (`id_estado`),
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `fk_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`),
  ADD CONSTRAINT `fk_marca` FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id_marca`);

--
-- Filtros para la tabla `productos_pedidos`
--
ALTER TABLE `productos_pedidos`
  ADD CONSTRAINT `productos_pedidos_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  ADD CONSTRAINT `productos_pedidos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
