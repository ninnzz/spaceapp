
CREATE TABLE `album_user_ratings` (
    `album_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `rating` int(1) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `album_id_user_id` UNIQUE (`album_id`, `user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `albums` (
    `album_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `cover` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `rating` float(2,1) COLLATE utf8mb4_unicode_ci,
    `artist_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`album_id`),
    CONSTRAINT `name_artist_id` UNIQUE (`name`, `artist_id`),
    KEY index1 (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `applications` (
    `application_id` MEDIUMINT COLLATE utf8mb4_unicode_ci NOT NULL AUTO_INCREMENT,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `contract_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `agree_on_contract` varchar(4) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'yes',
    `source` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_applied` datetime,
    `date_approved` datetime,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`application_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `artist_user_ratings` (
    `artist_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `rating` int(1) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `artist_id_user_id` UNIQUE (`artist_id`, `user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `artists` (
    `artist_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `picture` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `rating` float(2,1) COLLATE utf8mb4_unicode_ci,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT 'e0c7b640-3bf7-4570-8137-8ee32892c417',
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `genre` varchar(512) COLLATE utf8mb4_unicode_ci,
    `original_music` varchar(16) COLLATE utf8mb4_unicode_ci,
    `music_location` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`artist_id`),
    UNIQUE (`name`),
    KEY index1 (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `backup_table` (
    `id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `table_name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `data` text(10000000) COLLATE utf8mb4_unicode_ci NOT NULL,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `claims` (
    `claim_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `asset_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `video_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `video_views` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT '0',
    `video_title` varchar(256) COLLATE utf8mb4_unicode_ci,
    `status` varchar(256) COLLATE utf8mb4_unicode_ci,
    `content_type` varchar(256) COLLATE utf8mb4_unicode_ci,
    `origin_source` varchar(256) COLLATE utf8mb4_unicode_ci,
    `released` tinyint(1) COLLATE utf8mb4_unicode_ci,
    `partner_uploaded` tinyint(1) COLLATE utf8mb4_unicode_ci,
    `time_created` datetime NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`claim_id`),
    KEY `video_id` (`video_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `contracts` (
    `contract_id` MEDIUMINT COLLATE utf8mb4_unicode_ci NOT NULL AUTO_INCREMENT,
    `name` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `type` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'artist_contract',
    `version` int(4) COLLATE utf8mb4_unicode_ci NOT NULL,
    `file` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `date_effective` datetime NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`contract_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `composition` (
    `id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `custom_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `asset_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `related_isrc` varchar(256) COLLATE utf8mb4_unicode_ci,
    `related_asset_id` varchar(256) COLLATE utf8mb4_unicode_ci,
    `iswc` varchar(16) COLLATE utf8mb4_unicode_ci,
    `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `add_asset_labels` varchar(512) COLLATE utf8mb4_unicode_ci,
    `hfa_song_code` varchar(8) COLLATE utf8mb4_unicode_ci,
    `writers` varchar(512) COLLATE utf8mb4_unicode_ci,
    `match_policy` varchar(256) COLLATE utf8mb4_unicode_ci,
    `publisher_name` varchar(256) COLLATE utf8mb4_unicode_ci,
    `sync_ownership_share` float(10) COLLATE utf8mb4_unicode_ci,
    `sync_ownership_territory` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `sync_ownership_restriction` enum('include', 'exclude') COLLATE utf8mb4_unicode_ci DEFAULT 'exclude',
    `mechanical_ownership_share` float(10) COLLATE utf8mb4_unicode_ci,
    `mechanical_ownership_territory` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `mechanical_ownership_restriction` enum('include', 'exclude') COLLATE utf8mb4_unicode_ci DEFAULT 'exclude',
    `performance_ownership_share` float(10) COLLATE utf8mb4_unicode_ci,
    `performance_ownership_territory` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `performance_ownership_restriction` enum('include', 'exclude') COLLATE utf8mb4_unicode_ci DEFAULT 'exclude',
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `disputes` (
    `claim_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `asset_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `video_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `video_views` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT '0',
    `video_title` varchar(256) COLLATE utf8mb4_unicode_ci,
    `channel_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `status` varchar(256) COLLATE utf8mb4_unicode_ci,
    `content_type` varchar(256) COLLATE utf8mb4_unicode_ci,
    `origin_source` varchar(256) COLLATE utf8mb4_unicode_ci,
    `reason` varchar(256) COLLATE utf8mb4_unicode_ci,
    `note` varchar(512) COLLATE utf8mb4_unicode_ci,
    `notified` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT '0',
    `partner_uploaded` tinyint(1) COLLATE utf8mb4_unicode_ci,
    `dispute_date` timestamp NULL,
    `expiration` timestamp NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`claim_id`),
    KEY `video_id` (`video_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `dispute_actions` (
    `id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `claim_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `asset_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `video_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `channel_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `action` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `done` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `flagged_tracks` (
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `genre` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `mood` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `instrument` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `lyrics` text(1000000) COLLATE utf8mb4_unicode_ci,
    `country` varchar(256) COLLATE utf8mb4_unicode_ci,
    `filename` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `file_path` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `source` varchar(256) COLLATE utf8mb4_unicode_ci,
    `length` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
    `rating` float(2,1) COLLATE utf8mb4_unicode_ci,
    `date` varchar(64) COLLATE utf8mb4_unicode_ci,
    `artist_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `album_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `status` enum('private', 'public') COLLATE utf8mb4_unicode_ci DEFAULT 'public',
    `asset_id` varchar(32) COLLATE utf8mb4_unicode_ci,
    `is_uploadedS3` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `is_uploadedYT` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `date_uploadedS3` datetime,
    `date_uploadedYT` datetime,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`track_id`),
    KEY index1 (`title`),
    KEY index2 (`genre`),
    KEY index3 (`mood`),
    KEY index4 (`instrument`),
    KEY index5 (`country`),
    KEY index6 (`asset_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `genres` (
    `genre_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `cover` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`genre_id`),
    UNIQUE (`name`),
    KEY index1 (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `instruments` (
    `instrument_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`instrument_id`),
    UNIQUE (`name`),
    KEY index1 (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `moods` (
    `mood_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`mood_id`),
    UNIQUE (`name`),
    KEY index1 (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `music_assets` (
    `asset_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
    `asset_type` varchar(64) COLLATE utf8mb4_unicode_ci,
    `status` varchar(32) COLLATE utf8mb4_unicode_ci,
    `metadata_origination` varchar(64) COLLATE utf8mb4_unicode_ci,
    `custom_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `freedom_user_id` bigint(20) COLLATE utf8mb4_unicode_ci,
    `isrc` varchar(64) COLLATE utf8mb4_unicode_ci,
    `grid` varchar(64) COLLATE utf8mb4_unicode_ci,
    `upc` varchar(64) COLLATE utf8mb4_unicode_ci,
    `artist` varchar(256) COLLATE utf8mb4_unicode_ci,
    `song` varchar(256) COLLATE utf8mb4_unicode_ci,
    `album` varchar(256) COLLATE utf8mb4_unicode_ci,
    `label` varchar(256) COLLATE utf8mb4_unicode_ci,
    `constituent_asset_ids` varchar(256) COLLATE utf8mb4_unicode_ci,
    `active_reference_ids` varchar(256) COLLATE utf8mb4_unicode_ci,
    `inactive_reference_ids` varchar(256) COLLATE utf8mb4_unicode_ci,
    `match_policy` varchar(256) COLLATE utf8mb4_unicode_ci,
    `is_merged_asset` varchar(16) COLLATE utf8mb4_unicode_ci,
    `ownership` varchar(256) COLLATE utf8mb4_unicode_ci,
    `conflicting_territories` varchar(256) COLLATE utf8mb4_unicode_ci,
    `comp_publishing_cleard` varchar(16) COLLATE utf8mb4_unicode_ci,
    `comp_100_ownership` varchar(16) COLLATE utf8mb4_unicode_ci,
    `embedded_asset_ids` varchar(256) COLLATE utf8mb4_unicode_ci,
    `asset_labels` varchar(256) COLLATE utf8mb4_unicode_ci,
    `recent_daily_average` float(10) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `edit_status` enum('unverified', 'verified') COLLATE utf8mb4_unicode_ci,
    `auto_release` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 1,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`asset_id`),
    KEY index1 (`asset_id`),
    KEY index2 (`asset_type`),
    KEY index3 (`status`),
    KEY index4 (`custom_id`),
    KEY index5 (`isrc`),
    KEY index6 (`song`),
    KEY index7 (`artist`),
    KEY index8 (`album`),
    KEY index9 (`label`),
    KEY index10 (`freedom_user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `music_provider_owners_managers` (
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `role` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    CONSTRAINT `user_id_music_provider_id` UNIQUE (`user_id`, `music_provider_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `music_providers` (
    `id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `description` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `logo` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `banner` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `website` varchar(256) COLLATE utf8mb4_unicode_ci,
    `email` varchar(256) COLLATE utf8mb4_unicode_ci,
    `contact_numbers` varchar(256) COLLATE utf8mb4_unicode_ci,
    `url` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `session` (
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `mida` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    CONSTRAINT `user_id_mida` UNIQUE (`user_id`, `mida`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `sound_recording` (
    `id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `filename` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `custom_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `asset_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `isrc` varchar(16) COLLATE utf8mb4_unicode_ci,
    `add_asset_labels` varchar(512) COLLATE utf8mb4_unicode_ci,
    `upc` varchar(64) COLLATE utf8mb4_unicode_ci,
    `grid` varchar(32) COLLATE utf8mb4_unicode_ci,
    `song_title` varchar(256) COLLATE utf8mb4_unicode_ci,
    `artist` varchar(256) COLLATE utf8mb4_unicode_ci,
    `album` varchar(256) COLLATE utf8mb4_unicode_ci,
    `genre` varchar(256) COLLATE utf8mb4_unicode_ci,
    `label` varchar(256) COLLATE utf8mb4_unicode_ci,
    `original_release_date` varchar(16) COLLATE utf8mb4_unicode_ci,
    `ownership` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `match_policy` varchar(256) COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `tags` (
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `tag` varchar(140) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `track_id_tag` UNIQUE (`track_id`, `tag`),
    KEY index1 (`tag`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `track_genre_play` (
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `genre` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `track_upload_to_youtube_requests` (
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `genre` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `mood` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `instrument` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `lyrics` text(1000000) COLLATE utf8mb4_unicode_ci,
    `country` varchar(256) COLLATE utf8mb4_unicode_ci,
    `filename` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `file_path` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `source` varchar(256) COLLATE utf8mb4_unicode_ci,
    `length` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
    `rating` float(2,1) COLLATE utf8mb4_unicode_ci,
    `date` varchar(64) COLLATE utf8mb4_unicode_ci,
    `artist_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `album_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `status` enum('private', 'public') COLLATE utf8mb4_unicode_ci DEFAULT 'public',
    `asset_id` varchar(32) COLLATE utf8mb4_unicode_ci,
    `is_uploadedS3` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `is_uploadedYT` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `date_uploadedS3` datetime,
    `date_uploadedYT` datetime,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`track_id`),
    KEY index1 (`title`),
    KEY index2 (`genre`),
    KEY index3 (`mood`),
    KEY index4 (`instrument`),
    KEY index5 (`country`),
    KEY index6 (`asset_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `track_user_download` (
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `track_user_play` (
    `id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `length` varchar(10) COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `track_user_ratings` (
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `rating` int(1) COLLATE utf8mb4_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `track_id_user_id` UNIQUE (`track_id`, `user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `tracks` (
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `genre` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `mood` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `instrument` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `lyrics` text(1000000) COLLATE utf8mb4_unicode_ci,
    `country` varchar(256) COLLATE utf8mb4_unicode_ci,
    `filename` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `file_path` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `source` varchar(256) COLLATE utf8mb4_unicode_ci,
    `length` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
    `rating` float(2,1) COLLATE utf8mb4_unicode_ci,
    `date` varchar(64) COLLATE utf8mb4_unicode_ci,
    `artist_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `album_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `status` enum('private', 'public') COLLATE utf8mb4_unicode_ci DEFAULT 'public',
    `asset_id` varchar(32) COLLATE utf8mb4_unicode_ci,
    `is_uploadedS3` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `is_uploadedYT` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `date_uploadedS3` datetime,
    `date_uploadedYT` datetime,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`track_id`),
    KEY index1 (`title`),
    KEY index2 (`genre`),
    KEY index3 (`mood`),
    KEY index4 (`instrument`),
    KEY index5 (`country`),
    KEY index6 (`asset_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `upload_status` (
    `upload_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `track_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `progress` int(3) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `uploaded` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `failed` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `error_message` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `destination` enum('tunes', 'youtube') COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`upload_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user_invites` (
    `invite_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `email` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `role` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `music_provider_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `artist_id` varchar(64) COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`invite_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user_preferences` (
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `genre` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `mood` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `instrument` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user_scopes` (
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `scope` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    CONSTRAINT `user_id_scope` UNIQUE (`user_id`, `scope`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `users` (
    `user_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `email` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name` varchar(256) COLLATE utf8mb4_unicode_ci,
    `active` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT 1,
    `rank` int(11) COLLATE utf8mb4_unicode_ci DEFAULT 0,
    `role` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `picture` varchar(1024) COLLATE utf8mb4_unicode_ci,
    `skype` varchar(256) COLLATE utf8mb4_unicode_ci,
    `application_status` ENUM('accepted', 'applied') COLLATE utf8mb4_unicode_ci,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
