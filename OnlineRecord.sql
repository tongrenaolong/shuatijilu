/*
 Navicat Premium Data Transfer

 Source Server         : 云服务器
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41-0ubuntu0.22.04.1)
 Source Host           : 47.94.156.51:3306
 Source Schema         : OnlineRecordTest

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41-0ubuntu0.22.04.1)
 File Encoding         : 65001

 Date: 13/04/2025 19:56:18
*/
DROP database IF EXISTS OnlineRecord;
User OnlineRecord;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for Problem
-- ----------------------------
DROP TABLE IF EXISTS `Problem`;
CREATE TABLE `Problem`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '题目id',
  `problem_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '题目名',
  `link` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '题目链接',
  `create_time` datetime NULL DEFAULT NULL COMMENT '题目创建时间',
  `difficulty` int NULL DEFAULT NULL COMMENT '0-简单,1-中等,2-困难',
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `set_id` int NULL DEFAULT NULL COMMENT '题单id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_link`(`user_id` ASC, `set_id` ASC, `link` ASC) USING BTREE COMMENT '一个用户的一个表中每个题目链接只能添加一次'
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Problem
-- ----------------------------
INSERT INTO `Problem` VALUES (10, 'test1', 'test1', '2025-04-12 22:47:42', 0, 2, 2);
INSERT INTO `Problem` VALUES (17, 'LCP 29. 乐团站位 - 力扣（LeetCode）', 'https://leetcode.cn/problems/SNJvJP/', '2025-04-13 17:46:17', 1, 2, 2);
INSERT INTO `Problem` VALUES (18, '51. N 皇后 - 力扣（LeetCode）', 'https://leetcode.cn/problems/n-queens/description/', '2025-04-13 17:46:17', 2, 2, 2);

-- ----------------------------
-- Table structure for ProblemSet
-- ----------------------------
DROP TABLE IF EXISTS `ProblemSet`;
CREATE TABLE `ProblemSet`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '题目id',
  `set_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '题目名',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '题目描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ProblemSet
-- ----------------------------
INSERT INTO `ProblemSet` VALUES (2, 'set1', '2025-04-12 21:57:09', 'asdf');

-- ----------------------------
-- Table structure for SendEmailLog
-- ----------------------------
DROP TABLE IF EXISTS `SendEmailLog`;
CREATE TABLE `SendEmailLog`  (
  `id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `email` int NULL DEFAULT NULL,
  `update_time` int NULL DEFAULT NULL COMMENT '操作的日期',
  `status` int NULL DEFAULT NULL COMMENT '0-未发送，1-发送成功，2-发送失败',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '发送邮件日志' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of SendEmailLog
-- ----------------------------

-- ----------------------------
-- Table structure for User
-- ----------------------------
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `account` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '账号',
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '密码',
  `username` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `email` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `User_email_uindex`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of User
-- ----------------------------
INSERT INTO `User` VALUES (1, '3300763927@qq.com', '9ffcf5941848d931607aeadd0ec51a3f', 'infinity', '3300763927@qq.com', '2025-04-08 08:05:52');
INSERT INTO `User` VALUES (2, 'yao', '912ec803b2ce49e4a541068d495ab570', 'yao', '18706838263@163.com', '2025-04-10 09:22:33');

-- ----------------------------
-- Table structure for UserOperationLog
-- ----------------------------
DROP TABLE IF EXISTS `UserOperationLog`;
CREATE TABLE `UserOperationLog`  (
  `id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `user_permission` int NULL DEFAULT NULL COMMENT '标记用户等级，0-普通用户，1-系统管理员',
  `ip` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `url` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `method` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `user_agent` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ip`(`ip` ASC) USING BTREE,
  INDEX `method`(`method` ASC) USING BTREE,
  INDEX `url`(`url` ASC) USING BTREE,
  INDEX `user_agent`(`user_agent` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `user_permission`(`user_permission` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '用户操作记录日志' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of UserOperationLog
-- ----------------------------

-- ----------------------------
-- Table structure for UserProblem
-- ----------------------------
DROP TABLE IF EXISTS `UserProblem`;
CREATE TABLE `UserProblem`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `set_id` int NULL DEFAULT NULL,
  `problem_id` int NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL COMMENT '最近一次完成时间',
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `status` int NULL DEFAULT NULL COMMENT '0-未完成，1-完成',
  `image` longblob NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `problem_id`(`problem_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `set_id`(`set_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '用户对应题目的完成情况' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of UserProblem
-- ----------------------------
INSERT INTO `UserProblem` VALUES (1, 2, 2, 10, '2025-04-13 17:32:09', '示音地话各业真现。是必方消身。等布有商先半难严原。实又更比适本组分。根其地。化才段。', 1, NULL);
INSERT INTO `UserProblem` VALUES (2, 2, 2, 17, '2025-04-13 17:46:17', NULL, 0, NULL);
INSERT INTO `UserProblem` VALUES (3, 2, 2, 18, '2025-04-13 17:46:17', NULL, 0, NULL);

-- ----------------------------
-- Table structure for UserProblemLog
-- ----------------------------
DROP TABLE IF EXISTS `UserProblemLog`;
CREATE TABLE `UserProblemLog`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `set_id` int NULL DEFAULT NULL,
  `problem_id` int NULL DEFAULT NULL COMMENT '题目id',
  `status` int NULL DEFAULT NULL COMMENT '0未完成，1完成',
  `update_time` datetime NULL DEFAULT NULL COMMENT '打卡时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `unique_user_problem`(`user_id` ASC, `problem_id` ASC) USING BTREE COMMENT '记录每个人题目的状态',
  INDEX `user_id`(`user_id` ASC) USING BTREE COMMENT '用户id',
  INDEX `problem_id`(`problem_id` ASC) USING BTREE COMMENT '题目id',
  INDEX `update_time`(`update_time` ASC) USING BTREE COMMENT '打卡时间',
  INDEX `set_id`(`set_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '记录用户对应的题目完成日志' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of UserProblemLog
-- ----------------------------
INSERT INTO `UserProblemLog` VALUES (1, 2, 2, 10, 1, '2025-04-12 23:02:08');
INSERT INTO `UserProblemLog` VALUES (3, 2, 2, 10, 1, '2025-04-13 17:32:09');

-- ----------------------------
-- Table structure for UserProblemSetLog
-- ----------------------------
DROP TABLE IF EXISTS `UserProblemSetLog`;
CREATE TABLE `UserProblemSetLog`  (
  `id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `set_id` int NULL DEFAULT NULL,
  `op_type` tinyint NULL DEFAULT NULL COMMENT '操作类型，1-创建题单，2-加入题单，3-退出题单，4-添加题目，5-删除题目，0-删除题单',
  `problem_id` int NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `set_id`(`set_id` ASC) USING BTREE,
  INDEX `op_type`(`op_type` ASC) USING BTREE,
  INDEX `problem_id`(`problem_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of UserProblemSetLog
-- ----------------------------

-- ----------------------------
-- Table structure for UserSubscription
-- ----------------------------
DROP TABLE IF EXISTS `UserSubscription`;
CREATE TABLE `UserSubscription`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `set_id` int NULL DEFAULT NULL COMMENT '题单id',
  `authority` int NULL DEFAULT NULL COMMENT '用户是否可以修改题单，0不能修改，1可以修改',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_user_set`(`user_id` ASC, `set_id` ASC) USING BTREE COMMENT '一个题单对应一个人'
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of UserSubscription
-- ----------------------------
INSERT INTO `UserSubscription` VALUES (4, 2, 2, 1);

SET FOREIGN_KEY_CHECKS = 1;
