#!/bin/bash
### 0xc4s OpenSSL bruter for HTB's 'Hawk'

# Declare wordlists
# Declare array of possible ciphers (based on common ones from 'openssl help')
ciphers=(
    -aes-256-cbc
)

# Loop through ciphers
echo "TRYING CIPHER: $cipher"

# Loop through wordlist
while read passTry; do
  openssl enc -d -a -aes-256-cbc -k $passTry -in hash.txt -out tmp &>/dev/null

  if [ $? -eq 0 ]; then
    echo "PASSWORD FOUND!"
    echo "Pass is: $passTry"
    echo "===DECRYPTED TEXT BELOW==="
    cat tmp
    echo "===END DECRYPTED TEXT==="
    # For Hawk, it gets the correct password on first try
    # However, a 0-exit code doesn't always mean getting the key right
    # As such, don't exit (spam alert!)
    #exit 0
  fi
  rm tmp

done < /usr/share/wordlists/rockyou.txt

rm tmp
