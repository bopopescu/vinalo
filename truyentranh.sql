-- phpMyAdmin SQL Dump
-- version 4.7.3
-- https://www.phpmyadmin.net/
--
-- Host: 172.17.0.4
-- Generation Time: Aug 05, 2017 at 01:00 PM
-- Server version: 5.7.19
-- PHP Version: 7.1.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `truyentranh`
--

-- --------------------------------------------------------

--
-- Table structure for table `Book`
--

CREATE TABLE `Book` (
  `book_id` int(11) NOT NULL,
  `book_name` varchar(255) NOT NULL DEFAULT '',
  `book_site` int(11) NOT NULL,
  `book_linkUpdate` varchar(255) DEFAULT '',
  `book_slug` varchar(255) DEFAULT '',
  `book_author` varchar(255) DEFAULT NULL,
  `book_description` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Category`
--

CREATE TABLE `Category` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `category_site` int(11) NOT NULL,
  `category_slug` varchar(255) NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Chapter`
--

CREATE TABLE `Chapter` (
  `chapter_id` int(11) NOT NULL,
  `chapter_book` int(11) NOT NULL,
  `chapter_name` varchar(255) NOT NULL DEFAULT '',
  `chapter_content` mediumtext,
  `chapter_slug` varchar(255) NOT NULL DEFAULT '',
  `chapter_order` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `map_book_category`
--

CREATE TABLE `map_book_category` (
  `book_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Site`
--

CREATE TABLE `Site` (
  `site_id` int(11) NOT NULL,
  `site_name` varchar(255) CHARACTER SET latin1 NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Book`
--
ALTER TABLE `Book`
  ADD PRIMARY KEY (`book_id`),
  ADD KEY `name` (`book_name`),
  ADD KEY `site` (`book_site`);

--
-- Indexes for table `Category`
--
ALTER TABLE `Category`
  ADD PRIMARY KEY (`category_id`),
  ADD KEY `site` (`category_site`);

--
-- Indexes for table `Chapter`
--
ALTER TABLE `Chapter`
  ADD PRIMARY KEY (`chapter_id`),
  ADD KEY `bookId` (`chapter_book`);

--
-- Indexes for table `map_book_category`
--
ALTER TABLE `map_book_category`
  ADD PRIMARY KEY (`book_id`,`category_id`);

--
-- Indexes for table `Site`
--
ALTER TABLE `Site`
  ADD PRIMARY KEY (`site_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Book`
--
ALTER TABLE `Book`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=355;
--
-- AUTO_INCREMENT for table `Category`
--
ALTER TABLE `Category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
--
-- AUTO_INCREMENT for table `Chapter`
--
ALTER TABLE `Chapter`
  MODIFY `chapter_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17649;
--
-- AUTO_INCREMENT for table `Site`
--
ALTER TABLE `Site`
  MODIFY `site_id` int(11) NOT NULL AUTO_INCREMENT;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
