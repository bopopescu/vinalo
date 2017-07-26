-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 26, 2017 at 06:44 AM
-- Server version: 5.5.22
-- PHP Version: 5.3.10-1ubuntu3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `truyentranh`
--

-- --------------------------------------------------------

--
-- Table structure for table `Book`
--

CREATE TABLE IF NOT EXISTS `Book` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `book_category` int(11) NOT NULL,
  `book_site` int(11) NOT NULL,
  `book_linkUpdate` varchar(255) CHARACTER SET latin1 DEFAULT '',
  `book_slug` varchar(255) CHARACTER SET latin1 DEFAULT '',
  `book_author` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `book_description` text,
  PRIMARY KEY (`book_id`),
  KEY `name` (`book_name`,`book_category`),
  KEY `site` (`book_site`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf32 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `Category`
--

CREATE TABLE IF NOT EXISTS `Category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `category_site` int(11) NOT NULL,
  `category_slug` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`category_id`),
  KEY `site` (`category_site`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- Table structure for table `Chapter`
--

CREATE TABLE IF NOT EXISTS `Chapter` (
  `chapter_id` int(11) NOT NULL AUTO_INCREMENT,
  `chapter_book` int(11) NOT NULL,
  `chapter_name` varchar(255) NOT NULL DEFAULT '',
  `chapter_content` text,
  `chapter_slug` varchar(255) NOT NULL DEFAULT '',
  `chapter_order` int(11) NOT NULL,
  PRIMARY KEY (`chapter_id`),
  KEY `bookId` (`chapter_book`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `map_book_category`
--

CREATE TABLE IF NOT EXISTS `map_book_category` (
  `book_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`category_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Site`
--

CREATE TABLE IF NOT EXISTS `Site` (
  `site_id` int(11) NOT NULL AUTO_INCREMENT,
  `site_name` varchar(255) NOT NULL,
  PRIMARY KEY (`site_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
