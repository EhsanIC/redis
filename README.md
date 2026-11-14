<p align="center"><b>English</b> | <a href="README.fa.md">فارسی</a></p>

# Build Your Own Redis in Python

<p align="center">
  <a href="https://app.codecrafters.io/users/EhsanIC">
    <img src="https://backend.codecrafters.io/progress/redis/52edac4e-c367-4015-9ef5-4f44b1e9d729" alt="CodeCrafters progress" width="100%"/>
  </a>
</p>

A hand-rolled Redis clone in Python — no frameworks, just raw sockets and a single-threaded event loop.

![Demo](docs/demo.gif)
<!-- [placeholder] Add a short demo recording at docs/demo.gif -->

## ✨ Features

- [x] `PING` / `ECHO`
- [x] `SET` with expiry (`EX` / `PX`) and `GET` with lazy expiration
- [x] Lists: `RPUSH`, `LPUSH`, `LRANGE`, `LLEN`, `LPOP`
- [x] `BLPOP` — blocking pop with per-key waiter queues and timeouts
- [x] `TYPE`
- [x] Hand-written RESP encoding/decoding
- [x] Single-threaded event loop over non-blocking sockets

## 🚀 Quick start

```bash
git clone https://github.com/EhsanIC/redis
cd redis
./your_program.sh
```

Then, in another terminal:

```text
redis-cli
127.0.0.1:6379> SET greeting "hello"
OK
127.0.0.1:6379> GET greeting
"hello"
127.0.0.1:6379> RPUSH mylist a b c
(integer) 3
```

## ⚙️ How it works

**Protocol.** Clients talk RESP2. Incoming bytes are split on CRLF to extract the command and its arguments; replies are encoded by hand with small helpers for bulk strings, integers, arrays, simple strings and errors.

**Concurrency.** A single thread runs a non-blocking event loop: accept new connections, expire any timed-out blocking clients, poll every connected client for input, dispatch the command, and write the reply back. No threads, no asyncio — the same shape Redis itself uses.

**Storage.** Plain dicts, one per data type: strings (`key → [value, expire_at]`), lists, and streams. Expiration is lazy: `GET` checks whether the key's deadline has passed and answers with a null bulk string if it has.

**Blocking commands.** `BLPOP` registers the client in a per-key waiter queue with a deadline. When `RPUSH`/`LPUSH` add an element, the first waiter is served immediately; on timeout the loop hands back a null array.

### Project layout

```text
.
├── app/
│   ├── main.py        # entry point
│   ├── server.py      # the event loop: accept / expire / poll / reply
│   ├── commands.py    # command dispatch and implementations
│   ├── helpers.py     # RESP encode/decode, expiry utilities
│   ├── waiters.py     # registry of blocked clients for BLPOP
│   └── test.py
├── your_program.sh
└── codecrafters.yml
```

## 🧪 Testing

Run the challenge test suite:

```bash
codecrafters test
```

Or test manually with `redis-cli` against `./your_program.sh`. When ready, submit:

```bash
codecrafters submit
```

## 📚 What I learned

- The RESP2 wire protocol, byte by byte
- How a single-threaded event loop multiplexes many clients without threads
- How Redis implements blocking list operations (waiter queues + deadlines)
- Lazy vs. active key expiration
- Dependency injection — `main()` builds the pieces and passes them into `Server` instead of it constructing its own

## 🔧 What I'd improve

- Delete dead code and commented-out experiments — git remembers history
- Use `is None` instead of `== None` (PEP 8)
- One `resp_int(n)` helper instead of duplicated integer-reply code
- Replace bare `[value, expire_at]` entries with a small dataclass
- Consistent dict initialization (`setdefault` everywhere)
- Finish `XADD`: ID validation, auto-generated IDs, multiple field-value pairs, and `XRANGE`

## 🙏 Credits

Built through the [CodeCrafters "Build Your Own Redis" challenge](https://codecrafters.io/challenges/redis) — the challenge scaffolding is theirs, **the implementation is entirely my own.**
