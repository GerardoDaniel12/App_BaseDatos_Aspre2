-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: tabla1
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `formulario_inspeccion`
--

DROP TABLE IF EXISTS `formulario_inspeccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formulario_inspeccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `doc` varchar(255) DEFAULT NULL,
  `fecha_realizado` date DEFAULT NULL,
  `planta` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `numero_extintor` varchar(255) DEFAULT NULL,
  `ubicacion_extintor` varchar(255) DEFAULT NULL,
  `tipo` varchar(255) DEFAULT NULL,
  `capacidad_kg` decimal(10,2) DEFAULT NULL,
  `fecha_fabricacion` date DEFAULT NULL,
  `fecha_recarga` date DEFAULT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `fecha_ultima_prueba` date DEFAULT NULL,
  `presion` varchar(50) DEFAULT NULL,
  `manometro` varchar(50) DEFAULT NULL,
  `seguro` varchar(50) DEFAULT NULL,
  `etiquetas` varchar(50) DEFAULT NULL,
  `senalamientos` varchar(50) DEFAULT NULL,
  `circulo_numero` varchar(50) DEFAULT NULL,
  `pintura` varchar(50) DEFAULT NULL,
  `manguera` varchar(50) DEFAULT NULL,
  `boquilla` varchar(50) DEFAULT NULL,
  `golpes_danos` varchar(50) DEFAULT NULL,
  `obstruido` varchar(50) DEFAULT NULL,
  `comentarios` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formulario_inspeccion`
--

LOCK TABLES `formulario_inspeccion` WRITE;
/*!40000 ALTER TABLE `formulario_inspeccion` DISABLE KEYS */;
INSERT INTO `formulario_inspeccion` VALUES (2,'A0000001','2024-12-25','Frisa santa catarina','forja','1','forja','CO2',2.20,'2023-10-12','2020-09-10','2020-09-10','2021-05-25','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','Nada visto'),(3,'A0000002','2024-12-25','Frisa santa catarina','forja','2','forja','PQS',2.20,'2023-10-12','2020-09-10','2020-09-10','2021-05-25','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','Todo bien'),(4,'A0000002','2024-12-25','Frisa santa catarina','forja','2','forja','PQS',2.20,'2023-10-12','2020-09-10','2020-09-10','2021-05-25','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','Todo bien'),(5,'A0000002','2024-12-25','Frisa santa catarina','forja','2','forja','PQS',2.20,'2023-10-12','2020-09-10','2020-09-10','2021-05-25','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','Todo bien'),(6,'A0000002','2024-12-25','Frisa santa catarina','forja','2','forja','PQS',2.20,'2023-10-12','2020-09-10','2020-09-10','2021-05-25','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','ok','Todo bien');
/*!40000 ALTER TABLE `formulario_inspeccion` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-31  9:29:37
