# ascento aliases
alias cda='cd ~/catkin_ws/src/ascento'
alias cdc='cd ~/catkin_ws'
alias srcascento='source ~/catkin_ws/devel/setup.bash'
alias kg="killall -9 gazebo & killall -9 gzserver  & killall -9 gzclient"

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias srcbashrc='source ~/.bashrc'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
