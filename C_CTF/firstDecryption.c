#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/err.h>

#define ENCRYPT 1
#define DECRYPT 0
#define MAX_BUFFER 1024

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char **argv){

    // echo "jyS3NIBqen2CWpDI2jkSu+z93NkDbWkUMitg2Q==" | openssl base64 -d > in.txt
    // ./a.out in.txt 0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF 11111111111111112222222222222222 out.txt

    // CRYPTO24{MyDecryptedString}
    
    if (argc != 5){
        fprintf(stderr, "Invalid parameters. Usage: %s file_in key iv file_out\n", argv[0]);
        exit(1);
    }

    FILE *f_in;
    if ((f_in = fopen(argv[1], "r")) == NULL){
        fprintf(stderr, "Couldn't open the input file, try again\n");
        abort();
    }

    if (strlen(argv[2]) != 64){
        fprintf(stderr, "Wrong key length\n");
        abort();
    }
    if (strlen(argv[3]) != 32){
        fprintf(stderr, "Wrong IV length\n");
        abort();
    }

    FILE *f_out;
    if ((f_out = fopen(argv[4], "wb")) == NULL){
        fprintf(stderr, "Couldn't open the output file, try again\n");
        abort();
    }

    unsigned char key[strlen(argv[2]) / 2];
    for (int i = 0; i < strlen(argv[2]) / 2; i++){
        sscanf(&argv[2][2 * i], "%2hhx", &key[i]);
    }

    unsigned char iv[strlen(argv[3]) / 2];
    for (int i = 0; i < strlen(argv[3]) / 2; i++){
        sscanf(&argv[3][2 * i], "%2hhx", &iv[i]);
    }

    /* Load the human readable error strings for libcrypto */
    ERR_load_crypto_strings();
    /* Load all digest and cipher algorithms */
    OpenSSL_add_all_algorithms();

    // pedantic mode: check NULL
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    if (!EVP_CipherInit(ctx, EVP_chacha20(), key, iv, DECRYPT))
        handle_errors();

    int length;
    unsigned char plaintext[MAX_BUFFER];

    int n_read;
    unsigned char buffer[MAX_BUFFER];

    while ((n_read = fread(buffer, 1, MAX_BUFFER, f_in)) > 0){
        // printf("n_Read=%d-", n_read);
        if (!EVP_CipherUpdate(ctx, plaintext, &length, buffer, n_read))
            handle_errors();
        // printf("length=%d\n", length);
        
        if (fwrite(plaintext, 1, length, f_out) < length){
            fprintf(stderr, "Error writing the output file\n");
            abort();
        }
    }

    if (!EVP_CipherFinal_ex(ctx, plaintext, &length))
        handle_errors();

    EVP_CIPHER_CTX_free(ctx);

    fclose(f_in);
    fclose(f_out);

    printf("File decrypted!\n");

    printf("%s\n",plaintext);

    // completely free all the cipher data
    CRYPTO_cleanup_all_ex_data();
    /* Remove error strings */
    ERR_free_strings();

    return 0;
}