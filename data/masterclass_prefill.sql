-- =====================================================
-- PREFILL DATA: AI Fundamentals Masterclass
-- Target Audience: Beginners who don't know what AI is
-- Purpose: Introduce AI concepts, use cases, and drive course enrollment
-- =====================================================

-- Insert Masterclass Record
INSERT INTO masterclasses (
    title,
    slug,
    short_description,
    detailed_description,
    banner_image,
    thumbnail,
    date,
    time,
    timezone,
    duration,
    registration_opens,
    registration_closes,
    instructor_name,
    instructor_photo,
    instructor_designation,
    instructor_company,
    instructor_bio,
    instructor_linkedin,
    status,
    max_seats,
    is_featured,
    show_floating_button,
    show_popup,
    show_sticky_banner,
    show_homepage_promotion,
    meta_title,
    meta_description,
    meta_keywords,
    about_content,
    what_you_learn,
    who_should_attend,
    prerequisites,
    benefits,
    agenda,
    faqs,
    language,
    mode,
    reminder_settings,
    created_at,
    updated_at
) VALUES (
    'AI Fundamentals: Discover How Artificial Intelligence Can Transform Your Life & Career',
    'ai-fundamentals-beginners-masterclass',
    'A free 90-minute masterclass for beginners to understand what AI is, how it works, and how it can solve real problems in your daily life and profession.',
    'Are you curious about Artificial Intelligence but feel overwhelmed by technical jargon? Do you wonder how AI actually helps people in their jobs and daily lives? This masterclass is designed specifically for complete beginners who want to understand AI without any technical background.

In this engaging 90-minute session, we''ll break down AI into simple concepts you can understand and relate to. Through real-world examples and hands-on demonstrations, you''ll discover how AI is already impacting your life and how it can become a powerful tool for your future.

The best part? This masterclass isn''t just about learning—it''s about discovering YOUR potential. At the end, you''ll get access to a personalized learning path designed specifically for your goals and background.',
    'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1920&h=1080&fit=crop',
    'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=300&fit=crop',
    DATE('2026-08-15'),
    TIME('14:00:00'),
    'UTC',
    90,
    DATETIME('2026-07-01 00:00:00'),
    DATETIME('2026-08-15 13:00:00'),
    'Dr. Sarah Chen',
    'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=200&h=200&fit=crop&crop=face',
    'AI Education Specialist & Former Google ML Engineer',
    'HUMISENSE Academy',
    'Dr. Sarah Chen is a passionate AI educator who believes everyone deserves to understand and benefit from artificial intelligence. With 12 years of experience at Google, Stanford Research, and now HUMISENSE, she has helped over 50,000 beginners take their first steps into the world of AI. Her teaching style is known for making complex concepts accessible to everyone, regardless of technical background.

Dr. Chen holds a Ph.D. in Machine Learning from Stanford University and has published 15+ research papers on AI applications in education and healthcare.',
    'https://linkedin.com/in/dr-sarah-chen-ai',
    'registration_open',
    500,
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    'AI Fundamentals Masterclass - Free Session for Beginners | HUMISENSE',
    'Join our free 90-minute masterclass to discover what AI is, how it works, and how it can transform your life and career. Perfect for beginners with no technical background.',
    'ai masterclass, artificial intelligence for beginners, ai course, learn ai, ai fundamentals, ai education, ai career, ai tools, chatgpt, machine learning basics',
    '<h2>About This Free Masterclass</h2>
    <p>Imagine understanding AI so well that you can confidently discuss it in job interviews, use AI tools to automate your daily tasks, and make informed decisions about AI investments for your career.</p>
    <p>This isn''t another technical webinar filled with complex mathematics and programming code. This is a beginner-friendly session designed to give you a solid foundation in AI concepts through:</p>
    <ul>
        <li>Simple explanations with relatable everyday examples</li>
        <li>Live demonstrations of AI tools you can use today</li>
        <li>Interactive Q&A sessions with our expert instructor</li>
        <li>Personalized next-step recommendations</li>
    </ul>
    <p>By the end of this masterclass, you won''t just understand what AI is—you''ll know how to use it to solve real problems in your specific situation.</p>',
    '["What Artificial Intelligence actually means (in simple terms)","How AI learns from data - the core concept explained","7 ways AI is already helping millions of people daily","How to use AI tools like ChatGPT effectively (hands-on demo)","AI use cases specific to your profession and industry","How to identify which AI skills are most valuable for YOUR career goals","Where to start your AI learning journey (personalized roadmap)","How AI courses are structured and what to look for before buying","Live Q&A - Get your specific questions answered","Certificate of Participation"]',
    '["Complete beginners with zero technical background","College students exploring career options","Working professionals wondering how AI affects their industry","Small business owners looking to leverage AI tools","Parents wanting to understand AI for their children''s education","Anyone curious about AI but intimidated by technical content","Career switchers considering tech industries","Professionals who want to speak confidently about AI"]',
    '["No programming experience required - this is for non-technical people","No prior knowledge of AI or machine learning needed","Just bring your curiosity and questions!","A device to attend the session (laptop, tablet, or phone)","Internet connection"]',
    '["Free certificate of participation","Access to AI tools we demonstrate during the session","Personalized learning path based on your goals","Exclusive discount coupon for HUMISENSE AI courses","Follow-up resource guide with all discussed tools and links","Lifetime access to session recording (for registered attendees)","Direct channel to ask questions after the masterclass"]',
    '[{"time":"0:00","title":"Welcome & Introduction","description":"Meet Dr. Sarah Chen and understand what to expect from this session"},{"time":"0:10","title":"What is AI Really?","description":"Breaking down the jargon into simple concepts everyone can understand"},{"time":"0:25","title":"AI in Your Daily Life","description":"7 surprising ways AI is already helping you (without you knowing)"},{"time":"0:40","title":"Live Demo: AI Tools You Can Use Today","description":"Hands-on demonstration of practical AI tools for productivity"},{"time":"0:55","title":"AI for Your Profession","description":"Industry-specific use cases and opportunities"},{"time":"1:10","title":"Your Personalized AI Journey","description":"How to start learning AI in a way that fits your goals"},{"time":"1:20","title":"Q&A Session","description":"Get your specific questions answered by our expert"},{"time":"1:30","title":"Next Steps & Certificate Distribution","description":"Certificate, resources, and exclusive offers"}]',
    '[{"question":"Is this masterclass really free?","answer":"Yes, this 90-minute masterclass is completely free. We believe everyone deserves access to quality AI education. At the end, you''ll have the option to explore our paid courses, but there''s no pressure to purchase anything."},{"question":"I have no technical background. Is this for me?","answer":"Absolutely! This masterclass is specifically designed for complete beginners with no technical background. We explain everything in simple, relatable terms without overwhelming you with technical jargon."},{"question":"What will I learn by the end?","answer":"You''ll understand what AI actually is, how it''s used in real life, how to use popular AI tools, and have a personalized roadmap for your AI learning journey."},{"question":"Do I need to install any software?","answer":"No installation required! We''ll show you web-based AI tools that you can start using immediately after the session."},{"question":"Will there be a recording?","answer":"Yes! All registered attendees will receive a link to the session recording within 24 hours after the masterclass."},{"question":"How is this different from YouTube videos?","answer":"Unlike generic YouTube content, this masterclass is interactive, beginner-specific, and includes personalized guidance. You can ask questions live and receive a customized learning path."},{"question":"What''s the catch? Why is it free?","answer":"We offer this as a service to the community. Our revenue comes from comprehensive courses, and this masterclass helps people decide if structured learning is right for them."},{"question":"Can I get a job in AI after this masterclass?","answer":"This masterclass is a starting point. You''ll understand if AI is right for you and get guidance on next steps. For career-focused AI skills, we offer in-depth courses with job placement support."}]',
    'English',
    'online',
    '{"send_24h": true, "send_3h": true, "send_30min": true, "send_immediately": true}',
    DATETIME('2026-07-15 00:00:00'),
    DATETIME('2026-07-15 00:00:00')
);

-- =====================================================
-- SAMPLE REGISTRATIONS (for testing analytics)
-- =====================================================

INSERT INTO masterclass_registrations (
    masterclass_id,
    first_name,
    last_name,
    email,
    phone,
    country,
    company,
    job_title,
    experience,
    industry,
    linkedin,
    receive_updates,
    status,
    registration_id,
    source_page,
    device,
    created_at
) VALUES
-- Confirmed Registrations
(1, 'James', 'Wilson', 'james.wilson@techcorp.com', '+1-555-0101', 'US', 'TechCorp Inc', 'Software Developer', 'intermediate', 'Technology', 'https://linkedin.com/in/jameswilson', TRUE, 'confirmed', 'MC-1-JK8M2P', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'desktop', DATETIME('2026-07-16 09:30:00')),
(1, 'Maria', 'Garcia', 'maria.garcia@university.edu', '+1-555-0102', 'US', 'State University', 'Graduate Student', 'beginner', 'Education', 'https://linkedin.com/in/mariagarcia', TRUE, 'confirmed', 'MC-1-NK3Q7R', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'mobile', DATETIME('2026-07-16 10:15:00')),
(1, 'Amit', 'Patel', 'amit.patel@startup.io', '+91-9876543210', 'IN', 'HealthTech Startup', 'Founder & CEO', 'intermediate', 'Healthcare', 'https://linkedin.com/in/amitpatel', TRUE, 'confirmed', 'MC-1-MP5T9W', 'https://twitter.com/humisense/status/123', 'mobile', DATETIME('2026-07-16 11:45:00')),
(1, 'Emma', 'Thompson', 'emma.t@designstudio.co', '+44-20-1234-5678', 'UK', 'Creative Design Studio', 'UX Designer', 'beginner', 'Design', 'https://linkedin.com/in/emmathompson', TRUE, 'confirmed', 'MC-1-QR7V2X', 'https://www.google.com/search?q=ai+masterclass', 'desktop', DATETIME('2026-07-16 14:20:00')),
(1, 'Carlos', 'Rodriguez', 'carlos.r@consulting.com', '+34-612-345-678', 'ES', 'Global Consulting LLP', 'Business Analyst', 'beginner', 'Consulting', 'https://linkedin.com/in/carlosrodriguez', TRUE, 'confirmed', 'MC-1-ST9Y4Z', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'tablet', DATETIME('2026-07-16 15:30:00')),
(1, 'Priya', 'Sharma', 'priya.sharma@email.com', '+91-8765432109', 'IN', 'Freelancer', 'Content Writer', 'beginner', 'Media', 'https://linkedin.com/in/priyasharma', TRUE, 'confirmed', 'MC-1-UV1A3B', 'https://www.facebook.com/humisense/posts/456', 'mobile', DATETIME('2026-07-16 16:00:00')),
(1, 'Michael', 'Brown', 'michael.brown@corp.net', '+1-555-0201', 'US', 'Finance Corp', 'Financial Analyst', 'intermediate', 'Finance', 'https://linkedin.com/in/michaelbrown', TRUE, 'confirmed', 'MC-1-WX3C5D', 'https://linkedin.com/post/ai-masterclass', 'desktop', DATETIME('2026-07-16 17:15:00')),
(1, 'Sophie', 'Martin', 'sophie.martin@gmail.com', '+33-6-12-34-56-78', 'FR', 'E-commerce Business', 'Small Business Owner', 'beginner', 'Retail', 'https://linkedin.com/in/sophiemartin', TRUE, 'confirmed', 'MC-1-YZ5E7F', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'mobile', DATETIME('2026-07-16 18:45:00')),
(1, 'Raj', 'Kumar', 'raj.kumar@company.in', '+91-9988776655', 'IN', 'IT Services Company', 'Project Manager', 'advanced', 'IT Services', 'https://linkedin.com/in/rajkumar', TRUE, 'confirmed', 'MC-1-AB7G9H', 'https://newsletter.humisense.com/ai-guide', 'desktop', DATETIME('2026-07-16 20:00:00')),
(1, 'Lisa', 'Anderson', 'lisa.anderson@outlook.com', '+1-555-0301', 'US', NULL, 'Homemaker', 'beginner', NULL, NULL, TRUE, 'confirmed', 'MC-1-CD9I1J', 'https://www.instagram.com/p/ai-course', 'mobile', DATETIME('2026-07-16 21:30:00')),
(1, 'David', 'Kim', 'david.kim@enterprise.kr', '+82-10-1234-5678', 'KR', 'Samsung Enterprise', 'Marketing Manager', 'beginner', 'Electronics', 'https://linkedin.com/in/davidkim', TRUE, 'confirmed', 'MC-1-EF1K3L', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'desktop', DATETIME('2026-07-17 08:00:00')),
(1, 'Fatima', 'Hassan', 'fatima.h@edu.ae', '+971-50-123-4567', 'AE', 'Dubai University', 'Professor', 'intermediate', 'Education', 'https://linkedin.com/in/fatimahassan', TRUE, 'confirmed', 'MC-1-GH3M5N', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'tablet', DAT.datetime('2026-07-17 09:30:00')),
(1, 'John', 'O''Brien', 'john.obrien@tech.ie', '+353-87-123-4567', 'IE', 'Innovation Hub', 'Entrepreneur', 'intermediate', 'Technology', 'https://linkedin.com/in/johnobrien', TRUE, 'confirmed', 'MC-1-IJ5O7P', 'https://podcast.interview/ai-episode', 'desktop', DATETIME('2026-07-17 10:00:00')),
(1, 'Yuki', 'Tanaka', 'yuki.tanaka@company.jp', '+81-90-1234-5678', 'JP', 'Manufacturing Co', 'Production Manager', 'beginner', 'Manufacturing', 'https://linkedin.com/in/yukitanaka', TRUE, 'confirmed', 'MC-1-KL7Q9R', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'desktop', DATETIME('2026-07-17 11:15:00')),
(1, 'Nina', 'Williams', 'nina.williams@gmail.com', '+1-555-0401', 'CA', NULL, 'Career Changer', 'beginner', 'Healthcare', 'https://linkedin.com/in/ninawilliams', TRUE, 'confirmed', 'MC-1-MN9S1T', 'https://webinar.ai-summit', 'mobile', DATETIME('2026-07-17 12:30:00')),
(1, 'Ahmed', 'Ali', 'ahmed.ali@corp.eg', '+20-100-123-4567', 'EG', 'Digital Agency', 'Creative Director', 'intermediate', 'Advertising', 'https://linkedin.com/in/ahmedali', TRUE, 'confirmed', 'MC-1-OP1U3V', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'desktop', DATETIME('2026-07-17 14:00:00')),
(1, 'Rachel', 'Green', 'rachel.green@lawfirm.com', '+1-555-0501', 'US', 'Legal Associates', 'Senior Associate', 'beginner', 'Legal', 'https://linkedin.com/in/rachelgreen', TRUE, 'confirmed', 'MC-1-QR3W5X', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'desktop', DATETIME('2026-07-17 15:45:00')),
(1, 'Sven', 'Johansson', 'sven.j@scandinavian.se', '+46-70-123-4567', 'SE', 'Logistics Company', 'Operations Director', 'intermediate', 'Logistics', 'https://linkedin.com/in/svenjohansson', TRUE, 'confirmed', 'MC-1-ST5Y7Z', 'https://youtube.com/watch?v=ai-intro', 'mobile', DATETIME('2026-07-17 16:30:00')),
(1, 'Ananya', 'Reddy', 'ananya.reddy@startup.in', '+91-98765-43210', 'IN', 'EdTech Startup', 'Product Manager', 'advanced', 'Education Technology', 'https://linkedin.com/in/ananyareddy', TRUE, 'confirmed', 'MC-1-UV7A9B', 'https://linkedin.com/in/humisense', 'desktop', DATETIME('2026-07-17 18:00:00')),
(1, 'Thomas', 'Mueller', 'thomas.mueller@firm.de', '+49-170-1234567', 'DE', 'Engineering GmbH', 'Mechanical Engineer', 'beginner', 'Engineering', 'https://linkedin.com/in/thomasmueller', TRUE, 'confirmed', 'MC-1-WX9C1D', 'https://humisense.com/masterclass/ai-fundamentals-beginners-masterclass', 'tablet', DATETIME('2026-07-17 19:30:00'));

-- =====================================================
-- SAMPLE ANALYTICS DATA
-- =====================================================

INSERT INTO masterclass_analytics (
    masterclass_id,
    event_type,
    ip_address,
    device,
    utm_source,
    utm_medium,
    utm_campaign,
    created_at
) VALUES
(1, 'page_view', '192.168.1.101', 'desktop', 'google', 'cpc', 'ai-masterclass-july', DATETIME('2026-07-15 10:00:00')),
(1, 'page_view', '192.168.1.102', 'mobile', 'twitter', 'social', 'ai-launch', DATETIME('2026-07-15 10:15:00')),
(1, 'page_view', '192.168.1.103', 'desktop', NULL, NULL, NULL, DATETIME('2026-07-15 10:30:00')),
(1, 'registration', '192.168.1.101', 'desktop', 'google', 'cpc', 'ai-masterclass-july', DATETIME('2026-07-16 09:30:00')),
(1, 'page_view', '192.168.1.104', 'tablet', 'linkedin', 'social', 'ai-webinar', DATETIME('2026-07-15 11:00:00')),
(1, 'page_view', '192.168.1.105', 'mobile', 'newsletter', 'email', 'july-digest', DATETIME('2026-07-15 12:00:00')),
(1, 'registration', '192.168.1.102', 'mobile', 'twitter', 'social', 'ai-launch', DATETIME('2026-07-16 10:15:00')),
(1, 'page_view', '192.168.1.106', 'desktop', 'youtube', 'video', 'ai-explainer', DATETIME('2026-07-15 14:00:00')),
(1, 'registration', '192.168.1.103', 'desktop', NULL, NULL, NULL, DATETIME('2026-07-16 14:20:00')),
(1, 'page_view', '192.168.1.107', 'mobile', 'facebook', 'social', 'free-ai-class', DATETIME('2026-07-15 15:00:00')),
(1, 'page_view', '192.168.1.108', 'desktop', 'webinar', 'affiliate', 'ai-summit', DATETIME('2026-07-15 16:00:00')),
(1, 'registration', '192.168.1.104', 'tablet', 'linkedin', 'social', 'ai-webinar', DATETIME('2026-07-16 15:30:00')),
(1, 'registration', '192.168.1.105', 'mobile', 'newsletter', 'email', 'july-digest', DATETIME('2026-07-16 16:00:00')),
(1, 'page_view', '192.168.1.109', 'desktop', 'direct', NULL, NULL, DATETIME('2026-07-15 17:00:00')),
(1, 'page_view', '192.168.1.110', 'mobile', 'reddit', 'social', 'ai-ama', DATETIME('2026-07-15 18:00:00')),
(1, 'registration', '192.168.1.106', 'desktop', 'youtube', 'video', 'ai-explainer', DATETIME('2026-07-16 17:15:00'));

-- =====================================================
-- MASTERCLASS SETTINGS
-- =====================================================

INSERT INTO site_settings (key, value, value_type) VALUES
('masterclass_enable_module', 'true', 'bool'),
('masterclass_enable_homepage_promotion', 'true', 'bool'),
('masterclass_enable_floating_cta', 'true', 'bool'),
('masterclass_enable_popup', 'true', 'bool'),
('masterclass_enable_sticky_banner', 'true', 'bool'),
('masterclass_enable_reminder_emails', 'true', 'bool'),
('masterclass_enable_calendar_integration', 'true', 'bool'),
('masterclass_enable_waitlist', 'false', 'bool'),
('masterclass_enable_certificates', 'true', 'bool'),
('masterclass_enable_analytics', 'true', 'bool'),
('masterclass_admin_email', 'admin@humisense.com', 'string');
