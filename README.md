# helpmanual.io

Tools for building [helpmanual.io](https://helpmanual.io).


To deploy

```
source env/bin/activate
./src/50_build_site.py
aws s3 sync site/ s3://helpmanual.io/ --region us-east-1 --delete
```
