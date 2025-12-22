All utilities are stored here,

Each utility should have a .pyw Module with the same name as the utility
and a data.json with a
 - FileName (str) - The name of the utility file
 - LongName (str) - Full, display name
 - Description (str) - Short, user-facing description explaining what the utility is for
 - ConfigInputs (dict) - A list of variables that are to be modified by the user
   - The key of each variable is the base display name
   - The first value is the type of the value (Text, Int, Enum, etc.)
   - The second value is an optional description
   - The third value is Config key that will be saved and will be retrieved via ConfigREST.