#!/bin/bash
[ -f .env ] && export $(grep -v '^#' .env | xargs)
WHITE='\033[1;37m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' 

if ! command -v jq &> /dev/null; then
    echo -e "${RED}------------------------------------------${NC}"
    echo -e "${RED} ERROR: 'jq' is not installed.            ${NC}"
    echo -e "${RED} Please install it (sudo pacman -S jq)    ${NC}"
    echo -e "${RED}------------------------------------------${NC}"
    exit 1
fi

clear
echo -e "${WHITE}------------------------------------------${NC}"
echo -e "${WHITE}  SUBGIT BASH EDITION              ${NC}"
echo -e "${WHITE}------------------------------------------${NC}"

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "SESSION: ${RED}ANONYMOUS${NC}"
    AUTH_HEADER=""
else
    echo -e "SESSION: ${GREEN}AUTHENTICATED${NC}"
    AUTH_HEADER="Authorization: token $GITHUB_TOKEN"
fi

echo -ne "\n${WHITE}INPUT URL: ${NC}"
read REPO_URL

IFS='/' read -ra ADDR <<< "${REPO_URL#https://github.com/}"
USER=${ADDR[0]}
REPO=${ADDR[1]}
BRANCH=${ADDR[3]}
FOLDER_PATH=$(echo "${ADDR[@]:4}" | tr ' ' '/')

TARGET_DIR=$(basename "$FOLDER_PATH")
[ -z "$TARGET_DIR" ] && TARGET_DIR=$REPO

API_URL="https://api.github.com/repos/$USER/$REPO/contents/$FOLDER_PATH?ref=$BRANCH"

echo -e "${CYAN}SCANNING STRUCTURE...${NC}"

download_folder() {
    local url=$1
    local dest=$2
    mkdir -p "$dest"

    local response=$(curl -s -H "$AUTH_HEADER" "$url")
    
    echo "$response" | jq -c '.[]' | while read -r item; do
        local type=$(echo "$item" | jq -r '.type')
        local name=$(echo "$item" | jq -r '.name')
        
        if [ "$type" == "file" ]; then
            local dl_url=$(echo "$item" | jq -r '.download_url')
            echo -e "${BLUE}FETCHING${NC} $name"
            curl -s -L -H "$AUTH_HEADER" "$dl_url" -o "$dest/$name"
        elif [ "$type" == "dir" ]; then
            local sub_url=$(echo "$item" | jq -r '.url')
            download_folder "$sub_url" "$dest/$name"
        fi
    done
}

download_folder "$API_URL" "$TARGET_DIR"

echo -e "\n${GREEN}COMPLETED${NC}"
echo -e "${WHITE}PATH:${NC} $(pwd)/$TARGET_DIR"