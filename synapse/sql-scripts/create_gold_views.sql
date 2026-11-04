USE gold_db
GO

CREATE OR ALTER PROC CreateSqlServerlessView_gold
    @ViewName NVARCHAR(100)
AS
BEGIN

    DECLARE @statement VARCHAR(MAX)

    SET @statement = N'
        CREATE OR ALTER VIEW ' + QUOTENAME(@ViewName) + ' AS
        SELECT *
        FROM
            OPENROWSET(
                BULK ''https://demodedl01.dfs.core.windows.net/gold/SalesLT/'
                + @ViewName + '/'',
                FORMAT = ''DELTA''
            ) AS [result]
    '

    EXEC (@statement)

END
GO
