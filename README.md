# asteroid-player

Sample configuration file:
```yml
database: "mongodb://localhost:27017"

logging:
  level: INFO
  format: "%(asctime)s %(levelname)s: %(message)s"
  datefmt: "%d/%m/%Y %H:%M:%S"

musicfiles: "/path/to/musicfiles"
```

Uses [playsound](https://github.com/TaylorSMarks/playsound), which may require additional unlisted dependencies on different operating systems.

- OSX

You'll also need [`pyobjc`](https://github.com/ronaldoussoren/pyobjc).
