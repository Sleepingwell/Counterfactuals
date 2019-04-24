alias patsrv='docker run -it --rm -v "$(pwd)":/pat -p 8888:8888 pat'
alias patshell='docker run -it --rm -v "$(pwd)":/pat --user "$(id -u)":"$(id -g)" -e DISPLAY="$DISPLAY" -v /tmp/.X11-unix:/tmp/.X11-unix:ro --entrypoint bash --workdir /pat/package pat'
alias pattest='docker run -it --rm -v "$(pwd)":/pat --entrypoint python --workdir /pat/package pat -m pytest'
alias patenvroot='docker run -it --rm --entrypoint bash --workdir /pat pat'
