-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: mediquick
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `beds`
--

DROP TABLE IF EXISTS `beds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beds` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hospital_id` int DEFAULT NULL,
  `bed_number` varchar(10) NOT NULL,
  `is_occupied` tinyint(1) DEFAULT '0',
  `hold_until` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `beds_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beds`
--

LOCK TABLES `beds` WRITE;
/*!40000 ALTER TABLE `beds` DISABLE KEYS */;
INSERT INTO `beds` VALUES (1,1,'K1-B1',0,'2025-05-30 20:11:26'),(2,1,'K1-B2',1,NULL),(3,1,'K1-B3',0,NULL),(4,1,'K1-B4',1,NULL),(5,1,'K1-B5',0,NULL),(6,2,'C1-B1',1,NULL),(7,2,'C1-B2',0,NULL),(8,2,'C1-B3',1,NULL),(9,2,'C1-B4',0,NULL),(10,2,'C1-B5',1,NULL),(11,3,'R1-B1',0,NULL),(12,3,'R1-B2',1,NULL),(13,3,'R1-B3',0,NULL),(14,3,'R1-B4',1,NULL),(15,3,'R1-B5',0,NULL),(16,4,'S1-B1',1,NULL),(17,4,'S1-B2',0,NULL),(18,4,'S1-B3',0,NULL),(19,4,'S1-B4',1,NULL),(20,4,'S1-B5',1,NULL),(21,5,'SS1-B1',0,NULL),(22,5,'SS1-B2',1,NULL),(23,5,'SS1-B3',0,NULL),(24,5,'SS1-B4',1,NULL),(25,5,'SS1-B5',0,NULL);
/*!40000 ALTER TABLE `beds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hospital_id` int DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `specialization` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,1,'Dr. Anjali Rao','Cardiologist'),(2,1,'Dr. Vivek Mehra','Neurologist'),(3,2,'Dr. Sara Iqbal','Cardiologist'),(4,2,'Dr. Manish Kulkarni','Orthopedic'),(5,2,'Dr. Nisitha Prasad','Trauma Surgeon'),(6,3,'Dr. Tanya Sinha','Pulmonologist'),(7,3,'Dr. Rajeev Sharma','Dermatologist');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals`
--

DROP TABLE IF EXISTS `hospitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `location_lat` double NOT NULL,
  `location_lon` double NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals`
--

LOCK TABLES `hospitals` WRITE;
/*!40000 ALTER TABLE `hospitals` DISABLE KEYS */;
INSERT INTO `hospitals` VALUES (1,'Kiran Hospital',17.3453,78.5282,'12345'),(2,'Care Hospital',17.373093,78.490036,'abcd'),(3,'Retreat Hospital',17.3748,78.5071,'xyz23'),(4,'Sapthagiri Hospital',17.3691,78.5302,'7890'),(5,'Sai Sanjeevini Hospital',17.3609,78.5432,'yuiop');
/*!40000 ALTER TABLE `hospitals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `emergency_type` varchar(100) NOT NULL,
  `hospital_id` int DEFAULT NULL,
  `bed_id` int DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('on_hold','booked','discharged') DEFAULT 'on_hold',
  `bed_confirmed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `hospital_id` (`hospital_id`),
  KEY `bed_id` (`bed_id`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`),
  CONSTRAINT `patients_ibfk_2` FOREIGN KEY (`bed_id`) REFERENCES `beds` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (6,'Eesha','8106912113','Cardiac',2,10,'2025-05-28 19:18:58','on_hold',0),(7,'AriKAKI','8106912113','Respiratory',3,14,'2025-05-28 19:27:43','on_hold',0),(8,'Leo','9876543210','Cardiac',2,7,'2025-05-28 23:11:33','on_hold',0),(12,'John Doe','9876543210','Cardiac',1,1,'2025-05-30 20:08:28','on_hold',0),(13,'John Doe','9876543210','Cardiac',1,1,'2025-05-30 20:10:25','on_hold',0);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-31 11:08:33
