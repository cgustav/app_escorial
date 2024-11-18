-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 21-12-2024 a las 23:13:59
-- Versión del servidor: 8.0.17
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `el_escorial`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Cargo', 7, 'add_cargo'),
(26, 'Can change Cargo', 7, 'change_cargo'),
(27, 'Can delete Cargo', 7, 'delete_cargo'),
(28, 'Can view Cargo', 7, 'view_cargo'),
(29, 'Can add Departamento', 8, 'add_departamento'),
(30, 'Can change Departamento', 8, 'change_departamento'),
(31, 'Can delete Departamento', 8, 'delete_departamento'),
(32, 'Can view Departamento', 8, 'view_departamento'),
(33, 'Can add Empleado', 9, 'add_empleado'),
(34, 'Can change Empleado', 9, 'change_empleado'),
(35, 'Can delete Empleado', 9, 'delete_empleado'),
(36, 'Can view Empleado', 9, 'view_empleado'),
(37, 'Can add Cantidad', 10, 'add_cantidad'),
(38, 'Can change Cantidad', 10, 'change_cantidad'),
(39, 'Can delete Cantidad', 10, 'delete_cantidad'),
(40, 'Can view Cantidad', 10, 'view_cantidad'),
(41, 'Can add Repuesto', 11, 'add_repuesto'),
(42, 'Can change Repuesto', 11, 'change_repuesto'),
(43, 'Can delete Repuesto', 11, 'delete_repuesto'),
(44, 'Can view Repuesto', 11, 'view_repuesto'),
(45, 'Can add tipo', 12, 'add_tipo'),
(46, 'Can change tipo', 12, 'change_tipo'),
(47, 'Can delete tipo', 12, 'delete_tipo'),
(48, 'Can view tipo', 12, 'view_tipo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$AbSZpQJFLHEPNss6JfhXQg$YyG//VuMAdp3WRMpzlXTv8MOps6tpMp8UprU4g2o/gg=', NULL, 1, 'admin', '', '', 'admin@correo.cl', 1, 1, '2024-11-12 03:21:08.449464'),
(2, 'pbkdf2_sha256$390000$PerGFAp5kStgn2HqRV6bkY$r607XXIZE1CljYNz3CuE8LCRz/0EGiAzlgsgkVSDSzY=', '2024-12-21 22:50:09.379412', 1, 'admin_escorial', '', '', 'admin_escorial@gmail.com', 1, 1, '2024-11-13 02:10:15.914894');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cantidad`
--

CREATE TABLE `cantidad` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `creado` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `cantidad`
--

INSERT INTO `cantidad` (`id`, `nombre`, `creado`) VALUES
(1, '1', '2024-11-13 02:11:32.000000'),
(2, '2', '2024-11-13 02:11:50.000000'),
(3, '3', '2024-11-13 02:11:55.000000'),
(4, '4', '2024-11-13 02:11:57.000000'),
(5, '5', '2024-11-13 02:11:58.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-11-13 02:11:50.881850', '1', '1', 1, '[{\"added\": {}}]', 10, 2),
(2, '2024-11-13 02:11:55.702818', '2', '2', 1, '[{\"added\": {}}]', 10, 2),
(3, '2024-11-13 02:11:57.118651', '3', '3', 1, '[{\"added\": {}}]', 10, 2),
(4, '2024-11-13 02:11:58.790082', '4', '4', 1, '[{\"added\": {}}]', 10, 2),
(5, '2024-11-13 02:12:00.010736', '5', '5', 1, '[{\"added\": {}}]', 10, 2),
(6, '2024-11-13 02:14:42.073434', '1', 'Baterias', 1, '[{\"added\": {}}]', 12, 2),
(7, '2024-11-13 02:14:49.502143', '2', 'Lubricantes', 1, '[{\"added\": {}}]', 12, 2),
(8, '2024-11-13 02:15:40.187909', '3', 'Neumaticos', 1, '[{\"added\": {}}]', 12, 2),
(9, '2024-11-13 02:17:03.046268', '4', 'Repuestos John Deere', 1, '[{\"added\": {}}]', 12, 2),
(10, '2024-11-13 02:17:22.914870', '5', 'Repuestos Landini', 1, '[{\"added\": {}}]', 12, 2),
(11, '2024-11-13 02:17:31.250659', '6', 'Repuestos Same', 1, '[{\"added\": {}}]', 12, 2),
(12, '2024-11-13 02:18:11.381370', '7', 'Repuestos Massey Ferguson', 1, '[{\"added\": {}}]', 12, 2),
(13, '2024-11-13 22:43:57.552125', '4', 'Bateria 1', 1, '[{\"added\": {}}]', 11, 2),
(14, '2024-11-13 22:56:10.678039', '5', 'Neumaticos 1', 1, '[{\"added\": {}}]', 11, 2),
(15, '2024-11-14 01:48:59.636904', '6', 'insecticida 8', 1, '[{\"added\": {}}]', 11, 2),
(16, '2024-11-15 03:31:53.024776', '13', 'neumatic 4', 1, '[{\"added\": {}}]', 11, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'tiendaApp', 'cargo'),
(8, 'tiendaApp', 'departamento'),
(9, 'tiendaApp', 'empleado'),
(10, 'tiendaApp', 'cantidad'),
(11, 'tiendaApp', 'repuesto'),
(12, 'tiendaApp', 'tipo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-11-12 03:20:26.407670'),
(2, 'auth', '0001_initial', '2024-11-12 03:20:26.971766'),
(3, 'admin', '0001_initial', '2024-11-12 03:20:27.212675'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-11-12 03:20:27.217676'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-11-12 03:20:27.223678'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-11-12 03:20:27.310240'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-11-12 03:20:27.348503'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-11-12 03:20:27.405672'),
(9, 'auth', '0004_alter_user_username_opts', '2024-11-12 03:20:27.410666'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-11-12 03:20:27.458283'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-11-12 03:20:27.460283'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-11-12 03:20:27.465427'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-11-12 03:20:27.506450'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-11-12 03:20:27.547062'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-11-12 03:20:27.584072'),
(16, 'auth', '0011_update_proxy_permissions', '2024-11-12 03:20:27.592312'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-11-12 03:20:27.623904'),
(18, 'sessions', '0001_initial', '2024-11-12 03:20:27.678677'),
(19, 'tiendaApp', '0001_initial', '2024-11-12 03:20:27.902045'),
(20, 'tiendaApp', '0002_cantidad_repuesto_tipo_remove_empleado_cargo_and_more', '2024-11-12 03:32:16.500074'),
(21, 'tiendaApp', '0003_alter_repuesto_options_rename_sueldo_repuesto_precio', '2024-11-12 19:17:49.910163'),
(22, 'tiendaApp', '0004_remove_repuesto_fechanac_remove_repuesto_materno_and_more', '2024-11-13 02:48:39.341377'),
(23, 'tiendaApp', '0005_alter_repuesto_fotografia', '2024-11-15 02:59:01.597203'),
(24, 'tiendaApp', '0006_alter_repuesto_fotografia', '2024-11-17 02:40:06.761775');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('01ghx6zlxjibodevoy3ogfkmlrh4wc54', '.eJxVjMsOwiAQRf-FtSHQ4enSvd9AYAakaiAp7cr479qkC93ec859sRC3tYZt5CXMxM5sYqffLUV85LYDusd26xx7W5c58V3hBx382ik_L4f7d1DjqN86RSpeKCm1gyRJIIERKB0geAO5QFJWF0TtnVFaGesckLJWIEygbGTvD9R8Nuo:1r2MPv:NDFNFzI9HoQSF1azt_iAgYVoWr39Y6vieBLdd-oLWr8', '2024-11-27 02:11:11.776824'),
('9erh82z625k78ogndh14tlxpqhkclay8', '.eJxVjDsOwjAQRO_iGln-xE6Wkj5nsHa9Ng4gR4qTCnF3EikFNFPMezNvEXBbS9haWsLE4iqMuPx2hPGZ6gH4gfU-yzjXdZlIHoo8aZPjzOl1O92_g4Kt7OuYO2AAp4iy1Q57ZwZlPSMozY6NQr-HB6s8WdCZmCjpHCMNOfZdFp8v3uM4Wg:1rGRrl:laDRygXjl5cnhBeNo17DkeePIuSuf0rAhiHAdsnn2wM', '2024-01-04 22:50:09.383705');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `repuesto`
--

CREATE TABLE `repuesto` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `codigoRepuesto` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `precio` int(10) UNSIGNED NOT NULL,
  `creado` datetime(6) NOT NULL,
  `cantidad_id` bigint(20) DEFAULT NULL,
  `tipo_id` bigint(20) NOT NULL,
  `fotografia` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `repuesto`
--

INSERT INTO `repuesto` (`id`, `nombre`, `codigoRepuesto`, `precio`, `creado`, `cantidad_id`, `tipo_id`, `fotografia`) VALUES
(2, 'Neumatico 55x90', '002', 70000, '2024-11-15 21:56:21.528746', 2, 3, 'repuestos/ampolleta_02rdG1u.png'),
(6, 'Aceite Total 525', '001', 89900, '2024-12-20 18:14:50.476283', 3, 2, 'repuestos/tempalta.png'),
(27, 'rsxhxh', '453', 4354, '2024-11-17 03:40:48.280942', 3, 3, 'repuestos/tractor.png'),
(30, 'Parabrisa tra 890', '003', 70000, '2024-12-20 18:14:41.398914', 1, 4, 'repuestos/tractor.png'),
(31, 'Rodamiento caja MF', '002', 50000, '2024-12-20 18:12:01.360487', 1, 7, 'repuestos/tractor.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo`
--

CREATE TABLE `tipo` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `creado` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `tipo`
--

INSERT INTO `tipo` (`id`, `nombre`, `creado`) VALUES
(1, 'Baterias', '2024-11-13 02:12:20.000000'),
(2, 'Lubricantes', '2024-11-13 02:14:42.000000'),
(3, 'Neumaticos', '2024-11-13 02:14:49.000000'),
(4, 'Repuestos John Deere', '2024-11-13 02:16:36.000000'),
(5, 'Repuestos Landini', '2024-11-13 02:17:03.000000'),
(6, 'Repuestos Same', '2024-11-13 02:17:22.000000'),
(7, 'Repuestos Massey Ferguson', '2024-11-13 02:17:31.000000');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  ADD KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  ADD KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  ADD KEY `auth_user_groups_group_id_97559544` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  ADD KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`);

--
-- Indices de la tabla `cantidad`
--
ALTER TABLE `cantidad`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `repuesto`
--
ALTER TABLE `repuesto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `repuesto_cantidad_id_b797a841` (`cantidad_id`),
  ADD KEY `repuesto_tipo_id_60667cff` (`tipo_id`);

--
-- Indices de la tabla `tipo`
--
ALTER TABLE `tipo`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cantidad`
--
ALTER TABLE `cantidad`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `repuesto`
--
ALTER TABLE `repuesto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `tipo`
--
ALTER TABLE `tipo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
