@echo off
echo Generating SSL Key and Certificate...
"C:\Program Files\OpenSSL-Win64\bin\openssl.exe" req -new -x509 -keyout server-key.key -out server-cert.crt -days 365 -config server-cert.cnf -nodes
echo Certificate generation completed.
