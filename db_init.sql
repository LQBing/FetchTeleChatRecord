/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : parcelx_tel

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-06-14 23:55:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for add_users
-- ----------------------------
DROP TABLE IF EXISTS `add_users`;
CREATE TABLE `add_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(20) DEFAULT NULL,
  `channel_id` int(20) DEFAULT NULL,
  `inviter_id` int(20) DEFAULT NULL,
  `invitee_id` int(20) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `add_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2429 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for channels
-- ----------------------------
DROP TABLE IF EXISTS `channels`;
CREATE TABLE `channels` (
  `id` int(20) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `action` varchar(255) DEFAULT NULL,
  `inviter_id` int(20) DEFAULT NULL,
  `message_id` int(20) DEFAULT NULL,
  `message_type` varchar(255) DEFAULT NULL,
  `to_id` int(20) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `message` mediumtext,
  `out` bit(1) DEFAULT NULL,
  `mentioned` bit(1) DEFAULT NULL,
  `media_unread` bit(1) DEFAULT NULL,
  `silent` bit(1) DEFAULT NULL,
  `post` bit(1) DEFAULT NULL,
  `from_id` int(20) DEFAULT NULL,
  `fwd_from` datetime DEFAULT NULL,
  `via_bot_id` int(20) DEFAULT NULL,
  `reply_to_msg_id` int(20) DEFAULT NULL,
  `media` varchar(255) DEFAULT NULL,
  `reply_markup` varchar(255) DEFAULT NULL,
  `edit_date` datetime DEFAULT NULL,
  `post_author` varchar(255) DEFAULT NULL,
  `grouped_id` int(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3156 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(20) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
