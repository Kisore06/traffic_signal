-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 22, 2024 at 01:17 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `traffic_signal`
--

-- --------------------------------------------------------

--
-- Table structure for table `ap_admin`
--

CREATE TABLE `ap_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `utype` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_admin`
--

INSERT INTO `ap_admin` (`username`, `password`, `utype`) VALUES
('admin', 'admin', 1);

-- --------------------------------------------------------

--
-- Table structure for table `ap_temp`
--

CREATE TABLE `ap_temp` (
  `id` int(11) NOT NULL,
  `value1` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_temp`
--

INSERT INTO `ap_temp` (`id`, `value1`) VALUES
(1, 6),
(2, 16),
(3, 6),
(4, 6),
(5, 0),
(6, 0),
(7, 0),
(8, 0),
(9, 0),
(10, 0);
