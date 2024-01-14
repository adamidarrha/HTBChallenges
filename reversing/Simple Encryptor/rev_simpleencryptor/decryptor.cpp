#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file = fopen("flag.enc", "rb");
    if (file == NULL) {
        printf("Could not open file flag.enc\n");
        return 1;
    }

    unsigned int seed;
    size_t bytesRead = fread(&seed, sizeof(unsigned int), 1, file);
    if (bytesRead != 1) {
        printf("Could not read seed from file\n");
        return 1;
    }

    srand(seed);

    // Get the file size
    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file) - sizeof(unsigned int);
    fseek(file, sizeof(unsigned int), SEEK_SET);

    // Allocate memory for the file data
    unsigned char *fileDataPointer = (unsigned char *)malloc(fileSize);
    if (fileDataPointer == NULL) {
        printf("Could not allocate memory for file data\n");
        return 1;
    }

    // Read the file data
    bytesRead = fread(fileDataPointer, 1, fileSize, file);
    if (bytesRead != fileSize) {
        printf("Could not read file data\n");
        return 1;
    }

    for (long i = 0; i < fileSize; i++) {
    // Generate the same random numbers in the same sequence
    unsigned char firstRandomNumber = rand();
    unsigned int secondRandomNumber = rand();
    secondRandomNumber = secondRandomNumber & 7;

    // Reverse the bit rotation
    unsigned char originalByte = fileDataPointer[i];
    originalByte = originalByte >> secondRandomNumber | originalByte << (8 - secondRandomNumber);

    // Reverse the XOR operation
    fileDataPointer[i] = originalByte ^ firstRandomNumber;
}

    // Open the output file
    FILE *outputFile = fopen("flag", "wb");
    if (outputFile == NULL) {
        printf("Could not open output file\n");
        return 1;
    }

    // Write the data to the output file
    size_t bytesWritten = fwrite(fileDataPointer, 1, fileSize, outputFile);
    if (bytesWritten != fileSize) {
        printf("Could not write data to output file\n");
        return 1;
    }

    // Close the output file
    fclose(outputFile);

    free(fileDataPointer);
    fclose(file);
    return 0;
}