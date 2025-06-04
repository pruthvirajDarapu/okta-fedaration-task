Connect-AzureAD
# Generate a new ImmutableId
$ImmutableId = [Convert]::ToBase64String(([guid]::NewGuid()).ToByteArray())

# Create a new Azure AD user
New-AzureADUser -DisplayName "Second User Demo" `
  -UserPrincipalName "seconduserdemo@a114.mywiclab.com" `
  -MailNickname "seconduserdemo" `
  -AccountEnabled $true `
  -PasswordProfile @{
      Password = "P@ssword1234"
      ForceChangePasswordNextLogin = $true
  } `
  -ImmutableId $ImmutableId
