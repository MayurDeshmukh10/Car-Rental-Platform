-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: car_rental
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.18.04.1

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
-- Table structure for table `Admin_User`
--

DROP TABLE IF EXISTS `Admin_User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Admin_User` (
  `userId` varchar(100) NOT NULL,
  `fName` varchar(100) DEFAULT NULL,
  `lName` varchar(100) DEFAULT NULL,
  `emailId` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `registration_Date` varchar(100) DEFAULT NULL,
  `password` varchar(1000) DEFAULT NULL,
  `reset_Question` varchar(100) DEFAULT NULL,
  `reset_Ans_Type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin_User`
--

LOCK TABLES `Admin_User` WRITE;
/*!40000 ALTER TABLE `Admin_User` DISABLE KEYS */;
/*!40000 ALTER TABLE `Admin_User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking`
--

DROP TABLE IF EXISTS `Booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Booking` (
  `bookingId` int(50) NOT NULL AUTO_INCREMENT,
  `userId` varchar(100) DEFAULT NULL,
  `Cab` varchar(100) DEFAULT NULL,
  `startDate` varchar(100) DEFAULT NULL,
  `endDate` varchar(100) DEFAULT NULL,
  `Pickup_time` varchar(100) DEFAULT NULL,
  `Pickup_location` varchar(100) DEFAULT NULL,
  `Drop_off_location` varchar(100) DEFAULT NULL,
  `driverId` int(50) DEFAULT NULL,
  `carid` varchar(100) DEFAULT NULL,
  `cab_route` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`bookingId`),
  KEY `userId` (`userId`),
  KEY `driverId` (`driverId`),
  CONSTRAINT `Booking_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `Cust_User` (`userId`),
  CONSTRAINT `Booking_ibfk_2` FOREIGN KEY (`driverId`) REFERENCES `Driver` (`driverId`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking`
--

LOCK TABLES `Booking` WRITE;
/*!40000 ALTER TABLE `Booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Car`
--

DROP TABLE IF EXISTS `Car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Car` (
  `Car_id` varchar(100) NOT NULL,
  `model_name` varchar(100) DEFAULT NULL,
  `registeration_no` varchar(100) DEFAULT NULL,
  `seating_capacity` varchar(100) DEFAULT NULL,
  `Car_type` varchar(100) DEFAULT NULL,
  `price_per_km` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'Available',
  PRIMARY KEY (`Car_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Car`
--

LOCK TABLES `Car` WRITE;
/*!40000 ALTER TABLE `Car` DISABLE KEYS */;
/*!40000 ALTER TABLE `Car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cust_User`
--

DROP TABLE IF EXISTS `Cust_User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cust_User` (
  `userId` varchar(100) NOT NULL,
  `fName` varchar(100) DEFAULT NULL,
  `lName` varchar(100) DEFAULT NULL,
  `emailId` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `registration_Date` varchar(100) DEFAULT NULL,
  `password` varchar(1000) DEFAULT NULL,
  `reset_Question` varchar(100) DEFAULT NULL,
  `reset_Ans_Type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cust_User`
--

LOCK TABLES `Cust_User` WRITE;
/*!40000 ALTER TABLE `Cust_User` DISABLE KEYS */;
/*!40000 ALTER TABLE `Cust_User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Driver`
--

DROP TABLE IF EXISTS `Driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Driver` (
  `driverId` int(50) NOT NULL AUTO_INCREMENT,
  `fName` varchar(100) DEFAULT NULL,
  `lName` varchar(100) DEFAULT NULL,
  `phone_no` varchar(100) DEFAULT NULL,
  `licence_no` varchar(50) DEFAULT NULL,
  `age` int(10) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'Available',
  PRIMARY KEY (`driverId`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Driver`
--

LOCK TABLES `Driver` WRITE;
/*!40000 ALTER TABLE `Driver` DISABLE KEYS */;
/*!40000 ALTER TABLE `Driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback`
--

DROP TABLE IF EXISTS `Feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback` (
  `userId` varchar(100) DEFAULT NULL,
  `fName` varchar(100) DEFAULT NULL,
  `lName` varchar(100) DEFAULT NULL,
  `emailId` varchar(100) DEFAULT NULL,
  `rating` varchar(100) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `Date` varchar(100) DEFAULT NULL,
  KEY `userId` (`userId`),
  CONSTRAINT `Feedback_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `Cust_User` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback`
--

LOCK TABLES `Feedback` WRITE;
/*!40000 ALTER TABLE `Feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Login_History`
--

DROP TABLE IF EXISTS `Login_History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Login_History` (
  `user` varchar(100) DEFAULT NULL,
  `userId` varchar(100) DEFAULT NULL,
  `Date` varchar(100) DEFAULT NULL,
  `Time` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Login_History`
--

LOCK TABLES `Login_History` WRITE;
/*!40000 ALTER TABLE `Login_History` DISABLE KEYS */;
/*!40000 ALTER TABLE `Login_History` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Payment`
--

DROP TABLE IF EXISTS `Payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Payment` (
  `Payment_id` int(50) NOT NULL AUTO_INCREMENT,
  `payment_type` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `bookingId` int(50) DEFAULT NULL,
  `total_amount` int(255) DEFAULT NULL,
  PRIMARY KEY (`Payment_id`),
  KEY `bookingId` (`bookingId`),
  CONSTRAINT `Payment_ibfk_1` FOREIGN KEY (`bookingId`) REFERENCES `Booking` (`bookingId`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Payment`
--

LOCK TABLES `Payment` WRITE;
/*!40000 ALTER TABLE `Payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Payment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-27  0:00:48
