-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: epub_reader
-- ------------------------------------------------------
-- Server version	5.5.35-0ubuntu0.12.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tabBook`
--

DROP TABLE IF EXISTS `tabBook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBook` (
  `id` varchar(50) DEFAULT NULL,
  `book_name` varchar(50) DEFAULT NULL,
  `author` varchar(50) DEFAULT NULL,
  `publisher` varchar(50) DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  `edition` varchar(30) NOT NULL,
  `more_details` varchar(30) NOT NULL,
  `owner` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='latin1_swedish_ci';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabBook`
--

LOCK TABLES `tabBook` WRITE;
/*!40000 ALTER TABLE `tabBook` DISABLE KEYS */;
INSERT INTO `tabBook` VALUES ('BOOK-5','Pied Piper','Akhilesh','Edward Publications',120,'2nd Edition','','admin');
/*!40000 ALTER TABLE `tabBook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabIssue`
--

DROP TABLE IF EXISTS `tabIssue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabIssue` (
  `id` varchar(20) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabIssue`
--

LOCK TABLES `tabIssue` WRITE;
/*!40000 ALTER TABLE `tabIssue` DISABLE KEYS */;
INSERT INTO `tabIssue` VALUES ('ISSUE-1','Test','Test Data verified');
/*!40000 ALTER TABLE `tabIssue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabProfile`
--

DROP TABLE IF EXISTS `tabProfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProfile` (
  `id` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL DEFAULT '',
  `last_name` varchar(30) NOT NULL DEFAULT '',
  `login_id` varchar(15) DEFAULT NULL,
  `password` varchar(15) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `date_of_birth` datetime NOT NULL,
  `enabled` int(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='latin1_swedish_ci';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabProfile`
--

LOCK TABLES `tabProfile` WRITE;
/*!40000 ALTER TABLE `tabProfile` DISABLE KEYS */;
INSERT INTO `tabProfile` VALUES ('admin','Administrator','','admin','admin123','Administrator','0000-00-00 00:00:00',1);
/*!40000 ALTER TABLE `tabProfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabadmin`
--

DROP TABLE IF EXISTS `tabadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabadmin` (
  `book` varchar(20) DEFAULT NULL,
  `favorite` varchar(20) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `book_path` varchar(100) DEFAULT NULL,
  `book_cover_path` varchar(100) DEFAULT NULL,
  `format` varchar(10) DEFAULT NULL,
  `shared` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabadmin`
--

LOCK TABLES `tabadmin` WRITE;
/*!40000 ALTER TABLE `tabadmin` DISABLE KEYS */;
INSERT INTO `tabadmin` VALUES ('BOOK-5','Yes',0,'files/books/admin/BOOK-5/piedpiper.epub','files/books/admin/BOOK-5/Pied_piper.jpg','epub','No');
/*!40000 ALTER TABLE `tabadmin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-04-13 23:04:08
