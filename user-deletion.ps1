# Connect to Azure AD
Connect-AzureAD

# Delete the user by UserPrincipalName
Remove-AzureADUser -ObjectId "seconduserdemo@a114.mywiclab.com"
