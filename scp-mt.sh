scp -P 23456 -o 'ProxyCommand ssh liling@login.coli.uni-saarland.de nc %h %p 2>/dev/null' usaarhat@localhost:/home/ussarhat/testing/from_usaar_to_laptop.txt .

scp -P 23456 -o 'ProxyCommand ssh liling@login.coli.uni-saarland.de nc %h %p 2>/dev/null' from_laptop_to_usaar.txt usaarhat@localhost:/home/usaarhat/testing/

