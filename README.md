# knock

`knock` is a minimal Python implementation of [knock(1)](https://github.com/jvinet/knock).

See the Internet Archive's archive of [portknocking.org](https://web.archive.org/web/20180726181817/http://www.portknocking.org/) for more information on port knocking.

## Usage

`knock [-h] [-d DELAY] [-t TIMEOUT] [-u] [-V] [-v] <host> <port[:protocol]> [[port[:protocol] ...]`

### Examples

```shell
% ./knock host.domain 123:tcp 456:upd 789

% ./knock host.domain 123 456 -d 10

% ./knock host.domain 123 -t 10
```

### Options

- `host` **[REQUIRED]** - the host to knock
- `ports` **[REQUIRED]** - a sequence of one or more ports or port:protocol pairs to knock
- `-d <DELAY>`, `--delay <DELAY>` - the delay between knocks, in milliseconds (defaults to 5 ms)
- `-h`, `--help` - print usage information and exit
- `-t <TIMEOUT>`, `--timeout <TIMEOUT>` - the connection timeout, in seconds (defaults to 0.5 s)
- `-u`, `--udp` - use UDP for ports without protocols (defaults to TCP)
- `-V`, `--version` - print the version and exit
- `-v`, `--verbose` - print debugging information during execution

## License

`knock` is released under the [BSD 3-Clause License](LICENSE.md).
