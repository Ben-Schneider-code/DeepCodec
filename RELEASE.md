## Release Build Steps

TODO: script this all out

- run the docker container interactively -- many need to change manylinux dist for different hardware - need apt support to get x264 and x265
`docker pull quay.io/pypa/manylinux_2_24_aarch64`
`docker run --rm -it -v $(pwd):/project quay.io/pypa/manylinux_2_24_aarch64 /bin/bash`
- install build reqs in container
`cd project`

you will need to change where your apt pkg manager index to the archived version
```
echo "deb http://archive.debian.org/debian stretch main contrib non-free" | tee /etc/apt/sources.list
echo "deb http://archive.debian.org/debian-security stretch/updates main contrib non-free" | tee -a /etc/apt/sources.list
```


first one is for 264 second is for 265, but highly redundant clearly, gui thing seems irrelevant, nvm it literally has a gui what a hellscape
```
apt install -y build-essential cmake git yasm
sudo apt-get install git-all cmake cmake-curses-gui build-essential yasm
```

```
git clone https://code.videolan.org/videolan/x264.git
cd x264
./configure --enable-shared --enable-pic
make -j$(nproc)
make install
```
instructions for x265 -- NOTE different for ARM vs. x86 instruction sets
https://bitbucket.org/multicoreware/x265_git/wiki/Home
make install (at the end)
```
```

apt install -y libxml2-dev




`alias python=/opt/python/cp311-cp311/bin/python` # python3.11 install location
`alias pip=/opt/python/cp311-cp311/bin/pip`
/opt/_internal/cpython-3.11.1/bin/python -m pip install --upgrade pip
pip install setuptools
pip install auditwheel
pip install twine
pip install virtualenv

alias virtualenv=/opt/python/cp311-cp311/bin/virtualenv
`source ./scripts/activate.sh`
`unalias python` # make sure you're using the newly created venv. Probably shouldn't have created this alias in the first place
`unalias pip`
make # installs cython and stuff
make release

`
auditwheel repair dist/*.whl --plat manylinux_2_28_x86_64 -w repaired_wheels/
`

twine upload -u __token__ -p <YOUR_API_TOKEN> repaired_wheels/*.whl
