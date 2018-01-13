# Author: github.com/jtara1
# Source: https://github.com/jtara1/misc_scripts
# Description: Create the next git tag and push the tag
# Follows the version schema of MAJOR.MINOR.PATCH
# Uses numbers and "." character exclusively in tag
# creation and regex matching of previous tag
# Arguments: Increments PATCH by default or MAJOR or MINOR
# with --major or --minor cli args respectively
# Passes any other arguments to `git tag MAJOR.MINOR.PATCH`

# avoid overwriting the file just in-case another program 
# uses this file
temp_file="git_tags.tmp"
if [ -e "$temp_file" ]; then
	echo "Warning: $temp_file already exists and I don't 
	want to overwrite it."
	exit
fi

# write output of `git tag` to file
(git tag) > $temp_file
# read last line of tags (most recent tag)
tag=$(tail -n 1 $temp_file)
rm $temp_file  # remove temp file

echo "Most recent tag: $tag"

if [ "$tag" == "" ]; then
	echo "There are no tags for this project or 
the working directory does not have git setup"
	exit
fi

length=${#tag}
next_number_regex="[0-9]*\."
# index after first "." character
major_end=$(expr match $tag $next_number_regex) 
major=${tag:0:major_end-1}

remainder=${tag:major_end:length}
# index after second "." character
minor_end=$(expr match $remainder $next_number_regex)
minor=${remainder:0:minor_end-1}

patch=${remainder:minor_end:length}

args_length=$#
# increment major
if [ "$1" == "--major" ]; then
	major=$(expr $major + 1)
	minor="0"
	patch="0"
	cli_args=${@:7:args_length}
# increment minor
elif [ "$1" == "--minor" ]; then
	minor=$(expr $minor + 1)
	patch="0"
	cli_args=${@:7:args_length}
# increment patch
else
	cli_args=$@
	patch=$(expr $patch + 1)
	cli_args=$@
fi

new_tag=$(printf "%s.%s.%s" $major $minor $patch)

echo "Create tag: $new_tag ? [enter/n]"
read answer

# create and push new_tag if user accepts it
if [ "$answer" == "" ]; then
	git tag $new_tag $cli_args
	echo "Push tag: $new_tag ? [enter/n]"
	read answer
	if [ "$answer" == "" ]; then
		git push --tag
	fi
fi