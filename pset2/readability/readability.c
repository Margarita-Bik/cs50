#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");
    float letters = 0;
    float words = 1;
    float sentences = 0;
    for (int i = 0 ; i< strlen(text) ; i++)
    {
        if (isalpha(text[i]))
        {
        letters = letters + 1; 
        }
        if (text[i] == ' ')
        {
        words = words + 1;
        }
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
        sentences = sentences +1;
        }
    }
    printf ("%.0f letter(s)\n" , letters);
    printf ("%.0f word(s)\n" , words);
    printf ("%.0f sentence(s)\n" , sentences);
    float L = (letters/words)*100;
    float S = (sentences/words)*100;
    float index = 0.0588*L-0.296*S-15.8;
    if (index < 1)
        {
        printf ("Before Grade 1\n");
        }
        else if (index >= 16)
        {
            printf ("Grade 16+\n");
        }
        else
        {
        printf ("Grade %.0f\n" , round(index));
        }
}