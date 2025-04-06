drop database OnlineRecord;
create database if not exists OnlineRecord;
use OnlineRecord;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for Problem
-- ----------------------------
DROP TABLE IF EXISTS `Problem`;
CREATE TABLE `Problem`  (
  `id` int NOT NULL COMMENT '题目id',
  `problem_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '题目名',
  `link` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '题目链接',
  `create_time` datetime NULL DEFAULT NULL COMMENT '题目创建时间',
  `difficulty` int NULL DEFAULT NULL COMMENT '0-简单,1-中等,2-困难',
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `set_id` int NULL DEFAULT NULL COMMENT '题单id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_link`(`user_id` ASC, `set_id` ASC, `link` ASC) USING BTREE COMMENT '一个用户的一个表中每个题目链接只能添加一次'
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ProblemSet
-- ----------------------------
DROP TABLE IF EXISTS `ProblemSet`;
CREATE TABLE `ProblemSet`  (
  `id` int NOT NULL COMMENT '题目id',
  `set_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '题目名',
  `creat_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '题目描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for User
-- ----------------------------
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User`  (
  `id` int NOT NULL COMMENT '用户id',
  `account` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '账号',
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '密码',
  `username` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `creat_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for userProblemStatus
-- ----------------------------
DROP TABLE IF EXISTS `userProblemStatus`;
CREATE TABLE `userProblemStatus`  (
  `id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `problem_id` int NULL DEFAULT NULL COMMENT '题目id',
  `status` int NULL DEFAULT NULL COMMENT '0未完成，1完成',
  `time_spend` int NULL DEFAULT NULL COMMENT '所用时间(s)',
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '描述',
  `image` longblob NULL COMMENT '图片',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `unique_user_problem`(`user_id` ASC, `problem_id` ASC) USING BTREE COMMENT '记录每个人题目的状态'
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for userSubscription
-- ----------------------------
DROP TABLE IF EXISTS `userSubscription`;
CREATE TABLE `userSubscription`  (
  `id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `set_id` int NULL DEFAULT NULL COMMENT '题单id',
  `authority` int NULL DEFAULT NULL COMMENT '用户是否可以修改题单，0不能修改，1可以修改',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_user_set`(`user_id` ASC, `set_id` ASC) USING BTREE COMMENT '一个题单对应一个人'
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
