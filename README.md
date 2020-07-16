# INSTALL
## Docker
Run `docker run --publish 8080:5000 --detach --name snapgene-submit-plug synbiohub/plugin-submit-snapgene:snapshot` Check it is up using localhost:8080/dnasubmit/status

## Python
Using python run `pip install -r requirements.txt` to install the requirements.
then run `FLASK_APP=Snapgene_Submit_v002_20200127 python -m flask run`.
A flask module will run at localhost:5000/dnasubmit/.
