# Data Converter

## Download EPL Twitter datas from AWS server

```sh
# download Game Week 11 (GW11)
$ scp -r -i ~/.ssh/bya-aws.pem ubuntu@54.92.75.228:/home/ubuntu/datas/GW11/ ~/Dropbox/Research/datas
game1.txt                               100%  245MB   2.9MB/s   01:26
game8.txt                               100%   20MB   3.4MB/s   00:06
game9.txt                               100%   16MB   2.6MB/s   00:06
game10.txt                              100%   53MB   2.6MB/s   00:20
game2_7.txt                             100%  224MB   3.6MB/s   01:02
```


## Convert JSON file to Text file

Only extract ['text', 'date', 'user', 'tags'] from every Tweet.
```sh
# extract Game Week 11
$ /Users/Bya/.virtualenvs/py3/bin/python ~/git/predictEPL/DataConverter/JSON_to_CSV.py 11
```
