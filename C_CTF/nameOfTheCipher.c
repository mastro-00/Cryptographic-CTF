#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/err.h>

#define ENCRYPT 1
#define DECRYPT 0
#define MAX_BUFFER 1024

void handle_errors()
{
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char **argv)
{
    //CRYPTO24{EVP_get_cipherbyname}

    // ./a.out in.txt 0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF 11111111111111112222222222222222 out.txt aes-128-cbc
    // openssl enc -d -aes-128-cbc -in out.txt -K 0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF -iv 11111111111111112222222222222222
    
    // argy[1] -> input file
    // argv[2] -> key
    // argv[3] -> iv
    // argv[4] -> file output
    // argv[5] -> enc_algorithm
 

    if (argc != 6){
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

    if (!EVP_CipherInit(ctx, EVP_get_cipherbyname(argv[5]), key, iv, ENCRYPT))
        handle_errors();

    int length;
    unsigned char ciphertext[MAX_BUFFER + 16];

    int n_read;
    unsigned char buffer[MAX_BUFFER];

    while ((n_read = fread(buffer, 1, MAX_BUFFER, f_in)) > 0){
        printf("n_Read=%d-", n_read);
        if (!EVP_CipherUpdate(ctx, ciphertext, &length, buffer, n_read))
            handle_errors();
        printf("length=%d\n", length);
        if (fwrite(ciphertext, 1, length, f_out) < length){
            fprintf(stderr, "Error writing the output file\n");
            abort();
        }
    }

    if (!EVP_CipherFinal_ex(ctx, ciphertext, &length))
        handle_errors();

    printf("lenght=%d\n", length);

    if (fwrite(ciphertext, 1, length, f_out) < length){
        fprintf(stderr, "Error writing in the output file\n");
        abort();
    }

    EVP_CIPHER_CTX_free(ctx);

    fclose(f_in);
    fclose(f_out);

    printf("File encrypted!\n");

    // completely free all the cipher data
    CRYPTO_cleanup_all_ex_data();
    /* Remove error strings */
    ERR_free_strings();

    return 0;
}