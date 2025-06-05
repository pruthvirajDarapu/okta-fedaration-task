Connect-AzureAD
# Generate a new ImmutableId
$ImmutableId = [Convert]::ToBase64String(([guid]::NewGuid()).ToByteArray())

# Create a new Azure AD user
New-AzureADUser -DisplayName "new User Demo" `
  -UserPrincipalName "new.user11@a114.mywiclab.com" `
  -MailNickname "newuser11" `
  -AccountEnabled $true `
  -PasswordProfile @{
      Password = "P@ssword1234"
      ForceChangePasswordNextLogin = $true
  } `
  -ImmutableId $ImmutableId
