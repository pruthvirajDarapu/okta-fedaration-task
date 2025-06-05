Connect-AzureAD
# Generate a new ImmutableId
$ImmutableId = [Convert]::ToBase64String(([guid]::NewGuid()).ToByteArray())

# Create a new Azure AD user
New-AzureADUser -DisplayName "Second User Demo" `
  -UserPrincipalName "new.user@a114.mywiclab.com" `
  -MailNickname "newuser" `
  -AccountEnabled $true `
  -PasswordProfile @{
      Password = "P@ssword1234"
      ForceChangePasswordNextLogin = $true
  } `
  -ImmutableId $ImmutableId
