#include"data_header.h"

FILE *fptr = NULL;
FILE *fptr2 = NULL;
FILE *exist = NULL;

void savefile()
{
    char folder_path[100];
    char file_name[100];
    char ch;

    printf("Enter folder path where you want to save the file: ");
    fgets(folder_path, sizeof(folder_path), stdin);
    folder_path[strcspn(folder_path, "\n")] = '\0'; // Remove the newline character

    // Open the source file for reading
    FILE *fptr = fopen("data.txt", "r");

    if (fptr == NULL)
    {
        printf("Error opening the source file for reading\n");
        return;
    }

    printf("Enter file name (without extension): ");
    fgets(file_name, sizeof(file_name), stdin);
    file_name[strcspn(file_name, "\n")] = '\0'; // Remove the newline character

    // Add the ".txt" extension to the file name
    strcat(file_name, ".txt");

    // Combine folder path and file name to create the complete file path
    char complete_path[200];
    snprintf(complete_path, sizeof(complete_path), "%s/%s", folder_path, file_name);

    // Open the destination file for writing
    FILE *fptr2 = fopen(complete_path, "w");

    if (fptr2 == NULL)
    {
        printf("Error creating/appending the file\n");
        fclose(fptr); // Close the source file before returning
        return;
    }

    // Copy the contents of the source file to the destination file
    while ((ch = fgetc(fptr)) != EOF)
    {
        fputc(ch, fptr2);
    }

    // Close both files
    fclose(fptr);
    fclose(fptr2);

    printf("File saved successfully as %s\n", complete_path);
}

void existing_file()
{
char folder_path[100];
    char file_name[100];
    printf("Enter folder path from where you want to open the file: ");
    fgets(folder_path, sizeof(folder_path), stdin);
    folder_path[strcspn(folder_path, "\n")] = '\0'; // Remove the newline character

    printf("Enter file name (without extension): ");
    fgets(file_name, sizeof(file_name), stdin);
    file_name[strcspn(file_name, "\n")] = '\0'; // Remove the newline character

    // Add the ".txt" extension to the file name
    strcat(file_name, ".txt");

    // Combine folder path and file name to create the complete file path
    char complete_path[200];
    snprintf(complete_path, sizeof(complete_path), "%s\\%s", folder_path, file_name); // Use "\\" for Windows paths

    FILE *exist = fopen(complete_path, "r"); // Open the existing file for reading

    if (exist == NULL) {
        printf("Error opening '%s' for reading.\n", file_name);
        exit(1);
    }

    char buffer[1024];

    while (fgets(buffer, sizeof(buffer), exist) != NULL) {
        printf("%s", buffer); // Print the line to the console
    }

    fclose(exist);
}

