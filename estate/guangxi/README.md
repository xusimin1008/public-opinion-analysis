# 


## 库表结构

create database public_opinion;


```
CREATE TABLE `corpus` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(200) NOT NULL DEFAULT '',
  `website` varchar(16) DEFAULT NULL,
  `location` varchar(16) DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `html` mediumtext,
  `content` mediumtext,
  `word_freq` mediumtext,
  `topic` bigint(20) DEFAULT NULL,
  `status` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `url_index` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```