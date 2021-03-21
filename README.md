# mammut_start_hack
Backend part of the MVP. It provides the only available analytics of the given h5 files:  
[*] Count of the climbs
[*] An average climbing speed m/s  
[*] An average number of the hand movements per minute
[*] Evaluation of the climber performance considering up flow and average time of the actions. Then it is re-scaled into a scale from 0 to 5 where 5 is the best performance.  
This metrics could be improved.  
# Execution  
To start the backend copy the data directory from the original git [https://github.com/START-Global/MAMMUT-STARTHACK21] and execute ```pip install -r requirements.txt``` then ```python main.py```