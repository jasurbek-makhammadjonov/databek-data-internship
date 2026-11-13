/* ===================================================
   1. DATABASE
=================================================== */

IF DB_ID('Store') IS NOT NULL
BEGIN
    ALTER DATABASE Store SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE Store;
END
GO

CREATE DATABASE Store;
GO

USE Store;
GO

/* ===================================================
   2. SEQUENCE FOR EMP_CODE
=================================================== */

IF OBJECT_ID('dbo.Seq_EMP_CODE', 'SO') IS NOT NULL
    DROP SEQUENCE dbo.Seq_EMP_CODE;
GO

CREATE SEQUENCE dbo.Seq_EMP_CODE
START WITH 1
INCREMENT BY 1;
GO

/* ===================================================
   3. TABLES
=================================================== */

IF OBJECT_ID('dbo.EMPLOYEE', 'U') IS NOT NULL
    DROP TABLE dbo.EMPLOYEE;
GO

IF OBJECT_ID('dbo.STORE', 'U') IS NOT NULL
    DROP TABLE dbo.STORE;
GO

IF OBJECT_ID('dbo.REGION', 'U') IS NOT NULL
    DROP TABLE dbo.REGION;
GO


/* ---------- REGION ---------- */

CREATE TABLE REGION
(
    REGION_CODE       INT PRIMARY KEY,
    REGION_DESCRIPT   VARCHAR(50) NOT NULL
);
GO


/* ---------- STORE ---------- */

CREATE TABLE STORE
(
    STORE_CODE        INT PRIMARY KEY,
    STORE_NAME        VARCHAR(50) NOT NULL,

    STORE_YTD_SALES   DECIMAL(12,2) NOT NULL,

    REGION_CODE       INT NOT NULL,

    EMP_CODE          INT NULL,

    CONSTRAINT CK_STORE_YTD_SALES
        CHECK (STORE_YTD_SALES > 0),

    CONSTRAINT FK_STORE_REGION
        FOREIGN KEY (REGION_CODE)
        REFERENCES REGION(REGION_CODE)
);
GO


/******** EMPLOYEE ********/

CREATE TABLE EMPLOYEE
(
    EMP_CODE      INT PRIMARY KEY,

    EMP_TITLE     VARCHAR(10),

    EMP_LNAME     VARCHAR(30) NOT NULL,

    EMP_FNAME     VARCHAR(30) NOT NULL,

    EMP_INITIAL   CHAR(1),

    EMP_DOB       DATE,

    STORE_CODE    INT
        CONSTRAINT DF_EMPLOYEE_STORE_CODE DEFAULT(3),

    CONSTRAINT FK_EMPLOYEE_STORE
        FOREIGN KEY (STORE_CODE)
        REFERENCES STORE(STORE_CODE)
);
GO


/* ===================================================
   4. INSERT REGION
=================================================== */

INSERT INTO REGION
VALUES
(1,'East'),
(2,'West');
GO


/* ===================================================
   5. INSERT STORE
   (EMP_CODE keyin update qilinadi)
=================================================== */

INSERT INTO STORE
(
    STORE_CODE,
    STORE_NAME,
    STORE_YTD_SALES,
    REGION_CODE,
    EMP_CODE
)
VALUES
(1,'Access Junction',1003455.76,2,NULL),
(2,'Database Corner',1421987.39,2,NULL),
(3,'Tuple Charge',986783.22,1,NULL),
(4,'Attribute Alley',944568.56,2,NULL),
(5,'Primary Key Point',2930098.45,1,NULL);
GO


/* ===================================================
   6. INSERT EMPLOYEE
   EMP_CODE = NEXT VALUE FOR SEQUENCE
=================================================== */

INSERT INTO EMPLOYEE
VALUES
(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Williamson','John','W','1964-05-21',3),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Ms.','Ratula','Nancy',NULL,'1969-02-09',2),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Ms.','Greenboro','Lottie','R','1961-10-02',4),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mrs.','Rumplesfro','Jennie','S','1971-06-01',5),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Smith','Robert','L','1959-11-23',3),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Renselaer','Cary','A','1965-12-25',1),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Ogallo','Roberto','S','1962-07-31',3),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Ms.','Johnsson','Elizabeth','I','1968-09-10',1),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Eindsmar','Jack','W','1955-04-19',2),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mrs.','Jones','Rose','R','1966-03-06',4),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Broderick','Tom',NULL,'1972-10-21',3),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Washington','Alan','Y','1974-09-08',2),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Smith','Peter','N','1964-08-25',3),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Ms.','Smith','Sherry','H','1966-05-25',4),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Olenko','Howard','U','1964-05-24',5),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Achiolo','Barry','V','1960-09-03',5),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Ms.','Grimaldo','Jeanine','K','1970-11-12',4),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Rosenberg','Andrew','D','1971-01-24',4),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Rosten','Peter','F','1968-10-03',4),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Mr.','Mckee','Robert','S','1970-03-06',1),

(NEXT VALUE FOR dbo.Seq_EMP_CODE,'Ms.','Baumann','Jennifer','A','1974-12-11',3);
GO


/* ===================================================
   7. STORE MANAGERS
=================================================== */

UPDATE STORE SET EMP_CODE = 8  WHERE STORE_CODE = 1;
UPDATE STORE SET EMP_CODE = 12 WHERE STORE_CODE = 2;
UPDATE STORE SET EMP_CODE = 7  WHERE STORE_CODE = 3;
UPDATE STORE SET EMP_CODE = 3  WHERE STORE_CODE = 4;
UPDATE STORE SET EMP_CODE = 15 WHERE STORE_CODE = 5;
GO


/* ===================================================
   8. ADD FINAL FK STORE -> EMPLOYEE
=================================================== */

ALTER TABLE STORE
ADD CONSTRAINT FK_STORE_MANAGER
FOREIGN KEY (EMP_CODE)
REFERENCES EMPLOYEE(EMP_CODE);
GO


/* ===================================================
   9. TESTS
=================================================== */

SELECT * FROM REGION;
SELECT * FROM STORE;
SELECT * FROM EMPLOYEE;
GO