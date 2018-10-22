void main(/*isso nao importa rsrs*/)
{
    /* este programa deveria passar normalmente pela compilacao,
       apresentando apenas um erro no momento de execucao pela atribuicao
       de uma variavel muito grande para um char */

    char joAuUU1;
    int k04L4, R4BaN373_;

    joAuUU1 = 3;
    k04L4 =    2000  /* este numero e maior do que um char deveria
                        aceitar */;
    R4BaN373_ = 5 /* este valor eh aceitavel para um char; */ ;
    printf(joAuUU1);

    joAuUU1 = R4BaN373_; /* deveria aceitar */
    printf(joAuUU1);

    joAuUU1 = k04L4;  /* nao aceitavel!!! */
    printf(joAuUU1);
}
