#~/darknet/build/darknet detector train ../cfgs/001-v4.data ../cfgs/001-v4.cfg ../backups/000-backup/000-v4_best.weights -map -gpus 0,1 -clear -dont_show -mjpeg_port 8090
~/darknet/build/darknet detector train ../cfgs/001-v4.data ../cfgs/001-v4.cfg ../backups/001-backup/001-v4_last.weights -map -gpus 0,1 -dont_show -mjpeg_port 8090
