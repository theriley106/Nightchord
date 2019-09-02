if which sox; then
    if [ ! -f .installCompleted ]; then
		pip install -r simple_requirements.txt
	    if python -c "import moviepy;import requests;import bs4;" ; then
	   		touch .installCompleted
		fi
		else
		    echo "Dependencies already installed - starting nightcore generator"
	fi

	python simple.py
else
    echo 'SOX IS NOT INSTALLED'
    echo "Download sox and rerun simple.sh"
fi

