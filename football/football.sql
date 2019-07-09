-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: football
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

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
-- Table structure for table `bifen_bodan_std`
--

DROP TABLE IF EXISTS `bifen_bodan_std`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bifen_bodan_std` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `insert_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `win_bodan_std` float(20,3) DEFAULT NULL,
  `dogfall_bodan_std` float(20,3) DEFAULT NULL,
  `lose_bodan_std` float(20,3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=872 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bifen_index`
--

DROP TABLE IF EXISTS `bifen_index`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bifen_index` (
  `id` bigint(5) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL,
  `html_index` int(11) DEFAULT NULL,
  `com_name` varchar(45) DEFAULT NULL COMMENT '公司名字',
  `win_type` varchar(45) DEFAULT NULL,
  `m1_0` varchar(45) DEFAULT NULL,
  `m2_0` varchar(45) DEFAULT NULL,
  `m2_1` varchar(45) DEFAULT NULL,
  `m3_0` varchar(45) DEFAULT NULL,
  `m3_1` varchar(45) DEFAULT NULL,
  `m3_2` varchar(45) DEFAULT NULL,
  `m4_0` varchar(45) DEFAULT NULL,
  `m4_1` varchar(45) DEFAULT NULL,
  `m4_2` varchar(45) DEFAULT NULL,
  `m4_3` varchar(45) DEFAULT NULL,
  `m0_0` varchar(45) DEFAULT NULL,
  `m1_1` varchar(45) DEFAULT NULL,
  `m2_2` varchar(45) DEFAULT NULL,
  `m3_3` varchar(45) DEFAULT NULL,
  `m4_4` varchar(45) DEFAULT NULL,
  `insert_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `game_id` int(11) DEFAULT NULL,
  `order_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_bifen_index_game_id` (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9505 DEFAULT CHARSET=utf8mb4 COMMENT='比分指数';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bifen_index_std`
--

DROP TABLE IF EXISTS `bifen_index_std`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bifen_index_std` (
  `id` bigint(5) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL,
  `win_type` varchar(45) DEFAULT NULL,
  `m1_0` varchar(20) DEFAULT NULL,
  `m2_0` varchar(45) DEFAULT NULL,
  `m2_1` varchar(45) DEFAULT NULL,
  `m3_0` varchar(45) DEFAULT NULL,
  `m3_1` varchar(45) DEFAULT NULL,
  `m3_2` varchar(45) DEFAULT NULL,
  `m4_0` varchar(45) DEFAULT NULL,
  `m4_1` varchar(45) DEFAULT NULL,
  `m4_2` varchar(45) DEFAULT NULL,
  `m4_3` varchar(45) DEFAULT NULL,
  `m0_0` varchar(45) DEFAULT NULL,
  `m1_1` varchar(45) DEFAULT NULL,
  `m2_2` varchar(45) DEFAULT NULL,
  `m3_3` varchar(45) DEFAULT NULL,
  `m4_4` varchar(45) DEFAULT NULL,
  `insert_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `game_id` int(11) DEFAULT NULL,
  `order_num` int(11) DEFAULT '100',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `football_game_info`
--

DROP TABLE IF EXISTS `football_game_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `football_game_info` (
  `game_no` int(11) NOT NULL COMMENT '比赛编号',
  `game_week` varchar(50) DEFAULT NULL COMMENT '比赛场次',
  `start_datetime` datetime DEFAULT NULL COMMENT '开始时间',
  `team1_name` varchar(25) DEFAULT NULL COMMENT '队1',
  `team2_name` varchar(25) DEFAULT NULL COMMENT '队2',
  PRIMARY KEY (`game_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oupei_info`
--

DROP TABLE IF EXISTS `oupei_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oupei_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `orderNum` int(11) DEFAULT NULL,
  `pay_comp_name` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  `eu_win_num` float DEFAULT NULL,
  `eu_avg_num` float DEFAULT NULL,
  `eu_lost_num` float DEFAULT NULL,
  `get_datetime` datetime DEFAULT NULL COMMENT '网页上面数据的时间',
  `kelly_win_num` float DEFAULT NULL,
  `kelly_avg_num` float DEFAULT NULL,
  `kelly_lost_num` float DEFAULT NULL,
  `game_id` int(11) DEFAULT NULL,
  `insert_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=690 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oupei_startvalue_info`
--

DROP TABLE IF EXISTS `oupei_startvalue_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oupei_startvalue_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `oupei_startvalue_info` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  `get_datetime` datetime DEFAULT NULL COMMENT '网页上面数据的时间',
  `kelly_win_num` float DEFAULT NULL,
  `kelly_avg_num` float DEFAULT NULL,
  `kelly_lost_num` float DEFAULT NULL,
  `jishi_kelly_win_num` float DEFAULT NULL,
  `jishi_kelly_avg_num` float DEFAULT NULL,
  `jishi_kelly_lost_num` float DEFAULT NULL,
  `game_id` int(11) DEFAULT NULL,
  `insert_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=213 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pay_info`
--

DROP TABLE IF EXISTS `pay_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pay_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `orderNum` int(11) DEFAULT NULL,
  `pay_comp_name` varchar(50) DEFAULT NULL,
  `eu_win_num` float DEFAULT NULL,
  `eu_avg_num` float DEFAULT NULL,
  `eu_lost_num` float DEFAULT NULL,
  `get_datetime` datetime DEFAULT NULL COMMENT '网页上面数据的时间',
  `kelly_win_num` float DEFAULT NULL,
  `kelly_avg_num` float DEFAULT NULL,
  `kelly_lost_num` float DEFAULT NULL,
  `game_id` int(11) DEFAULT NULL,
  `insert_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=856 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rangqiu_startvalue_info`
--

DROP TABLE IF EXISTS `rangqiu_startvalue_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rangqiu_startvalue_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `oupei_startvalue_info` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  `get_datetime` datetime DEFAULT NULL COMMENT '网页上面数据的时间',
  `kelly_win_num` float DEFAULT NULL,
  `kelly_avg_num` float DEFAULT NULL,
  `kelly_lost_num` float DEFAULT NULL,
  `jishi_kelly_win_num` float DEFAULT NULL,
  `jishi_kelly_avg_num` float DEFAULT NULL,
  `jishi_kelly_lost_num` float DEFAULT NULL,
  `game_id` int(11) DEFAULT NULL,
  `insert_datetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=164 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-09 17:48:13
