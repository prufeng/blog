```
$EmailFrom = “from_email_id”
$EmailTo = “to_email_id”
$Subject = “Subject”
$Body = “Hello User”
$SMTPServer = “smtp.gmail.com”
$SMTPClient = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
$SMTPClient.EnableSsl = $true
$SMTPClient.Credentials = New-Object System.Net.NetworkCredential(“emailid”, “password”);
$SMTPClient.Send($EmailFrom, $EmailTo, $Subject, $Body)
```
