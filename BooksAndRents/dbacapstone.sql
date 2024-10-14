-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-10-2024 a las 23:51:47
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dbacapstone`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin_interface_theme`
--

CREATE TABLE `admin_interface_theme` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `title_visible` tinyint(1) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `logo_visible` tinyint(1) NOT NULL,
  `css_header_background_color` varchar(10) NOT NULL,
  `title_color` varchar(10) NOT NULL,
  `css_header_text_color` varchar(10) NOT NULL,
  `css_header_link_color` varchar(10) NOT NULL,
  `css_header_link_hover_color` varchar(10) NOT NULL,
  `css_module_background_color` varchar(10) NOT NULL,
  `css_module_text_color` varchar(10) NOT NULL,
  `css_module_link_color` varchar(10) NOT NULL,
  `css_module_link_hover_color` varchar(10) NOT NULL,
  `css_module_rounded_corners` tinyint(1) NOT NULL,
  `css_generic_link_color` varchar(10) NOT NULL,
  `css_generic_link_hover_color` varchar(10) NOT NULL,
  `css_save_button_background_color` varchar(10) NOT NULL,
  `css_save_button_background_hover_color` varchar(10) NOT NULL,
  `css_save_button_text_color` varchar(10) NOT NULL,
  `css_delete_button_background_color` varchar(10) NOT NULL,
  `css_delete_button_background_hover_color` varchar(10) NOT NULL,
  `css_delete_button_text_color` varchar(10) NOT NULL,
  `list_filter_dropdown` tinyint(1) NOT NULL,
  `related_modal_active` tinyint(1) NOT NULL,
  `related_modal_background_color` varchar(10) NOT NULL,
  `related_modal_rounded_corners` tinyint(1) NOT NULL,
  `logo_color` varchar(10) NOT NULL,
  `recent_actions_visible` tinyint(1) NOT NULL,
  `favicon` varchar(100) NOT NULL,
  `related_modal_background_opacity` varchar(5) NOT NULL,
  `env_name` varchar(50) NOT NULL,
  `env_visible_in_header` tinyint(1) NOT NULL,
  `env_color` varchar(10) NOT NULL,
  `env_visible_in_favicon` tinyint(1) NOT NULL,
  `related_modal_close_button_visible` tinyint(1) NOT NULL,
  `language_chooser_active` tinyint(1) NOT NULL,
  `language_chooser_display` varchar(10) NOT NULL,
  `list_filter_sticky` tinyint(1) NOT NULL,
  `form_pagination_sticky` tinyint(1) NOT NULL,
  `form_submit_sticky` tinyint(1) NOT NULL,
  `css_module_background_selected_color` varchar(10) NOT NULL,
  `css_module_link_selected_color` varchar(10) NOT NULL,
  `logo_max_height` smallint(5) UNSIGNED NOT NULL CHECK (`logo_max_height` >= 0),
  `logo_max_width` smallint(5) UNSIGNED NOT NULL CHECK (`logo_max_width` >= 0),
  `foldable_apps` tinyint(1) NOT NULL,
  `language_chooser_control` varchar(20) NOT NULL,
  `list_filter_highlight` tinyint(1) NOT NULL,
  `list_filter_removal_links` tinyint(1) NOT NULL,
  `show_fieldsets_as_tabs` tinyint(1) NOT NULL,
  `show_inlines_as_tabs` tinyint(1) NOT NULL,
  `css_generic_link_active_color` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_arriendo`
--

CREATE TABLE `app_arriendo` (
  `id` bigint(20) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `cliente_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_arriendo`
--

INSERT INTO `app_arriendo` (`id`, `fecha_inicio`, `fecha_fin`, `cliente_id`) VALUES
(1, '2024-10-12', '2024-11-11', 1),
(2, '2024-10-12', '2024-11-11', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_autor`
--

CREATE TABLE `app_autor` (
  `id` bigint(20) NOT NULL,
  `nombre_autor` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_autor`
--

INSERT INTO `app_autor` (`id`, `nombre_autor`) VALUES
(1, 'Pablo peruda'),
(2, 'Suzanne Collins'),
(3, 'George R. R. Martin'),
(4, 'J. K. Rowling'),
(5, 'LaRousse'),
(6, 'Jean Blot'),
(7, 'Mario Amorós'),
(8, 'Lesley-Ann Jones');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_carrito`
--

CREATE TABLE `app_carrito` (
  `id` bigint(20) NOT NULL,
  `cliente_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_carrito`
--

INSERT INTO `app_carrito` (`id`, `cliente_id`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_compra`
--

CREATE TABLE `app_compra` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `fecha_compra` datetime(6) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_customuser`
--

CREATE TABLE `app_customuser` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `rut` varchar(50) DEFAULT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `telefono` int(11) DEFAULT NULL,
  `fechanac` date DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_customuser`
--

INSERT INTO `app_customuser` (`id`, `password`, `last_login`, `is_superuser`, `email`, `rut`, `first_name`, `last_name`, `telefono`, `fechanac`, `direccion`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$260000$Ni6sAXQjXLZRujMdBuJRiz$r62n2Q9/P1SdgOk/xL0Pcu777ghLCW10ER1riQic5Yc=', '2024-10-14 20:39:53.016443', 1, 'admin@admin.cl', NULL, 'admin', 'admin', NULL, NULL, NULL, 1, 1, '2024-10-12 01:00:40.080086'),
(2, 'pbkdf2_sha256$260000$WlkdBMZQzDrNM4MrbNXSsl$KLGQuODfBxiB4S7Y3ciB27BcxqTbs8h9QIPRGxX53Do=', '2024-10-14 20:33:58.225366', 0, 'jose@jose.cl', '123456789', 'jose', 'jose', 123658412, '2002-01-09', 'lota 45', 0, 1, '2024-10-14 20:33:58.221378');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_customuser_groups`
--

CREATE TABLE `app_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_customuser_user_permissions`
--

CREATE TABLE `app_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_generolib`
--

CREATE TABLE `app_generolib` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_generolib`
--

INSERT INTO `app_generolib` (`id`, `nombre`) VALUES
(1, 'Comedia'),
(2, 'Ciencia ficción'),
(3, 'Acción'),
(4, 'Fantasía'),
(5, 'Libros de referencia'),
(6, 'biografía'),
(7, 'Politica');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_itemarriendo`
--

CREATE TABLE `app_itemarriendo` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `arriendo_id` bigint(20) NOT NULL,
  `libro_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_itemcarrito`
--

CREATE TABLE `app_itemcarrito` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `carrito_id` bigint(20) NOT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_libro`
--

CREATE TABLE `app_libro` (
  `id` bigint(20) NOT NULL,
  `nom_libro` varchar(255) NOT NULL,
  `precio` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `id_autor_id` bigint(20) DEFAULT NULL,
  `id_genero_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_libro`
--

INSERT INTO `app_libro` (`id`, `nom_libro`, `precio`, `stock`, `imagen`, `id_autor_id`, `id_genero_id`) VALUES
(2, 'Los Juegos Del Hambre', 23000, 15, 'C:\\BooksAndRents\\media\\libros\\Los_Juegos_Del_Hambre.jpg', 2, 2),
(3, 'Juego De Tronos', 19000, 21, 'C:\\BooksAndRents\\media\\libros\\Juego_De_Tronos.jpg', 3, 3),
(4, 'Harry Potter y la piedra filosofal', 14000, 54, 'C:\\BooksAndRents\\media\\libros\\Harry_Potter_y_la_piedra_filosofal.jpg', 4, 4),
(5, 'Diccionario', 3000, 123, 'C:\\BooksAndRents\\media\\libros\\Diccionario.jpg', 5, 5),
(6, 'Wolfgang Amadeus Mozart', 31000, 5, 'C:\\BooksAndRents\\media\\libros\\Wolfgang_Amadeus_Mozart.jpg', 6, 6),
(7, 'Allende', 12030, 24, 'C:\\BooksAndRents\\media\\libros\\Allende.jpg', 7, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_libroarr`
--

CREATE TABLE `app_libroarr` (
  `id` bigint(20) NOT NULL,
  `nom_libro` varchar(255) NOT NULL,
  `stock` int(11) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `id_autor_id` bigint(20) DEFAULT NULL,
  `id_genero_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_libroarr`
--

INSERT INTO `app_libroarr` (`id`, `nom_libro`, `stock`, `imagen`, `id_autor_id`, `id_genero_id`) VALUES
(2, 'Los Juegos Del Hambre', 10, 'libros/Los-juegos.jpg', 2, 2),
(3, 'Juego de Tronos', 4, 'libros/geo.jpg', 3, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_sub`
--

CREATE TABLE `app_sub` (
  `id` bigint(20) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `id_ts_id` bigint(20) DEFAULT NULL,
  `id_us_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_sub`
--

INSERT INTO `app_sub` (`id`, `fecha_inicio`, `id_ts_id`, `id_us_id`) VALUES
(1, '2024-10-12', 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_subscripcion`
--

CREATE TABLE `app_subscripcion` (
  `id` bigint(20) NOT NULL,
  `nom_sus` varchar(100) NOT NULL,
  `dcto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_tiposubcripscion`
--

CREATE TABLE `app_tiposubcripscion` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `precio` int(11) NOT NULL,
  `dcto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_tiposubcripscion`
--

INSERT INTO `app_tiposubcripscion` (`id`, `nombre`, `precio`, `dcto`) VALUES
(1, 'Basica', 4500, 0),
(2, 'Completa', 5500, 10),
(3, 'Ultra', 6500, 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_usersub`
--

CREATE TABLE `app_usersub` (
  `id` bigint(20) NOT NULL,
  `id_Sub_id` bigint(20) DEFAULT NULL,
  `id_usuario_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add custom user', 6, 'add_customuser'),
(22, 'Can change custom user', 6, 'change_customuser'),
(23, 'Can delete custom user', 6, 'delete_customuser'),
(24, 'Can view custom user', 6, 'view_customuser'),
(25, 'Can add arriendo', 7, 'add_arriendo'),
(26, 'Can change arriendo', 7, 'change_arriendo'),
(27, 'Can delete arriendo', 7, 'delete_arriendo'),
(28, 'Can view arriendo', 7, 'view_arriendo'),
(29, 'Can add autor', 8, 'add_autor'),
(30, 'Can change autor', 8, 'change_autor'),
(31, 'Can delete autor', 8, 'delete_autor'),
(32, 'Can view autor', 8, 'view_autor'),
(33, 'Can add carrito', 9, 'add_carrito'),
(34, 'Can change carrito', 9, 'change_carrito'),
(35, 'Can delete carrito', 9, 'delete_carrito'),
(36, 'Can view carrito', 9, 'view_carrito'),
(37, 'Can add genero lib', 10, 'add_generolib'),
(38, 'Can change genero lib', 10, 'change_generolib'),
(39, 'Can delete genero lib', 10, 'delete_generolib'),
(40, 'Can view genero lib', 10, 'view_generolib'),
(41, 'Can add subscripcion', 11, 'add_subscripcion'),
(42, 'Can change subscripcion', 11, 'change_subscripcion'),
(43, 'Can delete subscripcion', 11, 'delete_subscripcion'),
(44, 'Can view subscripcion', 11, 'view_subscripcion'),
(45, 'Can add tipo subcripscion', 12, 'add_tiposubcripscion'),
(46, 'Can change tipo subcripscion', 12, 'change_tiposubcripscion'),
(47, 'Can delete tipo subcripscion', 12, 'delete_tiposubcripscion'),
(48, 'Can view tipo subcripscion', 12, 'view_tiposubcripscion'),
(49, 'Can add user sub', 13, 'add_usersub'),
(50, 'Can change user sub', 13, 'change_usersub'),
(51, 'Can delete user sub', 13, 'delete_usersub'),
(52, 'Can view user sub', 13, 'view_usersub'),
(53, 'Can add sub', 14, 'add_sub'),
(54, 'Can change sub', 14, 'change_sub'),
(55, 'Can delete sub', 14, 'delete_sub'),
(56, 'Can view sub', 14, 'view_sub'),
(57, 'Can add libro arr', 15, 'add_libroarr'),
(58, 'Can change libro arr', 15, 'change_libroarr'),
(59, 'Can delete libro arr', 15, 'delete_libroarr'),
(60, 'Can view libro arr', 15, 'view_libroarr'),
(61, 'Can add libro', 16, 'add_libro'),
(62, 'Can change libro', 16, 'change_libro'),
(63, 'Can delete libro', 16, 'delete_libro'),
(64, 'Can view libro', 16, 'view_libro'),
(65, 'Can add item carrito', 17, 'add_itemcarrito'),
(66, 'Can change item carrito', 17, 'change_itemcarrito'),
(67, 'Can delete item carrito', 17, 'delete_itemcarrito'),
(68, 'Can view item carrito', 17, 'view_itemcarrito'),
(69, 'Can add item arriendo', 18, 'add_itemarriendo'),
(70, 'Can change item arriendo', 18, 'change_itemarriendo'),
(71, 'Can delete item arriendo', 18, 'delete_itemarriendo'),
(72, 'Can view item arriendo', 18, 'view_itemarriendo'),
(73, 'Can add compra', 19, 'add_compra'),
(74, 'Can change compra', 19, 'change_compra'),
(75, 'Can delete compra', 19, 'delete_compra'),
(76, 'Can view compra', 19, 'view_compra'),
(77, 'Can add Theme', 20, 'add_theme'),
(78, 'Can change Theme', 20, 'change_theme'),
(79, 'Can delete Theme', 20, 'delete_theme'),
(80, 'Can view Theme', 20, 'view_theme');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-10-12 01:01:23.133013', '1', 'Comedia', 1, '[{\"added\": {}}]', 10, 1),
(2, '2024-10-12 01:01:32.411522', '1', 'Pablo peruda', 1, '[{\"added\": {}}]', 8, 1),
(3, '2024-10-12 01:01:55.990034', '1', 'Prueba1', 1, '[{\"added\": {}}]', 16, 1),
(4, '2024-10-12 01:02:12.285489', '1', 'Basica', 1, '[{\"added\": {}}]', 12, 1),
(5, '2024-10-12 01:02:19.411083', '2', 'Completa', 1, '[{\"added\": {}}]', 12, 1),
(6, '2024-10-12 01:02:26.615517', '3', 'Ultra', 1, '[{\"added\": {}}]', 12, 1),
(7, '2024-10-12 01:02:43.368174', '1', 'PruebaArr1', 1, '[{\"added\": {}}]', 15, 1),
(8, '2024-10-14 20:40:36.785843', '2', 'Suzanne Collins', 1, '[{\"added\": {}}]', 8, 1),
(9, '2024-10-14 20:41:27.257050', '3', 'George R. R. Martin', 1, '[{\"added\": {}}]', 8, 1),
(10, '2024-10-14 20:41:53.050150', '4', 'J. K. Rowling', 1, '[{\"added\": {}}]', 8, 1),
(11, '2024-10-14 20:42:55.326476', '5', 'LaRousse', 1, '[{\"added\": {}}]', 8, 1),
(12, '2024-10-14 20:44:23.852826', '6', 'Wolfgang Amadeus Mozart', 1, '[{\"added\": {}}]', 8, 1),
(13, '2024-10-14 20:45:06.342867', '7', 'Mario Amorós', 1, '[{\"added\": {}}]', 8, 1),
(14, '2024-10-14 20:46:01.176083', '2', 'Ciencia ficción', 1, '[{\"added\": {}}]', 10, 1),
(15, '2024-10-14 20:46:28.076442', '3', 'Acción', 1, '[{\"added\": {}}]', 10, 1),
(16, '2024-10-14 20:46:54.963011', '4', 'Fantasía', 1, '[{\"added\": {}}]', 10, 1),
(17, '2024-10-14 20:48:22.988883', '5', 'Libros de referencia', 1, '[{\"added\": {}}]', 10, 1),
(18, '2024-10-14 20:50:02.449396', '6', 'Jean Blot', 2, '[{\"changed\": {\"fields\": [\"Nombre autor\"]}}]', 8, 1),
(19, '2024-10-14 20:50:08.134914', '6', 'Jean Blot', 2, '[]', 8, 1),
(20, '2024-10-14 20:50:55.560595', '6', 'biografía', 1, '[{\"added\": {}}]', 10, 1),
(21, '2024-10-14 20:53:04.915560', '8', 'Lesley-Ann Jones', 1, '[{\"added\": {}}]', 8, 1),
(22, '2024-10-14 20:53:40.813437', '7', 'Politica', 1, '[{\"added\": {}}]', 10, 1),
(23, '2024-10-14 21:07:14.717829', '1', 'PruebaArr1', 3, '', 15, 1),
(24, '2024-10-14 21:07:56.349663', '2', 'Los Juegos Del Hambre', 1, '[{\"added\": {}}]', 15, 1),
(25, '2024-10-14 21:08:29.707901', '3', 'Juego de Tronos', 1, '[{\"added\": {}}]', 15, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(20, 'admin_interface', 'theme'),
(7, 'app', 'arriendo'),
(8, 'app', 'autor'),
(9, 'app', 'carrito'),
(19, 'app', 'compra'),
(6, 'app', 'customuser'),
(10, 'app', 'generolib'),
(18, 'app', 'itemarriendo'),
(17, 'app', 'itemcarrito'),
(16, 'app', 'libro'),
(15, 'app', 'libroarr'),
(14, 'app', 'sub'),
(11, 'app', 'subscripcion'),
(12, 'app', 'tiposubcripscion'),
(13, 'app', 'usersub'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-10-12 00:59:25.014843'),
(2, 'contenttypes', '0002_remove_content_type_name', '2024-10-12 00:59:25.077676'),
(3, 'auth', '0001_initial', '2024-10-12 00:59:25.300220'),
(4, 'auth', '0002_alter_permission_name_max_length', '2024-10-12 00:59:25.357037'),
(5, 'auth', '0003_alter_user_email_max_length', '2024-10-12 00:59:25.365033'),
(6, 'auth', '0004_alter_user_username_opts', '2024-10-12 00:59:25.372017'),
(7, 'auth', '0005_alter_user_last_login_null', '2024-10-12 00:59:25.381448'),
(8, 'auth', '0006_require_contenttypes_0002', '2024-10-12 00:59:25.384859'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2024-10-12 00:59:25.393849'),
(10, 'auth', '0008_alter_user_username_max_length', '2024-10-12 00:59:25.400816'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2024-10-12 00:59:25.409792'),
(12, 'auth', '0010_alter_group_name_max_length', '2024-10-12 00:59:25.420761'),
(13, 'auth', '0011_update_proxy_permissions', '2024-10-12 00:59:25.430942'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2024-10-12 00:59:25.437750'),
(15, 'app', '0001_initial', '2024-10-12 00:59:26.940342'),
(16, 'admin', '0001_initial', '2024-10-12 00:59:27.072160'),
(17, 'admin', '0002_logentry_remove_auto_add', '2024-10-12 00:59:27.090112'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2024-10-12 00:59:27.113480'),
(19, 'admin_interface', '0001_initial', '2024-10-12 00:59:27.136439'),
(20, 'admin_interface', '0002_add_related_modal', '2024-10-12 00:59:27.199281'),
(21, 'admin_interface', '0003_add_logo_color', '2024-10-12 00:59:27.224891'),
(22, 'admin_interface', '0004_rename_title_color', '2024-10-12 00:59:27.242479'),
(23, 'admin_interface', '0005_add_recent_actions_visible', '2024-10-12 00:59:27.262426'),
(24, 'admin_interface', '0006_bytes_to_str', '2024-10-12 00:59:27.338578'),
(25, 'admin_interface', '0007_add_favicon', '2024-10-12 00:59:27.360542'),
(26, 'admin_interface', '0008_change_related_modal_background_opacity_type', '2024-10-12 00:59:27.396486'),
(27, 'admin_interface', '0009_add_enviroment', '2024-10-12 00:59:27.433141'),
(28, 'admin_interface', '0010_add_localization', '2024-10-12 00:59:27.460054'),
(29, 'admin_interface', '0011_add_environment_options', '2024-10-12 00:59:27.531009'),
(30, 'admin_interface', '0012_update_verbose_names', '2024-10-12 00:59:27.545652'),
(31, 'admin_interface', '0013_add_related_modal_close_button', '2024-10-12 00:59:27.569017'),
(32, 'admin_interface', '0014_name_unique', '2024-10-12 00:59:27.597517'),
(33, 'admin_interface', '0015_add_language_chooser_active', '2024-10-12 00:59:27.621418'),
(34, 'admin_interface', '0016_add_language_chooser_display', '2024-10-12 00:59:27.643433'),
(35, 'admin_interface', '0017_change_list_filter_dropdown', '2024-10-12 00:59:27.656033'),
(36, 'admin_interface', '0018_theme_list_filter_sticky', '2024-10-12 00:59:27.678875'),
(37, 'admin_interface', '0019_add_form_sticky', '2024-10-12 00:59:27.714991'),
(38, 'admin_interface', '0020_module_selected_colors', '2024-10-12 00:59:27.813044'),
(39, 'admin_interface', '0021_file_extension_validator', '2024-10-12 00:59:27.830237'),
(40, 'admin_interface', '0022_add_logo_max_width_and_height', '2024-10-12 00:59:27.870539'),
(41, 'admin_interface', '0023_theme_foldable_apps', '2024-10-12 00:59:27.895626'),
(42, 'admin_interface', '0024_remove_theme_css', '2024-10-12 00:59:27.937604'),
(43, 'admin_interface', '0025_theme_language_chooser_control', '2024-10-12 00:59:27.958874'),
(44, 'admin_interface', '0026_theme_list_filter_highlight', '2024-10-12 00:59:27.985767'),
(45, 'admin_interface', '0027_theme_list_filter_removal_links', '2024-10-12 00:59:28.010338'),
(46, 'admin_interface', '0028_theme_show_fieldsets_as_tabs_and_more', '2024-10-12 00:59:28.047401'),
(47, 'admin_interface', '0029_theme_css_generic_link_active_color', '2024-10-12 00:59:28.070635'),
(48, 'sessions', '0001_initial', '2024-10-12 00:59:28.109077');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1m95fayih4acoscu0cy04s3ek70fo1ka', '.eJxVjMEOwiAQRP-FsyEgy4oevfcbGpbdStVAUtqT8d-VpAfN3Oa9mZca47bmcWuyjDOri7Lq8NtRTA8pHfA9llvVqZZ1mUl3Re-06aGyPK-7-3eQY8t97Y78jUN0BGTO4k9MwUJKPFmfxFtAw2AcAKENE7AwIkAMjAJJ1PsD3hI3-g:1t0Rr7:wqaTMWrW7U61kZHr_x4LSWsqwyAmxPmO1pLb_yiqKRw', '2024-10-28 20:39:53.018594'),
('dzroq500jkfp4v7h48udp4weeo40h0rw', '.eJxVjDEOAiEQRe9CbUhAZhBLe89AhmGQVQPJslsZ766bbKHtf-_9l4q0LjWuQ-Y4ZXVWRh1-t0T8kLaBfKd265p7W-Yp6U3ROx362rM8L7v7d1Bp1G8NFtEhl8IUBLw3XCyhBYfJAZ18dsdCYB0KSWCyUFI2LD7YUEIwrN4f6VI4Sw:1szQVH:uUqHQ2gky9Hc_FzWC2fFnVKENhN8kXUmwAGrJuU8p8A', '2024-10-26 01:01:07.244590');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admin_interface_theme`
--
ALTER TABLE `admin_interface_theme`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `admin_interface_theme_name_30bda70f_uniq` (`name`);

--
-- Indices de la tabla `app_arriendo`
--
ALTER TABLE `app_arriendo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_arriendo_cliente_id_45434d16_fk_app_customuser_id` (`cliente_id`);

--
-- Indices de la tabla `app_autor`
--
ALTER TABLE `app_autor`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_carrito`
--
ALTER TABLE `app_carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_carrito_cliente_id_4321eb42_fk_app_customuser_id` (`cliente_id`);

--
-- Indices de la tabla `app_compra`
--
ALTER TABLE `app_compra`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_compra_cliente_id_66e2a9f0_fk_app_customuser_id` (`cliente_id`),
  ADD KEY `app_compra_producto_id_fada055c_fk_app_libro_id` (`producto_id`);

--
-- Indices de la tabla `app_customuser`
--
ALTER TABLE `app_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `app_customuser_groups`
--
ALTER TABLE `app_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_customuser_groups_customuser_id_group_id_a5a0ca22_uniq` (`customuser_id`,`group_id`),
  ADD KEY `app_customuser_groups_group_id_47e49ebd_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `app_customuser_user_permissions`
--
ALTER TABLE `app_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_customuser_user_perm_customuser_id_permission_22e31019_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `app_customuser_user__permission_id_c5920c75_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `app_generolib`
--
ALTER TABLE `app_generolib`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_itemarriendo`
--
ALTER TABLE `app_itemarriendo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_itemarriendo_arriendo_id_37fc288f_fk_app_arriendo_id` (`arriendo_id`),
  ADD KEY `app_itemarriendo_libro_id_4ca4e948_fk_app_libroarr_id` (`libro_id`);

--
-- Indices de la tabla `app_itemcarrito`
--
ALTER TABLE `app_itemcarrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_itemcarrito_carrito_id_02f22e19_fk_app_carrito_id` (`carrito_id`),
  ADD KEY `app_itemcarrito_producto_id_4e2f7064_fk_app_libro_id` (`producto_id`);

--
-- Indices de la tabla `app_libro`
--
ALTER TABLE `app_libro`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_libro_id_autor_id_5d82464f_fk_app_autor_id` (`id_autor_id`),
  ADD KEY `app_libro_id_genero_id_59bb8c99_fk_app_generolib_id` (`id_genero_id`);

--
-- Indices de la tabla `app_libroarr`
--
ALTER TABLE `app_libroarr`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_libroarr_id_autor_id_fc2e6e08_fk_app_autor_id` (`id_autor_id`),
  ADD KEY `app_libroarr_id_genero_id_8e8ecfdd_fk_app_generolib_id` (`id_genero_id`);

--
-- Indices de la tabla `app_sub`
--
ALTER TABLE `app_sub`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_sub_id_ts_id_10c803ad_fk_app_tiposubcripscion_id` (`id_ts_id`),
  ADD KEY `app_sub_id_us_id_50e92fd2_fk_app_customuser_id` (`id_us_id`);

--
-- Indices de la tabla `app_subscripcion`
--
ALTER TABLE `app_subscripcion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_tiposubcripscion`
--
ALTER TABLE `app_tiposubcripscion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_usersub`
--
ALTER TABLE `app_usersub`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_usersub_id_Sub_id_c5516a41_fk_app_subscripcion_id` (`id_Sub_id`),
  ADD KEY `app_usersub_id_usuario_id_c4ddb2c4_fk_app_customuser_id` (`id_usuario_id`);

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
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_app_customuser_id` (`user_id`);

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
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `admin_interface_theme`
--
ALTER TABLE `admin_interface_theme`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_arriendo`
--
ALTER TABLE `app_arriendo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `app_autor`
--
ALTER TABLE `app_autor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `app_carrito`
--
ALTER TABLE `app_carrito`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `app_compra`
--
ALTER TABLE `app_compra`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_customuser`
--
ALTER TABLE `app_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `app_customuser_groups`
--
ALTER TABLE `app_customuser_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_customuser_user_permissions`
--
ALTER TABLE `app_customuser_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_generolib`
--
ALTER TABLE `app_generolib`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `app_itemarriendo`
--
ALTER TABLE `app_itemarriendo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `app_itemcarrito`
--
ALTER TABLE `app_itemcarrito`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `app_libro`
--
ALTER TABLE `app_libro`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `app_libroarr`
--
ALTER TABLE `app_libroarr`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `app_sub`
--
ALTER TABLE `app_sub`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `app_subscripcion`
--
ALTER TABLE `app_subscripcion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_tiposubcripscion`
--
ALTER TABLE `app_tiposubcripscion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `app_usersub`
--
ALTER TABLE `app_usersub`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `app_arriendo`
--
ALTER TABLE `app_arriendo`
  ADD CONSTRAINT `app_arriendo_cliente_id_45434d16_fk_app_customuser_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_customuser` (`id`);

--
-- Filtros para la tabla `app_carrito`
--
ALTER TABLE `app_carrito`
  ADD CONSTRAINT `app_carrito_cliente_id_4321eb42_fk_app_customuser_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_customuser` (`id`);

--
-- Filtros para la tabla `app_compra`
--
ALTER TABLE `app_compra`
  ADD CONSTRAINT `app_compra_cliente_id_66e2a9f0_fk_app_customuser_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_customuser` (`id`),
  ADD CONSTRAINT `app_compra_producto_id_fada055c_fk_app_libro_id` FOREIGN KEY (`producto_id`) REFERENCES `app_libro` (`id`);

--
-- Filtros para la tabla `app_customuser_groups`
--
ALTER TABLE `app_customuser_groups`
  ADD CONSTRAINT `app_customuser_group_customuser_id_164d073f_fk_app_custo` FOREIGN KEY (`customuser_id`) REFERENCES `app_customuser` (`id`),
  ADD CONSTRAINT `app_customuser_groups_group_id_47e49ebd_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `app_customuser_user_permissions`
--
ALTER TABLE `app_customuser_user_permissions`
  ADD CONSTRAINT `app_customuser_user__customuser_id_4bcbaafb_fk_app_custo` FOREIGN KEY (`customuser_id`) REFERENCES `app_customuser` (`id`),
  ADD CONSTRAINT `app_customuser_user__permission_id_c5920c75_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Filtros para la tabla `app_itemarriendo`
--
ALTER TABLE `app_itemarriendo`
  ADD CONSTRAINT `app_itemarriendo_arriendo_id_37fc288f_fk_app_arriendo_id` FOREIGN KEY (`arriendo_id`) REFERENCES `app_arriendo` (`id`),
  ADD CONSTRAINT `app_itemarriendo_libro_id_4ca4e948_fk_app_libroarr_id` FOREIGN KEY (`libro_id`) REFERENCES `app_libroarr` (`id`);

--
-- Filtros para la tabla `app_itemcarrito`
--
ALTER TABLE `app_itemcarrito`
  ADD CONSTRAINT `app_itemcarrito_carrito_id_02f22e19_fk_app_carrito_id` FOREIGN KEY (`carrito_id`) REFERENCES `app_carrito` (`id`),
  ADD CONSTRAINT `app_itemcarrito_producto_id_4e2f7064_fk_app_libro_id` FOREIGN KEY (`producto_id`) REFERENCES `app_libro` (`id`);

--
-- Filtros para la tabla `app_libro`
--
ALTER TABLE `app_libro`
  ADD CONSTRAINT `app_libro_id_autor_id_5d82464f_fk_app_autor_id` FOREIGN KEY (`id_autor_id`) REFERENCES `app_autor` (`id`),
  ADD CONSTRAINT `app_libro_id_genero_id_59bb8c99_fk_app_generolib_id` FOREIGN KEY (`id_genero_id`) REFERENCES `app_generolib` (`id`);

--
-- Filtros para la tabla `app_libroarr`
--
ALTER TABLE `app_libroarr`
  ADD CONSTRAINT `app_libroarr_id_autor_id_fc2e6e08_fk_app_autor_id` FOREIGN KEY (`id_autor_id`) REFERENCES `app_autor` (`id`),
  ADD CONSTRAINT `app_libroarr_id_genero_id_8e8ecfdd_fk_app_generolib_id` FOREIGN KEY (`id_genero_id`) REFERENCES `app_generolib` (`id`);

--
-- Filtros para la tabla `app_sub`
--
ALTER TABLE `app_sub`
  ADD CONSTRAINT `app_sub_id_ts_id_10c803ad_fk_app_tiposubcripscion_id` FOREIGN KEY (`id_ts_id`) REFERENCES `app_tiposubcripscion` (`id`),
  ADD CONSTRAINT `app_sub_id_us_id_50e92fd2_fk_app_customuser_id` FOREIGN KEY (`id_us_id`) REFERENCES `app_customuser` (`id`);

--
-- Filtros para la tabla `app_usersub`
--
ALTER TABLE `app_usersub`
  ADD CONSTRAINT `app_usersub_id_Sub_id_c5516a41_fk_app_subscripcion_id` FOREIGN KEY (`id_Sub_id`) REFERENCES `app_subscripcion` (`id`),
  ADD CONSTRAINT `app_usersub_id_usuario_id_c4ddb2c4_fk_app_customuser_id` FOREIGN KEY (`id_usuario_id`) REFERENCES `app_customuser` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `app_customuser` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
