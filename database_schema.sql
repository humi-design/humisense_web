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
