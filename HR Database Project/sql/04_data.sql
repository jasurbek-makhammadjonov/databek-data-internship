USE Store;
GO

-- Namuna ma'lumot (rasmda yo'q)
INSERT INTO dbo.STORE (STORE_CODE, STORE_NAME, STORE_YTD_SALES) VALUES
(1, 'Central Store', 1250000.50),
(2, 'North Store',    830400.00),
(3, 'Main Store',    1010250.75);

-- STORE_CODE berilmaydi -> default 3; EMP_CODE berilmaydi -> sequence
INSERT INTO dbo.EMPLOYEE (Employee_ID, Employee_FName, Employee_LName, Employee_HireDate, Employee_Title) VALUES
('02345', 'Johnny',   'Jones',      '1995-02-14', 'DBA'),
('03373', 'Franklin', 'Johnson',    '2002-03-15', 'Purchasing Agent'),
('04893', 'Patricia', 'Richards',   '2004-06-11', 'DBA'),
('06234', 'Jasmine',  'Patel',      '2005-08-10', 'Programmer'),
('08273', 'Marco',    'Bienz',      '2006-07-28', 'Analyst'),
('09002', 'Ben',      'Joiner',     '2010-05-20', 'Clerk'),
('09283', 'Juan',     'Chavez',     '2010-07-04', 'Clerk'),
('09382', 'Jessica',  'Johnson',    '2010-08-02', 'Database Programmer'),
('10282', 'Amanda',   'Richardson', '2011-04-11', 'Clerk'),
('13383', 'Raymond',  'Matthews',   '2012-03-12', 'Programmer'),
('13567', 'Robert',   'Almond',     '2012-09-30', 'Analyst'),
('13992', 'Megan',    'Lee',        '2013-09-29', 'Programmer'),
('14311', 'Lee',      'Duong',      '2014-09-01', 'Programmer');

INSERT INTO dbo.SKILL (Skill_ID, Skill_Name, Skill_Description) VALUES
(100, 'Basic Database Management',        'Create and manage database user accounts.'),
(110, 'Basic Web Design',                 'Create and maintain HTML and CSS documents.'),
(120, 'Advanced Spreadsheets',            'Use of advanced functions, user-defined functions, and macroing.'),
(130, 'Basic Process Modeling',           'Create core business process models using standard libraries.'),
(140, 'Basic Database Design',            'Create simple data models.'),
(150, 'Master Database Programming',      'Create integrated trigger and procedure packages for a distributed environment.'),
(160, 'Basic Spreadsheets',               'Create single tab worksheets with basic formulas'),
(170, 'Basic C# Programming',             'Create single-tier data aware modules.'),
(180, 'Advanced Database Management',     'Manage Database Server Clusters.'),
(190, 'Advance Process Modeling',         'Evaluate and Redesign cross-functional internal and external business processes.'),
(200, 'Advance C# Programming',           'Create multi-tier applications using multi-threading'),
(210, 'Basic Database Manipulation',      'Create simple data retrieval and manipulation statements in SQL.'),
(220, 'Advanced Database Manipulation',   'Use of advanced data manipulation methods for multi-table inserts, set operations, and correlated subqueries.');

INSERT INTO dbo.CERTIFIED (Employee_ID, Skill_ID, Certified_Date) VALUES
('02345', 100, '2002-02-14'),
('02345', 110, '2003-08-09'),
('02345', 180, '2005-02-14'),
('03373', 120, '2011-06-20'),
('04893', 180, '2006-06-11'),
('04893', 220, '2012-09-20'),
('06234', 110, '2007-08-10'),
('06234', 200, '2007-08-10'),
('06234', 210, '2012-01-29'),
('08273', 110, '2009-03-08'),
('08273', 190, '2012-08-19'),
('09002', 110, '2013-05-16'),
('09002', 120, '2013-05-16'),
('09382', 140, '2012-08-02'),
('09382', 210, '2012-08-02'),
('09382', 220, '2013-05-01'),
('13383', 170, '2014-03-12'),
('13567', 130, '2014-09-30'),
('13567', 140, '2015-05-23'),
('14311', 110, '2016-09-01');
GO