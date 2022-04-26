#include <cs50.h>
#include <stdio.h>

int main (void)
{
    long card = get_long ("Number:");
    int i = 0;
    long c = card;
    while (c > 0)
    {
        c = c / 10;
        i++;
    }
    if (i != 13 && i!= 15 && i != 16)
    {
    printf ("INVALID\n");
    return 0;
    }
    int s1 = 0;
    int s2 = 0;
    int m1 = 0;
    int m2 = 0;
    int mm1 = 0;
    int mm2 = 0;
    long n = card;
    int total = 0;

    do
    {
        m1 = n % 10;
        n = n / 10;
        s1 = s1 + m1;

        m2 = n % 10;
        n = n / 10;

        m2 = m2 * 2;
        mm1 = m2 % 10;
        mm2 = m2 / 10;

        s2 = s2 + mm1 + mm2;
    }
        while (n >0);
        total = s1 +s2;

    if (total % 10 != 0)
    {
    printf ("INVALID\n");
    return 0;
    }
    long num = card;

    do
    {
        num = num / 10;
    }
        while (num > 99);


    if ( (i == 16) && (num / 10 == 5) && (num % 10 > 0 && num % 10 < 6))
    {
        printf ("MASTERCARD\n");
    }

    else if ( (i == 15) && (num / 10 == 3) && (num % 10 == 4 || num % 10 == 7))
    {
        printf ("AMEX\n");
    }

   else if ((i == 13 || i == 16) &&  (num /10 == 4))
    {
    printf ("VISA\n");
    }

    else
    {
        printf ("INVALID\n");
    }
}