# TSenhanced

Alternate Syntax for Typescript.

## Compile

### Compile files in directory to TypeScript

```bash
$ ./main.py -d [directory]
```

### Compile files in directory to JavaScript (not implemented)

```bash
$ ./main.py -j [directory]
```

## Compile and execute

### Single File with Deno

```bash
$ ./main.py -f [file]
```

### Single File with Bun

```bash
$ ./main.py -f [file] -bun
```

### All files in directory with Deno

```bash
$ ./main.py -a [directory]
```

### All files in directory with Bun

```bash
$ ./main.py -a [directory] -bun
```

Default file is `index.tsa`
