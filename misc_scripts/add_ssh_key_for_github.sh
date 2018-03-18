# source: 
# https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/

# generate new SSH key
ssh-keygen -t rsa -b 4096 -C $1

# add the SSH key to the ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/ssh/id_rsa

copy_to_clipboard() {
    sudo apt install xclip
    xclip -sel clip < ~/.ssh/id_rsa.pub

    echo "SSH Key is saved to clipboard. \nGo to Github > Settings > SSH and GPG keys > New SSH key"
}

copy_to_clipboard