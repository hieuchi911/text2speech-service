if [ ! -f assets/infore/hifigan/g_00800000 ]; then
  pip3 install gdown
  echo "Downloading models..."
  mkdir -p -p assets/infore/{nat,hifigan}
  gdown --id 16UhN8QBxG1YYwUh8smdEeVnKo9qZhvZj -O assets/infore/nat/duration_latest_ckpt.pickle
  gdown --id 1-8Ig65S3irNHSzcskT37SLgeyuUhjKdj -O assets/infore/nat/acoustic_latest_ckpt.pickle
  gdown --id 10SFOlAduG20TdjGC5e1Jod_vJIpxkD6u -O assets/infore/hifigan/g_00800000
  python -m vietTTS.hifigan.convert_torch_model_to_haiku --config-file=assets/hifigan/config.json --checkpoint-file=assets/infore/hifigan/g_00800000
fi