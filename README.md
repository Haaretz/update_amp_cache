# Purge amp cache

More info <https://developers.google.com/amp/cache/update-cache>

Generate a pair of RSA keys in the textual PEM format like this:

```bash
openssl genrsa 2048 > private-key.pem
openssl rsa -in private-key.pem -pubout >public-key.pem
```

Post the public key on the domain to be refreshed at the following location:

```bash
https://example.com/.well-known/amphtml/apikey.pub
```


## Examples

### Flask  

```bash
curl localhost:5000/update-cache -XPOST -d '{"url":"https://www.haaretz.com/amp/israel-news/podcasts/PODCAST-listen-when-will-saudi-arabia-also-make-peace-with-israel-1.10208557"}'
```

### CLI

```bash
python update_amp_cache.py "https://www.haaretz.com/amp/israel-news/podcasts/PODCAST-listen-when-will-saudi-arabia-also-make-peace-with-israel-1.10208557" 
```