#include <openssl/bn.h>
#include <string.h>
#include <ctype.h>

int main(void) {

  char hex_num1[] = "009eee82dc2cd4a00c4f5a7b8663b0c1ed0677fcebde1a235df4c3ff876a7dadc607faa835f6ae0503573e223676d50d574f99f958ad637ae745a6aafa023423b69d34157b1141b6b1cab91acd2955bd42f504abdf454a9d4eca4e01f9f8745967eeb6a9fb96b7c09400178a530eb6d831c968e66438d3633a04d7886bf0e1ad607f41bd857bd904e1975b1f9b05ceac2cc4553fb48b894d0a509a094e5e8f5b5f5569725f049b3a8a09b47f8db2ca520e5ebff4b0eec9badc934f6dd31f821ad9fc2ca73f18230dd744c728546784ee739265f01ce81e6d4d9565b4c84fb80462582bee3264a0a7dc99250e505376bc30db715e93d69f1f881c765d82c8593951";

  char hex_num2[] = "00d2c601326b4c4b855f527bb78ed68ae4c8767e6bc9249a3ecacd2fc9b875d4f97111e1cfbe62d32c5ff9fd9bfaed62f3df44c757fbee9bb232cb5449296c692e301d8c1ffab18ee44966c1fb927c82ca60c940a40ab2db50ecf6ff98a71623388d06d27ca9858ac22b4dd4e6f189e5b04254a05f3cddc764330511fbee8b2607";

  BIGNUM *num1 = BN_new();
  BIGNUM *num2 = BN_new();

  BN_hex2bn(&num1, hex_num1);
  BN_hex2bn(&num2, hex_num2);

  printf("Size of num1: %lu\n", BN_num_bytes(num1));
  printf("Size of num2: %lu\n", BN_num_bytes(num2));
  printf("\n");

  if(BN_check_prime(num1,NULL,NULL)){
    printf("num1 is a prime\n");
  }
  else{
    printf("num1 isn't a prime\n");
  }

  if(BN_check_prime(num2,NULL,NULL)){
    printf("num2 is a prime\n");
  }
  else{
    printf("num2 isn't a prime\n");
  }

  BN_CTX *ctx = BN_CTX_new();
  BIGNUM *res = BN_new();
  BIGNUM *rem = BN_new();

  BN_div(res, rem, num1, num2, ctx);

  printf("\n");
  printf("num1 / num2\n");
  printf("res:\n");
  BN_print_fp(stdout, res);
  printf("\n");
  printf("rem:\n");
  BN_print_fp(stdout, rem);
  printf("\n");

  if(BN_check_prime(res,NULL,NULL)){
    printf("res is a prime\n");
  }
  else{
    printf("res isn't a prime\n");
  }

  printf("size of res: %lu\n", BN_num_bytes(res));

  char *res_hex = BN_bn2hex(res);
  printf("Solution:\n");
  printf("CRYPTO24{00:");
  for(int i = 0; i < strlen(res_hex)-2; i+=2){
    printf("%c%c:", tolower(res_hex[i]), tolower(res_hex[i+1]));
    // printf("%c%c:", res_hex[i], res_hex[i+1]);
  }
  printf("%c%c}\n", tolower(res_hex[strlen(res_hex)-2]), tolower(res_hex[strlen(res_hex)-1]));

  return 0;
}