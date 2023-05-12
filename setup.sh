#!/usr/bin/env bash


directory_change(){
    cd "$1" 
    echo "Changing directory to $(pwd)"
    # if linux use bash if mac use zsh
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        exec bash
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        exec zsh
    fi
    exit 0

}

"${@:1}" "${@:3}"


mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = 8501\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml


