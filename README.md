# xpert
Anyone finds himself or herself an expert of something

## How to start
1. Clone this repo into your local folder.
1. Update all submodules
   + `git submodule update --init --recursive`
1. If you want to develop something, ensure you get the latest _juice_ :
   + `git submodule foreach --recursive "(git remote -v; git checkout master; git pull; echo ...)"`
