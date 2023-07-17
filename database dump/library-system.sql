SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `book` (
  `bookid` int(11) NOT NULL,
  `name` text COLLATE utf8_unicode_ci NOT NULL,
  `picture` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `isbn` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `no_of_copy` int(5) NOT NULL,
  `status` enum('Enable','Disable') COLLATE utf8_unicode_ci NOT NULL,
  `added_on` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_on` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


INSERT INTO `book` (`bookid`, `name`, `picture`,  `isbn`, `no_of_copy`, `status`, `added_on`, `updated_on`) VALUES
(1, 'The Joy of PHP Programming', 'joy-php.jpg',  'B00BALXN70', 10, 'Enable', '2022-06-12 11:12:48', '2022-06-12 11:13:27'),
(2, 'Head First PHP &amp; MySQL', 'header-first-php.jpg', '0596006306', 10, 'Enable', '2022-06-12 11:16:01', '2022-06-12 11:16:01'),
(3, 'dsgsdgsd', '', 'sdfsd2334', 23, 'Enable', '2022-06-12 13:29:14', '2022-06-12 13:29:14'),
(9, 'bbbbbbbbbbbbbb', '', '4346436463463', 2, 'Enable', '2023-03-25 14:44:18', '2023-03-25 14:44:18');



CREATE TABLE `issued_book` (
  `issuebookid` int(11) NOT NULL,
  `bookid` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `issue_date_time` datetime NOT NULL DEFAULT current_timestamp(),
  `expected_return_date` datetime NOT NULL,
  `return_date_time` datetime NOT NULL,
  `status` enum('Issued','Returned','Not Return') COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `user` (
  `id` int(11) UNSIGNED NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(64) NOT NULL,
  `role` enum('admin','user') DEFAULT 'admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `user` (`id`, `first_name`, `last_name`, `email`, `password`, `role`) VALUES
(2, 'Mark', 'Wood', 'mark@webdamn.com', '123', 'user'),
(3, 'George', 'Smith', 'goerge@webdamn.com', '123', 'admin'),
(4, 'Adam', NULL, 'adam@webdamn.com', '123', 'admin'),
(6, 'aaa', 'bbbbb', 'ab@webdamn.com', '123', 'user'),
(7, NULL, 'ARUNACHALAM G', 'arunachalamgurusamy2002@gmail.com', '123', NULL);

ALTER TABLE `book`
  ADD PRIMARY KEY (`bookid`);

ALTER TABLE `issued_book`
  ADD PRIMARY KEY (`issuebookid`);

ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `book`
  MODIFY `bookid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE `issued_book`
  MODIFY `issuebookid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE `user`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;