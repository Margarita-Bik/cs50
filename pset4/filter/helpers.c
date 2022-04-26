#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int rgbtoGray;
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            float Blues = image[i][j].rgbtBlue;
            float Reds = image[i][j].rgbtRed;
            float Greens= image[i][j].rgbtGreen;
            rgbtoGray = round ((Blues + Reds + Greens)/3);
            image[i][j].rgbtBlue = rgbtoGray;
            image[i][j].rgbtRed = rgbtoGray;
            image[i][j].rgbtGreen = rgbtoGray;
            
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < (width / 2) ; j++)
        {
        RGBTRIPLE temp = image[i][j];
        image[i][j] = image[i][width -j -1];
        image[i][width -j -1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp1[height][width];
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            temp1[i][j] = image[i][j];
        }
    }
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            float Blue = 0;
            float Red = 0;
            float Green = 0;
            int counter = 0;
            
            for (int k = -1 ; k < 2 ; k++)
            {
                if (i + k < 0 || i + k > height- 1)
                    {
                        continue;
                    }
                for (int l = -1 ; l < 2 ; l++)
                {
                    
                    if (j + l < 0 || j + l > width - 1)
                    {
                        continue;
                    }
                    Blue += image[i + k][j + l].rgbtBlue;
                    Red += image[i + k][j + l].rgbtRed;
                    Green += image[i + k][j + l].rgbtGreen;
                    counter++;
                    }
                
            }
            temp1[i][j].rgbtBlue = round (Blue / counter);
            temp1[i][j].rgbtRed = round (Red / counter);
            temp1[i][j].rgbtGreen = round (Green / counter);
        }
        
    }
     for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            image[i][j].rgbtBlue = temp1[i][j].rgbtBlue;
            image[i][j].rgbtRed = temp1[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp1[i][j].rgbtGreen;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp2[height][width];
    
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
           temp2[i][j] = image[i][j]; 
        }
    }
    
    int Gx[3][3] = { 
        {-1 , 0 , 1}, 
        {-2 , 0 , 2}, 
        {-1 , 0 , 1} 
        
    };
    int Gy[3][3] = { 
        {-1 , -2 , -1}, 
        {0 , 0 , 0}, 
        {1 , 2 , 1} 
        
    };
    
    
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            float GxBlue = 0;
            float GxRed = 0;
            float GxGreen = 0;
            float GyBlue = 0;
            float GyRed = 0;
            float GyGreen = 0;
         for (int k = -1 ; k < 2 ; k++)
            {
                 if (i + k < 0 || i + k > height -1)
                    {
                       continue;
                    }
                for (int l = -1 ; l < 2 ; l++)
                {
                   
                    if (j + l < 0 || j + l > width -1)
                    {
                       continue;
                    }
                    GxBlue += image[i + k][j + l].rgbtBlue * Gx[k + 1][l + 1];
                    GxRed += image[i + k][j + l].rgbtRed * Gx[k + 1][l + 1];
                    GxGreen += image[i + k][j + l].rgbtGreen * Gx[k + 1][l + 1];
                    GyBlue += image[i + k][j + l].rgbtBlue * Gy[k + 1][l + 1];
                    GyRed += image[i + k][j + l].rgbtRed * Gy[k + 1][l + 1];
                    GyGreen += image[i + k][j + l].rgbtGreen * Gy[k + 1][l + 1];
                }
            }
            int blue = round (sqrt (GxBlue * GxBlue + GyBlue * GyBlue));
            int red = round (sqrt (GxRed * GxRed + GyRed * GyRed));
            int green = round (sqrt (GxGreen * GxGreen + GyGreen * GyGreen));
            
            if (blue > 255)
            {
                blue = 255;
            }
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            
            temp2[i][j].rgbtBlue = blue;
            temp2[i][j].rgbtRed = red;
            temp2[i][j].rgbtGreen = green;
        }
        
    }
         for (int i = 0 ; i < height ; i++)
         {
            for (int j = 0 ; j < width ; j++)
             {
             image[i][j].rgbtBlue = temp2[i][j].rgbtBlue;
             image[i][j].rgbtRed = temp2[i][j].rgbtRed;
             image[i][j].rgbtGreen = temp2[i][j].rgbtGreen;
             }
         }
    return;
}
