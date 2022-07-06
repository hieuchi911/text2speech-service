# Text-To-Speech-Service
Text to Speech service for chatbot used at CT Group

# Speech-To-Text-Service
Here lives Text to speech (TTS) service for rasa chatbot at CT Group

## I. Notebook `test-sanic-service.ipynb`:
contains code for:
- load and test tts models
- testing sanic app that serve text2speech model

## II. Other python files:
contain sanic app that serves TTS model:
- `app.py` serves vietTTS TTS model (Duration model + Acoustic model + HiFiGAN vocoder)
- Preparation steps before running sanic app:
  - run bash file that lives in `vietTTS/scripts`: go to `vietTTS` and run command: `bash scripts/quick_start.sh`. This will download checkpoints from huggingface and store them in `vietTTS/assets/infore/nat` and `vietTTS/assets/infore/hifigan`
  - create folder: `audio/` to store audio generated by model inference

To host these sanic services on host machine, execute following command:
  >```
  > python -m sanic <name of file that stores sanic app, e.g if file named app_opus.py, type 'app_opus'>:<name of Sanic object defined in python file> -H <host address> -p <listening port>
  >```

## III. Docker:
- dockerfile in this repo builds docker image that holds:
  - environment (requirements.txt) runnable for text2speech service
  - app.py that stores code to host sanic service
  - vietTTS codes for loading model and perform inference and the models themselves
- docker image: hieuchi911/text2speech-service:with-ckpts
- **Building docker image**: docker image should be built from this repo (files and folders needed `dockerfile`, `.dockerignore`, `requirements.txt`, `app.py`, and `vietTTS/` folder that stores models that has already been downloaded by running bash file `vietTTS/scripts/quick_start.sh`)
- to run the docker service:
  - created a docker named volume: `docker volume create <volume name>`. This creates a binding directory between host machine and the container's working directory, and later when output audio saved to container's working directory, the audio will lives in the host machine as well
  - run the image, binding the container's working directory to the newly created docker volume
  - run sanic service in the container (either via `CMD` in dockerfile or provide command at `container run`)
  - these steps is shown in following example:
    >```
    > sudo docker run --name text2speech-service -p 8001:8000 -v tts-vol:/python-docker/ hieuchi911/text2speech-service:with-ckpts python -m sanic app:app -H 0.0.0.0 -p 8000
    >```
    ,where:
    - `-v tts-vol:/python-docker/` maps docker volume `tts-vol` to the container's working directory (`/python-docker/`)
    - `python -m sanic app:app -H 0.0.0.0 -p 8000` runs sanic service to listen at port 8000 in the container at container startup. This command is optional since the defined dockerfile already defines this at `CMD` instruction, port specified is 5352 instead of 8000 (the python command in dockerfile wont run since it's overwritten by the python command defined at `docker run`, according to https://docs.docker.com/engine/reference/run/#cmd-default-command-or-options)
    - `-p 8001:8000` maps port `8000` in container to port `8001` in local machine, so requests from outside should be sent to port `8001`
  - Example above corresponds to following docker-compose service block:
    >```
    >text2speech-service:
    >    image: "hieuchi911/text2speech-service:with-ckpts"
    >    expose:
    >       - 8001
    >    volumes:
    >       - tts-vol:/python-docker
    >    command: ["python", "-m", "sanic", "app:app", "-H", "0.0.0.0", "-p", "8000"]
    >```
    - later when running inference, output audio is in the volume created before (in the example, `tts-vol`). Run `docker inspect` and path to the volume is at Mountpoint key:
    >```
    >$ sudo docker volume inspect tts-vol
    >[
    >    {
    >        "CreatedAt": "2022-07-06T08:42:40+07:00",
    >        "Driver": "local",
    >        "Labels": {},
    >        "Mountpoint": "/var/lib/docker/volumes/tts-vol/_data",
    >        "Name": "tts-vol",
    >        "Options": {},
    >        "Scope": "local"
    >    }
    >]
    >```
