-- HUMISENSE Database Schema for MySQL
-- Run this in phpMyAdmin to create all database tables

-- =====================================================
-- Table: admins
-- =====================================================
CREATE TABLE IF NOT EXISTS `admins` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(80) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `email` VARCHAR(120),
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `last_login` DATETIME,
    INDEX `ix_admins_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: users
-- =====================================================
CREATE TABLE IF NOT EXISTS `users` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `company` VARCHAR(100),
    `phone` VARCHAR(20),
    `message` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `is_subscribed` BOOLEAN DEFAULT TRUE,
    INDEX `ix_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: contacts
-- =====================================================
CREATE TABLE IF NOT EXISTS `contacts` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(120) NOT NULL,
    `phone` VARCHAR(20),
    `company` VARCHAR(100),
    `subject` VARCHAR(200),
    `message` TEXT NOT NULL,
    `status` VARCHAR(20) DEFAULT 'new',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: newsletter
-- =====================================================
CREATE TABLE IF NOT EXISTS `newsletter` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `subscribed_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `is_active` BOOLEAN DEFAULT TRUE,
    INDEX `ix_newsletter_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: course_enrollments
-- =====================================================
CREATE TABLE IF NOT EXISTS `course_enrollments` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(120) NOT NULL,
    `course_id` VARCHAR(50) NOT NULL,
    `phone` VARCHAR(20),
    `company` VARCHAR(100),
    `experience_level` VARCHAR(50),
    `goals` TEXT,
    `status` VARCHAR(20) DEFAULT 'pending',
    `enrolled_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: research_submissions
-- =====================================================
CREATE TABLE IF NOT EXISTS `research_submissions` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(300) NOT NULL,
    `authors` TEXT NOT NULL,
    `email` VARCHAR(120) NOT NULL,
    `institution` VARCHAR(200),
    `research_area` VARCHAR(100),
    `abstract` TEXT NOT NULL,
    `keywords` VARCHAR(500),
    `status` VARCHAR(20) DEFAULT 'submitted',
    `submitted_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: masterclasses
-- =====================================================
CREATE TABLE IF NOT EXISTS `masterclasses` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `slug` VARCHAR(220) NOT NULL UNIQUE,
    `short_description` VARCHAR(500),
    `detailed_description` TEXT,
    `banner_image` VARCHAR(500),
    `thumbnail` VARCHAR(500),
    `featured_image` VARCHAR(500),
    `date` DATE NOT NULL,
    `time` TIME NOT NULL,
    `timezone` VARCHAR(50) DEFAULT 'UTC',
    `duration` INTEGER DEFAULT 60,
    `registration_opens` DATETIME,
    `registration_closes` DATETIME,
    `instructor_name` VARCHAR(100),
    `instructor_photo` VARCHAR(500),
    `instructor_designation` VARCHAR(100),
    `instructor_company` VARCHAR(100),
    `instructor_bio` TEXT,
    `instructor_linkedin` VARCHAR(500),
    `instructor_twitter` VARCHAR(500),
    `instructor_website` VARCHAR(500),
    `max_seats` INTEGER DEFAULT 500,
    `status` VARCHAR(20) DEFAULT 'draft',
    `is_featured` BOOLEAN DEFAULT FALSE,
    `show_floating_button` BOOLEAN DEFAULT TRUE,
    `show_popup` BOOLEAN DEFAULT FALSE,
    `show_sticky_banner` BOOLEAN DEFAULT FALSE,
    `show_homepage_promotion` BOOLEAN DEFAULT FALSE,
    `meta_title` VARCHAR(200),
    `meta_description` VARCHAR(500),
    `meta_keywords` VARCHAR(500),
    `og_image` VARCHAR(500),
    `canonical_url` VARCHAR(500),
    `about_content` TEXT,
    `what_you_learn` TEXT,
    `who_should_attend` TEXT,
    `prerequisites` TEXT,
    `benefits` TEXT,
    `agenda` TEXT,
    `faqs` TEXT,
    `testimonials` TEXT,
    `language` VARCHAR(20) DEFAULT 'English',
    `mode` VARCHAR(20) DEFAULT 'online',
    `reminder_settings` TEXT,
    `view_count` INTEGER DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME,
    INDEX `ix_masterclasses_slug` (`slug`),
    INDEX `ix_masterclasses_status` (`status`),
    INDEX `ix_masterclasses_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: masterclass_registrations
-- =====================================================
CREATE TABLE IF NOT EXISTS `masterclass_registrations` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `masterclass_id` INTEGER NOT NULL,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(120) NOT NULL,
    `phone` VARCHAR(20),
    `country` VARCHAR(100),
    `company` VARCHAR(100),
    `job_title` VARCHAR(100),
    `experience` VARCHAR(50),
    `industry` VARCHAR(100),
    `linkedin` VARCHAR(500),
    `receive_updates` BOOLEAN DEFAULT TRUE,
    `status` VARCHAR(20) DEFAULT 'pending',
    `registration_id` VARCHAR(50) UNIQUE,
    `confirmation_sent` BOOLEAN DEFAULT FALSE,
    `confirmation_sent_at` DATETIME,
    `reminder_24h_sent` BOOLEAN DEFAULT FALSE,
    `reminder_3h_sent` BOOLEAN DEFAULT FALSE,
    `reminder_30m_sent` BOOLEAN DEFAULT FALSE,
    `source_page` VARCHAR(200),
    `ip_address` VARCHAR(45),
    `user_agent` VARCHAR(500),
    `utm_source` VARCHAR(100),
    `utm_medium` VARCHAR(100),
    `utm_campaign` VARCHAR(100),
    `device` VARCHAR(50),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME,
    FOREIGN KEY (`masterclass_id`) REFERENCES `masterclasses`(`id`) ON DELETE CASCADE,
    INDEX `ix_registrations_masterclass` (`masterclass_id`),
    INDEX `ix_registrations_email` (`email`),
    INDEX `ix_registrations_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: masterclass_analytics
-- =====================================================
CREATE TABLE IF NOT EXISTS `masterclass_analytics` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `masterclass_id` INTEGER NOT NULL,
    `event_type` VARCHAR(50) NOT NULL,
    `event_data` TEXT,
    `ip_address` VARCHAR(45),
    `user_agent` VARCHAR(500),
    `device` VARCHAR(50),
    `country` VARCHAR(100),
    `utm_source` VARCHAR(100),
    `utm_medium` VARCHAR(100),
    `utm_campaign` VARCHAR(100),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`masterclass_id`) REFERENCES `masterclasses`(`id`) ON DELETE CASCADE,
    INDEX `ix_analytics_masterclass` (`masterclass_id`),
    INDEX `ix_analytics_event` (`event_type`),
    INDEX `ix_analytics_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: masterclass_email_logs
-- =====================================================
CREATE TABLE IF NOT EXISTS `masterclass_email_logs` (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `registration_id` INTEGER NOT NULL,
    `email_type` VARCHAR(50) NOT NULL,
    `subject` VARCHAR(200),
    `sent_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `opened_at` DATETIME,
    `clicked_at` DATETIME,
    `bounced` BOOLEAN DEFAULT FALSE,
    `failed` BOOLEAN DEFAULT FALSE,
    `error_message` TEXT,
    FOREIGN KEY (`registration_id`) REFERENCES `masterclass_registrations`(`id`) ON DELETE CASCADE,
    INDEX `ix_email_logs_registration` (`registration_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
