# Connect to Azure AD
Connect-AzureAD

# Delete the user by UserPrincipalName
Remove-AzureADUser -ObjectId "new.user11@a114.mywiclab.com"
