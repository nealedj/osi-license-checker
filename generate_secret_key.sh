#!/bin/sh

python -c "import os,binascii;print binascii.b2a_hex(os.urandom(32)).upper()" > checker/secret_key
