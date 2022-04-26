#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define BLOCKSIZE 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    FILE *raw = fopen(argv[1], "r");
    if (raw == NULL)
    {
        printf("Cannot open image\n");
        return 1;
    }
    typedef uint8_t BYTE;
    BYTE buffer[BLOCKSIZE];
    size_t read;
    bool first = false;
    FILE *current;
    char new[100];
    int number = 0;
    bool found = false;
    
    
    while (true)
    {
        read = fread(buffer, sizeof(BYTE), BLOCKSIZE, raw);
        if (read == 0)
        {
            break;
        }
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            found = true;
            if (!first)
            {
                first = true;
            }
            else
            {
                fclose(current);
            }
            sprintf(new, "%03i.jpg", number);
            current = fopen(new, "w");
            fwrite(buffer, sizeof(BYTE), read, current);
            number++;
        }
        else
        {
            if (found)
            {
                fwrite(buffer, sizeof(BYTE), read, current);
            }
        }
    }
    fclose(raw);
    fclose(current);

    return 0;
}