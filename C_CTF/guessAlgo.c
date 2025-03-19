#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/err.h>

#define ENCRYPT 1
#define DECRYPT 0
#define MAX_BUFFER 4000

void handle_errors(int i){
    printf("i: %d \n",i);
    ERR_print_errors_fp(stderr);
    //abort();
}

int main(int argc, char **argv){

    //  int EVP_CipherInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type, const unsigned char *key, const unsigned char *iv, int enc);
    //  int EVP_CipherUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl, const unsigned char *in, int inl);
    //  int EVP_CipherFinal(EVP_CIPHER_CTX *ctx, unsigned char *outm, int *outl);

    // echo "ZZJ+BKJNdpXA2jaX8Zg5ItRola18hi95MG8fA/9RPvg=" | openssl base64 -d > in.txt
    // ./a.out in.txt out.txt cipher.txt

    // Cipher List from: "openssl enc -d -list"
    // Algo: aria-128-cbc - Out: H1d1ng4lgo1sUs3l3ss-
    // aria-128-cbc -> EVP_aria_128_cbc()

    //CRYPTO24{H1d1ng4lgo1sUs3lEVP_aria_128_cbc}

    unsigned char key [] = "0123456789ABCDEF";
    unsigned char iv [] = "0123456789ABCDEF";

    FILE *f_in;
    if ((f_in = fopen(argv[1], "r")) == NULL){
        fprintf(stderr, "Couldn't open the input file, try again\n");
        abort();
    }

    FILE *f_out;
    if ((f_out = fopen(argv[2], "wb")) == NULL){
        fprintf(stderr, "Couldn't open the output file, try again\n");
        abort();
    }

    FILE *f_cipher;
    if ((f_cipher = fopen(argv[3], "r")) == NULL){
        fprintf(stderr, "Couldn't open the output file, try again\n");
        abort();
    }

    int j=0;
    unsigned char lineIn[30], *ciphers[149];

    while (fgets(lineIn, sizeof(lineIn), f_cipher) != NULL && j < 149) {
        lineIn[strcspn(lineIn, "\n")] = 0; // Remove the newline character if present
        ciphers[j] = malloc(strlen(lineIn) + 1); // Allocate memory for the string
        strcpy(ciphers[j], lineIn); // Copy the string into the ciphers
        j++;
    }

    /* Load the human readable error strings for libcrypto */
    ERR_load_crypto_strings();

    char lineOut[100];
    unsigned char encryptedString[MAX_BUFFER];
    unsigned char decrypted[MAX_BUFFER];

    int n_read = fread(encryptedString, 1, MAX_BUFFER, f_in);
    printf("Encrypted String: %s", encryptedString);

    for (int i=0; i<149; i++){

        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

        //if (!EVP_CipherInit(ctx, EVP_aria_128_cbc(), key, iv, DECRYPT))
        if (!EVP_CipherInit(ctx, EVP_get_cipherbyname(ciphers[i]), key, iv, DECRYPT))
            handle_errors(i);

        int update_len, final_len;
        int decrypted_len=0;
        
        //printf("n_Read=%d-", n_read);
        if (!EVP_CipherUpdate(ctx, decrypted, &update_len, encryptedString, n_read))
            handle_errors(i);
        decrypted_len+=update_len;
        //printf("update size: %d\n",decrypted_len);

        if (!EVP_CipherFinal_ex(ctx, decrypted+decrypted_len, &final_len))
            handle_errors(i);
        decrypted_len+=final_len;

        EVP_CIPHER_CTX_free(ctx);

        //printf("Decrypted lenght = %d\n",decrypted_len);

        sprintf(lineOut, "Algo: %s - Out: %s\n", ciphers[i], decrypted);
        fprintf(f_out, "%s", lineOut);
        
    }

    /*
        for(int i = 0; i < decrypted_len; i++)
            printf("%2x", decrypted[i]);
        printf("\n");
        for(int i = 0; i < decrypted_len; i++)
            printf("%c", decrypted[i]);
        printf("\n");
    */

    fclose(f_in);
    fclose(f_out);

    printf("File decrypted!\n");

    /* Remove error strings */
    ERR_free_strings();

    return 0;
}