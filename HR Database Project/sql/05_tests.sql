USE Store;
GO
SELECT * FROM dbo.STORE;
SELECT * FROM dbo.EMPLOYEE;
SELECT * FROM dbo.SKILL;
SELECT * FROM dbo.CERTIFIED;
GO

-- Default tekshiruvi: STORE_CODE = 3 bo'lishi kerak
INSERT INTO dbo.EMPLOYEE (Employee_ID, Employee_FName, Employee_LName, Employee_HireDate, Employee_Title)
VALUES ('99999', 'Test', 'User', '2024-01-01', 'Clerk');
SELECT Employee_ID, EMP_CODE, STORE_CODE FROM dbo.EMPLOYEE WHERE Employee_ID = '99999';
DELETE FROM dbo.EMPLOYEE WHERE Employee_ID = '99999';
GO

-- Check tekshiruvi: ikkalasi ham xato berishi kerak
BEGIN TRY
    UPDATE dbo.STORE SET STORE_YTD_SALES = 0 WHERE STORE_CODE = 1;
END TRY
BEGIN CATCH
    PRINT 'OK: 0 qabul qilinmadi - ' + ERROR_MESSAGE();
END CATCH;

BEGIN TRY
    UPDATE dbo.STORE SET STORE_YTD_SALES = -5 WHERE STORE_CODE = 1;
END TRY
BEGIN CATCH
    PRINT 'OK: manfiy qabul qilinmadi - ' + ERROR_MESSAGE();
END CATCH;
GO