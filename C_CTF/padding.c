#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>


#define ENCRYPT 1
#define DECRYPT 0

int main(){

    // CRYPTO24{EVP_CIPHER_CTX_set_padding(ctx,0);}
    
    unsigned char key[] = "0123456789ABCDEF";
    unsigned char iv[]  = "1111111111111111";

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_CipherInit(ctx,EVP_aes_128_cbc(), key, iv, ENCRYPT);

    EVP_CIPHER_CTX_set_padding(ctx,0); //TO AVOID PADDING
    /*
        Enables or disables padding. This function should be called after the context is set up for encryption or decryption with EVP_CipherInit().
        By default encryption operations are padded using standard block padding and the padding is checked and removed when decrypting.
        If the pad parameter is zero then no padding is performed, the total amount of data encrypted or decrypted must then be a multiple of the block size or an error will occur.
    */

    unsigned char plaintext[] = "This is the plaintext to encrypt."; //len 33
    unsigned char ciphertext[48];

    int update_len, final_len;
    int ciphertext_len=0;

    EVP_CipherUpdate(ctx,ciphertext,&update_len,plaintext,strlen(plaintext));
    ciphertext_len+=update_len;
    printf("update size: %d\n",ciphertext_len);

    EVP_CipherFinal_ex(ctx,ciphertext+ciphertext_len,&final_len);
    ciphertext_len+=final_len;

    EVP_CIPHER_CTX_free(ctx);

    printf("Ciphertext lenght = %d\n", ciphertext_len);
    for(int i = 0; i < ciphertext_len; i++)
        printf("%02x", ciphertext[i]);
    printf("\n");

    OpenSSL_add_all_algorithms();

    return 0;
}

