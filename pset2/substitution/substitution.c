#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main (int argc, string argv[])
{
   if (argc !=2) // checking command
   {
       printf ("Usage: ./substitution KEY\n");
       return 1;
   }
   int n = strlen(argv[1]);
   if (n != 26)  // checking key length
   {
       printf ("Key must contain 26 letters\n");
       return 1;
   }
   int i = 0;
   for (i=0; i<n; i++)  // checking if there are only letters in key
   {
       if (! isalpha(argv[1][i]))
       {
          printf ("Key must contain only letters\n");
          return 1;
       }
   }
   for (int j=0 ; j<n ; j++)
   {
      argv[1][j] = tolower (argv[1][j]);
   }
   int sum = 0;
   for (int k=0 ; k<n ; k++) // checking for duplicates
   {
     sum = sum + (argv[1][k]-96)*(argv[1][k]-96);
   }
  
   if (sum != 6201)
   {
      printf ("You must use each letter only once\n");
      return 1;
   }
   string plain = get_string ("plaintext: ");
   printf ("ciphertext: ");
   char alpha[] = "abcdefghijklmnopqrstuvwxyz";
   int l = strlen(plain);
   char cipher[l];
   for (int m = 0 ; m < l ; m++)
   {
      if (isalpha (plain[m]) )
      {
         if (islower (plain[m]))
         {
            for (int p = 0 ; p < n ; p++)
            {
               if (plain[m] == alpha[p])
               cipher[m] =  argv[1][p];
            }
         }
         else if (isupper (plain[m]))
         {
            for (int q = 0 ; q < n ; q++)
            {
               if (plain[m] == toupper (alpha[q]))
               {
                  cipher[m] = toupper (argv[1][q]);
               }
            }
         }
      }
      else
      {
      cipher[m] = plain[m];
      }
   }
   printf ("%s\n" , cipher);
   return 0;
}

