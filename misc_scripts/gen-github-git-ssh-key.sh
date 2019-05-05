function main() {
    echo "generating key for email: $1"
    email=$1
    
    if [[ $email == "" ]]
    then
        echo 1st arg needs to be email used for github or git
        exit
    fi
    
    ssh-keygen -t rsa -b 4096 -C $email

    private_key=~/.ssh/id_rsa
    echo "ssh private key: $private_key"
    
    eval "$(ssh-agent -s)"
    ssh-add $private_key
    
    # attempt to install program and use it to copy text to clipboard
    sudo apt-get install xclip # debian package manager needed & linux only
    
    public_key="${private_key}.pub"
    xclip -sel clip < $public_key

    echo
    cat $public_key
    echo
    
    echo the public key above copied to clipboard
    echo "add at"
    echo "https://github.com/settings/keys"
}

main $@
    
    
    
