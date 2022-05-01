
Excel - VBA导入CSV为文本格式及中文乱码问题
====

# VBA导入CSV为文本格式

Excel导入CSV时，会自动转换一些列的格式，特别是数值格式，非常烦。

找到以下VBA导入CSV为文本格式的方法，亲测可行。

先打开文件获取列数，将每一列的格式都设置为`xlTextFormat`, 然后再赋值给`QueryTable.TextFileColumnDataTypes`。

```vb
Public Sub ImportCSVAsText()
    Dim TempWorkbook As Workbook
    Dim TempWorksheet As Worksheet
    Dim ColumnCount As Integer
    Dim FileName As Variant
    Dim ColumnArray() As Integer

    'Get the file name
    FileName = Application.GetOpenFilename(FileFilter:="All Files (*.*),*.*", FilterIndex:=1, Title:="Select the CSV file", MultiSelect:=False)

    If FileName = False Then Exit Sub

    Application.ScreenUpdating = False

    'Open the file temporarily to get the count of columns
    Set TempWorkbook = Workbooks.Open(FileName)
    ColumnCount = TempWorkbook.Sheets(1).Range("A1").SpecialCells(xlCellTypeLastCell).Column
    TempWorkbook.Close SaveChanges:=False

    'Resize the array to number of columns
    ReDim ColumnArray(1 To ColumnCount)

    For i = 1 To ColumnCount
        ColumnArray(i) = xlTextFormat
    Next i

    Set TempWorkbook = Workbooks.Add
    Set TempWorksheet = TempWorkbook.Sheets(1)

    With TempWorksheet.QueryTables.Add("TEXT;" & FileName, TempWorksheet.Cells(1, 1))
        .FieldNames = True
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .TextFilePromptOnRefresh = False
        .TextFilePlatform = 1251
        .TextFileStartRow = 1
        .TextFileParseType = xlDelimited
        .TextFileTextQualifier = xlTextQualifierDoubleQuote
        .TextFileConsecutiveDelimiter = False
        .TextFileTabDelimiter = False
        .TextFileSemicolonDelimiter = False
        .TextFileCommaDelimiter = True
        .TextFileSpaceDelimiter = False
        .TextFileColumnDataTypes = ColumnArray
        .TextFileTrailingMinusNumbers = True
        .Refresh BackgroundQuery:=False
    End With

End Sub
```

# 中文乱码问题

修改配置`TextFilePlatform = 65001`，问题解决。

简单来说就是设置导入源文件的编码, 65001对应的是utf-8，编码的对应数值可以在手动导入CSV文件向导里看到。

> ### QueryTable.TextFilePlatform property (Excel)
>Returns or sets the origin of the text file that you are importing into the query table. This property determines which code page is used during the data import. Read/write XlPlatform.
> ### Remarks
>The default value is the current setting of the File Origin option in the Text File Import Wizard.
>Use this property only when your query table is based on data from a text file (with the QueryType property set to xlTextImport).
>If you import data by using the user interface, data from a web query or a text query is imported as a QueryTable object, while all other external data is imported as a ListObject object.
>If you import data by using the object model, data from a web query or a text query must be imported as a QueryTable, while all other external data can be imported as either a ListObject or a QueryTable.
>The TextFilePlatform property applies only to QueryTable objects.


# Reference

* https://superuser.com/questions/307496/how-can-i-set-excel-to-always-import-all-columns-of-csv-files-as-text
* https://docs.microsoft.com/en-us/office/vba/api/excel.querytable.textfileplatform
