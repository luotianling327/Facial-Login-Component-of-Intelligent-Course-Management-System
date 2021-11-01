-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facerecognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--
DROP TABLE IF EXISTS `Student`;

CREATE TABLE `Student` ( 
`student_id` INT NOT NULL , 
`name` VARCHAR(50) NOT NULL , 
`login_time` TIME NOT NULL , 
`login_date` DATE NOT NULL , 
`logout_time` TIME NOT NULL , 
`logout_date` DATE NOT NULL , 
`email` VARCHAR(50) NOT NULL , 
PRIMARY KEY (`student_id`)
) ENGINE = InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Student` WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
INSERT INTO `Student` VALUES (1, "Jack", NOW(), '2021-01-20', '14:24:25', '2021-01-18', "jack.goodboy3278@gmail.com"),
                             (2, "Amy", '14:24:19', '2021-01-19', '14:27:15', '2021-01-19', "amy@hku.hk"),
                             (3, "Tom", '15:24:36', '2021-01-18', '17:24:47', '2021-01-18', "tom@hku.hk"),
                             (4, "Kate", '16:24:08', '2021-01-03', '14:24:19', '2021-01-05', "kate@hku.hk"),
                             (5, "Kim", '17:24:44', '2021-01-16', '19:24:08', '2021-01-16', "kim@hku.hk"),
                             (6, "Rose", '18:24:12', '2021-01-18', '21:24:01', '2021-01-18', "rose@hku.hk"),
                             (7, "Lucy", '19:24:27', '2021-01-14', '19:30:37', '2021-01-14', "lucy@hku.hk"),
                             (8, "Lily", '20:21:30', '2021-01-15', '20:36:29', '2021-01-15', "lily@hku.hk");
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;

ALTER TABLE Student ADD duration TIME NULL;

-- Table structure for table `Course`
--
DROP TABLE IF EXISTS `Course`;

CREATE TABLE `Course` ( 
`course_id` INT NOT NULL , 
`course_name` VARCHAR(50) NOT NULL , 
`instructor` VARCHAR(50) NOT NULL , 
`teacher_message` VARCHAR(200) NOT NULL , 
PRIMARY KEY (`course_id`)
) ENGINE = InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Course` VALUES (1, "Computer Programming", 'Ting', "Please bring your laptop and mute your phone."),
                            (2, "Chemistry I", 'Ng', "Be safe in lab."),
                            (3, "Calculus", 'Chan', "Mathematics is the music of reason."),
                            (4, "Corporate Finance", 'Lin', "Do not sleep in class."),
                            (5, "Scientific Computing", 'Zhang', "Science is romantic."),
                            (6, "Computer Vision", 'Roosevelt', "Good luck with your work!");

-- Table structure for table `Classroom`
--
DROP TABLE IF EXISTS `Classroom`;

CREATE TABLE `Classroom` (
`classroom_id` INT NOT NULL , 
`classroom_address` VARCHAR(200) NOT NULL , 
PRIMARY KEY (`classroom_id`)
) ENGINE = InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Classroom` VALUES (1, "CPD-LG.07"),
                               (2, "CYCP1"),
                               (3, "KB223"),
                               (4, "KK102"),
                               (5, "MB217"),
                               (6, "LE1");


-- Table structure for table `Class`
--
DROP TABLE IF EXISTS `Class`;

CREATE TABLE `Class` ( 
`course_id` INT NOT NULL , 
`class_id` INT NOT NULL , 
`type` VARCHAR(20) NOT NULL, 
`class_start_time` TIME NOT NULL , 
`class_end_time` TIME NOT NULL , 
`class_date` DATE NOT NULL , 
`classroom_id` INT NOT NULL , 
`zoom_links` VARCHAR(200) NOT NULL , 
`material_links` VARCHAR(200) NOT NULL , 
PRIMARY KEY (`course_id`, `type`,`class_id`),
FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
) ENGINE = InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `Class` VALUES (1, 1, "Lecture", "09:30:00", "12:20:00", "2021-04-05", 1, "https://hku.zoom.us/j/97686555806
", "https://moodle.hku.hk" ),
                           (1, 2, "Lecture", "09:30:00", "12:20:00", "2021-04-19", 1, "https://hku.zoom.us/j/97686555806", "https://moodle.hku.hk" ),
                           (1, 3, "Lecture", "09:30:00", "12:20:00", "2021-05-03", 1, "https://hku.zoom.us/j/97686555806", "https://moodle.hku.hk" ),
                           (2, 1, "Lecture", "13:30:00", "16:20:00", "2021-04-05", 2, "https://hku.zoom.us/j/318659018", "https://moodle.hku.hk" ),
                           (2, 2, "Lecture", "13:30:00", "16:20:00", "2021-04-19", 2, "https://hku.zoom.us/j/318659018", "https://moodle.hku.hk" ),
                           (2, 3, "Lecture", "13:30:00", "16:20:00", "2021-05-03", 2, "https://hku.zoom.us/j/318659018", "https://moodle.hku.hk" ),
                           (3, 1, "Lecture", "09:30:00", "12:20:00", "2021-04-06", 3, "https://hku.zoom.us/j/95182028750", "https://moodle.hku.hk" ),
                           (3, 2, "Lecture", "09:30:00", "12:20:00", "2021-04-20", 3, "https://hku.zoom.us/j/95182028750", "https://moodle.hku.hk" ),
                           (3, 3, "Lecture", "09:30:00", "12:20:00", "2021-05-04", 3, "https://hku.zoom.us/j/95182028750", "https://moodle.hku.hk" ),
                           (4, 1, "Lecture", "13:30:00", "16:20:00", "2021-04-06", 4, "https://hku.zoom.us/j/36654613424", "https://moodle.hku.hk" ),
                           (4, 2, "Lecture", "13:30:00", "16:20:00", "2021-04-20", 4, "https://hku.zoom.us/j/36654613424", "https://moodle.hku.hk" ),
                           (4, 3, "Lecture", "13:30:00", "16:20:00", "2021-05-04", 4, "https://hku.zoom.us/j/36654613424", "https://moodle.hku.hk" ),
                           (5, 1, "Lecture", "09:30:00", "12:20:00", "2021-04-07", 5, "https://hku.zoom.us/j/93323402272", "https://moodle.hku.hk" ),
                           (5, 2, "Lecture", "09:30:00", "12:20:00", "2021-04-21", 5, "https://hku.zoom.us/j/93323402272", "https://moodle.hku.hk" ),
                           (5, 3, "Lecture", "09:30:00", "12:20:00", "2021-05-05", 5, "https://hku.zoom.us/j/93323402272", "https://moodle.hku.hk" ),
                           (6, 1, "Lecture", "13:30:00", "16:20:00", "2021-04-07", 6, "https://hku.zoom.us/j/94456098236", "https://moodle.hku.hk" ),
                           (6, 2, "Lecture", "13:30:00", "16:20:00", "2021-04-21", 6, "https://hku.zoom.us/j/94456098236", "https://moodle.hku.hk" ),
                           (6, 3, "Lecture", "13:30:00", "16:20:00", "2021-05-05", 6, "https://hku.zoom.us/j/94456098236", "https://moodle.hku.hk" );


INSERT INTO `Class` VALUES (1, 1, "Tutorial", "12:30:00", "13:20:00", "2021-04-07", 1, "https://hku.zoom.com.cn/j/2640918958", "https://moodle.hku.hk" ),
                           (1, 2, "Tutorial", "12:30:00", "13:20:00", "2021-04-21", 1, "https://hku.zoom.com.cn/j/2640918958", "https://moodle.hku.hk" ),
                           (1, 3, "Tutorial", "12:30:00", "13:20:00", "2021-05-05", 1, "https://hku.zoom.com.cn/j/2640918958", "https://moodle.hku.hk" ),
                           (2, 1, "Tutorial", "16:30:00", "17:20:00", "2021-04-07", 2, "https://hku.zoom.us/j/318659019", "https://moodle.hku.hk" ),
                           (2, 2, "Tutorial", "16:30:00", "17:20:00", "2021-04-21", 2, "https://hku.zoom.us/j/318659019", "https://moodle.hku.hk" ),
                           (2, 3, "Tutorial", "16:30:00", "17:20:00", "2021-05-05", 2, "https://hku.zoom.us/j/318659019", "https://moodle.hku.hk" ),
                           (3, 1, "Tutorial", "12:30:00", "13:20:00", "2021-04-08", 3, "https://hku.zoom.us/j/95182028751", "https://moodle.hku.hk" ),
                           (3, 2, "Tutorial", "12:30:00", "13:20:00", "2021-04-22", 3, "https://hku.zoom.us/j/95182028751", "https://moodle.hku.hk" ),
                           (3, 3, "Tutorial", "12:30:00", "13:20:00", "2021-05-06", 3, "https://hku.zoom.us/j/95182028751", "https://moodle.hku.hk" ),
                           (4, 1, "Tutorial", "16:30:00", "17:20:00", "2021-04-08", 4, "https://hku.zoom.us/j/96654613425", "https://moodle.hku.hk" ),
                           (4, 2, "Tutorial", "16:30:00", "17:20:00", "2021-04-22", 4, "https://hku.zoom.us/j/96654613425", "https://moodle.hku.hk" ),
                           (4, 3, "Tutorial", "16:30:00", "17:20:00", "2021-05-06", 4, "https://hku.zoom.us/j/96654613425", "https://moodle.hku.hk" ),
                           (5, 1, "Tutorial", "12:30:00", "13:20:00", "2021-04-09", 5, "https://hku.zoom.us/j/93323413472", "https://moodle.hku.hk" ),
                           (5, 2, "Tutorial", "12:30:00", "13:20:00", "2021-04-23", 5, "https://hku.zoom.us/j/93323413472", "https://moodle.hku.hk" ),
                           (5, 3, "Tutorial", "12:30:00", "13:20:00", "2021-05-07", 5, "https://hku.zoom.us/j/93323413472", "https://moodle.hku.hk" ),
                           (6, 1, "Tutorial", "16:30:00", "17:20:00", "2021-04-09", 6, "https://hku.zoom.us/j/95256098236", "https://moodle.hku.hk" ),
                           (6, 2, "Tutorial", "16:30:00", "17:20:00", "2021-04-23", 6, "https://hku.zoom.us/j/95256098236", "https://moodle.hku.hk" ),
                           (6, 3, "Tutorial", "16:30:00", "17:20:00", "2021-05-07", 6, "https://hku.zoom.us/j/95256098236", "https://moodle.hku.hk" );

-- Table structure for table `Takes`
--
DROP TABLE IF EXISTS `Takes`;

CREATE TABLE `Takes` ( 
`student_id` INT NOT NULL , 
`course_id` INT NOT NULL , 
PRIMARY KEY (`student_id`, `course_id`),
FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`),
FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
) ENGINE = InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Takes` VALUES (1, 1), (1, 3), (1, 6),
                           (2, 1), (2, 4), (2, 5),
                           (3, 2), (3, 3), (3, 6),
                           (4, 3), (4, 4), (4, 5),
                           (5, 1), (5, 2), (5, 3),
                           (6, 4), (6, 5), (6, 6),
                           (7, 1), (7, 3), (7, 4),
                           (8, 3), (8, 5), (8, 6);
     

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


