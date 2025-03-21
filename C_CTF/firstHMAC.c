#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/err.h>
#include <string.h>

#define MAXBUF 3000

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char **argv){

    // ./a.out file.txt file2.txt
    // CRYPTO24{9453ac565269a96ea3ea583b15b410111b42ae03d1054a02fe4ba4b1029734d3}

    unsigned char key[] = "keykeykeykeykeykey";

    unsigned char finalString[MAXBUF];

    strcpy(finalString, key);

    if (argc != 3){
        fprintf(stderr, "Invalid parameters. Usage: %s filename1 filename2 \n", argv[0]);
        exit(1);
    }

    FILE *f_in1, *f_in2;
    if ((f_in1 = fopen(argv[1], "r")) == NULL){
        fprintf(stderr, "Couldn't open the input file, try again\n");
        exit(1);
    }
    if ((f_in2 = fopen(argv[2], "r")) == NULL){
        fprintf(stderr, "Couldn't open the input file, try again\n");
        exit(1);
    }

    // EVP_MD_CTX *EVP_MD_CTX_new(void);
    // pedantic mode? Check if md == NULL
    EVP_MD_CTX *hmac_ctx = EVP_MD_CTX_new();

    // int EVP_DigestInit(EVP_MD_CTX *ctx, const EVP_MD *type);
    //  int EVP_DigestInit_ex(EVP_MD_CTX *ctx, const EVP_MD *type, ENGINE *impl);
    //  Returns 1 for success and 0 for failure.
    EVP_PKEY *hkey;
    hkey = EVP_PKEY_new_mac_key(EVP_PKEY_HMAC, NULL, key, strlen(key));

    if (!EVP_DigestSignInit(hmac_ctx, NULL, EVP_sha256(), NULL, hkey))
        handle_errors();

    size_t n, m;
    unsigned char buffer1[MAXBUF];
    unsigned char buffer2[MAXBUF];

    while ((n = fread(buffer1, 1, MAXBUF, f_in1)) > 0){
        if (!EVP_DigestSignUpdate(hmac_ctx, buffer1, n))
            handle_errors();
    }

    while ((m = fread(buffer2, 1, MAXBUF, f_in2)) > 0){
        if (!EVP_DigestSignUpdate(hmac_ctx, buffer2, m))
            handle_errors();
    }

    unsigned char hmac_value[EVP_MD_size(EVP_sha256())];
    size_t hmac_len = EVP_MD_size(EVP_sha256());

    // int EVP_DigestFinal_ex(EVP_MD_CTX *ctx, unsigned char *md, unsigned size_t *s);
    //  EVP_DigestSignFinal(hmac_ctx, NULL, &hmac_len);
    if (!EVP_DigestSignFinal(hmac_ctx, hmac_value, &hmac_len))
        handle_errors();

    // void EVP_MD_CTX_free(EVP_MD_CTX *ctx);
    EVP_MD_CTX_free(hmac_ctx);

    // printf("The HMAC is: ");
    // for (int i = 0; i < hmac_len; i++)
    //     printf("%02x", hmac_value[i]);
    // printf("\n");

    printf("CRYPTO24{");
    for (int i = 0; i < hmac_len; i++)
        printf("%02x", hmac_value[i]);
    printf("}\n");

    return 0;
}