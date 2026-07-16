-- ===============================================
-- MySQL Query to Update Masterclass Content
-- Run this in your phpMyAdmin or MySQL CLI
-- ===============================================

-- Update About Content
UPDATE masterclasses 
SET about_content = '<h2>About This Free Masterclass</h2>
<p>Imagine understanding AI so well that you can confidently discuss it in job interviews, use AI tools to automate your daily tasks, and make informed decisions about AI investments for your career.</p>
<p>This isn''t another technical webinar filled with complex mathematics and programming code. This is a beginner-friendly session designed to give you a solid foundation in AI concepts through:</p>
<ul>
<li>Simple explanations with relatable everyday examples</li>
<li>Live demonstrations of AI tools you can use today</li>
<li>Interactive Q&A sessions with our expert instructor</li>
<li>Personalized next-step recommendations</li>
</ul>
<p>By the end of this masterclass, you won''t just understand what AI is—you''ll know how to use it to solve real problems in your specific situation.</p>'
WHERE slug = 'ai-automation-for-business';

-- Update Overview (Short Description)
UPDATE masterclasses 
SET short_description = 'Complete beginners can join and understand AI and ML from scratch. Learn how to use it in your life and career. Ask your doubts and get personalized course recommendations. This masterclass is your entry point to the world of AI.'
WHERE slug = 'ai-automation-for-business';

-- Add "What You'll Learn" items
INSERT INTO masterclass_learning_items (masterclass_id, title, sort_order) 
SELECT id, item_title, item_order FROM (
  SELECT 'What AI really means and why it matters' as item_title, 1 as item_order FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'How to use AI tools in your daily work', 2 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Practical AI automation techniques', 3 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'How to discuss AI confidently in interviews', 4 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Making informed AI investment decisions', 5 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Personalized learning path recommendations', 6 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
) t;

-- Add "Who Should Attend" items
INSERT INTO masterclass_attendee_items (masterclass_id, title, sort_order) 
SELECT id, item_title, item_order FROM (
  SELECT 'Complete beginners with no prior AI experience' as item_title, 1 as item_order FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Professionals looking to understand AI for career growth', 2 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Entrepreneurs wanting to leverage AI in their business', 3 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Anyone curious about AI and its practical applications', 4 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Job seekers preparing for AI-related interviews', 5 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
) t;

-- Add FAQs
INSERT INTO masterclass_faqs (masterclass_id, question, answer, sort_order) 
SELECT id, question, answer, sort_order FROM (
  SELECT 'Do I need any prior coding experience?' as question, 'No! This masterclass is designed for complete beginners. We explain everything in simple terms without any programming or technical jargon.' as answer, 1 as sort_order FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'What will I learn in this masterclass?', 'You''ll learn the fundamentals of AI and ML, how to use AI tools in your daily life and work, practical automation techniques, and get personalized recommendations for further learning.', 2 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Is this masterclass really free?', 'Yes, this masterclass is completely free! We believe in making AI education accessible to everyone.', 3 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'How long is the masterclass?', 'The masterclass is approximately 2 hours long, including time for Q&A with the instructor.', 4 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Can I ask questions during the session?', 'Absolutely! We have dedicated Q&A sessions where you can ask any questions you have about AI.', 5 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'Will I get a certificate?', 'Yes, all participants who attend the live session will receive a certificate of completion.', 6 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
  UNION ALL SELECT 'What happens after the masterclass?', 'You''ll receive personalized course recommendations based on your interests and goals, and have the opportunity to enroll in our comprehensive AI courses.', 7 FROM dual WHERE EXISTS (SELECT 1 FROM masterclasses WHERE slug = 'ai-automation-for-business')
) t;
