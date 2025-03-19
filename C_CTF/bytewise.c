#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 64

void splitString(char string[], char *splittedString[]){
    char *token = strtok(string, "-");
    int index = 0;
    while (token != NULL) {
        splittedString[index++] = token;
        token = strtok(NULL, "-");
    }
}

void convertToHEX(char *stringArray[], unsigned char hexArray[]){
    for (int i=0; i<MAX; i++){
        hexArray[i] = strtol(stringArray[i], NULL, 16);
    }
}

void printArray(unsigned char *arr) {
    printf("CRYPTO24{");
    for (int i = 0; i < MAX-1; i++) {
        printf("%02x-", arr[i]);
    }
    printf("%02x", arr[MAX-1]);
    printf("}\n");
}

void bitwiseOR(unsigned char n1[], unsigned char n2[], unsigned char *res){
    for (int i = 0; i < MAX; i++) {
        res[i] = n1[i] | n2[i];
    }
}

void bitwiseAND(unsigned char n1[], unsigned char n2[], unsigned char *res){
    for (int i = 0; i < MAX; i++) {
        res[i] = n1[i] & n2[i];
    }
}

void bitwiseXOR(unsigned char n1[], unsigned char n2[], unsigned char *res){
    for (int i = 0; i < MAX; i++) {
        res[i] = n1[i] ^ n2[i];
    }
}

int main() {

    // CRYPTO24{f1-3e-b5-b2-9f-9f-9e-87-58-bb-09-8c-fe-f0-03-d9-0b-79-bb-75-a5-52-ca-35-65-30-32-55-7b-c6-b7-6b-7b-5f-88-00-61-20-b5-66-bb-2d-f2-1e-54-d4-2f-31-59-8b-76-bc-f9-5c-20-59-da-26-47-14-5f-75-b5-86}

    char r1[] = "63-3b-6d-07-65-1a-09-31-7a-4f-b4-aa-ef-3f-7a-55-d0-33-93-52-1e-81-fb-63-11-26-ed-9e-8e-a7-10-f6-63-9d-eb-92-90-eb-76-0b-90-5a-eb-b4-75-d3-a1-cf-d2-91-39-c1-89-32-84-22-12-4e-77-57-4d-25-85-98";
    char r2[] = "92-05-d8-b5-fa-85-97-b6-22-f4-bd-26-11-cf-79-8c-db-4a-28-27-bb-d3-31-56-74-16-df-cb-f5-61-a7-9d-18-c2-63-92-f1-cb-c3-6d-2b-77-19-aa-21-07-8e-fe-8b-1a-4f-7d-70-6e-a4-7b-c8-68-30-43-12-50-30-1e";
    char *r1_splitted[MAX];
    char *r2_splitted[MAX];

    splitString(r1, r1_splitted);
    splitString(r2, r2_splitted);

    unsigned char rand1[MAX];
    unsigned char rand2[MAX];

    convertToHEX(r1_splitted, rand1);
    convertToHEX(r2_splitted, rand2);

    unsigned char k1[MAX];
    unsigned char k2[MAX];
    unsigned char key[MAX];

    bitwiseOR(rand1, rand2, k1);
    bitwiseAND(rand1, rand2, k2);
    bitwiseXOR(k1, k2, key);

    printArray(key);
    
    return 0;
}