#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#define BUFFER_SIZE 4096

int main(void) {
    char source[256], destination[256];
    char buffer[BUFFER_SIZE];
    ssize_t bytesRead, bytesWritten;

    printf("Source file: ");
    if (fgets(source, sizeof(source), stdin) == NULL) {
        perror("Input error");
        return 1;
    }

    printf("Destination file: ");
    if (fgets(destination, sizeof(destination), stdin) == NULL) {
        perror("Input error");
        return 1;
    }

    source[strcspn(source, "\n")] = '\0';
    destination[strcspn(destination, "\n")] = '\0';

    if (source[0] == '\0' || destination[0] == '\0') {
        fprintf(stderr, "Error: File name cannot be empty.\n");
        return 1;
    }

    if (strcmp(source, destination) == 0) {
        fprintf(stderr, "Error: Source and destination must be different.\n");
        return 1;
    }

    int input = open(source, O_RDONLY);

    if (input == -1) {
        fprintf(stderr, "Error opening source file '%s': %s\n",
                source, strerror(errno));
        return 1;
    }

    int output = open(destination, O_WRONLY | O_CREAT | O_TRUNC, 0644);

    if (output == -1) {
        fprintf(stderr, "Error creating destination file '%s': %s\n",
                destination, strerror(errno));
        close(input);
        return 1;
    }

    while ((bytesRead = read(input, buffer, BUFFER_SIZE)) > 0) {
        char *ptr = buffer;
        ssize_t remaining = bytesRead;

        while (remaining > 0) {
            bytesWritten = write(output, ptr, remaining);

            if (bytesWritten == -1) {
                fprintf(stderr, "Error writing file: %s\n",
                        strerror(errno));
                close(input);
                close(output);
                return 1;
            }

            ptr += bytesWritten;
            remaining -= bytesWritten;
        }
    }

    if (bytesRead == -1) {
        fprintf(stderr, "Error reading source file: %s\n",
                strerror(errno));
        close(input);
        close(output);
        return 1;
    }

    if (close(input) == -1) {
        perror("Error closing source file");
        close(output);
        return 1;
    }

    if (close(output) == -1) {
        perror("Error closing destination file");
        return 1;
    }

    printf("File copied successfully.\n");

    return 0;
}