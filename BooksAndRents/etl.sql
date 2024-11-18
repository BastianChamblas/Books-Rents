-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-11-2024 a las 17:37:03
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
-- Base de datos: `etl`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dimarriendos`
--

CREATE TABLE `dimarriendos` (
  `id_arriendo` int(11) NOT NULL,
  `nom_libro` varchar(255) DEFAULT NULL,
  `nombre_autor` varchar(255) DEFAULT NULL,
  `nombre_genero` varchar(255) DEFAULT NULL,
  `stock_total_arriendo` int(11) DEFAULT NULL,
  `id_tiempo_arriendo` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dimarriendos`
--

INSERT INTO `dimarriendos` (`id_arriendo`, `nom_libro`, `nombre_autor`, `nombre_genero`, `stock_total_arriendo`, `id_tiempo_arriendo`) VALUES
(19, 'Un libroasdasd', 'George R. R. Martinasdas', 'biografía', 1, 17),
(20, 'Un libroasdasd', 'George R. R. Martinasdas', 'biografía', 1, 18),
(21, 'Un libroasdasd', 'George R. R. Martinasdas', 'biografía', 1, 19),
(22, 'Un libroasdasd', 'George R. R. Martinasdas', 'biografía', 1, 19),
(23, 'Los Juegos Del Hambre', 'Suzanne Collins', 'Ciencia ficción', 6, 19),
(24, 'Un libroasdasd', 'George R. R. Martinasdas', 'biografía', 1, 19),
(25, 'Los Juegos Del Hambre', 'Suzanne Collins', 'Ciencia ficción', 6, 19),
(26, 'Los Juegos Del Hambre', 'Suzanne Collins', 'Ciencia ficción', 6, 19),
(27, 'Los Juegos Del Hambre', 'Suzanne Collins', 'Ciencia ficción', 6, 19);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dimcliente`
--

CREATE TABLE `dimcliente` (
  `id_cliente` int(11) NOT NULL,
  `email` varchar(1000) DEFAULT NULL,
  `rut` varchar(20) DEFAULT NULL,
  `first_name` varchar(1000) DEFAULT NULL,
  `last_name` varchar(1000) DEFAULT NULL,
  `telefono` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dimcliente`
--

INSERT INTO `dimcliente` (`id_cliente`, `email`, `rut`, `first_name`, `last_name`, `telefono`) VALUES
(417, 'Bastian@gmail.com', '120987654-2', 'Bastian', 'chamblas', '981415111'),
(418, 'Nicolas@gmail.com', '987632546', 'Nicolas', 'Nico', '981415111'),
(419, 'jose@gmail.com', '21.117.906-6', 'jose', 'agurto', '981415111'),
(420, 'manea@gmail.com', '987632546', 'mane', 'mani', '981415111'),
(421, 'julio@gmail.com', '122231212', 'julio', 'tantas', '981415111'),
(422, 'agurtojose150@gmail.com', '873873823', 'Jose Agurto', 'mamam', '981415111'),
(423, 'joseto@gmail.com', '12.967.904-2', 'Jose Agurto', 'manaas', '981415111'),
(424, 'pepe@tapia.cl', '11.877.923-1', 'pepe', 'tapia', '48137575'),
(425, 'paraborrar@gmail.com', '987632546-0', 'borra', 'borra', '981415111'),
(426, 'a@a.cl', '200839749', 'aasdasd', 'aasdasd', '934366162'),
(427, 'javier@gmail.com', '987632546-0', 'javier', 'Contreras', '981415111');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dimcompras`
--

CREATE TABLE `dimcompras` (
  `id_compra` int(11) NOT NULL,
  `nom_libro` varchar(255) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `stock_total_compras` int(11) DEFAULT NULL,
  `cantidad_comprado` int(11) DEFAULT NULL,
  `nombre_autor` varchar(255) DEFAULT NULL,
  `nombre_genero` varchar(255) DEFAULT NULL,
  `id_tiempo_compra` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dimcompras`
--

INSERT INTO `dimcompras` (`id_compra`, `nom_libro`, `precio`, `stock_total_compras`, `cantidad_comprado`, `nombre_autor`, `nombre_genero`, `id_tiempo_compra`) VALUES
(19, '12312323', 123.00, 69, 1, 'Mario Amorós', 'Ciencia ficción', 30),
(20, '12312323', 123.00, 69, 3, 'Mario Amorós', 'Ciencia ficción', 30),
(21, '12312323', 123.00, 69, 38, 'Mario Amorós', 'Ciencia ficción', 31),
(22, 'asd', 123.00, 211, 1, 'George R. R. Martinasdas', 'Acción', 31),
(23, 'asd', 123.00, 211, 1, 'George R. R. Martinasdas', 'Acción', 31),
(24, '12312323', 123.00, 69, 1, 'Mario Amorós', 'Ciencia ficción', 31),
(25, 'asd', 123.00, 211, 1, 'George R. R. Martinasdas', 'Acción', 31),
(26, '12312323', 123.00, 69, 1, 'Mario Amorós', 'Ciencia ficción', 31),
(27, 'asd', 123.00, 211, 1, 'George R. R. Martinasdas', 'Acción', 31),
(28, '12312323', 123.00, 69, 1, 'Mario Amorós', 'Ciencia ficción', 31),
(29, 'asd', 123.00, 211, 1, 'George R. R. Martinasdas', 'Acción', 31),
(30, 'asd', 123.00, 211, 20, 'George R. R. Martinasdas', 'Acción', 31),
(31, 'asd', 123.00, 211, 1, 'George R. R. Martinasdas', 'Acción', 31),
(32, '12312323', 123.00, 69, 1, 'Mario Amorós', 'Ciencia ficción', 31),
(33, 'asd', 123.00, 211, 1, 'George R. R. Martinasdas', 'Acción', 31),
(34, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 31),
(35, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 31),
(36, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 31),
(37, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 31),
(38, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 31),
(39, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 31),
(40, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 31),
(41, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 32),
(42, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 32),
(43, 'Allende', 13000.00, 13, 3, 'Mario Amorós', 'biografía', 32),
(44, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 32),
(45, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 32),
(46, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 32),
(47, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 32),
(48, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 32),
(49, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 32),
(50, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 32),
(51, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 32),
(52, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 32),
(53, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 32),
(54, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 32),
(55, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 32),
(56, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 32),
(57, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 32),
(58, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 32),
(59, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 32),
(60, 'Diccionario', 8000.00, 5, 3, 'LaRousse', 'Libros de referencia', 32),
(61, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 32),
(62, 'Juego de Tronos', 12000.00, 6, 3, 'George R. R. Martinasdas', 'Ciencia ficción', 32),
(63, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 32),
(64, 'Allende', 13000.00, 13, 4, 'Mario Amorós', 'biografía', 32),
(65, 'Harry Potter y la piedra filosofal', 29000.00, 17, 4, 'J. K. Rowling', 'Ciencia ficción', 32),
(66, 'Anatomía Del Mal', 25000.00, 35, 5, 'Jordi Wild', 'Fantasía', 32),
(67, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 32),
(68, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 32),
(69, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 32),
(70, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 32),
(71, 'Allende', 13000.00, 13, 4, 'Mario Amorós', 'biografía', 32),
(72, 'Los Juegos Del Hambre', 27000.00, 6, 3, 'Suzanne Collins', 'Acción', 32),
(73, 'Harry Potter y la piedra filosofal', 29000.00, 17, 3, 'J. K. Rowling', 'Ciencia ficción', 32),
(74, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 32),
(75, 'Anatomía Del Mal', 25000.00, 35, 3, 'Jordi Wild', 'Fantasía', 32),
(76, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 32),
(77, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 33),
(78, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 34),
(79, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 35),
(80, 'Anatomía Del Mal', 25000.00, 35, 3, 'Jordi Wild', 'Fantasía', 36),
(81, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 37),
(82, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 38),
(83, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 39),
(84, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 40),
(85, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 32),
(86, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 41),
(87, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 42),
(88, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 43),
(89, 'Anatomía Del Mal', 25000.00, 35, 3, 'Jordi Wild', 'Fantasía', 44),
(90, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 45),
(91, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 46),
(92, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 47),
(93, 'Allende', 13000.00, 13, 3, 'Mario Amorós', 'biografía', 48),
(94, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 49),
(95, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 50),
(96, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 51),
(97, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 52),
(98, 'Harry Potter y la piedra filosofal', 29000.00, 17, 3, 'J. K. Rowling', 'Ciencia ficción', 53),
(99, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 54),
(100, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 55),
(101, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 56),
(102, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 57),
(103, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 58),
(104, 'Allende', 13000.00, 13, 3, 'Mario Amorós', 'biografía', 59),
(105, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 60),
(106, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 61),
(107, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 62),
(108, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 63),
(109, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 64),
(110, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 65),
(111, 'Los Juegos Del Hambre', 27000.00, 6, 2, 'Suzanne Collins', 'Acción', 66),
(112, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 67),
(113, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 68),
(114, 'Anatomía Del Mal', 25000.00, 35, 3, 'Jordi Wild', 'Fantasía', 69),
(115, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 70),
(116, 'Los Juegos Del Hambre', 27000.00, 6, 2, 'Suzanne Collins', 'Acción', 71),
(117, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 72),
(118, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 73),
(119, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 74),
(120, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 75),
(121, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 76),
(122, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 77),
(123, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 78),
(124, 'Los Juegos Del Hambre', 27000.00, 6, 3, 'Suzanne Collins', 'Acción', 79),
(125, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 80),
(126, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 81),
(127, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 82),
(128, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 83),
(129, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 84),
(130, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 85),
(131, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 86),
(132, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 87),
(133, 'Los Juegos Del Hambre', 27000.00, 6, 2, 'Suzanne Collins', 'Acción', 88),
(134, 'Anatomía Del Mal', 25000.00, 35, 3, 'Jordi Wild', 'Fantasía', 89),
(135, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 90),
(136, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 91),
(137, 'Juego de Tronos', 12000.00, 6, 3, 'George R. R. Martinasdas', 'Ciencia ficción', 92),
(138, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 93),
(139, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 94),
(140, 'Harry Potter y la piedra filosofal', 29000.00, 17, 3, 'J. K. Rowling', 'Ciencia ficción', 95),
(141, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 96),
(142, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 97),
(143, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 98),
(144, 'Anatomía Del Mal', 25000.00, 35, 3, 'Jordi Wild', 'Fantasía', 99),
(145, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 100),
(146, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 101),
(147, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 102),
(148, 'Harry Potter y la piedra filosofal', 29000.00, 17, 3, 'J. K. Rowling', 'Ciencia ficción', 103),
(149, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 104),
(150, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 105),
(151, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 106),
(152, 'Diccionario', 8000.00, 5, 3, 'LaRousse', 'Libros de referencia', 107),
(153, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 108),
(154, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 109),
(155, 'Allende', 13000.00, 13, 3, 'Mario Amorós', 'biografía', 110),
(156, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 111),
(157, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 112),
(158, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 113),
(159, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 114),
(160, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 115),
(161, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 116),
(162, 'Juego de Tronos', 12000.00, 6, 2, 'George R. R. Martinasdas', 'Ciencia ficción', 117),
(163, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 118),
(164, 'Allende', 13000.00, 13, 3, 'Mario Amorós', 'biografía', 119),
(165, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 120),
(166, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 121),
(167, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 106),
(168, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 122),
(169, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 109),
(170, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 123),
(171, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 124),
(172, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 115),
(173, 'Harry Potter y la piedra filosofal', 29000.00, 17, 3, 'J. K. Rowling', 'Ciencia ficción', 117),
(174, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 125),
(175, 'Diccionario', 8000.00, 5, 1, 'LaRousse', 'Libros de referencia', 105),
(176, 'Anatomía Del Mal', 25000.00, 35, 2, 'Jordi Wild', 'Fantasía', 126),
(177, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 127),
(178, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 128),
(179, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 129),
(180, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 130),
(181, 'Harry Potter y la piedra filosofal', 29000.00, 17, 3, 'J. K. Rowling', 'Ciencia ficción', 131),
(182, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 132),
(183, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 32),
(184, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 32),
(185, 'Allende', 13000.00, 13, 1, 'Mario Amorós', 'biografía', 32),
(186, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 32),
(187, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 32),
(188, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 32),
(189, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 32),
(190, 'La Magia de Pensar en Grande', 11000.00, 28, 1, 'David J.Schwartz', 'Fantasía', 32),
(191, 'El día que se perdió la cordura', 27000.00, 30, 1, 'Javier Castillo', 'Ciencia ficción', 32),
(192, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 32),
(193, 'Las doce puertas', 17000.00, 40, 1, 'Vicente Raga', 'Ciencia ficción', 32),
(194, 'Valentia 1', 9900.00, 30, 1, 'Kelvin Torres', 'Ciencia ficción', 32),
(195, 'Diccionario', 8000.00, 5, 4, 'LaRousse', 'Libros de referencia', 133),
(196, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 133),
(197, 'Los Juegos Del Hambre', 27000.00, 6, 2, 'Suzanne Collins', 'Acción', 133),
(198, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 134),
(199, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 135),
(200, 'Anatomía Del Mal', 25000.00, 35, 3, 'Jordi Wild', 'Fantasía', 35),
(201, 'La Magia de Pensar en Grande', 11000.00, 28, 1, 'David J.Schwartz', 'Fantasía', 136),
(202, 'El día que se perdió la cordura', 27000.00, 30, 2, 'Javier Castillo', 'Ciencia ficción', 37),
(203, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 40),
(204, 'Las doce puertas', 17000.00, 40, 1, 'Vicente Raga', 'Ciencia ficción', 40),
(205, 'Valentia 1', 9900.00, 30, 2, 'Kelvin Torres', 'Ciencia ficción', 137),
(206, 'Diccionario', 8000.00, 5, 3, 'LaRousse', 'Libros de referencia', 138),
(207, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 42),
(208, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 43),
(209, 'Harry Potter y la piedra filosofal', 29000.00, 17, 3, 'J. K. Rowling', 'Ciencia ficción', 44),
(210, 'Juego de Tronos', 12000.00, 6, 1, 'George R. R. Martinasdas', 'Ciencia ficción', 45),
(211, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 139),
(212, 'La Magia de Pensar en Grande', 11000.00, 28, 2, 'David J.Schwartz', 'Fantasía', 140),
(213, 'El día que se perdió la cordura', 27000.00, 30, 2, 'Javier Castillo', 'Ciencia ficción', 141),
(214, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 142),
(215, 'Las doce puertas', 17000.00, 40, 5, 'Vicente Raga', 'Ciencia ficción', 143),
(216, 'Valentia 1', 9900.00, 30, 3, 'Kelvin Torres', 'Ciencia ficción', 144),
(217, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 48),
(218, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 145),
(219, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 146),
(220, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 147),
(221, 'Juego de Tronos', 12000.00, 6, 3, 'George R. R. Martinasdas', 'Ciencia ficción', 148),
(222, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 149),
(223, 'La Magia de Pensar en Grande', 11000.00, 28, 2, 'David J.Schwartz', 'Fantasía', 150),
(224, 'El día que se perdió la cordura', 27000.00, 30, 4, 'Javier Castillo', 'Ciencia ficción', 151),
(225, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 53),
(226, 'Las doce puertas', 17000.00, 40, 2, 'Vicente Raga', 'Ciencia ficción', 152),
(227, 'Valentia 1', 9900.00, 30, 1, 'Kelvin Torres', 'Ciencia ficción', 153),
(228, 'Diccionario', 8000.00, 5, 3, 'LaRousse', 'Libros de referencia', 57),
(229, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 58),
(230, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 154),
(231, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 155),
(232, 'Juego de Tronos', 12000.00, 6, 4, 'George R. R. Martinasdas', 'Ciencia ficción', 156),
(233, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 62),
(234, 'La Magia de Pensar en Grande', 11000.00, 28, 2, 'David J.Schwartz', 'Fantasía', 157),
(235, 'El día que se perdió la cordura', 27000.00, 30, 3, 'Javier Castillo', 'Ciencia ficción', 158),
(236, 'La Teoría de la Relatividad', 45000.00, 13, 1, 'Freida McFADDEN', 'Libros de referencia', 66),
(237, 'Las doce puertas', 17000.00, 40, 3, 'Vicente Raga', 'Ciencia ficción', 159),
(238, 'Valentia 1', 9900.00, 30, 1, 'Kelvin Torres', 'Ciencia ficción', 160),
(239, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 69),
(240, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 161),
(241, 'Los Juegos Del Hambre', 27000.00, 6, 3, 'Suzanne Collins', 'Acción', 162),
(242, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 163),
(243, 'Juego de Tronos', 12000.00, 6, 2, 'George R. R. Martinasdas', 'Ciencia ficción', 72),
(244, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 164),
(245, 'La Magia de Pensar en Grande', 11000.00, 28, 2, 'David J.Schwartz', 'Fantasía', 165),
(246, 'El día que se perdió la cordura', 27000.00, 30, 2, 'Javier Castillo', 'Ciencia ficción', 75),
(247, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 166),
(248, 'Las doce puertas', 17000.00, 40, 3, 'Vicente Raga', 'Ciencia ficción', 167),
(249, 'Valentia 1', 9900.00, 30, 1, 'Kelvin Torres', 'Ciencia ficción', 168),
(250, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 80),
(251, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 169),
(252, 'Los Juegos Del Hambre', 27000.00, 6, 2, 'Suzanne Collins', 'Acción', 170),
(253, 'Harry Potter y la piedra filosofal', 29000.00, 17, 1, 'J. K. Rowling', 'Ciencia ficción', 171),
(254, 'Juego de Tronos', 12000.00, 6, 3, 'George R. R. Martinasdas', 'Ciencia ficción', 84),
(255, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 172),
(256, 'La Magia de Pensar en Grande', 11000.00, 28, 1, 'David J.Schwartz', 'Fantasía', 173),
(257, 'El día que se perdió la cordura', 27000.00, 30, 2, 'Javier Castillo', 'Ciencia ficción', 88),
(258, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 174),
(259, 'Las doce puertas', 17000.00, 40, 2, 'Vicente Raga', 'Ciencia ficción', 175),
(260, 'Valentia 1', 9900.00, 30, 3, 'Kelvin Torres', 'Ciencia ficción', 91),
(261, 'Diccionario', 8000.00, 5, 2, 'LaRousse', 'Libros de referencia', 176),
(262, 'Allende', 13000.00, 13, 3, 'Mario Amorós', 'biografía', 177),
(263, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 178),
(264, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 96),
(265, 'Juego de Tronos', 12000.00, 6, 3, 'George R. R. Martinasdas', 'Ciencia ficción', 179),
(266, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 180),
(267, 'La Magia de Pensar en Grande', 11000.00, 28, 2, 'David J.Schwartz', 'Fantasía', 99),
(268, 'El día que se perdió la cordura', 27000.00, 30, 2, 'Javier Castillo', 'Ciencia ficción', 181),
(269, 'La Teoría de la Relatividad', 45000.00, 13, 3, 'Freida McFADDEN', 'Libros de referencia', 182),
(270, 'Las doce puertas', 17000.00, 40, 4, 'Vicente Raga', 'Ciencia ficción', 183),
(271, 'Valentia 1', 9900.00, 30, 2, 'Kelvin Torres', 'Ciencia ficción', 104),
(272, 'Diccionario', 8000.00, 5, 3, 'LaRousse', 'Libros de referencia', 184),
(273, 'Allende', 13000.00, 13, 2, 'Mario Amorós', 'biografía', 185),
(274, 'Los Juegos Del Hambre', 27000.00, 6, 1, 'Suzanne Collins', 'Acción', 126),
(275, 'Harry Potter y la piedra filosofal', 29000.00, 17, 2, 'J. K. Rowling', 'Ciencia ficción', 108),
(276, 'Juego de Tronos', 12000.00, 6, 3, 'George R. R. Martinasdas', 'Ciencia ficción', 127),
(277, 'Anatomía Del Mal', 25000.00, 35, 1, 'Jordi Wild', 'Fantasía', 186),
(278, 'La Magia de Pensar en Grande', 11000.00, 28, 2, 'David J.Schwartz', 'Fantasía', 112),
(279, 'El día que se perdió la cordura', 27000.00, 30, 3, 'Javier Castillo', 'Ciencia ficción', 123),
(280, 'La Teoría de la Relatividad', 45000.00, 13, 2, 'Freida McFADDEN', 'Libros de referencia', 124),
(281, 'Las doce puertas', 17000.00, 40, 3, 'Vicente Raga', 'Ciencia ficción', 115),
(282, 'Valentia 1', 9900.00, 30, 2, 'Kelvin Torres', 'Ciencia ficción', 131),
(283, 'Diccionario', 8000.00, 5, 3, 'LaRousse', 'Libros de referencia', 187),
(284, 'Allende', 13000.00, 13, 3, 'Mario Amorós', 'biografía', 125),
(285, 'Los Juegos Del Hambre', 27000.00, 6, 2, 'Suzanne Collins', 'Acción', 120);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dimestadodevolucion`
--

CREATE TABLE `dimestadodevolucion` (
  `id_estado_devolucion` int(11) NOT NULL,
  `estado` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dimestadodevolucion`
--

INSERT INTO `dimestadodevolucion` (`id_estado_devolucion`, `estado`) VALUES
(3, '0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dimtiempoarriendos`
--

CREATE TABLE `dimtiempoarriendos` (
  `id_tiempo_arriendo` int(11) NOT NULL,
  `fecha_arriendo` date DEFAULT NULL,
  `fecha_devolucion` date DEFAULT NULL,
  `mes` int(11) DEFAULT NULL,
  `anio` int(11) DEFAULT NULL,
  `dia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dimtiempoarriendos`
--

INSERT INTO `dimtiempoarriendos` (`id_tiempo_arriendo`, `fecha_arriendo`, `fecha_devolucion`, `mes`, `anio`, `dia`) VALUES
(17, '2024-11-06', '2024-11-14', 11, 2024, 6),
(18, '2024-11-19', '2024-11-20', 11, 2024, 19),
(19, '2024-11-18', '2024-12-18', 11, 2024, 18);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dimtiempocompras`
--

CREATE TABLE `dimtiempocompras` (
  `id_tiempo_compra` int(11) NOT NULL,
  `fecha_compra` date DEFAULT NULL,
  `dia` int(11) DEFAULT NULL,
  `mes` int(11) DEFAULT NULL,
  `anio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dimtiempocompras`
--

INSERT INTO `dimtiempocompras` (`id_tiempo_compra`, `fecha_compra`, `dia`, `mes`, `anio`) VALUES
(30, '2024-11-01', 1, 11, 2024),
(31, '2024-11-17', 17, 11, 2024),
(32, '2024-11-18', 18, 11, 2024),
(33, '2023-11-02', 2, 11, 2023),
(34, '2023-11-04', 4, 11, 2023),
(35, '2023-11-15', 15, 11, 2023),
(36, '2023-11-18', 18, 11, 2023),
(37, '2023-11-25', 25, 11, 2023),
(38, '2023-11-28', 28, 11, 2023),
(39, '2023-11-29', 29, 11, 2023),
(40, '2023-11-30', 30, 11, 2023),
(41, '2023-12-02', 2, 12, 2023),
(42, '2023-12-05', 5, 12, 2023),
(43, '2023-12-10', 10, 12, 2023),
(44, '2023-12-15', 15, 12, 2023),
(45, '2023-12-18', 18, 12, 2023),
(46, '2024-01-03', 3, 1, 2024),
(47, '2024-01-08', 8, 1, 2024),
(48, '2024-01-12', 12, 1, 2024),
(49, '2024-01-16', 16, 1, 2024),
(50, '2024-01-28', 28, 1, 2024),
(51, '2024-01-31', 31, 1, 2024),
(52, '2024-02-07', 7, 2, 2024),
(53, '2024-02-10', 10, 2, 2024),
(54, '2024-02-14', 14, 2, 2024),
(55, '2024-02-18', 18, 2, 2024),
(56, '2024-02-21', 21, 2, 2024),
(57, '2024-02-25', 25, 2, 2024),
(58, '2024-02-28', 28, 2, 2024),
(59, '2024-03-02', 2, 3, 2024),
(60, '2024-03-06', 6, 3, 2024),
(61, '2024-03-11', 11, 3, 2024),
(62, '2024-03-15', 15, 3, 2024),
(63, '2024-03-19', 19, 3, 2024),
(64, '2024-03-23', 23, 3, 2024),
(65, '2024-03-27', 27, 3, 2024),
(66, '2024-03-30', 30, 3, 2024),
(67, '2024-04-02', 2, 4, 2024),
(68, '2024-04-06', 6, 4, 2024),
(69, '2024-04-10', 10, 4, 2024),
(70, '2024-04-23', 23, 4, 2024),
(71, '2024-04-27', 27, 4, 2024),
(72, '2024-04-30', 30, 4, 2024),
(73, '2024-05-02', 2, 5, 2024),
(74, '2024-05-06', 6, 5, 2024),
(75, '2024-05-10', 10, 5, 2024),
(76, '2024-05-14', 14, 5, 2024),
(77, '2024-05-18', 18, 5, 2024),
(78, '2024-05-22', 22, 5, 2024),
(79, '2024-05-26', 26, 5, 2024),
(80, '2024-05-30', 30, 5, 2024),
(81, '2024-06-03', 3, 6, 2024),
(82, '2024-06-07', 7, 6, 2024),
(83, '2024-06-11', 11, 6, 2024),
(84, '2024-06-15', 15, 6, 2024),
(85, '2024-06-19', 19, 6, 2024),
(86, '2024-06-23', 23, 6, 2024),
(87, '2024-06-27', 27, 6, 2024),
(88, '2024-06-30', 30, 6, 2024),
(89, '2024-07-02', 2, 7, 2024),
(90, '2024-07-06', 6, 7, 2024),
(91, '2024-07-10', 10, 7, 2024),
(92, '2024-07-14', 14, 7, 2024),
(93, '2024-07-18', 18, 7, 2024),
(94, '2024-07-22', 22, 7, 2024),
(95, '2024-07-26', 26, 7, 2024),
(96, '2024-07-30', 30, 7, 2024),
(97, '2024-08-02', 2, 8, 2024),
(98, '2024-08-06', 6, 8, 2024),
(99, '2024-08-10', 10, 8, 2024),
(100, '2024-08-14', 14, 8, 2024),
(101, '2024-08-18', 18, 8, 2024),
(102, '2024-08-22', 22, 8, 2024),
(103, '2024-08-26', 26, 8, 2024),
(104, '2024-08-30', 30, 8, 2024),
(105, '2024-09-03', 3, 9, 2024),
(106, '2024-09-07', 7, 9, 2024),
(107, '2024-09-11', 11, 9, 2024),
(108, '2024-09-15', 15, 9, 2024),
(109, '2024-09-19', 19, 9, 2024),
(110, '2024-09-23', 23, 9, 2024),
(111, '2024-09-27', 27, 9, 2024),
(112, '2024-09-30', 30, 9, 2024),
(113, '2024-10-02', 2, 10, 2024),
(114, '2024-10-06', 6, 10, 2024),
(115, '2024-10-10', 10, 10, 2024),
(116, '2024-10-14', 14, 10, 2024),
(117, '2024-10-18', 18, 10, 2024),
(118, '2024-10-22', 22, 10, 2024),
(119, '2024-10-26', 26, 10, 2024),
(120, '2024-10-30', 30, 10, 2024),
(121, '2024-09-02', 2, 9, 2024),
(122, '2024-09-14', 14, 9, 2024),
(123, '2024-10-01', 1, 10, 2024),
(124, '2024-10-05', 5, 10, 2024),
(125, '2024-10-25', 25, 10, 2024),
(126, '2024-09-10', 10, 9, 2024),
(127, '2024-09-20', 20, 9, 2024),
(128, '2024-09-28', 28, 9, 2024),
(129, '2024-10-03', 3, 10, 2024),
(130, '2024-10-08', 8, 10, 2024),
(131, '2024-10-15', 15, 10, 2024),
(132, '2024-10-27', 27, 10, 2024),
(133, '2023-11-01', 1, 11, 2023),
(134, '2023-11-05', 5, 11, 2023),
(135, '2023-11-10', 10, 11, 2023),
(136, '2023-11-20', 20, 11, 2023),
(137, '2023-12-01', 1, 12, 2023),
(138, '2023-12-03', 3, 12, 2023),
(139, '2023-12-20', 20, 12, 2023),
(140, '2023-12-22', 22, 12, 2023),
(141, '2023-12-25', 25, 12, 2023),
(142, '2023-12-30', 30, 12, 2023),
(143, '2024-01-01', 1, 1, 2024),
(144, '2024-01-05', 5, 1, 2024),
(145, '2024-01-15', 15, 1, 2024),
(146, '2024-01-20', 20, 1, 2024),
(147, '2024-01-22', 22, 1, 2024),
(148, '2024-01-25', 25, 1, 2024),
(149, '2024-01-30', 30, 1, 2024),
(150, '2024-02-01', 1, 2, 2024),
(151, '2024-02-05', 5, 2, 2024),
(152, '2024-02-15', 15, 2, 2024),
(153, '2024-02-20', 20, 2, 2024),
(154, '2024-03-01', 1, 3, 2024),
(155, '2024-03-05', 5, 3, 2024),
(156, '2024-03-10', 10, 3, 2024),
(157, '2024-03-20', 20, 3, 2024),
(158, '2024-03-25', 25, 3, 2024),
(159, '2024-04-01', 1, 4, 2024),
(160, '2024-04-05', 5, 4, 2024),
(161, '2024-04-15', 15, 4, 2024),
(162, '2024-04-20', 20, 4, 2024),
(163, '2024-04-25', 25, 4, 2024),
(164, '2024-05-01', 1, 5, 2024),
(165, '2024-05-05', 5, 5, 2024),
(166, '2024-05-15', 15, 5, 2024),
(167, '2024-05-20', 20, 5, 2024),
(168, '2024-05-25', 25, 5, 2024),
(169, '2024-06-01', 1, 6, 2024),
(170, '2024-06-05', 5, 6, 2024),
(171, '2024-06-10', 10, 6, 2024),
(172, '2024-06-20', 20, 6, 2024),
(173, '2024-06-25', 25, 6, 2024),
(174, '2024-07-01', 1, 7, 2024),
(175, '2024-07-05', 5, 7, 2024),
(176, '2024-07-15', 15, 7, 2024),
(177, '2024-07-20', 20, 7, 2024),
(178, '2024-07-25', 25, 7, 2024),
(179, '2024-08-01', 1, 8, 2024),
(180, '2024-08-05', 5, 8, 2024),
(181, '2024-08-15', 15, 8, 2024),
(182, '2024-08-20', 20, 8, 2024),
(183, '2024-08-25', 25, 8, 2024),
(184, '2024-09-01', 1, 9, 2024),
(185, '2024-09-05', 5, 9, 2024),
(186, '2024-09-25', 25, 9, 2024),
(187, '2024-10-20', 20, 10, 2024);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hechosventaslibros`
--

CREATE TABLE `hechosventaslibros` (
  `id_cliente` int(11) DEFAULT NULL,
  `id_estado_devolucion` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `id_arriendo` int(11) DEFAULT NULL,
  `id_compra` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `hechosventaslibros`
--

INSERT INTO `hechosventaslibros` (`id_cliente`, `id_estado_devolucion`, `id`, `id_arriendo`, `id_compra`) VALUES
(418, 3, 2, 20, NULL),
(417, NULL, 3, NULL, 20),
(419, NULL, 4, NULL, 21),
(419, NULL, 5, NULL, 22),
(419, NULL, 6, NULL, 23),
(419, NULL, 7, NULL, 24),
(419, NULL, 8, NULL, 25),
(419, NULL, 9, NULL, 26),
(419, NULL, 10, NULL, 27),
(419, NULL, 11, NULL, 28),
(419, NULL, 12, NULL, 29),
(419, NULL, 13, NULL, 30),
(419, NULL, 14, NULL, 31),
(419, NULL, 15, NULL, 32),
(419, NULL, 16, NULL, 33),
(419, NULL, 17, NULL, 34),
(419, NULL, 18, NULL, 35),
(419, NULL, 19, NULL, 36),
(419, NULL, 20, NULL, 37),
(419, NULL, 21, NULL, 38),
(419, NULL, 22, NULL, 39),
(419, NULL, 23, NULL, 40),
(420, NULL, 24, NULL, 41),
(420, NULL, 25, NULL, 42),
(420, NULL, 26, NULL, 43),
(417, NULL, 27, NULL, 44),
(417, NULL, 28, NULL, 45),
(417, NULL, 29, NULL, 46),
(417, NULL, 30, NULL, 47),
(417, NULL, 31, NULL, 48),
(418, NULL, 32, NULL, 49),
(418, NULL, 33, NULL, 50),
(418, NULL, 34, NULL, 51),
(418, NULL, 35, NULL, 52),
(419, NULL, 36, NULL, 53),
(419, NULL, 37, NULL, 54),
(419, NULL, 38, NULL, 55),
(419, NULL, 39, NULL, 56),
(419, NULL, 40, NULL, 57),
(419, NULL, 41, NULL, 58),
(420, NULL, 42, NULL, 59),
(420, NULL, 43, NULL, 60),
(420, NULL, 44, NULL, 61),
(420, NULL, 45, NULL, 62),
(420, NULL, 46, NULL, 63),
(420, NULL, 47, NULL, 64),
(421, NULL, 48, NULL, 65),
(421, NULL, 49, NULL, 66),
(421, NULL, 50, NULL, 67),
(421, NULL, 51, NULL, 68),
(421, NULL, 52, NULL, 69),
(421, NULL, 53, NULL, 70),
(422, NULL, 54, NULL, 71),
(422, NULL, 55, NULL, 72),
(422, NULL, 56, NULL, 73),
(422, NULL, 57, NULL, 74),
(422, NULL, 58, NULL, 75),
(422, NULL, 59, NULL, 76),
(423, NULL, 60, NULL, 77),
(417, NULL, 61, NULL, 78),
(421, NULL, 62, NULL, 79),
(422, NULL, 63, NULL, 80),
(419, NULL, 64, NULL, 81),
(422, NULL, 65, NULL, 82),
(424, NULL, 66, NULL, 83),
(421, NULL, 67, NULL, 84),
(425, 3, 68, 21, NULL),
(425, 3, 69, 22, NULL),
(425, 3, 70, 23, NULL),
(425, 3, 71, 24, NULL),
(425, 3, 72, 25, NULL),
(425, NULL, 73, NULL, 85),
(425, 3, 74, 26, NULL),
(426, NULL, 75, NULL, 86),
(417, NULL, 76, NULL, 87),
(421, NULL, 77, NULL, 88),
(422, NULL, 78, NULL, 89),
(419, NULL, 79, NULL, 90),
(420, NULL, 80, NULL, 91),
(422, NULL, 81, NULL, 92),
(426, NULL, 82, NULL, 93),
(417, NULL, 83, NULL, 94),
(418, NULL, 84, NULL, 95),
(424, NULL, 85, NULL, 96),
(420, NULL, 86, NULL, 97),
(421, NULL, 87, NULL, 98),
(426, NULL, 88, NULL, 99),
(422, NULL, 89, NULL, 100),
(419, NULL, 90, NULL, 101),
(417, NULL, 91, NULL, 102),
(418, NULL, 92, NULL, 103),
(424, NULL, 93, NULL, 104),
(426, NULL, 94, NULL, 105),
(427, NULL, 95, NULL, 106),
(420, NULL, 96, NULL, 107),
(421, NULL, 97, NULL, 108),
(419, NULL, 98, NULL, 109),
(417, NULL, 99, NULL, 110),
(422, NULL, 100, NULL, 111),
(421, NULL, 101, NULL, 112),
(419, NULL, 102, NULL, 113),
(427, NULL, 103, NULL, 114),
(422, NULL, 104, NULL, 115),
(426, NULL, 105, NULL, 116),
(417, NULL, 106, NULL, 117),
(418, NULL, 107, NULL, 118),
(420, NULL, 108, NULL, 119),
(426, NULL, 109, NULL, 120),
(417, NULL, 110, NULL, 121),
(419, NULL, 111, NULL, 122),
(422, NULL, 112, NULL, 123),
(421, NULL, 113, NULL, 124),
(427, NULL, 114, NULL, 125),
(420, NULL, 115, NULL, 126),
(419, NULL, 116, NULL, 127),
(426, NULL, 117, NULL, 128),
(424, NULL, 118, NULL, 129),
(417, NULL, 119, NULL, 130),
(421, NULL, 120, NULL, 131),
(422, NULL, 121, NULL, 132),
(427, NULL, 122, NULL, 133),
(426, NULL, 123, NULL, 134),
(420, NULL, 124, NULL, 135),
(421, NULL, 125, NULL, 136),
(424, NULL, 126, NULL, 137),
(419, NULL, 127, NULL, 138),
(417, NULL, 128, NULL, 139),
(422, NULL, 129, NULL, 140),
(427, NULL, 130, NULL, 141),
(426, NULL, 131, NULL, 142),
(420, NULL, 132, NULL, 143),
(419, NULL, 133, NULL, 144),
(421, NULL, 134, NULL, 145),
(422, NULL, 135, NULL, 146),
(417, NULL, 136, NULL, 147),
(427, NULL, 137, NULL, 148),
(424, NULL, 138, NULL, 149),
(420, NULL, 139, NULL, 150),
(422, NULL, 140, NULL, 151),
(426, NULL, 141, NULL, 152),
(419, NULL, 142, NULL, 153),
(417, NULL, 143, NULL, 154),
(424, NULL, 144, NULL, 155),
(421, NULL, 145, NULL, 156),
(427, NULL, 146, NULL, 157),
(422, NULL, 147, NULL, 158),
(420, NULL, 148, NULL, 159),
(426, NULL, 149, NULL, 160),
(419, NULL, 150, NULL, 161),
(417, NULL, 151, NULL, 162),
(421, NULL, 152, NULL, 163),
(424, NULL, 153, NULL, 164),
(427, NULL, 154, NULL, 165),
(420, NULL, 155, NULL, 166),
(419, NULL, 156, NULL, 167),
(417, NULL, 157, NULL, 168),
(426, NULL, 158, NULL, 169),
(420, NULL, 159, NULL, 170),
(424, NULL, 160, NULL, 171),
(419, NULL, 161, NULL, 172),
(421, NULL, 162, NULL, 173),
(417, NULL, 163, NULL, 174),
(418, NULL, 164, NULL, 175),
(427, NULL, 165, NULL, 176),
(421, NULL, 166, NULL, 177),
(419, NULL, 167, NULL, 178),
(422, NULL, 168, NULL, 179),
(426, NULL, 169, NULL, 180),
(424, NULL, 170, NULL, 181),
(427, NULL, 171, NULL, 182),
(423, NULL, 172, NULL, 183),
(423, 3, 173, 27, NULL),
(423, NULL, 174, NULL, 184),
(423, NULL, 175, NULL, 185),
(423, NULL, 176, NULL, 186),
(423, NULL, 177, NULL, 187),
(423, NULL, 178, NULL, 188),
(423, NULL, 179, NULL, 189),
(423, NULL, 180, NULL, 190),
(423, NULL, 181, NULL, 191),
(423, NULL, 182, NULL, 192),
(423, NULL, 183, NULL, 193),
(423, NULL, 184, NULL, 194),
(423, NULL, 185, NULL, 195),
(427, NULL, 186, NULL, 196),
(417, NULL, 187, NULL, 197),
(418, NULL, 188, NULL, 198),
(419, NULL, 189, NULL, 199),
(420, NULL, 190, NULL, 200),
(421, NULL, 191, NULL, 201),
(422, NULL, 192, NULL, 202),
(427, NULL, 193, NULL, 203),
(417, NULL, 194, NULL, 204),
(418, NULL, 195, NULL, 205),
(419, NULL, 196, NULL, 206),
(420, NULL, 197, NULL, 207),
(421, NULL, 198, NULL, 208),
(422, NULL, 199, NULL, 209),
(427, NULL, 200, NULL, 210),
(417, NULL, 201, NULL, 211),
(418, NULL, 202, NULL, 212),
(419, NULL, 203, NULL, 213),
(420, NULL, 204, NULL, 214),
(421, NULL, 205, NULL, 215),
(422, NULL, 206, NULL, 216),
(427, NULL, 207, NULL, 217),
(417, NULL, 208, NULL, 218),
(418, NULL, 209, NULL, 219),
(419, NULL, 210, NULL, 220),
(420, NULL, 211, NULL, 221),
(421, NULL, 212, NULL, 222),
(422, NULL, 213, NULL, 223),
(427, NULL, 214, NULL, 224),
(417, NULL, 215, NULL, 225),
(418, NULL, 216, NULL, 226),
(419, NULL, 217, NULL, 227),
(420, NULL, 218, NULL, 228),
(421, NULL, 219, NULL, 229),
(422, NULL, 220, NULL, 230),
(427, NULL, 221, NULL, 231),
(417, NULL, 222, NULL, 232),
(418, NULL, 223, NULL, 233),
(419, NULL, 224, NULL, 234),
(420, NULL, 225, NULL, 235),
(421, NULL, 226, NULL, 236),
(422, NULL, 227, NULL, 237),
(427, NULL, 228, NULL, 238),
(417, NULL, 229, NULL, 239),
(418, NULL, 230, NULL, 240),
(419, NULL, 231, NULL, 241),
(420, NULL, 232, NULL, 242),
(421, NULL, 233, NULL, 243),
(422, NULL, 234, NULL, 244),
(427, NULL, 235, NULL, 245),
(417, NULL, 236, NULL, 246),
(418, NULL, 237, NULL, 247),
(419, NULL, 238, NULL, 248),
(420, NULL, 239, NULL, 249),
(421, NULL, 240, NULL, 250),
(422, NULL, 241, NULL, 251),
(427, NULL, 242, NULL, 252),
(417, NULL, 243, NULL, 253),
(418, NULL, 244, NULL, 254),
(419, NULL, 245, NULL, 255),
(420, NULL, 246, NULL, 256),
(421, NULL, 247, NULL, 257),
(422, NULL, 248, NULL, 258),
(427, NULL, 249, NULL, 259),
(417, NULL, 250, NULL, 260),
(418, NULL, 251, NULL, 261),
(419, NULL, 252, NULL, 262),
(420, NULL, 253, NULL, 263),
(421, NULL, 254, NULL, 264),
(422, NULL, 255, NULL, 265),
(427, NULL, 256, NULL, 266),
(417, NULL, 257, NULL, 267),
(418, NULL, 258, NULL, 268),
(419, NULL, 259, NULL, 269),
(420, NULL, 260, NULL, 270),
(421, NULL, 261, NULL, 271),
(422, NULL, 262, NULL, 272),
(427, NULL, 263, NULL, 273),
(417, NULL, 264, NULL, 274),
(418, NULL, 265, NULL, 275),
(419, NULL, 266, NULL, 276),
(420, NULL, 267, NULL, 277),
(421, NULL, 268, NULL, 278),
(422, NULL, 269, NULL, 279),
(427, NULL, 270, NULL, 280),
(417, NULL, 271, NULL, 281),
(418, NULL, 272, NULL, 282),
(419, NULL, 273, NULL, 283),
(420, NULL, 274, NULL, 284),
(421, NULL, 275, NULL, 285);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hechos_buffer`
--

CREATE TABLE `hechos_buffer` (
  `id_compra` int(11) DEFAULT NULL,
  `id_arriendo` int(11) DEFAULT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_estado_devolucion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `hechos_buffer`
--

INSERT INTO `hechos_buffer` (`id_compra`, `id_arriendo`, `id_cliente`, `id_estado_devolucion`) VALUES
(19, NULL, 417, NULL),
(NULL, 19, 417, 3),
(NULL, 20, 418, 3),
(20, NULL, 417, NULL),
(21, NULL, 419, NULL),
(22, NULL, 419, NULL),
(23, NULL, 419, NULL),
(24, NULL, 419, NULL),
(25, NULL, 419, NULL),
(26, NULL, 419, NULL),
(27, NULL, 419, NULL),
(28, NULL, 419, NULL),
(29, NULL, 419, NULL),
(30, NULL, 419, NULL),
(31, NULL, 419, NULL),
(32, NULL, 419, NULL),
(33, NULL, 419, NULL),
(34, NULL, 419, NULL),
(35, NULL, 419, NULL),
(36, NULL, 419, NULL),
(37, NULL, 419, NULL),
(38, NULL, 419, NULL),
(39, NULL, 419, NULL),
(40, NULL, 419, NULL),
(41, NULL, 420, NULL),
(42, NULL, 420, NULL),
(43, NULL, 420, NULL),
(44, NULL, 417, NULL),
(45, NULL, 417, NULL),
(46, NULL, 417, NULL),
(47, NULL, 417, NULL),
(48, NULL, 417, NULL),
(49, NULL, 418, NULL),
(50, NULL, 418, NULL),
(51, NULL, 418, NULL),
(52, NULL, 418, NULL),
(53, NULL, 419, NULL),
(54, NULL, 419, NULL),
(55, NULL, 419, NULL),
(56, NULL, 419, NULL),
(57, NULL, 419, NULL),
(58, NULL, 419, NULL),
(59, NULL, 420, NULL),
(60, NULL, 420, NULL),
(61, NULL, 420, NULL),
(62, NULL, 420, NULL),
(63, NULL, 420, NULL),
(64, NULL, 420, NULL),
(65, NULL, 421, NULL),
(66, NULL, 421, NULL),
(67, NULL, 421, NULL),
(68, NULL, 421, NULL),
(69, NULL, 421, NULL),
(70, NULL, 421, NULL),
(71, NULL, 422, NULL),
(72, NULL, 422, NULL),
(73, NULL, 422, NULL),
(74, NULL, 422, NULL),
(75, NULL, 422, NULL),
(76, NULL, 422, NULL),
(77, NULL, 423, NULL),
(78, NULL, 417, NULL),
(79, NULL, 421, NULL),
(80, NULL, 422, NULL),
(81, NULL, 419, NULL),
(82, NULL, 422, NULL),
(83, NULL, 424, NULL),
(84, NULL, 421, NULL),
(NULL, 21, 425, 3),
(NULL, 22, 425, 3),
(NULL, 23, 425, 3),
(NULL, 24, 425, 3),
(NULL, 25, 425, 3),
(85, NULL, 425, NULL),
(NULL, 26, 425, 3),
(86, NULL, 426, NULL),
(87, NULL, 417, NULL),
(88, NULL, 421, NULL),
(89, NULL, 422, NULL),
(90, NULL, 419, NULL),
(91, NULL, 420, NULL),
(92, NULL, 422, NULL),
(93, NULL, 426, NULL),
(94, NULL, 417, NULL),
(95, NULL, 418, NULL),
(96, NULL, 424, NULL),
(97, NULL, 420, NULL),
(98, NULL, 421, NULL),
(99, NULL, 426, NULL),
(100, NULL, 422, NULL),
(101, NULL, 419, NULL),
(102, NULL, 417, NULL),
(103, NULL, 418, NULL),
(104, NULL, 424, NULL),
(105, NULL, 426, NULL),
(106, NULL, 427, NULL),
(107, NULL, 420, NULL),
(108, NULL, 421, NULL),
(109, NULL, 419, NULL),
(110, NULL, 417, NULL),
(111, NULL, 422, NULL),
(112, NULL, 421, NULL),
(113, NULL, 419, NULL),
(114, NULL, 427, NULL),
(115, NULL, 422, NULL),
(116, NULL, 426, NULL),
(117, NULL, 417, NULL),
(118, NULL, 418, NULL),
(119, NULL, 420, NULL),
(120, NULL, 426, NULL),
(121, NULL, 417, NULL),
(122, NULL, 419, NULL),
(123, NULL, 422, NULL),
(124, NULL, 421, NULL),
(125, NULL, 427, NULL),
(126, NULL, 420, NULL),
(127, NULL, 419, NULL),
(128, NULL, 426, NULL),
(129, NULL, 424, NULL),
(130, NULL, 417, NULL),
(131, NULL, 421, NULL),
(132, NULL, 422, NULL),
(133, NULL, 427, NULL),
(134, NULL, 426, NULL),
(135, NULL, 420, NULL),
(136, NULL, 421, NULL),
(137, NULL, 424, NULL),
(138, NULL, 419, NULL),
(139, NULL, 417, NULL),
(140, NULL, 422, NULL),
(141, NULL, 427, NULL),
(142, NULL, 426, NULL),
(143, NULL, 420, NULL),
(144, NULL, 419, NULL),
(145, NULL, 421, NULL),
(146, NULL, 422, NULL),
(147, NULL, 417, NULL),
(148, NULL, 427, NULL),
(149, NULL, 424, NULL),
(150, NULL, 420, NULL),
(151, NULL, 422, NULL),
(152, NULL, 426, NULL),
(153, NULL, 419, NULL),
(154, NULL, 417, NULL),
(155, NULL, 424, NULL),
(156, NULL, 421, NULL),
(157, NULL, 427, NULL),
(158, NULL, 422, NULL),
(159, NULL, 420, NULL),
(160, NULL, 426, NULL),
(161, NULL, 419, NULL),
(162, NULL, 417, NULL),
(163, NULL, 421, NULL),
(164, NULL, 424, NULL),
(165, NULL, 427, NULL),
(166, NULL, 420, NULL),
(167, NULL, 419, NULL),
(168, NULL, 417, NULL),
(169, NULL, 426, NULL),
(170, NULL, 420, NULL),
(171, NULL, 424, NULL),
(172, NULL, 419, NULL),
(173, NULL, 421, NULL),
(174, NULL, 417, NULL),
(175, NULL, 418, NULL),
(176, NULL, 427, NULL),
(177, NULL, 421, NULL),
(178, NULL, 419, NULL),
(179, NULL, 422, NULL),
(180, NULL, 426, NULL),
(181, NULL, 424, NULL),
(182, NULL, 427, NULL),
(183, NULL, 423, NULL),
(NULL, 27, 423, 3),
(184, NULL, 423, NULL),
(185, NULL, 423, NULL),
(186, NULL, 423, NULL),
(187, NULL, 423, NULL),
(188, NULL, 423, NULL),
(189, NULL, 423, NULL),
(190, NULL, 423, NULL),
(191, NULL, 423, NULL),
(192, NULL, 423, NULL),
(193, NULL, 423, NULL),
(194, NULL, 423, NULL),
(195, NULL, 423, NULL),
(196, NULL, 427, NULL),
(197, NULL, 417, NULL),
(198, NULL, 418, NULL),
(199, NULL, 419, NULL),
(200, NULL, 420, NULL),
(201, NULL, 421, NULL),
(202, NULL, 422, NULL),
(203, NULL, 427, NULL),
(204, NULL, 417, NULL),
(205, NULL, 418, NULL),
(206, NULL, 419, NULL),
(207, NULL, 420, NULL),
(208, NULL, 421, NULL),
(209, NULL, 422, NULL),
(210, NULL, 427, NULL),
(211, NULL, 417, NULL),
(212, NULL, 418, NULL),
(213, NULL, 419, NULL),
(214, NULL, 420, NULL),
(215, NULL, 421, NULL),
(216, NULL, 422, NULL),
(217, NULL, 427, NULL),
(218, NULL, 417, NULL),
(219, NULL, 418, NULL),
(220, NULL, 419, NULL),
(221, NULL, 420, NULL),
(222, NULL, 421, NULL),
(223, NULL, 422, NULL),
(224, NULL, 427, NULL),
(225, NULL, 417, NULL),
(226, NULL, 418, NULL),
(227, NULL, 419, NULL),
(228, NULL, 420, NULL),
(229, NULL, 421, NULL),
(230, NULL, 422, NULL),
(231, NULL, 427, NULL),
(232, NULL, 417, NULL),
(233, NULL, 418, NULL),
(234, NULL, 419, NULL),
(235, NULL, 420, NULL),
(236, NULL, 421, NULL),
(237, NULL, 422, NULL),
(238, NULL, 427, NULL),
(239, NULL, 417, NULL),
(240, NULL, 418, NULL),
(241, NULL, 419, NULL),
(242, NULL, 420, NULL),
(243, NULL, 421, NULL),
(244, NULL, 422, NULL),
(245, NULL, 427, NULL),
(246, NULL, 417, NULL),
(247, NULL, 418, NULL),
(248, NULL, 419, NULL),
(249, NULL, 420, NULL),
(250, NULL, 421, NULL),
(251, NULL, 422, NULL),
(252, NULL, 427, NULL),
(253, NULL, 417, NULL),
(254, NULL, 418, NULL),
(255, NULL, 419, NULL),
(256, NULL, 420, NULL),
(257, NULL, 421, NULL),
(258, NULL, 422, NULL),
(259, NULL, 427, NULL),
(260, NULL, 417, NULL),
(261, NULL, 418, NULL),
(262, NULL, 419, NULL),
(263, NULL, 420, NULL),
(264, NULL, 421, NULL),
(265, NULL, 422, NULL),
(266, NULL, 427, NULL),
(267, NULL, 417, NULL),
(268, NULL, 418, NULL),
(269, NULL, 419, NULL),
(270, NULL, 420, NULL),
(271, NULL, 421, NULL),
(272, NULL, 422, NULL),
(273, NULL, 427, NULL),
(274, NULL, 417, NULL),
(275, NULL, 418, NULL),
(276, NULL, 419, NULL),
(277, NULL, 420, NULL),
(278, NULL, 421, NULL),
(279, NULL, 422, NULL),
(280, NULL, 427, NULL),
(281, NULL, 417, NULL),
(282, NULL, 418, NULL),
(283, NULL, 419, NULL),
(284, NULL, 420, NULL),
(285, NULL, 421, NULL);

--
-- Disparadores `hechos_buffer`
--
DELIMITER $$
CREATE TRIGGER `trg_insert_hechos_from_buffer` AFTER INSERT ON `hechos_buffer` FOR EACH ROW BEGIN
    -- Insertar en la tabla de hechos
    INSERT INTO hechosventaslibros (id_cliente, id_compra, id_arriendo, id_estado_devolucion)
    VALUES (NEW.id_cliente, NEW.id_compra, NEW.id_arriendo, NEW.id_estado_devolucion);
END
$$
DELIMITER ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `dimarriendos`
--
ALTER TABLE `dimarriendos`
  ADD PRIMARY KEY (`id_arriendo`),
  ADD KEY `fk_id_tiempo_arriendo` (`id_tiempo_arriendo`);

--
-- Indices de la tabla `dimcliente`
--
ALTER TABLE `dimcliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `dimcompras`
--
ALTER TABLE `dimcompras`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `fk_id_tiempo_compra` (`id_tiempo_compra`);

--
-- Indices de la tabla `dimestadodevolucion`
--
ALTER TABLE `dimestadodevolucion`
  ADD PRIMARY KEY (`id_estado_devolucion`);

--
-- Indices de la tabla `dimtiempoarriendos`
--
ALTER TABLE `dimtiempoarriendos`
  ADD PRIMARY KEY (`id_tiempo_arriendo`);

--
-- Indices de la tabla `dimtiempocompras`
--
ALTER TABLE `dimtiempocompras`
  ADD PRIMARY KEY (`id_tiempo_compra`);

--
-- Indices de la tabla `hechosventaslibros`
--
ALTER TABLE `hechosventaslibros`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_cliente` (`id_cliente`),
  ADD KEY `fk_estado_devolucion` (`id_estado_devolucion`),
  ADD KEY `fk_id_arriendo` (`id_arriendo`),
  ADD KEY `fk_id_compra` (`id_compra`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `dimarriendos`
--
ALTER TABLE `dimarriendos`
  MODIFY `id_arriendo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `dimcliente`
--
ALTER TABLE `dimcliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=428;

--
-- AUTO_INCREMENT de la tabla `dimcompras`
--
ALTER TABLE `dimcompras`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=286;

--
-- AUTO_INCREMENT de la tabla `dimestadodevolucion`
--
ALTER TABLE `dimestadodevolucion`
  MODIFY `id_estado_devolucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `dimtiempoarriendos`
--
ALTER TABLE `dimtiempoarriendos`
  MODIFY `id_tiempo_arriendo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `dimtiempocompras`
--
ALTER TABLE `dimtiempocompras`
  MODIFY `id_tiempo_compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=188;

--
-- AUTO_INCREMENT de la tabla `hechosventaslibros`
--
ALTER TABLE `hechosventaslibros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=276;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `dimarriendos`
--
ALTER TABLE `dimarriendos`
  ADD CONSTRAINT `fk_id_tiempo_arriendo` FOREIGN KEY (`id_tiempo_arriendo`) REFERENCES `dimtiempoarriendos` (`id_tiempo_arriendo`);

--
-- Filtros para la tabla `dimcompras`
--
ALTER TABLE `dimcompras`
  ADD CONSTRAINT `fk_id_tiempo_compra` FOREIGN KEY (`id_tiempo_compra`) REFERENCES `dimtiempocompras` (`id_tiempo_compra`);

--
-- Filtros para la tabla `hechosventaslibros`
--
ALTER TABLE `hechosventaslibros`
  ADD CONSTRAINT `fk_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `dimcliente` (`id_cliente`),
  ADD CONSTRAINT `fk_estado_devolucion` FOREIGN KEY (`id_estado_devolucion`) REFERENCES `dimestadodevolucion` (`id_estado_devolucion`),
  ADD CONSTRAINT `fk_id_arriendo` FOREIGN KEY (`id_arriendo`) REFERENCES `dimarriendos` (`id_arriendo`),
  ADD CONSTRAINT `fk_id_compra` FOREIGN KEY (`id_compra`) REFERENCES `dimcompras` (`id_compra`),
  ADD CONSTRAINT `hechosventaslibros_ibfk_3` FOREIGN KEY (`id_cliente`) REFERENCES `dimcliente` (`id_cliente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
