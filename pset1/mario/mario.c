#include <stdio.h>
#include <cs50.h>

int get_positive_int (void);
int main (void)
{
  int i = get_positive_int ();

  for (int l = 1 ; l < i+1 ; l++)
  {
     for (int j = 0 ; j < i ; j++)
     {
        if (j < i-l)
        {
            printf (" ");
        }
        else
        {
            printf ("#");
        }
     }
     printf ("\n");
  }
}




int get_positive_int (void)
{
    int n;
    do
    {
        n = get_int ("Height:");
    }
    while (n<1 || n>8);
    return n;
}