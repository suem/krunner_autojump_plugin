echo "installing autojump krunner plugin"
plasmapkg --type runner -install krunner_autojump_plugin.zip
echo "restarting krunner..."
kquitapp krunner
sleep 3
krunner
