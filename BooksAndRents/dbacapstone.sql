-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-11-2024 a las 17:37:09
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
  `css_generic_link_active_color` varchar(10) NOT NULL,
  `collapsible_stacked_inlines` tinyint(1) NOT NULL,
  `collapsible_stacked_inlines_collapsed` tinyint(1) NOT NULL,
  `collapsible_tabular_inlines` tinyint(1) NOT NULL,
  `collapsible_tabular_inlines_collapsed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_arriendo`
--

CREATE TABLE `app_arriendo` (
  `id` bigint(20) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL,
  `arriendo_atraso` tinyint(1) NOT NULL,
  `libro_entregado` tinyint(1) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_arriendo`
--

INSERT INTO `app_arriendo` (`id`, `fecha_inicio`, `fecha_fin`, `arriendo_atraso`, `libro_entregado`, `cliente_id`, `producto_id`) VALUES
(1, '2024-11-14', '2024-11-21', 1, 1, 412, 11),
(90, '2024-11-21', '2024-11-21', 1, 1, 412, 11),
(124, '2024-11-06', '2024-11-14', 1, 0, 412, 11),
(123451, '2024-11-19', '2024-11-20', 1, 0, 123, 11),
(123452, '2024-11-18', '2024-12-18', 0, 0, 1, 11),
(123453, '2024-11-18', '2024-12-18', 0, 0, 1, 11),
(123454, '2024-11-18', '2024-12-18', 0, 0, 1, 2),
(123455, '2024-11-18', '2024-12-18', 0, 0, 1, 11),
(123456, '2024-11-18', '2024-12-18', 0, 0, 1, 2),
(123457, '2024-11-18', '2024-12-18', 0, 0, 1, 2),
(123458, '2024-11-18', '2024-12-18', 0, 0, 423, 2);

--
-- Disparadores `app_arriendo`
--
DELIMITER $$
CREATE TRIGGER `trg_fill_buffer_arriendos` AFTER INSERT ON `app_arriendo` FOR EACH ROW BEGIN
    DECLARE new_id_cliente INT;
    DECLARE new_id_tiempo INT;
    DECLARE new_id_arriendo INT;
    DECLARE new_id_estado INT;

    SET new_id_cliente = (SELECT id_cliente FROM etl.dimCliente WHERE email = (SELECT email FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id LIMIT 1));
    IF new_id_cliente IS NULL THEN
        INSERT INTO etl.dimCliente (email, rut, first_name, last_name, telefono)
        SELECT email, rut, first_name, last_name, telefono
        FROM dbacapstone.app_customuser
        WHERE id = NEW.cliente_id;
        SET new_id_cliente = LAST_INSERT_ID();
    END IF;

    SET new_id_tiempo = (SELECT id_tiempo_arriendo FROM etl.dimTiempoArriendos WHERE fecha_arriendo = NEW.fecha_inicio AND fecha_devolucion = NEW.fecha_fin LIMIT 1);
    IF new_id_tiempo IS NULL THEN
        INSERT INTO etl.dimTiempoArriendos (fecha_arriendo, fecha_devolucion, mes, anio, dia)
        VALUES (NEW.fecha_inicio, NEW.fecha_fin, MONTH(NEW.fecha_inicio), YEAR(NEW.fecha_inicio), DAY(NEW.fecha_inicio));
        SET new_id_tiempo = LAST_INSERT_ID();
    END IF;

    INSERT INTO etl.dimArriendos (nom_libro, nombre_autor, nombre_genero, stock_total_arriendo, id_tiempo_arriendo)
    SELECT 
        l.nom_libro,
        a.nombre_autor,
        g.nombre,
        l.stock,
        new_id_tiempo
    FROM dbacapstone.app_libroarr l
    LEFT JOIN dbacapstone.app_autor a ON l.id_autor_id = a.id
    LEFT JOIN dbacapstone.app_generolib g ON l.id_genero_id = g.id
    WHERE l.id = NEW.producto_id;
    SET new_id_arriendo = LAST_INSERT_ID();

    SET new_id_estado = (SELECT id_estado_devolucion FROM etl.dimEstadoDevolucion WHERE estado = NEW.libro_entregado LIMIT 1);
    IF new_id_estado IS NULL THEN
        INSERT INTO etl.dimEstadoDevolucion (estado)
        VALUES (NEW.libro_entregado);
        SET new_id_estado = LAST_INSERT_ID();
    END IF;

    INSERT INTO etl.hechos_buffer (id_compra, id_arriendo, id_cliente, id_estado_devolucion)
    VALUES (NULL, new_id_arriendo, new_id_cliente, new_id_estado);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_update_dimArriendos_on_update` AFTER UPDATE ON `app_arriendo` FOR EACH ROW BEGIN
    UPDATE etl.dimArriendos
    SET 
        nom_libro = (SELECT l.nom_libro FROM dbacapstone.app_libroarr l WHERE l.id = NEW.producto_id),
        nombre_autor = (SELECT a.nombre_autor FROM dbacapstone.app_libroarr l 
                        JOIN dbacapstone.app_autor a ON l.id_autor_id = a.id WHERE l.id = NEW.producto_id),
        nombre_genero = (SELECT g.nombre FROM dbacapstone.app_libroarr l 
                         JOIN dbacapstone.app_generolib g ON l.id_genero_id = g.id WHERE l.id = NEW.producto_id),
        stock_total_arriendo = (SELECT l.stock FROM dbacapstone.app_libroarr l WHERE l.id = NEW.producto_id)
    WHERE id_arriendo = OLD.id;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_update_dimEstadoDevolucion` AFTER UPDATE ON `app_arriendo` FOR EACH ROW BEGIN
    DECLARE id_estado INT;

    SET id_estado = (SELECT id_estado_devolucion 
                     FROM etl.dimEstadoDevolucion 
                     WHERE estado = NEW.libro_entregado 
                     LIMIT 1);

    IF id_estado IS NULL THEN
        INSERT INTO etl.dimEstadoDevolucion (estado)
        VALUES (NEW.libro_entregado);

        SET id_estado = LAST_INSERT_ID();
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_update_dimTiempoArriendos` AFTER UPDATE ON `app_arriendo` FOR EACH ROW BEGIN
    DECLARE id_tiempo INT;

    SET id_tiempo = (SELECT id_tiempo_arriendo FROM etl.dimTiempoArriendos 
                     WHERE fecha_arriendo = DATE(NEW.fecha_inicio) AND fecha_devolucion = DATE(NEW.fecha_fin) LIMIT 1);

    IF id_tiempo IS NULL THEN
        INSERT INTO etl.dimTiempoArriendos (fecha_arriendo, fecha_devolucion, dia, mes, anio)
        VALUES (DATE(NEW.fecha_inicio), DATE(NEW.fecha_fin), DAY(NEW.fecha_inicio), MONTH(NEW.fecha_inicio), YEAR(NEW.fecha_inicio));

        SET id_tiempo = LAST_INSERT_ID();
    END IF;

    UPDATE etl.dimArriendos
    SET 
        nom_libro = (SELECT l.nom_libro FROM dbacapstone.app_libroarr l WHERE l.id = NEW.producto_id),
        nombre_autor = (SELECT a.nombre_autor FROM dbacapstone.app_libroarr l 
                        JOIN dbacapstone.app_autor a ON l.id_autor_id = a.id WHERE l.id = NEW.producto_id),
        nombre_genero = (SELECT g.nombre FROM dbacapstone.app_libroarr l 
                         JOIN dbacapstone.app_generolib g ON l.id_genero_id = g.id WHERE l.id = NEW.producto_id),
        stock_total_arriendo = (SELECT l.stock FROM dbacapstone.app_libroarr l WHERE l.id = NEW.producto_id),
        id_tiempo_arriendo = id_tiempo
    WHERE id_arriendo = OLD.id;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_update_dimTiempoArriendos_on_update` AFTER UPDATE ON `app_arriendo` FOR EACH ROW BEGIN
    DECLARE id_tiempo INT;

    SET id_tiempo = (SELECT id_tiempo_arriendo FROM etl.dimTiempoArriendos 
                     WHERE fecha_arriendo = DATE(NEW.fecha_inicio) AND fecha_devolucion = DATE(NEW.fecha_fin) LIMIT 1);

    IF id_tiempo IS NULL THEN
        INSERT INTO etl.dimTiempoArriendos (fecha_arriendo, fecha_devolucion, dia, mes, anio)
        VALUES (DATE(NEW.fecha_inicio), DATE(NEW.fecha_fin), DAY(NEW.fecha_inicio), MONTH(NEW.fecha_inicio), YEAR(NEW.fecha_inicio));

        SET id_tiempo = LAST_INSERT_ID();
    END IF;

    UPDATE etl.dimArriendos
    SET 
        id_tiempo_arriendo = id_tiempo
    WHERE id_arriendo = OLD.id;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trigger_eliminar_arriendo` AFTER DELETE ON `app_arriendo` FOR EACH ROW BEGIN
    DELETE etl.dimArriendos
    FROM etl.dimArriendos
    JOIN etl.dimTiempoArriendos
    ON etl.dimArriendos.id_tiempo_arriendo = etl.dimTiempoArriendos.id_tiempo_arriendo
    WHERE etl.dimTiempoArriendos.fecha_arriendo = DATE(OLD.fecha_inicio)
      AND etl.dimTiempoArriendos.fecha_devolucion = DATE(OLD.fecha_fin);

    DELETE etl.dimTiempoArriendos
    FROM etl.dimTiempoArriendos
    LEFT JOIN etl.dimArriendos
    ON etl.dimTiempoArriendos.id_tiempo_arriendo = etl.dimArriendos.id_tiempo_arriendo
    WHERE etl.dimTiempoArriendos.fecha_arriendo = DATE(OLD.fecha_inicio)
      AND etl.dimTiempoArriendos.fecha_devolucion = DATE(OLD.fecha_fin)
      AND etl.dimArriendos.id_tiempo_arriendo IS NULL;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trigger_update_cliente_arriendo` AFTER UPDATE ON `app_arriendo` FOR EACH ROW BEGIN
    UPDATE etl.dimCliente
    SET 
        email = (SELECT email FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        rut = (SELECT rut FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        first_name = (SELECT first_name FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        last_name = (SELECT last_name FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        telefono = (SELECT telefono FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id)
    WHERE id_cliente = NEW.cliente_id;
END
$$
DELIMITER ;

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
(3, 'George R. R. Martinasdas'),
(4, 'J. K. Rowling'),
(5, 'LaRousse'),
(6, 'Jean Blot'),
(7, 'Mario Amorós'),
(8, 'Lesley-Ann Jones'),
(9, 'Jordi Wild'),
(10, 'Freida McFADDEN'),
(11, 'Dolores Redondo'),
(12, 'Han Kang'),
(13, 'Javier Castillo'),
(14, 'David J.Schwartz'),
(15, 'Vicente Raga'),
(16, 'Kelvin Torres');

--
-- Disparadores `app_autor`
--
DELIMITER $$
CREATE TRIGGER `trg_update_autor_genero_on_update` AFTER UPDATE ON `app_autor` FOR EACH ROW BEGIN
    -- Actualizar el nombre del autor en dimCompras
    UPDATE etl.dimCompras
    SET
        nombre_autor = NEW.nombre_autor
    WHERE
        nombre_autor = OLD.nombre_autor;

    -- Actualizar el nombre del autor en dimArriendos
    UPDATE etl.dimArriendos
    SET
        nombre_autor = NEW.nombre_autor
    WHERE
        nombre_autor = OLD.nombre_autor;
END
$$
DELIMITER ;

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
(1, 1),
(2, 413),
(3, 414),
(4, 416),
(5, 417),
(6, 418),
(7, 419),
(8, 420),
(9, 421),
(10, 422),
(11, 423);

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

--
-- Volcado de datos para la tabla `app_compra`
--

INSERT INTO `app_compra` (`id`, `cantidad`, `fecha_compra`, `cliente_id`, `producto_id`) VALUES
(1, 2, '2023-11-02 22:46:22.000000', 413, 23),
(2, 2, '2023-11-04 22:47:39.000000', 417, 28),
(3, 1, '2023-11-15 22:49:27.000000', 421, 31),
(4, 3, '2023-11-18 22:49:59.000000', 422, 30),
(5, 2, '2023-11-25 22:51:16.000000', 419, 31),
(6, 1, '2023-11-28 22:52:26.000000', 422, 24),
(7, 2, '2023-11-29 22:52:57.000000', 414, 31),
(8, 1, '2023-11-30 22:53:20.000000', 421, 24),
(12428, 1, '2024-11-17 23:37:20.141886', 1, 24),
(12429, 1, '2024-11-17 23:39:10.121989', 1, 23),
(12430, 1, '2024-11-17 23:50:00.562128', 1, 23),
(12431, 1, '2024-11-17 23:51:31.299886', 1, 23),
(12432, 1, '2024-11-17 23:53:31.112887', 1, 24),
(12433, 1, '2024-11-17 23:56:07.267925', 1, 23),
(12434, 1, '2024-11-17 23:56:07.273910', 1, 24),
(12435, 1, '2024-11-18 01:06:46.657021', 416, 30),
(12436, 1, '2024-11-18 01:06:46.665997', 416, 23),
(12437, 3, '2024-11-18 01:07:58.763999', 416, 23),
(12438, 2, '2024-11-18 01:11:17.299864', 417, 24),
(12439, 1, '2024-11-18 01:11:17.306844', 417, 25),
(12440, 1, '2024-11-18 01:13:05.423250', 417, 28),
(12441, 1, '2024-11-18 01:13:05.429238', 417, 31),
(12442, 1, '2024-11-18 01:13:05.434791', 417, 24),
(12443, 2, '2024-11-18 01:15:09.245751', 418, 30),
(12444, 1, '2024-11-18 01:15:09.252061', 418, 23),
(12445, 1, '2024-11-18 01:17:33.373971', 418, 29),
(12446, 1, '2024-11-18 01:17:33.375697', 418, 25),
(12447, 1, '2024-11-18 01:19:54.172105', 419, 23),
(12448, 1, '2024-11-18 01:19:54.177346', 419, 30),
(12449, 1, '2024-11-18 01:19:54.180338', 419, 28),
(12450, 2, '2024-11-18 01:21:52.501530', 419, 31),
(12451, 1, '2024-11-18 01:21:52.504603', 419, 23),
(12452, 1, '2024-11-18 01:21:52.506601', 419, 30),
(12453, 2, '2024-11-18 01:24:23.461013', 420, 23),
(12454, 3, '2024-11-18 01:24:23.465982', 420, 24),
(12455, 1, '2024-11-18 01:24:23.467976', 420, 25),
(12456, 3, '2024-11-18 01:25:17.201662', 420, 29),
(12457, 1, '2024-11-18 01:25:17.204655', 420, 31),
(12458, 4, '2024-11-18 01:26:09.363191', 420, 23),
(12459, 4, '2024-11-18 01:28:09.665083', 421, 28),
(12460, 5, '2024-11-18 01:28:09.668699', 421, 30),
(12461, 2, '2024-11-18 01:28:09.670695', 421, 31),
(12462, 2, '2024-11-18 01:29:32.225362', 421, 24),
(12463, 2, '2024-11-18 01:29:32.231345', 421, 28),
(12464, 1, '2024-11-18 01:29:32.233340', 421, 29),
(12465, 4, '2024-11-18 01:35:20.295623', 422, 23),
(12466, 3, '2024-11-18 01:35:20.301614', 422, 25),
(12467, 3, '2024-11-18 01:35:20.305602', 422, 28),
(12468, 2, '2024-11-18 01:35:20.307597', 422, 30),
(12469, 3, '2024-11-18 01:36:34.332891', 422, 30),
(12470, 1, '2024-11-18 01:36:34.336881', 422, 31),
(12471, 1, '2024-11-18 12:21:03.549481', 1, 24),
(12472, 1, '2023-12-02 10:15:22.000000', 413, 23),
(12473, 2, '2023-12-05 12:47:39.000000', 417, 28),
(12474, 1, '2023-12-10 09:33:15.000000', 421, 31),
(12475, 3, '2023-12-15 15:20:40.000000', 422, 30),
(12476, 2, '2023-12-18 18:45:00.000000', 419, 24),
(12480, 1, '2024-01-03 16:20:15.000000', 420, 30),
(12481, 2, '2024-01-08 10:50:30.000000', 422, 31),
(12482, 3, '2024-01-12 09:40:05.000000', 413, 23),
(12483, 1, '2024-01-16 14:15:55.000000', 417, 24),
(12486, 1, '2024-01-28 18:10:45.000000', 418, 25),
(12487, 1, '2024-01-31 21:15:22.000000', 414, 29),
(12489, 1, '2024-02-07 13:15:33.000000', 420, 30),
(12490, 3, '2024-02-10 11:40:50.000000', 421, 28),
(12491, 2, '2024-02-14 09:30:00.000000', 413, 24),
(12492, 1, '2024-02-18 18:20:45.000000', 422, 29),
(12493, 2, '2024-02-21 12:45:50.000000', 419, 23),
(12494, 1, '2024-02-25 15:50:22.000000', 417, 25),
(12495, 2, '2024-02-28 20:25:10.000000', 418, 30),
(12496, 3, '2024-03-02 10:10:10.000000', 414, 23),
(12497, 1, '2024-03-06 09:20:33.000000', 413, 28),
(12498, 2, '2024-03-11 17:40:22.000000', 416, 31),
(12499, 1, '2024-03-15 16:35:10.000000', 420, 24),
(12500, 2, '2024-03-19 14:25:55.000000', 421, 30),
(12501, 1, '2024-03-23 08:10:40.000000', 419, 29),
(12502, 3, '2024-03-27 11:45:00.000000', 417, 31),
(12503, 2, '2024-03-30 19:20:10.000000', 422, 25),
(12504, 1, '2024-04-02 12:15:30.000000', 421, 23),
(12505, 2, '2024-04-06 10:45:22.000000', 419, 28),
(12506, 3, '2024-04-10 16:20:10.000000', 416, 30),
(12509, 1, '2024-04-23 09:10:55.000000', 422, 29),
(12510, 2, '2024-04-27 13:20:33.000000', 413, 25),
(12511, 1, '2024-04-30 15:15:22.000000', 417, 28),
(12512, 2, '2024-05-02 08:40:33.000000', 418, 24),
(12513, 1, '2024-05-06 10:20:15.000000', 420, 30),
(12514, 3, '2024-05-10 13:45:10.000000', 413, 31),
(12515, 2, '2024-05-14 16:15:33.000000', 417, 28),
(12516, 1, '2024-05-18 11:30:00.000000', 419, 29),
(12517, 2, '2024-05-22 14:10:22.000000', 422, 23),
(12518, 3, '2024-05-26 17:25:10.000000', 421, 25),
(12519, 1, '2024-05-30 20:50:40.000000', 416, 28),
(12520, 2, '2024-06-03 09:20:15.000000', 420, 24),
(12521, 1, '2024-06-07 11:50:40.000000', 419, 30),
(12522, 3, '2024-06-11 10:35:55.000000', 413, 31),
(12523, 2, '2024-06-15 18:15:22.000000', 414, 28),
(12524, 1, '2024-06-19 15:45:33.000000', 417, 29),
(12525, 3, '2024-06-23 12:30:00.000000', 421, 31),
(12526, 1, '2024-06-27 14:40:50.000000', 422, 23),
(12527, 2, '2024-06-30 20:25:33.000000', 416, 25),
(12528, 3, '2024-07-02 16:20:10.000000', 413, 30),
(12529, 1, '2024-07-06 09:45:33.000000', 420, 28),
(12530, 2, '2024-07-10 10:35:22.000000', 421, 24),
(12531, 3, '2024-07-14 17:15:00.000000', 414, 29),
(12532, 2, '2024-07-18 14:30:55.000000', 419, 31),
(12533, 1, '2024-07-22 11:20:10.000000', 417, 25),
(12534, 3, '2024-07-26 15:40:33.000000', 422, 28),
(12535, 2, '2024-07-30 20:15:22.000000', 416, 30),
(12536, 1, '2024-08-02 09:30:10.000000', 413, 31),
(12537, 2, '2024-08-06 12:20:15.000000', 420, 24),
(12538, 3, '2024-08-10 16:45:22.000000', 419, 30),
(12539, 1, '2024-08-14 14:10:40.000000', 421, 29),
(12540, 2, '2024-08-18 11:35:33.000000', 422, 23),
(12541, 1, '2024-08-22 13:50:55.000000', 417, 25),
(12542, 3, '2024-08-26 17:25:10.000000', 416, 28),
(12543, 2, '2024-08-30 21:15:22.000000', 414, 31),
(12544, 2, '2024-09-03 08:45:33.000000', 420, 30),
(12545, 1, '2024-09-07 10:30:22.000000', 422, 28),
(12546, 3, '2024-09-11 11:20:10.000000', 413, 24),
(12547, 2, '2024-09-15 18:10:50.000000', 419, 31),
(12548, 1, '2024-09-19 15:50:40.000000', 417, 29),
(12549, 3, '2024-09-23 09:40:33.000000', 414, 23),
(12550, 1, '2024-09-27 13:25:22.000000', 421, 28),
(12551, 2, '2024-09-30 19:45:33.000000', 416, 31),
(12552, 1, '2024-10-02 09:15:22.000000', 422, 30),
(12553, 2, '2024-10-06 11:50:33.000000', 420, 24),
(12554, 3, '2024-10-10 14:20:10.000000', 413, 31),
(12555, 1, '2024-10-14 17:30:22.000000', 419, 28),
(12556, 2, '2024-10-18 15:45:33.000000', 417, 29),
(12557, 1, '2024-10-22 08:40:40.000000', 421, 25),
(12558, 3, '2024-10-26 13:20:55.000000', 414, 23),
(12559, 2, '2024-10-30 20:15:33.000000', 416, 30),
(12560, 2, '2024-09-02 10:30:22.000000', 420, 24),
(12561, 1, '2024-09-07 12:20:15.000000', 419, 30),
(12562, 3, '2024-09-14 16:45:10.000000', 417, 31),
(12563, 2, '2024-09-19 14:10:33.000000', 413, 28),
(12565, 3, '2024-10-01 08:45:33.000000', 420, 31),
(12566, 1, '2024-10-05 11:35:22.000000', 414, 25),
(12567, 2, '2024-10-10 14:50:55.000000', 419, 24),
(12568, 3, '2024-10-18 16:20:33.000000', 421, 28),
(12569, 1, '2024-10-25 19:15:22.000000', 417, 30),
(12570, 1, '2024-09-03 09:15:45.000000', 418, 24),
(12571, 2, '2024-09-10 11:50:33.000000', 416, 30),
(12572, 1, '2024-09-20 15:40:22.000000', 421, 28),
(12573, 3, '2024-09-28 20:25:10.000000', 419, 31),
(12574, 2, '2024-10-03 10:25:11.000000', 422, 24),
(12575, 1, '2024-10-08 13:45:33.000000', 413, 29),
(12576, 3, '2024-10-15 17:35:50.000000', 414, 28),
(12577, 1, '2024-10-27 21:10:40.000000', 416, 30),
(12578, 1, '2024-11-18 14:16:18.214096', 423, 23),
(12579, 2, '2024-11-18 15:57:19.532608', 423, 24),
(12580, 1, '2024-11-18 15:57:19.554548', 423, 23),
(12581, 1, '2024-11-18 15:57:19.563363', 423, 25),
(12582, 1, '2024-11-18 15:57:19.570348', 423, 28),
(12583, 1, '2024-11-18 15:57:19.578330', 423, 29),
(12584, 1, '2024-11-18 15:57:19.586301', 423, 30),
(12585, 1, '2024-11-18 15:57:19.594287', 423, 34),
(12586, 1, '2024-11-18 15:57:19.604757', 423, 33),
(12587, 1, '2024-11-18 15:57:19.614731', 423, 31),
(12588, 1, '2024-11-18 15:57:19.623263', 423, 35),
(12589, 1, '2024-11-18 15:57:19.631276', 423, 36),
(12590, 4, '2023-11-01 10:00:00.000000', 423, 24),
(12591, 2, '2023-11-01 10:05:00.000000', 416, 23),
(12592, 2, '2023-11-01 10:10:00.000000', 417, 25),
(12593, 2, '2023-11-05 11:20:00.000000', 418, 28),
(12594, 1, '2023-11-10 14:30:00.000000', 419, 29),
(12595, 3, '2023-11-15 15:40:00.000000', 420, 30),
(12596, 1, '2023-11-20 16:50:00.000000', 421, 34),
(12597, 2, '2023-11-25 17:00:00.000000', 422, 33),
(12598, 1, '2023-11-30 18:10:00.000000', 416, 31),
(12599, 1, '2023-11-30 18:20:00.000000', 417, 35),
(12600, 2, '2023-12-01 10:15:00.000000', 418, 36),
(12601, 3, '2023-12-03 11:25:00.000000', 419, 24),
(12602, 2, '2023-12-05 12:00:00.000000', 420, 23),
(12603, 1, '2023-12-10 13:10:00.000000', 421, 25),
(12604, 3, '2023-12-15 14:00:00.000000', 422, 28),
(12605, 1, '2023-12-18 16:00:00.000000', 416, 29),
(12606, 1, '2023-12-20 17:00:00.000000', 417, 30),
(12607, 2, '2023-12-22 18:00:00.000000', 418, 34),
(12608, 2, '2023-12-25 19:30:00.000000', 419, 33),
(12609, 2, '2023-12-30 10:30:00.000000', 420, 31),
(12610, 5, '2024-01-01 10:30:00.000000', 421, 35),
(12611, 3, '2024-01-05 11:30:00.000000', 422, 36),
(12612, 2, '2024-01-12 13:00:00.000000', 416, 24),
(12613, 2, '2024-01-15 14:00:00.000000', 417, 23),
(12614, 1, '2024-01-20 15:15:00.000000', 418, 25),
(12615, 2, '2024-01-22 16:30:00.000000', 419, 28),
(12616, 3, '2024-01-25 17:45:00.000000', 420, 29),
(12617, 1, '2024-01-30 18:00:00.000000', 421, 30),
(12618, 2, '2024-02-01 09:10:00.000000', 422, 34),
(12619, 4, '2024-02-05 10:20:00.000000', 416, 33),
(12620, 1, '2024-02-10 11:30:00.000000', 417, 31),
(12621, 2, '2024-02-15 13:00:00.000000', 418, 35),
(12622, 1, '2024-02-20 14:15:00.000000', 419, 36),
(12623, 3, '2024-02-25 15:45:00.000000', 420, 24),
(12624, 2, '2024-02-28 16:00:00.000000', 421, 23),
(12625, 1, '2024-03-01 09:00:00.000000', 422, 25),
(12626, 2, '2024-03-05 10:05:00.000000', 416, 28),
(12627, 4, '2024-03-10 11:10:00.000000', 417, 29),
(12628, 1, '2024-03-15 12:15:00.000000', 418, 30),
(12629, 2, '2024-03-20 13:30:00.000000', 419, 34),
(12630, 3, '2024-03-25 14:40:00.000000', 420, 33),
(12631, 1, '2024-03-30 15:50:00.000000', 421, 31),
(12632, 3, '2024-04-01 09:00:00.000000', 422, 35),
(12633, 1, '2024-04-05 10:05:00.000000', 416, 36),
(12634, 2, '2024-04-10 11:10:00.000000', 417, 24),
(12635, 2, '2024-04-15 12:15:00.000000', 418, 23),
(12636, 3, '2024-04-20 13:30:00.000000', 419, 25),
(12637, 1, '2024-04-25 14:40:00.000000', 420, 28),
(12638, 2, '2024-04-30 15:50:00.000000', 421, 29),
(12639, 1, '2024-05-01 09:00:00.000000', 422, 30),
(12640, 2, '2024-05-05 10:05:00.000000', 416, 34),
(12641, 2, '2024-05-10 11:10:00.000000', 417, 33),
(12642, 3, '2024-05-15 12:15:00.000000', 418, 31),
(12643, 3, '2024-05-20 13:20:00.000000', 419, 35),
(12644, 1, '2024-05-25 14:25:00.000000', 420, 36),
(12645, 2, '2024-05-30 15:30:00.000000', 421, 24),
(12646, 2, '2024-06-01 09:30:00.000000', 422, 23),
(12647, 2, '2024-06-05 10:35:00.000000', 416, 25),
(12648, 1, '2024-06-10 11:40:00.000000', 417, 28),
(12649, 3, '2024-06-15 12:45:00.000000', 418, 29),
(12650, 1, '2024-06-20 13:50:00.000000', 419, 30),
(12651, 1, '2024-06-25 14:55:00.000000', 420, 34),
(12652, 2, '2024-06-30 15:00:00.000000', 421, 33),
(12653, 2, '2024-07-01 09:00:00.000000', 422, 31),
(12654, 2, '2024-07-05 10:10:00.000000', 416, 35),
(12655, 3, '2024-07-10 11:20:00.000000', 417, 36),
(12656, 2, '2024-07-15 12:30:00.000000', 418, 24),
(12657, 3, '2024-07-20 13:40:00.000000', 419, 23),
(12658, 1, '2024-07-25 14:50:00.000000', 420, 25),
(12659, 2, '2024-07-30 15:00:00.000000', 421, 28),
(12660, 3, '2024-08-01 09:30:00.000000', 422, 29),
(12661, 1, '2024-08-05 10:40:00.000000', 416, 30),
(12662, 2, '2024-08-10 11:50:00.000000', 417, 34),
(12663, 2, '2024-08-15 12:00:00.000000', 418, 33),
(12664, 3, '2024-08-20 13:10:00.000000', 419, 31),
(12665, 4, '2024-08-25 14:20:00.000000', 420, 35),
(12666, 2, '2024-08-30 15:30:00.000000', 421, 36),
(12667, 3, '2024-09-01 09:40:00.000000', 422, 24),
(12668, 2, '2024-09-05 10:50:00.000000', 416, 23),
(12669, 1, '2024-09-10 11:00:00.000000', 417, 25),
(12670, 2, '2024-09-15 12:10:00.000000', 418, 28),
(12671, 3, '2024-09-20 13:20:00.000000', 419, 29),
(12672, 1, '2024-09-25 14:30:00.000000', 420, 30),
(12673, 2, '2024-09-30 15:40:00.000000', 421, 34),
(12674, 3, '2024-10-01 09:00:00.000000', 422, 33),
(12675, 2, '2024-10-05 10:10:00.000000', 416, 31),
(12676, 3, '2024-10-10 11:20:00.000000', 417, 35),
(12677, 2, '2024-10-15 12:30:00.000000', 418, 36),
(12678, 3, '2024-10-20 13:40:00.000000', 419, 24),
(12679, 3, '2024-10-25 14:50:00.000000', 420, 23),
(12680, 2, '2024-10-30 15:00:00.000000', 421, 25);

--
-- Disparadores `app_compra`
--
DELIMITER $$
CREATE TRIGGER `trg_delete_dimCompras` AFTER DELETE ON `app_compra` FOR EACH ROW BEGIN
    -- Eliminar el registro correspondiente en dimCompras
    DELETE FROM etl.dimCompras
    WHERE nom_libro = (SELECT p.nom_libro 
                       FROM dbacapstone.app_libro p
                       WHERE p.id = OLD.producto_id);

    -- Verificar si la fecha de compra aún tiene referencias en dimCompras, si no, eliminar de dimTiempoCompras
    IF NOT EXISTS (SELECT 1 FROM etl.dimCompras WHERE id_tiempo_compra = (SELECT id_tiempo_compra FROM etl.dimTiempoCompras WHERE fecha_compra = DATE(OLD.fecha_compra) LIMIT 1)) THEN
        DELETE FROM etl.dimTiempoCompras
        WHERE fecha_compra = DATE(OLD.fecha_compra);
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_fill_buffer_compras` AFTER INSERT ON `app_compra` FOR EACH ROW BEGIN
    DECLARE new_id_cliente INT;
    DECLARE new_id_tiempo INT;
    DECLARE new_id_compra INT;

    -- Verificar o insertar en etl.dimCliente usando cliente_id
    SET new_id_cliente = (SELECT id_cliente FROM etl.dimCliente WHERE email = (SELECT email FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id LIMIT 1));
    IF new_id_cliente IS NULL THEN
        INSERT INTO etl.dimCliente (email, rut, first_name, last_name, telefono)
        SELECT email, rut, first_name, last_name, telefono
        FROM dbacapstone.app_customuser
        WHERE id = NEW.cliente_id;
        SET new_id_cliente = LAST_INSERT_ID();
    END IF;

    -- Verificar o insertar en etl.dimTiempoCompras
    SET new_id_tiempo = (SELECT id_tiempo_compra FROM etl.dimTiempoCompras WHERE fecha_compra = DATE(NEW.fecha_compra) LIMIT 1);
    IF new_id_tiempo IS NULL THEN
        INSERT INTO etl.dimTiempoCompras (fecha_compra, dia, mes, anio)
        VALUES (DATE(NEW.fecha_compra), DAY(NEW.fecha_compra), MONTH(NEW.fecha_compra), YEAR(NEW.fecha_compra));
        SET new_id_tiempo = LAST_INSERT_ID();
    END IF;

    -- Insertar en etl.dimCompras
    INSERT INTO etl.dimCompras (nom_libro, precio, stock_total_compras, cantidad_comprado, nombre_autor, nombre_genero, id_tiempo_compra)
    SELECT 
        l.nom_libro,
        l.precio,
        l.stock,
        NEW.cantidad,
        a.nombre_autor,
        g.nombre,
        new_id_tiempo
    FROM dbacapstone.app_libro l
    LEFT JOIN dbacapstone.app_autor a ON l.id_autor_id = a.id
    LEFT JOIN dbacapstone.app_generolib g ON l.id_genero_id = g.id
    WHERE l.id = NEW.producto_id;
    SET new_id_compra = LAST_INSERT_ID();

    -- Insertar en etl.hechos_buffer
    INSERT INTO etl.hechos_buffer (id_compra, id_arriendo, id_cliente, id_estado_devolucion)
    VALUES (new_id_compra, NULL, new_id_cliente, NULL);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_update_dimCompras` AFTER UPDATE ON `app_compra` FOR EACH ROW BEGIN
    DECLARE id_tiempo INT;

    -- Verificar si ya existe el id_tiempo_compra en dimTiempoCompras para la fecha de compra actualizada
    SET id_tiempo = (SELECT id_tiempo_compra FROM etl.dimTiempoCompras WHERE fecha_compra = DATE(NEW.fecha_compra) LIMIT 1);

    -- Si no existe, insertar una nueva entrada en dimTiempoCompras
    IF id_tiempo IS NULL THEN
        INSERT INTO etl.dimTiempoCompras (fecha_compra, dia, mes, anio)
        VALUES (DATE(NEW.fecha_compra), DAY(NEW.fecha_compra), MONTH(NEW.fecha_compra), YEAR(NEW.fecha_compra));

        SET id_tiempo = LAST_INSERT_ID(); -- Obtén el id_tiempo_compra recién insertado
    END IF;

    -- Actualizar el registro en dimCompras relacionado con el producto modificado
    UPDATE etl.dimCompras
    SET 
        cantidad_comprado = NEW.cantidad,
        id_tiempo_compra = id_tiempo
    WHERE 
        id_tiempo_compra = (SELECT id_tiempo_compra FROM etl.dimTiempoCompras WHERE fecha_compra = DATE(OLD.fecha_compra) LIMIT 1)
        AND nom_libro = (SELECT p.nom_libro 
                        FROM dbacapstone.app_libro p
                        WHERE p.id = NEW.producto_id);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trigger_update_cliente_compra` AFTER UPDATE ON `app_compra` FOR EACH ROW BEGIN
    -- Actualizar cliente en dimCliente si hay cambios en app_compra
    UPDATE etl.dimCliente
    SET 
        email = (SELECT email FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        rut = (SELECT rut FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        first_name = (SELECT first_name FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        last_name = (SELECT last_name FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id),
        telefono = (SELECT telefono FROM dbacapstone.app_customuser WHERE id = NEW.cliente_id)
    WHERE id_cliente = NEW.cliente_id;
END
$$
DELIMITER ;

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
(1, 'pbkdf2_sha256$260000$Db9aTyD5xBSBpeNXWQicjJ$UMQ755RyyNpHh0V3vCuwWB1M+M5IffkPB55KGF0NFBU=', '2024-11-18 14:14:32.920330', 1, 'admin@admin.cl', NULL, 'admin', 'adminna', 1234567812, '2024-11-12', 'Noneaaaaaaaaaa', 1, 1, '2024-10-12 01:00:40.080086'),
(2, 'pbkdf2_sha256$260000$WlkdBMZQzDrNM4MrbNXSsl$KLGQuODfBxiB4S7Y3ciB27BcxqTbs8h9QIPRGxX53Do=', '2024-10-14 20:33:58.225366', 0, 'jose@jose.cl', '123456789', 'jose', 'jose', 123658412, '2002-01-09', 'lota 45', 0, 1, '2024-10-14 20:33:58.221378'),
(123, 'asd', '2024-11-05 16:41:29.000000', 1, '123', '123', '123', '123', 123, '2024-11-11', '123', 1, 1, '2024-11-07 16:41:29.000000'),
(412, '123', '2024-11-05 16:41:29.000000', 1, '12315', '123456789-1', '123', '123', 5, '2024-11-03', '123515', 1, 2, '2024-11-07 16:41:29.000000'),
(413, 'pbkdf2_sha256$260000$G3NWB2TwB5BAbEb6WnpqaI$Mop0HCyrc0GEZYPt2W/xSVX/wb0QKoR/dg5XkWiP9pA=', '2024-11-14 02:19:08.769546', 0, 'a@a.cl', '200839749', 'aasdasd', 'aasdasd', 934366162, '1998-12-02', 'Miguel Angel 3721, Dpto A24', 0, 1, '2024-11-14 02:18:47.215464'),
(414, 'pbkdf2_sha256$390000$fiIpudfleUnwiVkahhHAH6$wB18T9av1qDujQBYwRu/Jsusjwve2laPtG3NX6WmyUc=', '2024-11-17 02:05:10.627595', 0, 'pepe@tapia.cl', '11.877.923-1', 'pepe', 'tapia', 48137575, '1996-04-30', 'Lagunillas 3192', 0, 1, '2024-11-17 02:05:10.616652'),
(416, 'pbkdf2_sha256$260000$1mjcjRpWHBL3hUGVF9nYIA$AynJyJgtEuRVivf+3tXaP/lD/Q5hsM0YkCSYazFFEH8=', '2024-11-18 02:58:33.800863', 0, 'javier@gmail.com', '987632546-0', 'javier', 'Contreras', 981415111, '2002-01-09', 'lota 45', 0, 1, '2024-11-18 01:05:43.090151'),
(417, 'pbkdf2_sha256$260000$xmPSyKVrR9vEnlIHVYeY1w$SbA5ZZl8jkXm1UrRHqBg6DlTJohn5onT0lvEtq8uJVI=', '2024-11-18 01:10:00.330304', 0, 'Bastian@gmail.com', '120987654-2', 'Bastian', 'chamblas', 981415111, '2002-01-09', 'lota 45', 0, 1, '2024-11-18 01:10:00.324546'),
(418, 'pbkdf2_sha256$260000$AurJd77Igg89NCxNRbOC4q$WAlj5kge1XLCZ3kypSmIzaJP7P0LXAThZx2sb838Yg0=', '2024-11-18 01:13:48.873287', 0, 'Nicolas@gmail.com', '987632546', 'Nicolas', 'Nico', 981415111, '2002-01-09', 'lota 45', 0, 1, '2024-11-18 01:13:48.868302'),
(419, 'pbkdf2_sha256$260000$5IZuFUxVlo325dFTnXLRTH$XET42MfIwXStbyw9O0wHdcX3l23dEAtWoQ6twH2IC4c=', '2024-11-18 01:18:57.802076', 0, 'jose@gmail.com', '21.117.906-6', 'jose', 'agurto', 981415111, '2002-01-09', 'mi casita', 0, 1, '2024-11-18 01:18:57.798087'),
(420, 'pbkdf2_sha256$260000$J4wjzdKHA1TYDCzbqa9eVH$edU+qvAe7avrSTO/yRQ0vObGpCULVV450kEUDG0Yt+Y=', '2024-11-18 01:23:10.164393', 0, 'manea@gmail.com', '987632546', 'mane', 'mani', 981415111, '2002-01-09', 'mi casita', 0, 1, '2024-11-18 01:23:10.160404'),
(421, 'pbkdf2_sha256$260000$jMoQAd5otmb4eFhTlCYQkt$VNBhyRljGnYwfK1AzmQrfhHqXIk51wn80nI5boodh1w=', '2024-11-18 01:27:03.827706', 0, 'julio@gmail.com', '122231212', 'julio', 'tantas', 981415111, '2002-01-09', 'lota 45', 0, 1, '2024-11-18 01:27:03.823749'),
(422, 'pbkdf2_sha256$260000$DZfN3lv4VuzqpHfjmgpYxz$tPcq2hVrCELZbCrzVOkSdnNXs40ARz08CRIgH2b0ePI=', '2024-11-18 01:34:09.769916', 0, 'agurtojose150@gmail.com', '873873823', 'Jose Agurto', 'mamam', 981415111, '2002-01-09', 'lota 45', 0, 1, '2024-11-18 01:34:09.765343'),
(423, 'pbkdf2_sha256$260000$juXHGdnjznTmLivLddRiNw$GMDPX3f+38hCSEzuy2CuFPbeCfhnK3ifVxMWVaFTvm4=', '2024-11-18 14:52:20.494864', 0, 'joseto@gmail.com', '12.967.904-2', 'Jose Agurto', 'manaas', 981415111, '2024-11-07', 'lota 45', 0, 1, '2024-11-18 12:24:25.929058'),
(426, 'pbkdf2_sha256$260000$Ko2KL9qgLfkPctr9N5y1JG$c6komhVTVLc85ON4OiQAKCan10ob0wA3EXTMq59HGwY=', NULL, 0, 'ag@gmail.com', '21117906-6', 'lalalaa', 'aaaaaa', 123456789, NULL, 'xvdxc', 0, 0, '0000-00-00 00:00:00.000000');

--
-- Disparadores `app_customuser`
--
DELIMITER $$
CREATE TRIGGER `trigger_update_cliente_customuser` AFTER UPDATE ON `app_customuser` FOR EACH ROW BEGIN
    -- Actualizar cliente en dimCliente si hay cambios en app_customuser
    UPDATE etl.dimCliente
    SET 
        email = NEW.email,
        rut = NEW.rut,
        first_name = NEW.first_name,
        last_name = NEW.last_name,
        telefono = NEW.telefono
    WHERE id_cliente = NEW.id;
END
$$
DELIMITER ;

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

--
-- Disparadores `app_generolib`
--
DELIMITER $$
CREATE TRIGGER `trg_update_genero_on_update` AFTER UPDATE ON `app_generolib` FOR EACH ROW BEGIN
    -- Actualizar el nombre del género en dimCompras
    UPDATE etl.dimCompras
    SET
        nombre_genero = NEW.nombre
    WHERE
        nombre_genero = OLD.nombre;

    -- Actualizar el nombre del género en dimArriendos
    UPDATE etl.dimArriendos
    SET
        nombre_genero = NEW.nombre
    WHERE
        nombre_genero = OLD.nombre;
END
$$
DELIMITER ;

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

--
-- Volcado de datos para la tabla `app_itemcarrito`
--

INSERT INTO `app_itemcarrito` (`id`, `cantidad`, `carrito_id`, `producto_id`) VALUES
(519, 1, 10, 24),
(522, 1, 1, 24),
(523, 1, 1, 25);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_libro`
--

CREATE TABLE `app_libro` (
  `id` bigint(20) NOT NULL,
  `nom_libro` varchar(255) NOT NULL,
  `precio` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `imagen` varchar(500) DEFAULT NULL,
  `id_autor_id` bigint(20) DEFAULT NULL,
  `id_genero_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_libro`
--

INSERT INTO `app_libro` (`id`, `nom_libro`, `precio`, `stock`, `imagen`, `id_autor_id`, `id_genero_id`) VALUES
(23, 'Allende', 13000, 13, 'https://drive.google.com/file/d/1PXuptMFtBoohtdF0ihFbUl-sMVBJW6Bt/view?usp=drivesdk', 7, 6),
(24, 'Diccionario', 8000, 5, 'https://drive.google.com/file/d/1sed2VtoNe850qDtkJDjQQD7oIu8_MMGx/view?usp=drivesdk', 5, 5),
(25, 'Los Juegos Del Hambre', 27000, 6, 'https://drive.google.com/file/d/1Dl3Sti5DznW0r1gZ-olD7wrl7NzlVghF/view?usp=drivesdk', 2, 3),
(28, 'Harry Potter y la piedra filosofal', 29000, 17, 'https://drive.google.com/file/d/1BvFWN9WqO7IVGJlOOpo8rISKhYXySekV/view?usp=drivesdk', 4, 2),
(29, 'Juego de Tronos', 12000, 6, 'https://drive.google.com/file/d/1NF5qTYeQguZYPgMmVGW5zwxMHfFQZxxi/view?usp=drivesdk', 3, 2),
(30, 'Anatomía Del Mal', 25000, 35, 'https://drive.google.com/file/d/1oalxLK73xbkFdP3Bhmg5E72bSjKkddLe/view?usp=drivesdk', 9, 4),
(31, 'La Teoría de la Relatividad', 45000, 13, 'https://drive.google.com/file/d/1YJmcNyChr-pouc1g1fJoPeYQO71Ha05S/view?usp=drivesdk', 10, 5),
(33, 'El día que se perdió la cordura', 27000, 30, 'https://drive.google.com/file/d/1YN4V7yOtLN8pWwNkliisOdlgxZIQPrlF/view?usp=drivesdk', 13, 2),
(34, 'La Magia de Pensar en Grande', 11000, 28, 'https://drive.google.com/file/d/1PVIVCe2p-LmdxyzBT_AIgWTwOtN22LlP/view?usp=drivesdk', 14, 4),
(35, 'Las doce puertas', 17000, 40, 'https://drive.google.com/file/d/11pXperWBzYFbwn1dlXMz9gVodAD6o2PJ/view?usp=drivesdk', 15, 2),
(36, 'Valentia 1', 9900, 30, 'https://drive.google.com/file/d/11ICV40XPgbdVeRRmkRbuQR72QqEMCju9/view?usp=drivesdk', 16, 2);

--
-- Disparadores `app_libro`
--
DELIMITER $$
CREATE TRIGGER `trg_update_dimLibros` AFTER UPDATE ON `app_libro` FOR EACH ROW BEGIN
    -- Actualizar los datos del libro en dimCompras
    UPDATE etl.dimCompras
    SET
        nom_libro = NEW.nom_libro,
        precio = NEW.precio,
        stock_total_compras = NEW.stock,
        nombre_autor = (SELECT a.nombre_autor FROM dbacapstone.app_autor a WHERE a.id = NEW.id_autor_id),
        nombre_genero = (SELECT g.nombre FROM dbacapstone.app_generolib g WHERE g.id = NEW.id_genero_id)
    WHERE
        nom_libro = OLD.nom_libro;
END
$$
DELIMITER ;

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
(2, 'Los Juegos Del Hambre', 6, 'https://drive.google.com/file/d/1Pbbr2UWXbIR2HxmDRg10DfYneQ3lsKwy/view?usp=drivesdk', 2, 2),
(3, 'Juego de Tronos', 4, 'https://drive.google.com/file/d/1IGgIGCGoBrHTLb1O6up9UwuhvzGyKkIL/view?usp=drivesdk', 3, 3),
(11, 'Un libroasdasd', 1, 'https://drive.google.com/file/d/1ktPLBfpFClYAtzVBEiE_zsb5DxnapymN/view?usp=drivesdk', 3, 6);

--
-- Disparadores `app_libroarr`
--
DELIMITER $$
CREATE TRIGGER `trg_update_dimArriendos_on_libroarr_update` AFTER UPDATE ON `app_libroarr` FOR EACH ROW BEGIN
    -- Actualizar los datos en dimArriendos
    UPDATE etl.dimArriendos
    SET
        nom_libro = NEW.nom_libro,
        nombre_autor = (SELECT a.nombre_autor FROM dbacapstone.app_autor a WHERE a.id = NEW.id_autor_id),
        nombre_genero = (SELECT g.nombre FROM dbacapstone.app_generolib g WHERE g.id = NEW.id_genero_id),
        stock_total_arriendo = NEW.stock
    WHERE
        nom_libro = OLD.nom_libro;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_update_dimCompras_on_update` AFTER UPDATE ON `app_libroarr` FOR EACH ROW BEGIN
    -- Actualizar los datos en dimCompras
    UPDATE etl.dimCompras
    SET
        nom_libro = NEW.nom_libro,
        stock_total_compras = NEW.stock,
        nombre_autor = (SELECT a.nombre_autor FROM dbacapstone.app_autor a WHERE a.id = NEW.id_autor_id),
        nombre_genero = (SELECT g.nombre FROM dbacapstone.app_generolib g WHERE g.id = NEW.id_genero_id)
    WHERE
        nom_libro = OLD.nom_libro;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_sub`
--

CREATE TABLE `app_sub` (
  `id` bigint(20) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `id_ts_id` bigint(20) DEFAULT NULL,
  `id_us_id` bigint(20) DEFAULT NULL,
  `invalida` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_sub`
--

INSERT INTO `app_sub` (`id`, `fecha_inicio`, `id_ts_id`, `id_us_id`, `invalida`) VALUES
(1, '2024-10-12', 3, 1, NULL),
(2, '2024-11-17', 3, 1, 0),
(3, '2024-11-17', 3, 414, 0),
(5, '2024-11-18', 1, 423, 0);

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
(48, 'sessions', '0001_initial', '2024-10-12 00:59:28.109077'),
(49, 'admin_interface', '0030_theme_collapsible_stacked_inlines_and_more', '2024-11-07 01:54:22.795892');

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
('0996oydymcrs4v3l60mimh2vitpcxyai', '.eJxVjEEOwiAQRe_C2pChhQFcuvcMZKYDUjVtUtqV8e7apAvd_vfef6lE21rT1vKSRlFnZbtenX5XpuGRpx3JnabbrId5WpeR9a7ogzZ9nSU_L4f7d1Cp1W9dPA3QixQ0EFmsEYcBfEHKACCWHaMP1rAFRILAHFyMhQBi6QCten8AMTE3zQ:1tD36y:VMZuV1S4bEWRdGKlKdvmbUWWYGWkUqG4hNKLZ4LnZZY', '2024-12-02 14:52:20.497858'),
('1m95fayih4acoscu0cy04s3ek70fo1ka', '.eJxVjMEOwiAQRP-FsyEgy4oevfcbGpbdStVAUtqT8d-VpAfN3Oa9mZca47bmcWuyjDOri7Lq8NtRTA8pHfA9llvVqZZ1mUl3Re-06aGyPK-7-3eQY8t97Y78jUN0BGTO4k9MwUJKPFmfxFtAw2AcAKENE7AwIkAMjAJJ1PsD3hI3-g:1t0Rr7:wqaTMWrW7U61kZHr_x4LSWsqwyAmxPmO1pLb_yiqKRw', '2024-10-28 20:39:53.018594'),
('dzroq500jkfp4v7h48udp4weeo40h0rw', '.eJxVjDEOAiEQRe9CbUhAZhBLe89AhmGQVQPJslsZ766bbKHtf-_9l4q0LjWuQ-Y4ZXVWRh1-t0T8kLaBfKd265p7W-Yp6U3ROx362rM8L7v7d1Bp1G8NFtEhl8IUBLw3XCyhBYfJAZ18dsdCYB0KSWCyUFI2LD7YUEIwrN4f6VI4Sw:1szQVH:uUqHQ2gky9Hc_FzWC2fFnVKENhN8kXUmwAGrJuU8p8A', '2024-10-26 01:01:07.244590'),
('essvjx47zmqm2gw0jew42xpznb2uo4wi', '.eJxVjEEOwiAQRe_C2pChHaG4dN8zkIEZpGpoUtqV8e7apAvd_vfef6lA21rC1mQJE6uLQoPq9LtGSg-pO-I71dus01zXZYp6V_RBmx5nluf1cP8OCrXyrVPqYsKzF0R0riNkn_MAToTRWp_jkAkwOgOC0oPxlggEXC82evCs3h88mjhz:1tCUf0:KsTHDtLQFrBklqoHZ4Rdehzo5qu9AQI0CKC3s9KAtk8', '2024-12-01 02:05:10.633137'),
('l0e5fp3vz8lf3ifem8d5jno4udfsgqyn', '.eJxVjEEOwiAQRe_C2pChhQFcuvcMZKYDUjVtUtqV8e7apAvd_vfef6lE21rT1vKSRlFnZbtenX5XpuGRpx3JnabbrId5WpeR9a7ogzZ9nSU_L4f7d1Cp1W9dPA3QixQ0EFmsEYcBfEHKACCWHaMP1rAFRILAHFyMhQBi6QCten8AMTE3zQ:1tD2XF:KuAqxAXAbfxoqWGRBIAL7elaZab07LbgkRYiwMugSbg', '2024-12-02 14:15:25.314191'),
('ofy20jtxnjysw5sq3rx44087lyxexly5', '.eJxVjEEOwiAURO_C2pCA_R906d4zkIFPpWogKe3KeHdt0oVu5703LxWwLiWsPc9hEnVWRh1-t4j0yHUDcke9NZ1aXeYp6k3RO-362iQ_L7v7d1DQy7dm8ICTeDsQKPl0dOyNQY6JJLJxIDcCiTlTZDJEGQI_2ggziLOi3h_uMDiL:1tCyiw:FH97Kwg_uswr0yHALy73yKoY2jeCoZvomnLe2gkp7rs', '2024-12-02 10:11:14.825702'),
('v3btbb8yc7jk9fz7abf1ck76zre41a6c', '.eJxVjEEOwiAURO_C2pCA_R906d4zkIFPpWogKe3KeHdt0oVu5703LxWwLiWsPc9hEnVWRh1-t4j0yHUDcke9NZ1aXeYp6k3RO-362iQ_L7v7d1DQy7dm8ICTeDsQKPl0dOyNQY6JJLJxIDcCiTlTZDJEGQI_2ggziLOi3h_uMDiL:1tCn7J:y_0vk08jeNISIhwjH96E-rc3YkveOfPijTIcUYDVSJg', '2024-12-01 21:47:37.232858'),
('wdu1j9geet5o9peste21rgn5c0mndibl', '.eJxVjMEOwiAQRP-FsyEgy4oevfcbGpbdStVAUtqT8d-VpAfN3Oa9mZca47bmcWuyjDOri7Lq8NtRTA8pHfA9llvVqZZ1mUl3Re-06aGyPK-7-3eQY8t97Y78jUN0BGTO4k9MwUJKPFmfxFtAw2AcAKENE7AwIkAMjAJJ1PsD3hI3-g:1tBPSC:7XPjfWCLDYzmDoe0ELY4PUHBLdb6PKIrTRTIZ4fovwg', '2024-11-28 02:19:28.740953');

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
  ADD KEY `app_arriendo_cliente_id_45434d16_fk_app_customuser_id` (`cliente_id`),
  ADD KEY `app_arriendo_producto_id_24adbff7_fk_app_libroarr_id` (`producto_id`);

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=123459;

--
-- AUTO_INCREMENT de la tabla `app_autor`
--
ALTER TABLE `app_autor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT de la tabla `app_carrito`
--
ALTER TABLE `app_carrito`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `app_compra`
--
ALTER TABLE `app_compra`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12681;

--
-- AUTO_INCREMENT de la tabla `app_customuser`
--
ALTER TABLE `app_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=427;

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
-- AUTO_INCREMENT de la tabla `app_itemcarrito`
--
ALTER TABLE `app_itemcarrito`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=536;

--
-- AUTO_INCREMENT de la tabla `app_libro`
--
ALTER TABLE `app_libro`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `app_libroarr`
--
ALTER TABLE `app_libroarr`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `app_sub`
--
ALTER TABLE `app_sub`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `app_arriendo`
--
ALTER TABLE `app_arriendo`
  ADD CONSTRAINT `app_arriendo_cliente_id_45434d16_fk_app_customuser_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_customuser` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `app_arriendo_producto_id_24adbff7_fk_app_libroarr_id` FOREIGN KEY (`producto_id`) REFERENCES `app_libroarr` (`id`);

--
-- Filtros para la tabla `app_carrito`
--
ALTER TABLE `app_carrito`
  ADD CONSTRAINT `app_carrito_cliente_id_4321eb42_fk_app_customuser_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_customuser` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `app_compra`
--
ALTER TABLE `app_compra`
  ADD CONSTRAINT `app_compra_cliente_id_66e2a9f0_fk_app_customuser_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_customuser` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `app_compra_producto_id_fada055c_fk_app_libro_id` FOREIGN KEY (`producto_id`) REFERENCES `app_libro` (`id`) ON DELETE CASCADE;

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
-- Filtros para la tabla `app_itemcarrito`
--
ALTER TABLE `app_itemcarrito`
  ADD CONSTRAINT `app_itemcarrito_carrito_id_02f22e19_fk_app_carrito_id` FOREIGN KEY (`carrito_id`) REFERENCES `app_carrito` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `app_itemcarrito_producto_id_4e2f7064_fk_app_libro_id` FOREIGN KEY (`producto_id`) REFERENCES `app_libro` (`id`) ON DELETE CASCADE;

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
  ADD CONSTRAINT `app_sub_id_us_id_50e92fd2_fk_app_customuser_id` FOREIGN KEY (`id_us_id`) REFERENCES `app_customuser` (`id`) ON DELETE CASCADE;

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
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `app_customuser` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
