# Store database

SQL Server uchun do'kon savdo tizimi modeli (Ch01_Text namunasi asosida).

## Ishga tushirish
1. SSMS da run_all.sql ni oching (SQLCMD Mode yoqilgan bo'lsin) va Execute bosing.
2. Skript Store bazasini o'chirib qayta yaratadi, shuning uchun qayta ishga tushirish xavfsiz.

## Jadvallar
- EMPLOYEE, CERTIFIED, SKILL (rasmdagi ma'lumotlar)
- STORE (qo'shimcha: STORE_YTD_SALES > 0 CHECK)

## Talablar
- EMP_CODE: dbo.seq_emp_code orqali (DEFAULT NEXT VALUE FOR)
- EMPLOYEE.STORE_CODE: DEFAULT 3
- STORE.STORE_YTD_SALES: CHECK (> 0)