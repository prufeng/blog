error: RPC failed; HTTP 500 curl 22 The requested URL returned error: 500 Internal Server Error
===

```
$ git push -u origin master
Enumerating objects: 46, done.
Counting objects: 100% (46/46), done.
Delta compression using up to 8 threads.
Compressing objects: 100% (44/44), done.
error: RPC failed; HTTP 500 curl 22 The requested URL returned error: 500 Internal Server Error
fatal: The remote end hung up unexpectedly
Writing objects: 100% (46/46), 8.53 MiB | 7.21 MiB/s, done.
Total 46 (delta 8), reused 0 (delta 0)
fatal: The remote end hung up unexpectedly
Everything up-to-date
```

```
git config --global http.postBuffer 524288000
```
