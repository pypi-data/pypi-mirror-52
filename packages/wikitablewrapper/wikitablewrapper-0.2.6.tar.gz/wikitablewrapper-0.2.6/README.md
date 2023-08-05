# wikitablewrapper


**Install virtual ennvironment of python3**
```sh
sudo apt-get install curl
sudo apt install python3-pip
sudo apt install virtualenv
virtualenv env --python=python3
cd env && source bin/activate
```

**Install dependencies**
```sh
pip3 install simplejson
pip3 install xmltodict
```

**Install locally DBpedia Spotlight**
Ubuntu
```sh
sudo snap install docker
```
or Debian
```sh
wget https://download.docker.com/linux/debian/dists/jessie/pool/stable/amd64/docker-ce_17.03.0~ce-0~debian-jessie_amd64.deb
sudo dpkg -i docker-ce_17.03.0~ce-0~debian-jessie_amd64.deb
```

See if you have the image already in your computer
```sh
sudo docker image ls
```
if you don't have it, then run
```sh
sudo docker pull dbpedia/spotlight-english
sudo docker run -d -p 2222:80 dbpedia/spotlight-english spotlight.sh
```

If you have to stop it, see the CONTAINER ID, and then do it
```sh
sudo docker container ls
sudo docker stop CONTAINER_ID
```
test it
> curl http://localhost:2222/rest/annotate   -H "Accept: application/json"   --data-urlencode "text=Brazilian state-run giant oil company Petrobras signed a three-year technology and research cooperation agreement with oil service provider Halliburton."   --data "confidence=0.3"   --data "support=20"

**To install this package, just run:**
```sh
pip3 install -i https://test.pypi.org/simple/ wikitablewrapper
```


# How use it?


```python
wt = WikitableWrapper(20)
wt.createHtmlFile = True

wt.includeBabelfy = True
wt.includeTagme = True
wt.includeFremeNer = True
wt.includeDBpediaSpotlightLocal = True

# you can do, either
wt.outputFolder="1Out"  # Optional
wt.processJson("1Tablas/1003231_2.json")

# or
wt.ProcessFolderOfJson("100Tablas","100Out")
```

See below an example of how use the Benchamrk class

```python
wb = WikitableBenchmark()
dSys = {"Babelfy":"_babelfy", "TagME":"_tagme", "FremeNER":"_fremener", "DBpedia Spotlight":"_dbpst"}
wb.MeasureF1_and_Summarize("100Tablas","100Out", dSys, "100Benchmark")
```
