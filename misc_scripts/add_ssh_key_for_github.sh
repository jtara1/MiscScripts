# source: 
# https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/

comment=$1
if [ "$comment" == "" ]; then
    comment="github"
fi

# generate new SSH key
ssh-keygen -t rsa -b 4096 -C $comment

# add the SSH key to the ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/ssh/id_rsa

copy_to_clipboard() {
    sudo apt install xclip
    xclip -sel clip < ~/.ssh/id_rsa.pub

    echo "SSH Key is saved to clipboard. Go to Github > Settings > SSH and GPG keys > New SSH key"
    echo 'https://github.com/settings/keys'
}

copy_to_clipboard
