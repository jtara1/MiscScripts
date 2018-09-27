#!/usr/bin/env bash
#### Environment Variables #####
export GITHUB=~/_Github-Projects
export SCRIPTS=$GITHUB/misc_scripts/misc_scripts
export GOPATH=~/lib/go
export GOBIN=/opt/go-bin

#### Aliases #####
alias tagnext="$GITHUB/misc_scripts/misc_scripts/DevOps/create_and_push_next_tag.sh"
#alias ytdl="youtube-dl"
alias mkvenv="virtualenv --python=python3 venv"
alias venv=". ./venv/bin/activate"
alias pycharm="pycharm-professional | pycharm-community"

#### Functions ####
pypi () {
    echo "Upload from $PWD to pypi using python3 [y/n]"
    read answer
    if [ "$answer" = "y" ]
    then
        UPLOAD_PYPI="$SCRIPTS/DevOps/upload_pypi.sh"
        chmod +x $UPLOAD_PYPI
        $UPLOAD_PYPI
    fi
}

getTime() {
    python3 -c "print(int(__import__('time').time()))"
}

multiplyFile() {
    for (( i=1; i<=$2; i++))
    do
        filename="$i-$(getTime)-$1"
        cp $1 $filename;
        echo $filename
    done
}
alias multi=multiplyFile

getDateDaysAgo() {

}